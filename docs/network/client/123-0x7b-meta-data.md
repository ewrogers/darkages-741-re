# Meta Data (`CMetaData`)

<a id="purpose"></a>

The client requests one named metadata table after the server inventory shows that the local cache is missing or stale.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x7B` (123) |
| Transform | `static` |
| Name provenance | Related class vocabulary matched to the locally confirmed builder behavior |

## Sent by

`net_request_metadata` sends the request. Caller traversal reaches `TimerHandler::MetaTableManager` and metadata consumers such as the NPC illustration and metadata option managers. The exact call address is in [Client send sites](../../appendix/runtime/network-objects.md#client-send-sites).

## Body

```text
packet CMetaData {
    u8      opcode                    // 0x7B
    u8      operation                 // 0, request one table
    string8 name
}
```

`net_request_metadata` builds this packet. The paired [`SMetaData`](../server/111-0x6f-meta-data.md) operation 0 carries the zlib-compressed replacement. Function addresses are in the [function reference](../../appendix/functions.md).

See [Metadata files](../../file-formats/metadata.md) for the cache and decoded group format.
