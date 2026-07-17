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
