# Game loop

The game loop gives Windows messages and client events a turn on every pass. Think of it as the stage manager: it clears the outside mail, then lets the game process its own inbox and timers.

```text
repeat until quit
  |
  +-- drain Windows messages
  |     +-- keyboard, mouse, text, window events
  |
  +-- run one client event tick
        +-- dispatch queued events
        +-- fire due timers, at most 40 this tick
```

`app_run_message_loop` owns the loop. Windows calls `app_window_proc` for each message. `input_translate_win32_message` turns useful input messages into the client's own event objects.

After the Windows queue is empty, `event_dispatcher_tick` runs. It drains the client event queue and then handles due timers. The timer limit prevents a large timer backlog from taking over one loop pass.

## Pacing and redraw checks

The outer loop has no fixed frame rate. It runs an auxiliary clock check after more than 100 ms, drains Windows messages, and runs the dispatcher whenever it exists. That clock check does not drive game animation. After 402 tight passes the loop calls `Sleep(1)` and resets that pass counter.

The dispatcher uses `timeGetTime()` as its millisecond timer clock. When the next timer is more than 20 ms away, it can yield with `Sleep(5)`. Nearer timers are left for the repeatedly polled loop.

The root `ScreenPane` owns the recurring redraw service. Timer ID `0` calls `render_screen_timer_tick`, which checks the dirty pane tree through `render_screen_tree_frame` and queues itself again after 10 ms. The callback schedules from the current time, so a late redraw does not cause several catch-up callbacks.

