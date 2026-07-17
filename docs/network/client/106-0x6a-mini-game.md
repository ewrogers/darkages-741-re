# Mini Game (`CMiniGame`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x6A` (106) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **mini game**.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet
- `Pane::FindFarmpet::FindFarmpetPane`

## Body

```text
packet CMiniGame {
    u8      opcode                    // 0x6A
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
