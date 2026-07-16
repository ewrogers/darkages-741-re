# Stipulation (`SStipulation`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x60` (96) |
| Encoding | startup key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

This packet keeps the selected server greeting in sync. The local greeting is stored in `mServer.tbl`.

## Body

```c
packet SStipulation {
    u8 opcode;               // 0x60
    u8 mode;

    if (mode == 0) {
        u32be greeting_crc32;
    }

    if (mode == 1) {
        u16be compressed_size;
        u8 zlib_data[compressed_size];
    }
}
```

Mode 0 compares the received CRC32 with the decoded local greeting. A match displays the greeting. A mismatch sends an empty [`CStipulation`](../client/075-0x4b-stipulation.md) request.

Mode 1 inflates the replacement into a buffer capped at 10,000 bytes, saves the updated server table, and displays the new greeting.

## Handlers

- `net_handle_stipulation_raw` at `0x004B8570` parses a decoded packet buffer directly.
- `net_handle_stipulation` at `0x004B8890` handles the RTTI-backed packet object.

The constructor and packet factory also confirm opcode `0x60` for the `SStipulation` class. See [Server list and greeting](../server-tables.md).
