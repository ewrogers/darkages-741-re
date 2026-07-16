# Transfer Server (`CTransferServer`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x10` (16) |
| Encoding | none |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **transfer server**.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CTransferServer {
    u8 opcode                 // 0x10
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
