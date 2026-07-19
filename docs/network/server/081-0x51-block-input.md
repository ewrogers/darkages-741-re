# Block Input (`SBlockInput`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x51` (81) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

`SBlockInput` lets the server temporarily replace the normal cursor with an animated wait cursor and prevent ordinary pointer and keyboard input from reaching the rest of the UI.

This is a modal UI overlay, not a pause command. Network packets, timers, rendering, and the game loop continue while input is blocked.

## Body

```text
packet SBlockInput {
    u8 opcode                         // 0x51
    u8 state
    if state == 0 {
        u8 unknown_block_value
    }
}
```

| `state` | Behavior |
| --- | --- |
| `0` | Begin blocking input |
| `1` | End blocking input |
| Other | Parsed but ignored by the handler |

The conditional `unknown_block_value` is stored in the packet object but never read by the active handler. Its purpose remains unknown.

## Blocking input

For state `0`, the client first checks the `EventMan` mouse-button mask. If the left or right button is held, it emits the matching button-up event before opening the overlay. This avoids leaving a drag, click, or captured pane stuck when the block begins.

The client then creates the exact RTTI class `ClockPane` if its singleton does not already exist. The pane:

- loads `lodclk.epf`;
- selects cursor mode `3` in the root `ScreenPane`;
- follows pointer-move events so the animation stays centered on the pointer;
- returns true for every pointer event and every keyboard or text event, stopping normal pane-tree propagation;
- advances its image frame every 50 ms.

Repeated state `0` messages do not stack multiple panes or restart an existing pane. The button-release check still runs before the singleton test.

## Ending the block

State `1` cancels the clock timer, hides and destroys `ClockPane`, restores root cursor mode `0`, and clears the singleton pointer. A state `1` message does nothing when no clock pane exists.

The client sends no response packet for either state.

## Runtime state

The block is represented primarily by the live `ClockPane` singleton pointer, not by a field in the character, world, or status model. The packet object stores `state` at `+0x10` and the conditional unknown byte at `+0x11`.

The related live UI and input fields are:

- `clock_pane_singleton_ptr`: the active `ClockPane`, or null;
- `ScreenPane +0x27C`: cursor mode, changed to `3` while blocked and restored to `0`;
- `EventMan +0x458`: mouse-button bits, left `0x01` and right `0x02`, cleared through synthesized button-up events when blocking begins.

`SBlockInput` does not write the separate `EventMan +0x454` input-suppression bit. Its blocking behavior comes from `ClockPane` consuming events in the pane tree.

The concrete pane layout is in [Pane and event layouts](../../appendix/runtime/panes.md#clock-pane-fields). The wider dispatch behavior is described in the [event system](../../systems/events.md#server-controlled-input-blocking).
