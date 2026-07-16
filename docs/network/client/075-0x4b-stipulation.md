# Stipulation (`CStipulation`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x4B` (75) |
| Encoding | startup key |
| Name provenance | Related class vocabulary matched to the locally confirmed request behavior |

## Purpose

The client sends this empty request when the CRC in [`SStipulation`](../server/096-0x60-stipulation.md) does not match the current decoded server greeting. The server can answer with a zlib-compressed replacement.

## Body

```c
packet CStipulation {
    u8 opcode;               // 0x4B
}
```

## Sent by

- Direct call at `0x004B8739` from `net_handle_stipulation_raw`
- Direct call at `0x004B8A2F` from `net_handle_stipulation`

Both sites follow the same mismatch path. See [Server list and greeting](../server-tables.md).
