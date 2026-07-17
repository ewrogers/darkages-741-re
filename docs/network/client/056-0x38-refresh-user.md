# Refresh User (`CRefreshUser`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x38` (56) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed against the world pane paths |

## Purpose

The client sends this message for **refresh user**.

The builder submits a one-byte body containing only opcode `0x38`.

This request does not reset the rolling [`CMove`](006-0x06-move.md) step counter or its saved send time. `net_handle_move_server_packet` sends it when a direction-`4` correction reports coordinates that differ from the local player object.

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CRefreshUser {
    u8      opcode                    // 0x38
}
```
