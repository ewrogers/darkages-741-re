# Meta Data (`CMetaData`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x7B` (123) |
| Encoding | startup key |
| Name provenance | Related class vocabulary matched to the locally confirmed builder behavior |

## Purpose

The client requests one named metadata table after the server inventory shows that the local cache is missing or stale.

## Sent by

- Direct send at `0x004E54D9` in `net_request_metadata`
- Caller traversal reaches `TimerHandler::MetaTableManager` and metadata consumers such as the NPC illustration and metadata option managers

## Body

```c
packet CMetaData {
    u8 opcode;               // 0x7B
    u8 operation;            // 0, request one table
    u8 name_length;
    u8 name[name_length];
}
```

`net_request_metadata` builds this packet at `0x004E53F0`. The paired [`SMetaData`](../server/111-0x6f-meta-data.md) operation 0 carries the zlib-compressed replacement.

See [Metadata files](../../file-formats/metadata.md) for the cache and decoded group format.
