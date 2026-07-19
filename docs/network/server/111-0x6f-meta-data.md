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
    u8      opcode                    // 0x6F
    u8      operation

    if operation == 0 {
        string8 name
        u32     crc
        u16     payload_length
        bytes   payload[payload_length]
    }

    if operation == 1 {
        u16     entry_count
        repeat entry_count {
            string8 name
            u32     crc
        }
    }
}
```

Operation `0` inflates the zlib payload, checks CRC32 over the decoded bytes, saves the original compressed stream, and applies one named metadata table. Operation `1` rebuilds the manager's table of metadata names and CRC values, then requests files that are missing or stale.

The decoded payload is a big-endian group container with length-prefixed names and values. See [Metadata files](../../file-formats/metadata.md).

The paired request is [Meta Data (`CMetaData`)](../client/123-0x7b-meta-data.md).
