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

```c
packet CTransferServer {
    u8 opcode;                 // 0x10
    u8 token[];                // exact STransferServer token bytes
}
```

The body length is `1 + token_length`. The builder writes a local zero byte after the token so its temporary buffer can also be treated as a C string, but that terminator is outside the submitted packet length. In the supplied capture, the final displayed `00` is therefore not part of the body sent by this client.

This packet is raw. It does not carry an encrypted-packet sequence or transform trailer.
