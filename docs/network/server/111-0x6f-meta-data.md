# Meta Data (`SMetaData`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x6F` (111) |
| Common transform | static |
| Registered server packet class | None found |
| Dispatcher | `net_dispatch_metadata_events` at `0x004E4D80` |
| Handler | `net_handle_metadata` at `0x004E4EA0` |
| Internal name provenance | Project-owner protocol knowledge, confirmed by `MetaTableManager` behavior |

## Current evidence

The RTTI-backed `MetaTableManager` owns the dispatcher. At `0x004E4DB8` it compares the decoded body opcode with `0x6F` and routes the byte buffer directly. Metadata processing needs manager state and custom blob validation, so this opcode bypasses the general server packet factory.

## Plaintext body

```text
opcode:u8
operation:u8

if operation == 0:
    name_length:u8
    name:bytes[name_length]
    crc:u32be
    payload_length:u16be
    payload:bytes[payload_length]

if operation == 1:
    entry_count:u16be
    repeat entry_count times:
        name_length:u8
        name:bytes[name_length]
        crc:u32be
```

Operation `0` validates and applies one named metadata blob. Operation `1` rebuilds the manager's table of metadata names and CRC values. The payload's internal encoding remains to be documented.

The paired request is [Meta Data (`CMetaData`)](../client/123-0x7b-meta-data.md).
