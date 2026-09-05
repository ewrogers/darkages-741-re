# Send Alive (`CSendAlive`)

<a id="purpose"></a>

`CSendAlive` is an opcode-only message sent by a repeating Main Menu timer. Its 30-second callback interval supports a keepalive role; the server-side policy is not established here.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x71` (113) |
| Transform | `static` |
| Name provenance | Project-owner protocol name, confirmed against a repeating Main Menu timer path |

When its pending flag is set, the builder submits the opcode-only body, clears the flag, records connection state, and schedules another callback after `0x7530` milliseconds, or 30 seconds.

The client has no derived packet RTTI for this name.

## Sent by

Static caller traversal reaches main-menu, login, create-user, staff, and backstory pane paths. Exact UI or subsystem ownership remains incomplete beyond the repeating Main Menu timer path described above.

## Body

```text
packet CSendAlive {
    u8      opcode                    // 0x71
}
```
