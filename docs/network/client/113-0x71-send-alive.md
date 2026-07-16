# Send Alive (`CSendAlive`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x71` (113) |
| Encoding | startup key |
| Name provenance | Project-owner protocol name, confirmed against a repeating Main Menu timer path |

## Purpose

The client sends this message for **send alive**.

When its pending flag is set, the builder submits the opcode-only body, clears the flag, records connection state, and schedules another callback after `0x7530` milliseconds, or 30 seconds. This strongly supports a heartbeat or keepalive role.

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet
- `main-menu, login, create-user, staff, and backstory pane paths`

## Body

```text
packet CSendAlive {
    u8 opcode                 // 0x71
}
```
