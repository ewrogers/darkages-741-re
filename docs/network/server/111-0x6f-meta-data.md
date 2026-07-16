# Meta Data (`SMetaData`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x6F` (111) |
| Encoding | startup key |
| Packet class | None found |
| Internal name provenance | Project-owner protocol knowledge, confirmed by `MetaTableManager` behavior |

## Purpose

The server sends this message for **meta data**.

`MetaTableManager` compares the decoded command with `0x6F` and routes the body directly. Metadata processing needs manager state and custom blob validation, so this command bypasses the general server packet factory.

## Body

```text
packet SMetaData {
    u8 opcode                 // 0x6F
    u8 operation

    if operation == 0:
        u8 name_length
        bytes name[name_length]
        u32be crc
        u16be payload_length
        bytes payload[payload_length]

    if operation == 1:
        u16be entry_count
        repeat entry_count times:
            u8 name_length
            bytes name[name_length]
            u32be crc
}
```

Operation `0` validates and applies one named metadata blob. Operation `1` rebuilds the manager's table of metadata names and CRC values. The payload's internal encoding remains to be documented.

The paired request is [Meta Data (`CMetaData`)](../client/123-0x7b-meta-data.md).
