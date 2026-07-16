# UI and event architecture

The client uses a custom C++ event and pane framework. It is similar to a scene tree in that panes form a hierarchy, receive local-coordinate input, override base virtual handlers, and can be shown or hidden. It is not a single unified Unity or Godot-style node system. There are three related hierarchies:

1. `HierList<Screen>` stores spatial pane parentage and supplies absolute screen origins.
2. `EventHandlerList` stores the application pane tree used by central event dispatch.
3. `DialogPane` owns a separate ordered collection of controls used for hit testing, focus, and dialog actions.

The class names in this chapter come from Microsoft C++ RTTI in the executable. Function names are evidence-based project names. All addresses are static virtual addresses for preferred image base `0x00400000`.

## End-to-end flow

```text
Win32 messages ----> input_translate_win32_message ----> Event
                                                        |
socket worker ------> network Event type 0x13 ----------+----> direct on main thread
                                                        |      or copied to queue
                                                        v
                                               event_dispatcher_tick
                                                        |
                                      +-----------------+-----------------+
                                      |                                   |
                              captured pane                      EventHandlerList tree
                                                                          |
                                                            Pane virtual event family
                                                                          |
                                                         DialogPane control collection
                                                                          |
                                                             parent action callback

Timer queue --------> TimerHandler virtual +0x08 on the main-thread tick
```

`app_run_message_loop` at `0x004AC750` drains the Win32 message queue and then invokes `event_dispatcher_tick` at `0x00464180`. The main thread ID is stored in `app_main_thread_id` at `0x00740400`.

## Class model

The core hierarchy recovered from RTTI and constructor vtable writes is:

```text
LObject
+- Event
+- EventDispatcher
+- TimerHandler
+- Canvas
   +- Pane
      +- DialogPane
      |  +- LoginDialogPane
      +- ControlPane
         +- ButtonControlPane
            +- ImageButtonControlPane
```

`Pane` also contains a `TimerHandler` base subobject at `this + 0x11C`. `ui_pane_ctor` at `0x00549490` constructs that secondary base and installs separate primary and secondary vtables. Derived pane constructors replace both when necessary. This is real C++ multiple inheritance, not a guessed component relationship.

The `LoginDialogPane` constructor at `0x004BA180` is a useful concrete example. It installs the `LoginDialogPane` primary vtable at `0x0067896C` and its `TimerHandler` vtable at `0x00678954`. It inherits most `DialogPane` behavior while overriding:

| Primary vtable slot | Function | Role |
| --- | --- | --- |
| `+0x4C` | `0x004BA810` | Keyboard/text handler |
| `+0x50` | `0x004BA150` | Network handler |
| `+0x64` | `0x004BA8C0` | Dialog action callback |
| `+0x74` | `0x004BA9B0` | Additional derived-pane hook |

## Event object and families

`event_ctor` at `0x00466680` constructs an `Event` of exactly `0xA8` bytes and initializes its signed type byte at `+0x0C` to `0xFF`. The remainder is a tagged union. The meaning of `+0x10` and later fields depends on the type.

`event_dispatch_to_pane` at `0x00464F40` selects one of four pane virtuals:

| Event types | Family | Pane vtable slot |
| --- | --- | --- |
| `0x00` through `0x07` | Pointer | `+0x48` |
| `0x08` through `0x0C` | Keyboard and text | `+0x4C` |
| `0x0D` through `0x12` | Application and IME state | `+0x54` |
| `0x13` | Network | `+0x50` |

The return value is a consumed flag. A true result stops normal pane-tree traversal.

### Pointer types

The Win32 translator and `EventMan` producers establish this exact mapping:

| Type | Meaning |
| --- | --- |
| `0x00` | Pointer move |
| `0x01` | Left button down |
| `0x02` | Left button double click |
| `0x03` | Left button up |
| `0x04` | Right button down |
| `0x05` | Right button double click |
| `0x06` | Right button up |
| `0x07` | Mouse wheel |

