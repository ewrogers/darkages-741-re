# Keyboard behavior and outgoing packets

## Scan-code translation

`event_dispatch_key_down` at `0x467C10` receives the hardware scan code extracted from bits `16..23` of Win32 `lParam`. If the extended-key bit at bit `24` is set, the translator adds `0x80` before lookup.

The normal and shifted translation tables are stored inside EventMan. Confirmed internal arrow codes are:

| Key | Extended scan | Internal code |
|---|---:|---:|
| Left | `0xCB` | `0x80` |
| Up | `0xC8` | `0x81` |
| Right | `0xCD` | `0x82` |
| Down | `0xD0` | `0x83` |

F1 through F12 use internal values `0x85..0x90`. F5 is therefore `0x89`.

## World shortcuts

`input_handle_world_input_event` at `0x5F1480` handles refresh shortcuts first. Remaining key-down events go to `input_handle_world_key_event` at `0x5F0D20`.

| Input | Conditions | Recovered behavior | Packet |
|---|---|---|---|
| F5 | Internal key `0x89` | Clears movement synchronization state and requests a full object refresh | `CRefresh` `0x38` |
| Ctrl+R | Modifier byte exactly `2` | Same refresh path as F5 | `CRefresh` `0x38` |
| Arrow keys | No special modifier check in movement mapper | Turn, or move one tile when already facing that direction | `CChangeDir` `0x11` or `CMove` `0x06` |
| C, V, X, Z | Mapped to directions `0,1,2,3` | Same turn-or-move path | `CChangeDir` or `CMove` |
| Space | Key-down | Attack, with a short local throttle | `CAttack` `0x13` |
| B | No modifiers | Searches the tile ahead and attempts pickup, with a 100 ms throttle | `CGet` `0x07` when an item is found |
| `-`, `0..9`, `=` | No Alt or Ctrl | Selects hotbar slot `11`, `10`, `1..9`, or `12` | Depends on selected slot use |
| Alt or Ctrl plus number row | Mapping exists at `0x686C98` | Looks up and sends an emotion ID | `CEmotion` `0x1D` |
| Tab | Key-down | Toggles state on the current world child pane | None observed |
| Escape | Active world child exists | Hides or closes that child pane | None observed |
| Backtick | Key-down | Calls the same local mode routine with values `1` and `3`; purpose is still unnamed | None observed |
| J | No modifiers and local guards clear | Enables a local mode at world offsets `+0x280/+0x281`; purpose is still unnamed | Not established |

The number-row branch masks modifiers with `modifier & 3`, so it considers Alt and Ctrl but not Shift. Shift alone follows the no-Alt/no-Ctrl slot path.

## Turn and move sequence

`input_apply_world_direction` at `0x5F0C40` compares the requested direction with the self object:

```c
if (self->direction != direction) {
    object_living_set_direction(self, direction);
    net_send_c_change_dir(world, direction);
} else {
    input_try_move_self(world, direction);
}
```

`input_try_move_self` at `0x5F09E0` checks map bounds and `map_can_move_direction` before updating the local object. It then calls `net_send_c_move` at `0x5F4580`.

The recovered plaintext bodies are:

```text
CChangeDir: 11 direction:u8
CAttack:    13
CMove:      06 direction:u8 movement_sequence:u8
```

The movement sequence is stored at world offset `+0x28A` and increments before each send. World offset `+0x28C` records `timeGetTime()` when the packet is built.

## UI keys and text entry

UI panes receive keyboard events before the world when focused or modal. `ui_image_button_handle_key_event` at `0x438590` treats Enter and Space as button activation and reports the control ID to its parent.

Chat entry, tell entry, and their packet builders are documented separately in [Chat input and outgoing packets](../chat/input-and-send.md). IME composition is handled at the Win32 translation layer, so text panes receive internal composition and character events instead of raw `WM_IME_*` messages.
