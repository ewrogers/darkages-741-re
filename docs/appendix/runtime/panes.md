# Pane and event layouts

The event dispatcher routes input, network messages, application events, and timers through several related runtime objects. These layouts describe the shared event and pane machinery. Concrete RTTI class names are cataloged in the [pane type appendix](../pane-types.md).

## Event object

```text
struct Event {
    unknown header[0x0C]
    s8 type                     // +0x0C, starts as -1
    type-specific data[...]     // starts at +0x10
}                               // total size 0xA8
```

### Event types

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
| `0x08` | Key down |
| `0x09` | Key up |
| `0x0A` | IME composition text update |
| `0x0B` | Character or committed text |
| `0x0C` | Alternate translated key event, exact purpose unknown |
| `0x0D` | IME open-status change |
| `0x0E` | IME composition start |
| `0x0F` | IME composition end |
| `0x10` | IME candidate-list data |
| `0x11` | IME candidate-list close |
| `0x12` | Application event, exact purpose unknown |
| `0x13` | Decoded server packet |
| `0x14` | Intro state change |

The client creates double clicks itself. A second press must use the same button, arrive within 1000 ms, and be no more than two pixels away by Manhattan distance.

Input flags use `0x01` for Alt, `0x02` for Ctrl, `0x04` for Shift, `0x10` for left held, and `0x20` for right held. Mouse-wheel delta is divided by 120 before dispatch.

### Pane handler slots

| Event family | Primary vtable slot |
| --- | --- |
| Pointer, `0x00` to `0x07` | `+0x48` |
| Keyboard and text, `0x08` to `0x0C` | `+0x4C` |
| Network, `0x13` | `+0x50` |
| Application and IME, `0x0D` to `0x12` | `+0x54` |
| Dialog action callback | `+0x64` |

A true return value consumes the event and stops normal tree traversal.

## Event pane tree

`EventHandlerList` stores a flattened preorder tree. The dispatcher owns it at offset `+0x60`.

```text
struct EventHandlerEntry {
    Pane *pane                  // +0x00
    u32 depth                   // +0x04
    u32 identity_or_generation  // +0x08, exact purpose uncertain
}                               // size 0x0C
```

Example storage:

```text
depth 0  root A
depth 1    child A.1
depth 2      child A.1.a
depth 1    child A.2
depth 0  root B
```

Removing an entry also removes the following entries with greater depth. Child iterators use one of 16 tracked slots so a handler can change the tree without leaving a raw array pointer behind.

## Pane fields

```text
struct PaneFields {
    TimerHandler timer          // +0x11C, secondary base object
    s32 origin_x                // +0x128
    s32 origin_y                // +0x12C
    bool visible                // +0x130
    s32 input_priority          // +0x184
}
```

The dispatcher stores the captured pane at `+0x40` and the active minimum input priority at `+0x50`. The priority threshold provides modal-style input blocking without removing lower panes from the event tree.

## Message pane fields

`GameMessagePane` owns a fixed four-row display buffer. The matching world layout gives each row 49 colored byte cells.

```text
struct GameMessagePaneFields {
    s32 cells_per_row           // +0x1A4, 49 in the live world layout
    s32 row_height              // +0x1A8, 14 pixels
    s32 row_capacity            // +0x1AC, 4 in the live world layout
    MessageRow *rows            // +0x1B0
    s32 write_column            // +0x1B4
    s32 rotated_row_count       // +0x1B8, also used by the slide animation
    s32 content_width_cells     // +0x1BC
    s32 write_row               // +0x1C0
    u32 timer_serial            // +0x1C4
}
```

`NewSystemMessagePane` is the persistent-history frame. Its child is an RTTI-backed `NewSystemMessageTextPane` derived from `TextEditPane`.

```text
struct NewSystemMessagePaneFields {
    PixMap *skin                // +0x190
    s32 visible_lines           // +0x194, clamped from 1 through 10
    bool dragging_history_bar   // +0x1F8
    NewSystemMessageTextPane *text_pane // +0x1FC
}

struct NewSystemMessageTextPaneFields {
    // TextEditPane base fields precede these values.
    s16 max_bytes               // +0x1FC, initialized to 30000
    s16 max_lines               // +0x1FE, initialized to 30000
}
```

The text pane deletes the oldest bytes when `max_bytes` is exceeded. Its trimming loop preserves Windows DBCS character boundaries.

## Timer entry

```text
struct TimerEntry {
    TimerHandler *handler       // +0x00
    u32 timer_id                // +0x04
    u32 due_time                // +0x08
    u32 payload_1               // +0x0C
    u32 payload_2               // +0x10
}                               // size 0x14
```

The dispatcher removes a due entry before calling the timer handler. It processes at most 40 due entries per game-loop pass. Cancellation removes matching entries and uses a separate notification callback.

## Dialog pane fields

```text
struct DialogPaneFields {
    ControlList *controls       // +0x594
    s32 setup_index_a           // +0x598, exact purpose uncertain
    s32 setup_index_b           // +0x59C, exact purpose uncertain
    s32 focused_control         // +0x5AC
    s32 hovered_control         // +0x5BC
    s32 hover_zone              // +0x5C0
    s32 pointer_control_2       // +0x5C4
    s32 pointer_zone_2          // +0x5C8
}
```

Control indexes follow attachment order. They are used for focus, hit testing, and the parent dialog action callback.
