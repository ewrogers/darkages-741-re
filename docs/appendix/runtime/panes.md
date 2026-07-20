# Pane and event layouts

The event dispatcher routes input, network messages, application events, and timers through several related runtime objects. These layouts describe the shared event and pane machinery. Concrete RTTI class names are cataloged in the [pane type appendix](../pane-types.md).

## Event object

```text
struct Event {
    void *vtable                // +0x00, Event vtable for its LObject base
    u32 live_cookie             // +0x04, 0x79736F62 or bytes "bosy"
    u32 unobserved_08           // +0x08, not initialized or consumed
    s8 type                     // +0x0C, starts as -1
    u8 reserved_0d[3]           // +0x0D, no confirmed use
    u8 data[0x98]               // +0x10, family-specific payload
}                               // total size 0xA8
```

`Event` is the exact RTTI complete-object class name. It derives from the eight-byte `LObject` base. `lobject_ctor` installs the base vtable and writes `live_cookie`. `event_ctor` then installs the `Event` vtable and sets `type` to `-1`. Destruction reverses those steps and clears the cookie. `lobject_is_live` compares the cookie with `0x79736F62`, and `event_dispatch_immediate` performs that check before central dispatch.

The `+0x08` word is copied along with the rest of the object but is not initialized by either constructor. A review of all 26 direct `event_ctor` references found 25 stack events and one heap allocation helper. None of the stack-event functions accesses `+0x08`; the heap helper also leaves it untouched. The confirmed queue, classification, dispatch, and destruction paths do not consume it. Treat it as an unobserved or dormant member, not a zero-filled field.

Queue storage does not explain the word. `event_allocate_or_reuse` obtains a separate `Event*` from the dispatcher pool or creates a new `0xA8`-byte object. `event_recycle` returns that pointer to the pool. Queue push and pop copy the complete object with a fixed `0xA8`-byte copy.

The addresses below are static Binary Ninja virtual addresses for the preferred image base `0x00400000`.

| Function | Address | Header evidence |
| --- | ---: | --- |
| `event_allocate_or_reuse` | `0x00463C40` | Reuses a pooled pointer or allocates and constructs a `0xA8`-byte `Event`. |
| `event_recycle` | `0x00463CF0` | Returns an `Event*` to the separate dispatcher pool. |
| `event_queue_push_copy` | `0x00463D10` | Copies all `0xA8` bytes into queued storage. |
| `event_queue_pop_copy` | `0x00463D60` | Copies all `0xA8` bytes back to the caller. |
| `event_dispatch_immediate` | `0x00463F70` | Checks the `LObject` cookie before dispatch. |
| `event_ctor` | `0x00466680` | Installs the Event vtable and writes signed type `-1`. |
| `event_dtor` | `0x004666B0` | Resets type, then calls the base destructor. |
| `lobject_ctor` | `0x004B4480` | Installs the base vtable and writes the `bosy` cookie. |
| `lobject_dtor` | `0x004B44B0` | Restores the base vtable and clears the cookie. |
| `lobject_is_live` | `0x004B4550` | Returns whether the cookie equals `0x79736F62`. |

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

## Clock pane fields

`ClockPane` is the animated wait cursor used by `SBlockInput`. It is a `Pane`, a `TimerHandler`, and a `Singleton<ClockPane>`. The empty singleton base begins at `+0x190` and overlaps the first concrete field without storing per-instance data.

```text
struct ClockPaneFields {
    // Pane fields precede these values.
    s32 image_height             // +0x190
    s32 image_width              // +0x194
    s16 current_frame            // +0x198, starts at -1
    u16 unknown_19A
    s32 frame_count              // +0x19C
}                                // total object size 0x1A0
```

Timer ID `0x1234` advances `current_frame` modulo `frame_count` every 50 ms. The global `clock_pane_singleton_ptr` is null while input is not blocked. While the pane is active, root `ScreenPane +0x27C` contains cursor mode `3`; closing it restores mode `0`.

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

## User confirmation pane

`UserConfirmPane` is an RTTI-backed `AlertPane` created from `SMessage` type `0x11`. Its complete object is `0x73C` bytes.

```c
struct UserConfirmPaneFields {
    u8 alert_pane_base[0x634];
    u8 dialog_value_0;          // +0x634, supplied by SMessage
    u8 dialog_value_1;          // +0x635, supplied by SMessage
    char value[256];            // +0x636, string8 bytes plus local terminator
    u8 padding_736[2];
    u32 value_length;           // +0x738, wire range 0 through 255
};                              // size 0x73C
```

The pane displays the main `u16`-counted `SMessage` text. Its OK callback sends `CConfirm` choice `1`; Cancel sends choice `0`. Both echo the stored fields above. The prompt text itself is not retained in this trailing block and is not sent back.

## Town map pane

Exact RTTI `TownMapPane` supports both the built-in map button and server opcode [`0x6B`](../../network/server/107-0x6b-town-map.md).

```c
struct TownMapPaneFields {
    u8 pane_base[0x190];
    u32 animation_phase;        // +0x190, zero then one
    u32 marker_frame;           // +0x194, advanced modulo seven
    u8 unrelated_198[4];
    bool pointer_armed;         // +0x19C
    u8 unrelated_19D[0x33];
    u32 town_map_key;           // +0x1D0, packet u8 widened to u32
    bool current_map_matches;   // +0x1D4
    bool draw_town_icon;        // +0x1D5
    bool use_server_key;        // +0x1D6
};                              // size 0x1D8
```

The built-in button sets `use_server_key` to zero and selects `_tcoord.txt` using the active map number. `SScreenShot` sets it to one and selects `_tncoord.txt` using `town_map_key`.

Timer `0` starts after 100 ms and is then requeued every 50 ms. It advances `marker_frame`, changes `animation_phase` after the initial counter passes five, and invalidates the pane for redraw. The close path cancels all timers owned by the pane.

## Main menu stipulation gate

`MainMenuPane +0x500` is a 32-bit input gate. Both the pointer and keyboard handlers consume the event immediately when it is nonzero. The successful [`SStipulation`](../../network/server/096-0x60-stipulation.md) paths write zero after deciding whether to show `AgreementDialogPane`.

```text
partial struct MainMenuPaneFields {
    u32 stipulation_input_gate  // +0x500, zero allows menu input
    Pane *registered_screen     // +0x504
}
```

The agreement pane's OK action only closes and unregisters that pane. It does not send a packet or perform the gate write. This is why the no-dialog runtime patch can use the existing stipulation continuation without simulating a button press.
