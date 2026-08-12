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

## Client response

The packet opens no second `TownMapPane` while one is already active. Otherwise, the client matches `town_map_key` against `_tncoord.txt`. A match selects a town-map asset and its placement metadata. A miss queues an immediate close.

This server-keyed path can select an asset independently of the active client map. It sends no client packet in response. See [Town map overlay](../../rendering/town-map.md) for the shared local and server selection paths, image composition, coordinate projection, and marker animation.

Receiving `SScreenShot` sends no client packet and writes no file. The actual local screenshot function is `render_write_screenshot_bmp`, which creates `lodNNN.bmp`. `TownMapPane` can reach that function through its normal keyboard-command handler, but packet receipt never takes that branch.