The client synthesizes double clicks. It does not depend on `WM_LBUTTONDBLCLK` or `WM_RBUTTONDBLCLK`. A second down event becomes a double click when it uses the same button, arrives within 1000 ms, and has a Manhattan distance of at most two pixels from the first click.

The shared input flags use `0x01` for Alt, `0x02` for Ctrl, `0x04` for Shift, `0x10` for left held, and `0x20` for right held. Wheel delta is divided by `120` before dispatch.

### Keyboard, text, and IME types

`input_translate_win32_message` at `0x0048E980` converts `WM_KEYDOWN`, `WM_KEYUP`, `WM_CHAR`, and IME messages. Confirmed type meanings are:

| Type | Meaning |
| --- | --- |
| `0x08` | Key down |
| `0x09` | Key up |
| `0x0A` | IME composition text update |
| `0x0B` | Character or committed text |
| `0x0C` | Alternate translated key event; exact distinction remains unresolved |
| `0x0D` | IME open-status change |
| `0x0E` | IME composition start |
| `0x0F` | IME composition end |
| `0x10` | IME candidate-list data |
| `0x11` | IME candidate-list close |
| `0x12` | Unresolved application event |

This explicit IME path helps explain why some untranslated Korean text and input behavior do not fit a simple ASCII key model.

### Network and special events

`net_queue_server_packet_event` at `0x00468220` builds type `0x13`. A decoded opcode-first body is stored at event `+0x14`, its length at `+0x18`, and a parsed packet object is later stored at `+0x1C` when the server packet factory recognizes the opcode.

`event_dispatch` at `0x004647C0` runs the packet preprocessor first. If it does not consume the event, the pane tree receives it through virtual `+0x50`. The parsed object is released after dispatch. See [Network architecture](../network/architecture.md) for the socket and packet-factory stages.

Type `0x14` bypasses pane dispatch and goes to the application intro-state handler. It is outside the four classifier ranges above.

## Thread boundary and queue

`event_dispatch_or_queue` at `0x004670F0` compares `GetCurrentThreadId()` with `app_main_thread_id`:

- The main thread calls `event_dispatch_immediate` at `0x00463F70`.
- Any other thread calls `event_enqueue` at `0x00463F50`.

The queue copies all `0xA8` event bytes under synchronization. `event_dispatcher_tick` pops those copies and dispatches them on the main thread. This is how socket work can safely become UI-visible behavior without invoking panes from the network thread.

## Pane-tree propagation

`EventDispatcher + 0x60` contains an `EventHandlerList`. Its exact storage and RTTI inventory are described in [Pane registry](pane-registry.md).

Pointer conversion also consults the separate `HierList<Screen>` at `ui_screen_hierarchy_ptr` (`0x0073D948`). `ui_screen_hierarchy_get_absolute_origin` at `0x005528C0` walks spatial parents and accumulates each pane's `+0x128` and `+0x12C` origin until the startup `ScreenPane` root.

`event_dispatch_pane_subtree` at `0x00464D50` walks the tree depth first. For each pane it:

1. Validates the pane's `TimerHandler`/`LObject` subobject.
2. Checks input eligibility when the event is pointer or keyboard input.
3. Converts pointer coordinates from the current parent space to pane-local space.
4. Recursively visits immediate child panes.
5. Calls the current pane's matching event virtual if no child consumed the event.
6. Restores the original pointer coordinates before moving to the next branch.

This is child-before-parent propagation, similar to bubbling from a scene node toward an ancestor. Sibling traversal stops as soon as a handler returns true.

Pointer and keyboard events also pass a priority barrier. Each pane contributes its value at `Pane + 0x184`; `EventDispatcher + 0x50` is the minimum priority for the active branch. This supplies modal-style input gating without removing lower panes from the tree.

### Mouse capture

`EventDispatcher + 0x40` is the captured pane, not the keyboard focus pane. `input_set_capture_pane` at `0x00464780` stores it and calls `SetCapture` or `ReleaseCapture` for the main window.

