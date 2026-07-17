# Group (`CGroup`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x2E` (46) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed against the User Look dialog path |

## Purpose

The client sends this message for **group**.

The builder writes opcode `0x2E`, action `2`, and a length-prefixed user name taken from the owning dialog. This protocol uses “group,” not “party.”

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CGroup {
    u8      opcode                    // 0x2E
    u8      action                    // 2 in this builder
    u8      name_length
    bytes   name[name_length]
}
```
