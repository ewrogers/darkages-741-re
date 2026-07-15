# Version Check (`SVersionCheck`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x00` (0) |
| Common transform | raw |
| Registered server packet class | None found |
| Handler | `net_handle_version_check` at `0x004B7F80` |
| Internal name provenance | Project-owner protocol knowledge, supported by the local version/bootstrap handler |

## Current evidence

`net_dispatch_main_menu_events` at `0x004B8B70` routes decoded opcode `0x00` directly to `net_handle_version_check`. It does not construct an RTTI packet object. Subtype `0` checks configuration state and installs the session seed-table selector and static key.

## Plaintext body

```text
opcode:u8
subtype:u8

if subtype == 0:
    configuration_crc:u32be
    seed_table_selector:u8
    static_key_length:u8
    static_key:bytes[static_key_length]
```

The handler reads the selector from body offset 6 at `0x004B8038`, reads the key length from offset 7 at `0x004B805F`, and queues the key beginning at offset 8 at `0x004B806A`.

Selector values `0` through `9` choose the mappings documented in [Packet transforms](../packet-transforms.md). The executable starts with selector `0` and the embedded nine-byte static key, but this subtype can replace both values.

Subtype `1` displays a localized error. Subtype `2` opens a data-driven UI using the remaining body. Its detailed layout remains unknown.

The paired request is [Version (`CVersion`)](../client/000-0x00-version.md).
