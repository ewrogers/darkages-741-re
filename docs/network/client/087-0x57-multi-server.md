# Multi Server (`CMulti`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x57` (87) |
| Encoding | startup key |
| Behavioral alias | `CMultiServer` |
| Name provenance | Project-owner protocol name; server-selection behavior confirmed locally |

## Purpose

The client sends this message for **multi server**.

The exact client protocol name is `CMulti`. The more descriptive `CMultiServer` alias is supported by the caller, which selects a server record from configuration, and by the `ServerSelectDialogPane` RTTI owner. Server opcode `0x56` has the exact RTTI name [`SMulti`](../server/086-0x56-multi.md).

The client has no derived packet RTTI for `CMulti` itself. The paired names are preserved as recovered instead of being forced to match a constructed `SMultiServer` name.

## Sent by

Known static callers lead to:

- `TimerHandler::ServerSelectDialogPane`

## Body

```text
packet CMulti {
    u8 opcode                 // 0x57
    u8 reserved_0             // 0
    u8 server_index
    u8 reserved_1             // 0
}
```
