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