While capture is set, pointer, keyboard, and application events go directly to that pane instead of normal tree traversal. Pointer coordinates are still converted to pane-local space. Network events continue through the pane tree.

### Visibility is not registration

These states are independent:

| State | Storage or operation | Effect |
| --- | --- | --- |
| Screen registered | `HierList<Screen>`; pane virtual `+0x38`/`+0x3C` | Adds or removes spatial parentage used for coordinates and screen updates |
| Event registered | `EventHandlerList`; pane virtual `+0x40`/`+0x44` | Adds or removes a pane and its descendants from central traversal |
| Visible | `Pane + 0x130`; pane virtual `+0x1C`/`+0x20` | Enables or disables pointer and keyboard eligibility and invalidates affected regions |
| Mouse captured | `EventDispatcher + 0x40` | Routes pointer, keyboard, and application events directly to one pane |
| Dialog control focus | `DialogPane + 0x5AC` | Selects the child control that receives keyboard and application events |

`ui_pane_hide` at `0x00549C40` also releases capture if the hidden pane owns it. Hidden panes are skipped for pointer and keyboard input. Application and network events can still reach a hidden but registered pane because central traversal applies the visibility test only to the two interactive input families.

## Dialog controls and actions

`DialogPane + 0x594` points to an ordered control collection. `ui_dialog_add_control` at `0x00445670` adds layout-created controls. The collection index is the numeric control ID used by hit testing, focus, and the parent action callback.

Pointer flow in `ui_dialog_handle_pointer_event` at `0x00445A20` is:

1. `ui_dialog_hit_test_control` at `0x004468C0` checks control rectangles and asks virtual `+0x78` for a local hit zone.
2. `ui_dialog_dispatch_pointer_to_control` at `0x00446FE0` subtracts the control origin, calls the control's pointer virtual `+0x48`, and restores the coordinates.
3. The dialog tracks hover and pressed control indexes.
4. A completed activation invokes the dialog's virtual `+0x64` with the control index and action code.

Keyboard flow in `ui_dialog_handle_keyboard_event` at `0x00445FF0` uses `DialogPane + 0x5AC` as the focused control index. Tab and Shift+Tab call `ui_dialog_focus_next_control` or `ui_dialog_focus_previous_control`. Other accepted events go to the focused control through virtual `+0x4C`. Application and IME events use the focused control's `+0x54` virtual.

This gives derived dialogs two common override points: handle an event family directly, or inherit the base routing and override the parent action callback.

## Timers

The timer scheduler belongs to `EventDispatcher` and runs on the same main-thread tick as queued events. `ui_pane_schedule_timer` at `0x00464050` converts a pane pointer to its `TimerHandler` subobject at `+0x11C`, then calls `event_schedule_timer` at `0x00464520`.

Each sorted timer entry contains five 32-bit values:

| Entry offset | Meaning |
| --- | --- |
| `+0x00` | `TimerHandler *` |
| `+0x04` | Timer ID |
| `+0x08` | Due time |
| `+0x0C` | Payload 1 |
| `+0x10` | Payload 2 |

The tick removes a due entry before invoking `TimerHandler` virtual `+0x08` with the timer ID and two payload values. It processes at most `0x28` due timers per tick, preventing a large overdue queue from monopolizing one message-loop iteration. Timer cancellation uses virtual `+0x0C` as a notification hook, removes matching entries, and updates the next-due time.

Timers do not automatically become `Event` objects. A timer handler may update its pane directly or emit a new event. `EventMan` demonstrates the latter at `input_repeat_pointer_move_timer` (`0x00466B40`), which emits a stored pointer move and schedules another 20 ms callback.

## Remaining questions

- The exact semantic name of internal event type `0x0C` is not yet confirmed.
- Event type `0x12` has not yet been tied to a producer.
- The meaning and setter paths for every pane priority value at `+0x184` still need per-pane study.
- Static analysis establishes tree mechanics, but a runtime pane-tree snapshot would show which roots and modal branches are active in each game state.
