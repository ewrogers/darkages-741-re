# Field Map (`CFieldMap`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x3F` (63) |
| Encoding | session key |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

The client sends this message for **field map**.

## Sent by

Known static callers lead to:

- `LineInputPane::CommandLineInputPane`

## Body

```text
packet CFieldMap {
    u8 opcode                 // 0x3F
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
