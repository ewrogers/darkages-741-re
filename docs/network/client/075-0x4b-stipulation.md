# Stipulation (`CStipulation`)

<a id="purpose"></a>

The client sends this empty request when the CRC in [`SStipulation`](../server/096-0x60-stipulation.md) does not match the current decoded server greeting. The server can answer with a zlib-compressed replacement.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x4B` (75) |
| Transform | `static` |
| Name provenance | Related class vocabulary matched to the locally confirmed request behavior |

## Body

```text
packet CStipulation {
    u8      opcode                    // 0x4B
}
```

## Sent by

- `net_handle_stipulation_raw` handles the decoded body directly.
- `net_handle_stipulation` handles the typed packet object.

Both sites follow the same mismatch path. See [Server list and greeting](../server-tables.md) for behavior and [Client send sites](../../appendix/runtime/network-objects.md#client-send-sites) for call addresses.
