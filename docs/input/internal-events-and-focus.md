# Internal events, focus, and modals

## Input manager state

`input_manager_singleton` at `0x427380` returns the global manager stored in `input_manager_instance` at `0x6D9260`. Its constructor is `input_manager_ctor` at `0x4667E0`.

Important recovered offsets are:

| Offset | Type | Meaning |
|---:|---|---|
| `+0x034` | table | Modifier mask by scan code |
| `+0x134` | `u8[256]` | Normal scan-code translation table |
| `+0x234` | `u8[256]` | Shifted translation table |
| `+0x334` | `u8[256]` | Pressed-key state; high bit marks pressed |
| `+0x434` | `u8` | Current modifier mask |
| `+0x458` | `u32` | Current mouse-button bits; left `1`, right `2` |

The modifier byte is bitwise, not an enum:

```c
#define INPUT_ALT   0x01
#define INPUT_CTRL  0x02
#define INPUT_SHIFT 0x04
```

Left and right variants map to the same bit. Alt uses scan codes `0x38` and `0xB8`, Ctrl uses `0x1D` and `0x9D`, and Shift uses `0x2A` and `0x36`.

Pointer event flags also include `0x10` while the left button is held and `0x20` while the right button is held. For example, exact Shift+right-button is `0x24`.

## Event objects

`input_event_ctor` at `0x466680` initializes the common `0xA8`-byte event object. The event type is a signed byte at `+0x0C` and starts as `0xFF`.

Confirmed event values are:

| Type | Meaning | Emitter |
|---:|---|---|
| `0` | Mouse move | `input_emit_mouse_move_event` at `0x4672F0` |
| `1` | Left button down | `input_emit_left_button_down_event` at `0x4673F0` |
| `2` | Left double-click | Same emitter |
| `3` | Left button up | `input_emit_left_button_up_event` at `0x467680` |
| `4` | Right button down | `input_emit_right_button_down_event` at `0x467790` |
| `5` | Right double-click | Same emitter |
| `6` | Right button up | `input_emit_right_button_up_event` at `0x467A20` |
| `7` | Mouse wheel | `input_emit_mouse_wheel_event` at `0x467B30` |
| `8` | Key down | `input_emit_key_down_event` at `0x467C10` |
| `9` | Key up | `input_emit_key_up_event` at `0x467E30` |
| `0x0B` | Character input | `input_emit_char_event` at `0x467FE0` |
| `0x13` | Network receive | Existing receive pipeline |

IME-related values around this range still need names tied to each constructor.

Double-click detection uses at most `1000` milliseconds and a Manhattan coordinate difference of at most `2` logical pixels.

## Dispatch order

`input_dispatch_event` at `0x4647C0` is the central logical-event dispatcher. Its observed priority is:

1. A temporary key-sequence capture can consume matching key events.
2. The active focused or modal pane at application offset `+0x40` receives the event first.
3. Pointer coordinates are converted to that pane's local coordinate space.
4. If the pane does not consume the event, `input_dispatch_event_through_pane_tree` at `0x464D50` walks visible and active panes.
5. World input receives events that survive the UI layers.

The pane-tree walk performs hit testing, coordinate conversion, and child traversal. The value at pane offset `+0x184` participates in pane priority or stacking decisions.

`input_dispatch_or_queue_event` at `0x4670F0` dispatches directly only when called on the thread stored in `app_main_thread_id` at `0x740400`. Other producers copy the complete event into the application's synchronized queue. `input_process_main_thread_events_and_timers` at `0x464180` drains those copies on the main thread.

`input_dispatch_event_to_pane` at `0x464F40` selects a vtable slot by message family:

| Family | Pane vtable offset |
|---|---:|
| Pointer types `0..7` | `+0x48` |
| Keyboard, character, and IME | `+0x4C` |
| Network type `0x13` | `+0x50` |
| Other application events | `+0x54` |

This explains modal behavior without separate Win32 windows. A dialog is a pane that is placed first in the internal dispatch order.

## Server-controlled blocking

`net_handle_s_block_input` at `0x5F7AA0` handles `SBlockInput` opcode `0x51`:

- State `0` calls `input_begin_server_block` at `0x466CC0`. It emits releases for held left or right buttons and shows a centered loading-clock overlay.
- State `1` calls `input_end_server_block` at `0x466D00` and removes the overlay.

`ui_loading_clock_pane_ctor` at `0x42E8C0` loads `lodclk.epf`. The show and hide entry points are `ui_show_loading_clock_overlay` at `0x42E800` and `ui_hide_loading_clock_overlay` at `0x42E890`.
