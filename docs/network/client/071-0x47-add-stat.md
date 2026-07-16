# Add Stat (`CAddStat`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x47` (71) |
| Encoding | session key |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

The client sends this message for **add stat**.

## Sent by

Known static callers lead to:

- `Pane::StatusInfoPane`

## Body

```text
packet CAddStat {
    u8 opcode                 // 0x47
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
