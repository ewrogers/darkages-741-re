# Runtime structures

This appendix collects object layouts and dispatch tables used by the event and UI chapters. Offsets are relative to the object shown. They are not static process addresses.

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

## Decoded server event

```text
struct ServerEventFields {
    bytes *body                 // Event +0x14, command byte first
    u32 body_length             // Event +0x18
    ServerPacket *parsed        // Event +0x1C, null when no class exists
}
```

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

Function addresses and evidence notes are in the [function reference](functions.md) and YAML exports.
