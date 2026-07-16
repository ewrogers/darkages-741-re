# Version Check (`SVersionCheck`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x00` (0) |
| Encoding | none |
| Packet class | None found |
| Internal name provenance | Project-owner protocol knowledge, supported by the local version/bootstrap handler |

## Purpose

The server sends this message for **version check**.

`net_dispatch_main_menu_events` routes decoded opcode `0x00` directly to `net_handle_version_check`. It does not construct an RTTI packet object. Subtype `0` checks configuration state and installs the session seed-table selector and static key.

## Body

```text
packet SVersionCheck {
    u8 opcode                 // 0x00
    u8 subtype

    if subtype == 0:
        u32be configuration_crc
        u8 seed_table_selector
        u8 static_key_length
        bytes static_key[static_key_length]
}
```

The handler reads the selector from body offset 6, reads the key length from offset 7, and queues the key beginning at offset 8.

Selector values `0` through `9` choose the mappings documented in [Packet transforms](../packet-transforms.md). The executable starts with selector `0` and the embedded nine-byte static key, but this subtype can replace both values.

Subtype `1` displays a localized error. Subtype `2` opens a data-driven UI using the remaining body. Its detailed layout remains unknown.

The paired request is [Version (`CVersion`)](../client/000-0x00-version.md).
