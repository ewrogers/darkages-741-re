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

The ordinary equipment action handler accepts UI indices `0` through `17`, adds one, and calls `net_send_remove_equipment`. Wire slots are therefore one-based values `1` through `18`.

`EquipPane` also has a helper that submits slots `1` and `3` through the same builder. This is the tilde-key action identified by project-owner behavior. The local helper body confirms the two requests.

## Body

```text
packet CRemoveEquipment {
    u8      opcode                    // 0x44
    u8      slot                      // one-based equipment slot
}
```

The builder writes only the low byte supplied by the caller. It does not validate the range or check whether the selected slot is occupied. The server-side result is reflected through [`SRemoveEquip`](../server/056-0x38-remove-equip.md), whose consumers clear the corresponding local equipment entry. No additional client fields or variants were found in the representative builder.

The direct by-slot calling contract and main-thread restriction are in [Manual native actions](../../appendix/runtime/manual-actions.md#unequip-by-equipment-slot).
