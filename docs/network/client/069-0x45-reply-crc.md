# Reply CRC (`CReplyCRC`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x45` (69) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **reply crc**.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CReplyCRC {
    u8 opcode                 // 0x45
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
