# Check Time (`CCheckTime`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x75` (117) |
| Common transform | derived |
| Representative builder | `net_send_check_time` at `0x005F7830` |
| Name provenance | Project-owner protocol name, confirmed by direct pairing with RTTI-backed `SCheckTime` |

## Current evidence

The server dispatcher calls this builder only when it receives server opcode `0x68`, whose exact RTTI name is [`SCheckTime`](../server/104-0x68-check-time.md). The response echoes a four-byte server value and appends the current `timeGetTime()` tick count. The timing exchange could support speed-hack detection, but that purpose remains a hypothesis until its server-side expectations or trigger conditions are known.

The prior name came from this direct local pairing, not from client RTTI.

## Known send sites

- `0x005EDF0E` in `net_dispatch_server_packet`, immediately after the opcode `0x68` comparison at `0x005EDEF2`.

## Plaintext body

```text
opcode:u8                 // 0x75
server_value:u32be
client_tick_count:u32be   // timeGetTime()
```
