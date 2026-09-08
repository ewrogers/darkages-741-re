# Event system

Events are the client's common message format. Mouse input, keyboard input, text, timers, decoded server packets, and app state changes all meet here.

An event is like a small envelope. Its type says which handler family should open it, and the remaining fields carry the details.

Follow delivery and timer behavior below. The later [Event shape](#event-shape) and [Construction and queueing](#construction-and-queueing) sections explain representation, copying, and ownership.

## Dispatch flow

Main-thread producers deliver events immediately. A producer on another thread copies its event into the queue; the main-thread dispatcher delivers that copy on a later tick.

```text
producer calls event_dispatch_or_queue
    |
    +-- main thread ------> dispatch now
    |
    +-- another thread ---> copy to queue
                                |
                         main-thread tick
                                |
                           dispatch copy
```

Both delivery paths reach `event_dispatch`. It selects the handler family from the event type. Pane-routed families then use the captured pane or the event tree; intro state changes have their own handler.

`event_dispatch_pane_subtree` visits children before their parent. Returning true means the event was handled, so traversal stops. This is similar to offering input to the topmost child node before its container.

Mouse capture is a shortcut. While a pane owns capture, pointer events go directly to it instead of searching the whole tree.

Capture also sends keyboard and application events to that pane. Network events continue through the normal pane tree.

## Event families

`event_dispatch` groups event types by purpose:

| Types | Family |
| --- | --- |
| `0x00` to `0x07` | Pointer and mouse input |
| `0x08` to `0x0C` | Keyboard and text input |
| `0x0D` to `0x12` | Window, focus, and IME input |
| `0x13` | Decoded server packet |
| `0x14` | Intro state change |

The first four families can travel through the pane tree. Intro state events go straight to `event_handle_intro_state`. `event_post_intro_state` constructs that `0x14` event with three dword payload values and submits it through the same dispatch-or-queue path.

## Network events

`net_post_decoded_server_packet_event` creates type `0x13` after transport decryption. During dispatch, the client may build a typed server packet object. Packets without a registered class can still be handled directly by a pane or manager.

This keeps network code and gameplay code loosely joined. The socket only delivers a decoded message. The event system decides which game screen or manager sees it.

## Server-controlled input blocking

[`SBlockInput`](../network/server/081-0x51-block-input.md) opens the RTTI-backed `ClockPane` as a modal wait cursor. The pane follows pointer movement and returns true for pointer plus keyboard/text events, so those events stop before reaching ordinary UI and world handlers.

The block is represented by the live `ClockPane` singleton rather than a player or world-state flag. Beginning a block also emits button-up events for any held left or right mouse buttons. Ending it removes the pane and restores the normal cursor. Timers and network events continue throughout the block.

## Timers

Timers use the same main-thread tick but are stored separately from normal events. Their due times are unsigned millisecond values based on `timeGetTime()`.

A scheduled entry is one-shot. When it becomes due, the dispatcher removes it before calling the owner's `TimerHandler` callback. Repeating behavior, including the 10 ms screen redraw check, requeues another entry from its callback.

`event_schedule_timer` supports three timing bases:

| Scheduling form | Due-time base |
| --- | --- |
| Normal | Dispatcher's latest sampled time plus the delay |
| Current time | A new `timeGetTime()` value plus the delay |
| Current callback | The due time of the timer being handled plus the delay |

The callback-relative form falls back to the normal base when no timer callback is active. This distinction decides whether a repeating system preserves its earlier schedule or shifts after a late callback.

`event_dispatcher_tick` invokes at most 40 due callbacks per pass. When the next timer is more than 20 ms away, it can yield for 5 ms. The limit prevents a timer backlog from taking over the main thread.

A `Pane` contains a secondary `TimerHandler` base at offset `0x11C`. Because of that inheritance layout, a timer callback may receive a pointer adjusted to that base. This detail matters when naming callbacks or building hooks.

The dispatcher keeps the five-word entries ordered by due time. See the [timer entry layout](../appendix/runtime/panes.md#timer-entry) for the owner, timer ID, deadline, and callback payload fields.

## Pointer timing

Win32 pointer messages carry `GetMessageTime()` timestamps into the event system. `EventMan` synthesizes a double-click only when the new press uses the same button, arrives less than 1,000 ms after the saved press, and has a Manhattan coordinate difference of at most 2 logical pixels. A match emits left type `0x02` or right type `0x05` and clears the saved timestamp. A normal press stores its button, position, and time for the next comparison.

`input_repeat_pointer_move_timer` can emit the last stored pointer coordinates and requeue itself after 20 ms while its repeat state is enabled. A control starts this mode on a retained pointer press and stops it on release. Stopping clears the state and cancels all timers owned by that `EventMan` handler.

Programmatic pointer movement clamps the logical position to `0..639` by `0..479`, calls `SetCursorPos`, updates `EventMan`, and emits the same pointer-move event family. The manager also maintains a four-bit modifier mask derived from the high bits of its tracked keyboard-state bytes. Selection controls use that mask for additive and ranged selection behavior.

The complete event type table, pane handler slots, timer entry, and tree-entry layout are in [Pane and event layouts](../appendix/runtime/panes.md).

## Batched jobs

`BatchSession` sequences small asynchronous jobs without blocking the event loop. It owns a linked queue of `BatchJob` pointers and keeps at most one job active. `batch_session_start_next_job` removes entries from the front until it finds an enabled job, then calls `batch_job_begin`.

`BatchJob` is an abstract base. Beginning a job records its owning session and invokes the job's virtual execute method. When derived work finishes, `batch_job_complete` schedules timer ID `0` on the owning `BatchSession` and invokes the job's virtual cleanup method. The session's next timer callback starts the following queued job. Disabled jobs are cleaned up and skipped instead of stalling the queue.

## Event shape

An `Event` is a fixed `0xA8`-byte value with a signed one-byte type and a family-specific payload. The constructor uses `-1` for an unset type. The shared base supplies a live-object cookie, a marker that `event_dispatch_immediate` checks before dispatch. An event with a cleared cookie is rejected before dispatch.

The `unobserved_08` word is not initialized or consumed by the confirmed lifecycle. Whole-object queue copies preserve it, so a stack event may carry an indeterminate value there. It is not a queue link and must not be treated as a zero-filled field.

The [event object reference](../appendix/runtime/panes.md#event-object) holds the complete header, cookie bytes, constructor evidence, and object-relative offsets. The [decoded server payload](../appendix/runtime/panes.md#decoded-server-packet-payload) identifies the opcode-first body, its length, and the optional parsed packet pointer.

## Construction and queueing

Most producers construct an `Event` on the stack, set its signed type byte, fill the matching payload fields, and call `event_dispatch_or_queue`.

The cross-thread queue is synchronized. The dispatcher keeps a separate pool of reusable `Event` objects for that queue, but the pool stores pointers outside the objects. Neither allocation nor recycling uses `Event +0x08` as a link.

Changing a dialog's focused control also schedules a small dispatcher-owned focus-state check from the current `timeGetTime()` value. The main tick consumes that pending timestamp separately from normal queued events and pane timers.

`EventQueue` and the timer-side `EventStack` both own their stored event pointers. Their deletion callbacks invoke the event's virtual deleting destructor. Queue push and pop operations use the `EventDispatcher` critical section and copy the complete fixed-size event value between threads.

The underlying `PointerQueue<Event>` uses linked blocks of 1,024 pointers. A fully consumed block rotates to the reusable tail, while a partially filled block resets its read and write indexes in place. `PointerStack<Event>` begins with 1,024 pointers and grows in 1,024-entry steps. These are internal storage choices, not limits on the number of queued events or timers.

`EventHandlerList` keeps its pane registrations in contiguous 12-byte records. Insert and erase operations adjust every active iterator so a pane can register or remove a subtree without invalidating an in-progress traversal.

## Known limits

- The purpose of `unobserved_08` is not established. It is preserved by whole-object copies but unused by the confirmed event lifecycle.
- Many fields inside the family-specific payload union are still unnamed.
- Pointer-bearing event variants should not be copied across process boundaries until their ownership rules are known.
- Registration, visibility, focus, and mouse capture are separate states. A hidden pane may still be registered.

Addresses and confidence notes are in the [event function reference](../appendix/functions.md#events).
