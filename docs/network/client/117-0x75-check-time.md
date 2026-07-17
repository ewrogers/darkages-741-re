# Check Time (`CCheckTime`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x75` (117) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed by direct pairing with RTTI-backed `SCheckTime` |

## Purpose

The client sends this message for **check time**.

The server dispatcher calls this builder only when it receives server opcode `0x68`, whose exact RTTI name is [`SCheckTime`](../server/104-0x68-check-time.md). The response echoes a four-byte server value and appends the current `timeGetTime()` tick count. The timing exchange could support speed-hack detection, but that purpose remains a hypothesis until its server-side expectations or trigger conditions are known.

The prior name came from this direct local pairing, not from client RTTI.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CCheckTime {
    u8      opcode                    // 0x75
    u32     server_value
    u32     client_tick_count         // timeGetTime()
}
```
