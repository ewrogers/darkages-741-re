# Multi Server (`CMulti`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x57` (87) |
| Common transform | static |
| Representative builder | `net_send_multi_server_selection` at `0x0055A090` |
| Behavioral alias | `CMultiServer` |
| Name provenance | Project-owner protocol name; server-selection behavior confirmed locally |

## Current evidence

The exact client protocol name is `CMulti`. The more descriptive `CMultiServer` alias is supported by the caller, which selects a server record from configuration, and by the `ServerSelectDialogPane` RTTI owner. Server opcode `0x56` has the exact RTTI name [`SMulti`](../server/086-0x56-multi.md).

The client has no derived packet RTTI for `CMulti` itself. The paired names are preserved as recovered instead of being forced to match a constructed `SMultiServer` name.

## Known send sites

- `0x00559F57` in `sub_559F30`, reachable from `TimerHandler::ServerSelectDialogPane`.

## Plaintext body

```text
opcode:u8                 // 0x57
reserved_0:u8             // 0
server_index:u8
reserved_1:u8             // 0
```
