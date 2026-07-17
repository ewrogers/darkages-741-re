# Exception (`CException`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x42` (66) |
| Encoding | startup key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **exception**.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CException {
    u8      opcode                    // 0x42
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
