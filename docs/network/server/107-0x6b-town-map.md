# Town Map (`SScreenShot`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x6B` (107) |
| Encoding | derived |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server uses this packet to open `TownMapPane` for a table entry chosen by the server. It does not capture, save, or upload a screenshot.

`SScreenShot` is nevertheless the exact RTTI class name in this client. The name is misleading when read as an operating-system screenshot command, so this page uses Town Map as the behavioral label while preserving the concrete class name.

## Body

```text
packet SScreenShot {
    u8      opcode                    // 0x6B
    u8      town_map_key
}
```

`net_deserialize_screen_shot_server_packet` reads exactly one payload byte. The handler widens it for `TownMapPane`, but its wire type remains `u8`.

## Server-selected and local modes

The pane has two distinct ways to select town-map art:

| Open path | Selection source | Table |
| --- | --- | --- |
| Built-in map button | Current client map number | `_tcoord.txt` |
| `SScreenShot` | `town_map_key` supplied by the server | `_tncoord.txt` |

The built-in button constructs the pane in current-map mode without sending a packet. That mode finds the active map number in `_tcoord.txt`.

The server packet constructs the same exact RTTI `TownMapPane` in keyed mode. `_tncoord.txt` contains six decimal values per accepted record: the lookup key, a town-map asset number, and four placement values. The packet byte is matched against the first value. The resolved asset number selects `_t%d.spf` and `_t%dn.spf`.

This gives the server one capability the local button does not have: it can choose a town-map entry independently of the client's current map number. That could support subareas, aliases, or scripted map displays, but the exact server-side reason remains unconfirmed. If the key has no table entry, the pane queues an immediate close.

## Client response

The client opens no second `TownMapPane` while one is already active. For a valid entry, it composes the pane from `_t_back.spf`, the two selected town-map images, and `tmuser.epf` for the current-position marker when the resolved map matches the active map.

The marker timer begins with a 100 ms delay. Later ticks are requeued every 50 ms. The callback advances a frame index modulo seven, switches to its second invalidation phase after the initial counter passes five, and redraws the affected map area. Closing the pane cancels its timers.

Receiving `SScreenShot` sends no client packet and writes no file. The actual local screenshot function is `render_write_screenshot_bmp`, which creates `lodNNN.bmp`. `TownMapPane` can reach that function through its normal keyboard-command handler, but packet receipt never takes that branch.
