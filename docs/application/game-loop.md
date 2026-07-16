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

After the Windows queue is empty, `event_dispatcher_tick` runs. It drains the client event queue and then handles due timers. The timer limit prevents a large timer backlog from taking over one frame.

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

- The loop pumps and schedules work.
- The event dispatcher classifies work.
- The pane tree offers work to UI and game screens.
- Timer handlers run time-based behavior.

See [Event system](../systems/events.md) for dispatch and [UI and panes](../systems/ui.md) for the pane tree.
