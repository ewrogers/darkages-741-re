# Exit Editing Mode (`CExitEditingMode`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x23` (35) |
| Encoding | session key |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

The client sends this message for **exit editing mode**.

## Sent by

Known static callers lead to:

- `DialogPane::EditablePaperPane`

## Body

```text
packet CExitEditingMode {
    u8 opcode                 // 0x23
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
