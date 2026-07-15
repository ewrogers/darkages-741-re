# Send Alive (`CSendAlive`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x71` (113) |
| Common transform | static |
| Representative builder | `net_send_alive` at `0x004BA010` |
| Name provenance | Project-owner protocol name, confirmed against a repeating Main Menu timer path |

## Current evidence

When its pending flag is set, the builder submits the opcode-only body, clears the flag, records connection state, and schedules another callback after `0x7530` milliseconds, or 30 seconds. This strongly supports a heartbeat or keepalive role.

The client has no derived packet RTTI for this name.

## Known send sites

- `0x004B9F9C` in `sub_4B9F70`, a `TimerHandler::MainMenuPane` virtual method.
- `0x004B9FE6` in `sub_4B9FB0`, reachable from main-menu, login, create-user, staff, and backstory pane paths.

## Plaintext body

```text
opcode:u8                 // 0x71
```