Ten milliseconds is therefore a 100 Hz redraw check, not a promise of 100 visible frames per second. An unchanged tree is not presented, and the active DirectDraw or window output path can further constrain presentation. See [Renderer lifecycle](../rendering/lifecycle.md#redraw-and-presentation-cadence).

## Foreground and minimized windows

Losing the foreground does not pause the game loop. `WM_ACTIVATE` tells `app_window_proc` whether the window is inactive, active, or click-active. The handler records that state and forwards it to the video system, but `app_run_message_loop` continues draining Windows messages and running `event_dispatcher_tick` in every state.

The rendering result depends on the selected output mode:

| State | Exclusive full-screen mode | Nonexclusive window modes |
| --- | --- | --- |
| Inactive | Leave exclusive DirectDraw mode, mark video inactive, and minimize the window | Keep the video-active flag set |
| Redraw timer | Requeue every 10 ms but skip the screen-tree draw while video is inactive | Continue normal dirty-tree checks and presentation |
| Active again | Re-enter exclusive mode and force a root redraw | Force a root redraw |

The skipped full-screen work is scene composition and presentation, including one draw-owned time source. `render_world_pane_content` increments the world pane's visual frame once per draw, so world sprite phases stop while exclusive full-screen rendering is inactive and resume from that frame after restoration. The counter is passed into the object rendering queues; no traced movement, packet, or world-state update consumes it.

Dispatcher-owned work does not pause. Timer-driven pane and moving-effect animation, audio timers, action-delay expiry, held-pointer repeat, spell-cast sequencing, and periodic keepalive work still use the normal dispatcher clock. They do not switch to a slower background interval. Restoring the window can therefore show the current timer-driven state while draw-driven world animation resumes from its earlier visual frame.

Minimization has no separate client state. The `WM_SIZE` handler does not inspect `SIZE_MINIMIZED`; it treats size and move messages alike and only refreshes the windowed presentation origin. The executable does not import `IsIconic`, `GetForegroundWindow`, or `GetActiveWindow`. A minimized window usually also loses activation, but only exclusive full-screen mode turns that activation loss into a rendering suspension. A minimized nonexclusive window can therefore keep doing dirty software draws and output calls.

Network work also continues. A Winsock `FD_READ` window notification queues receive command `5` to the socket worker. Outgoing packet command `6` uses the same worker queue, and decoded server packets return to the always-running main-thread event dispatcher. Foreground loss does not pause packet sequences, receives, sends, or keepalive timers.

The client contains helpers that could temporarily apply a process priority class, but normal version 741 startup leaves that feature disabled. The application-state constructor clears its enable flag, and the only activation caller passes zero rather than configuring an override. Normal foreground changes therefore do not reach `SetPriorityClass` or deliberately lower background priority.

The practical consequences are:

- Exclusive full-screen backgrounding saves the expensive screen-tree draw and presentation work without pausing game or network state.
- Windowed minimization has no equivalent optimization and can waste CPU on animations, dirty-region composition, and presentation attempts that cannot be seen.
- No client-owned background optimization slows gameplay timers or packet handling, so there is no built-in sync penalty. An external scheduler stall can still delay the main thread and socket notification handling, but that is not a state-dependent policy requested by this client.

## Clock changes and speed hacks

A traditional speed utility does not make the processor or connection faster. It changes the time reported to one process. A typical virtual clock keeps a real and virtual baseline, then returns a scaled elapsed time:

```c
virtual_now = virtual_start + (real_now - real_start) * speed;
```

The effect is broad in this client because the event dispatcher uses `timeGetTime()` for its timer queue. A faster reported clock makes dispatcher-owned work become due sooner. This includes animation callbacks, the 20 ms held-pointer repeat, redraw checks, audio fades, server-supplied skill and spell action-delay expiry, and the one-second spell cast-line sequence. The keyboard attack path also compares `timeGetTime()` against a 100 ms local gate. Periodic work such as the 30-second `CSendAlive` timer also runs early, which is a side effect rather than a gameplay benefit.

Movement needs a narrower interpretation. `CMove` is sent as soon as a local tile step passes collision and action-state checks. The four 114 ms or eight 57 ms interpolation ticks animate a step that was already submitted. Shortening those ticks makes walking look faster but does not remove a packet delay. Keyboard repetition comes from Windows input messages. Held-pointer repetition does use a client timer and can therefore produce input attempts more often under a virtual clock. The server still accepts, rejects, or corrects the resulting movement requests.

There is no general fixed delay between ordinary packet construction and network transmission. `net_submit_client_packet` copies the body into communications event 6 and releases the worker semaphore. The worker transforms and sends it when scheduled. Incoming socket work posts a decoded event for the main thread, and `event_dispatcher_tick` drains queued events before handling timers. Removing the loop's `Sleep(1)` or timer yield `Sleep(5)` would mostly increase CPU use. It would not make a timer due before its recorded `timeGetTime()` deadline.

Spell casting is the important exception. `ui_start_spell_cast` deliberately holds a positive-line `CUseSpell` body. It schedules the first 1,000 ms callback, sends the delay request and first chant line, and submits the held body only after the last line. `ui_spell_delay_timer_callback` schedules each following 1,000 ms callback. A timing experiment must change both schedule sites or the first and later intervals will disagree. A zero-line spell already bypasses this queue and submits immediately.

The client has two separate speed checks:

- About every 100 ms, `app_check_speedhack_clocks` compares elapsed `timeGetTime`, `GetTickCount`, CRT time, and system `FILETIME`. A disagreement greater than five seconds can produce a one-per-process `CException` report after repeated mismatches.
- [`SCheckTime`](../network/server/104-0x68-check-time.md) receives an immediate [`CCheckTime`](../network/client/117-0x75-check-time.md) response containing the current `timeGetTime()` value. The client makes no decision, but the server can compare the reported clock rate with real elapsed time.

For a controlled client and server experiment, a scoped runtime patch is easier to reason about than a global virtual clock. Patch or hook only the owner being tested, keep the original behavior as the default, expose the interval as bounded configuration, and log every changed submission. A cast-cadence test should leave `CCheckTime`, the local clock comparison, packet sequencing, encryption, and the communications worker unchanged. Server traces should record each delay request, chant line, final `CUseSpell`, acceptance, cancellation, and correction. An observed 800 ms tolerance belongs in test results until repeated server measurements confirm it.

Use the [safe launcher](../appendix/runtime-patches/safe-launcher.md) pattern for any runtime experiment: fingerprint the executable, launch suspended, resolve RVAs from the loaded module base, verify original bytes, write complete instructions, flush the instruction cache, restore protection, and leave `Darkages.exe` unchanged on disk.

## Main-thread rule

Game objects and panes expect events on the main thread.

`event_dispatch_or_queue` checks the caller:

```text
if caller is the main thread
    dispatch now
else
    copy the event into the queue
```

This is why socket work can prepare a decoded packet away from the UI, while pane handlers still receive it during the normal game loop.

## Loop and event system

The loop decides **when** work runs. The event system decides **where** each event goes. Keeping those jobs separate makes the client easier to reason about:

- The loop pumps messages and repeatedly gives the dispatcher a turn.
- The event dispatcher classifies work.
- The pane tree offers work to UI and game screens.
- Timer handlers run time-based behavior.

See [Event system](../systems/events.md) for dispatch and [UI and panes](../systems/ui.md) for the pane tree.
