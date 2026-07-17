# Transfer Server (`CTransferServer`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x10` (16) |
| Transform | `raw` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message after reconnecting to the endpoint in [`STransferServer`](../server/003-0x03-transfer-server.md). It proves possession of the handoff token by returning it unchanged to the new server.

## Sent by

`net_dispatch_main_menu_events` routes an `STransferServer` object to `net_handle_transfer_server`. That handler owns the reconnect and sends this body after the new connection is ready.

## Body

```text
packet CTransferServer {
    u8      opcode                    // 0x10
    bytes   token[remaining]                   // exact STransferServer token bytes
    u8      terminator                // 0x00, appended by net_submit_client_packet
}
```

The builder passes `1 + token_length` bytes to `net_submit_client_packet`. The submission layer appends `0x00`, increases the queued length, and sends `2 + token_length` bytes. The final `00` in the supplied capture is therefore part of the raw body sent by this client.

This packet is raw. It does not carry an encrypted-packet sequence or transform trailer.
