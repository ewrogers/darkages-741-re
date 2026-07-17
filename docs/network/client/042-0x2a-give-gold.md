# Give Gold (`CGiveGold`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x2A` (42) |
| Encoding | session key |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

The client sends this message for **give gold**.

## Sent by

Known static callers lead to:

- `DialogPane::GiveGoldDialogPane`

## Body

```text
packet CGiveGold {
    u8      opcode                    // 0x2A
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
