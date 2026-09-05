# Refresh User (`CRefreshUser`)

<a id="purpose"></a>

`CRefreshUser` requests a player refresh. One confirmed trigger is a server movement correction whose coordinates differ from the local player object.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x38` (56) |
| Transform | `derived` |
| Name provenance | Project-owner protocol name, confirmed against the world pane paths |

The builder submits a one-byte body containing only opcode `0x38`.

This request does not reset the rolling [`CMove`](006-0x06-move.md) step counter or its saved send time. `net_handle_move_server_packet` sends it when a direction-`4` correction reports coordinates that differ from the local player object.

The client has no derived packet RTTI for this name.

## Sent by

The confirmed correction path is `net_handle_move_server_packet`, described above. A separate UI owner has not been established.

## Body

```text
packet CRefreshUser {
    u8      opcode                    // 0x38
}
```
