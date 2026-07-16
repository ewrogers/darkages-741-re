# Remove Equipment (`CRemoveEquipment`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x44` (68) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **remove equipment**.

## Sent by

Known static callers lead to:

- `DialogPane::EquipPane`
- UI or subsystem owner not known yet

## Body

```text
packet CRemoveEquipment {
    u8 opcode                 // 0x44
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
