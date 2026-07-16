# Change Direction (`CChangeDirection`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x11` (17) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed against the world input path |

## Purpose

The client sends this message for **change direction**.

The builder writes opcode `0x11` followed by one direction byte and submits a two-byte body.

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CChangeDirection {
    u8 opcode                 // 0x11
    u8 direction
}
```
