# Exchange (`CExchange`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x4A` (74) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **exchange**.

## Sent by

Known static callers lead to:

- `DialogPane::ExchangeDialog`

## Body

```text
packet CExchange {
    u8      opcode                    // 0x4A
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
