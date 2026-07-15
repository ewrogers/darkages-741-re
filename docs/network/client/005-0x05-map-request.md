# Map Request (`CMapRequest`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x05` (5) |
| Common transform | derived |
| Containing function | `0x005F1BF0` |
| Name provenance | Project-owner protocol name, confirmed against the map receive and validation path |

## Current evidence

The `SMap` handling path constructs opcode `0x05` inline at `0x005F1F9A`. It sends map coordinates and locally calculated map data after checking the received map state. The exact CRC-width helper at the end of the body still needs a dedicated trace.

The client has no derived packet RTTI for this name.

## Known send sites

- `0x005EDCE7` in `net_dispatch_server_packet` dispatches the enclosing `SMap` handler at `0x005F1BF0`. The outbound request is built inline at `0x005F1F9A`.

## Plaintext body

```text
opcode:u8                 // 0x05
reserved_0:u16be
reserved_1:u16be
map_x:u8
map_y:u8
... map validation value pending
```
