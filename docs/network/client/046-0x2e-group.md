# Group (`CGroup`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x2E` (46) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed against the User Look dialog path |

## Purpose

The client sends this message for **group**.

The known builders write opcode `0x2E`, an action byte, and a length-prefixed user name. This protocol uses “group,” not “party.”

Action `2` comes from the User Look dialog path. Action `3` is sent automatically after an incoming [`SGroup`](../server/099-0x63-group.md) request when the local `GroupAnswer` setting is enabled. The exact server meaning of action `3` still needs a paired capture.

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- the User Look dialog
- the `SGroup` handler's automatic answer path

## Body

```text
packet CGroup {
    u8      opcode                    // 0x2E
    u8      action                    // observed: 2 or 3
    u8      name_length
    bytes   name[name_length]
}
```
