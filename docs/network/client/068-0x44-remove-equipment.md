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

`EquipPane` also has a helper that submits slots `1` and `3` through the same builder. The one-byte slot is passed through unchanged.

## Body

```text
packet CRemoveEquipment {
    u8      opcode                    // 0x44
    u8      slot                      // one-based equipment slot
}
```

The server-side result is reflected through [`SRemoveEquip`](../server/056-0x38-remove-equip.md), whose consumers clear the corresponding local equipment entry. No additional client fields or variants were found in the representative builder.
