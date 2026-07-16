# Change Slot (`CChangeSlot`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x30` (48) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **change slot**.

## Sent by

Known static callers lead to:

- `Pane::InventoryPane_A, InventoryPane_A::ItemInventoryPane`

## Body

```text
packet CChangeSlot {
    u8 opcode                 // 0x30
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
