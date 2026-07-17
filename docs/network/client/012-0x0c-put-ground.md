# Put Ground (`CPutGround`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x0C` (12) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed against the local builder |

## Purpose

The client sends this message for **put ground**.

The builder writes opcode `0x0C`, a four-byte big-endian value, and submits a five-byte body. The value's exact object or item role remains to be confirmed from its callers.

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CPutGround {
    u8      opcode                    // 0x0C
    u32     value
}
```
