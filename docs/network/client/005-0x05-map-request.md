# Map Request (`CMapRequest`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x05` (5) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed against the map receive and validation path |

## Purpose

The client sends this message for **map request**.

The `SMap` handling path constructs opcode `0x05` inline. It sends map coordinates and locally calculated map data after checking the received map state. The exact CRC-width helper at the end of the body still needs a dedicated trace.

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CMapRequest {
    u8 opcode                 // 0x05
    u16be reserved_0
    u16be reserved_1
    u8 map_x
    u8 map_y
    ... map validation value pending
}
```
