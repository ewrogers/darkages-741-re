# Remove Equip (`SRemoveEquip`)

`SRemoveEquip` empties one worn-equipment slot in both equipment UI views. It does not send a client response.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x38` (56) |
| Transform | derived |
| UI owners | RTTI classes `EquipPane` and `UserInfoPane` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```c
struct SRemoveEquipBody {
    u8 opcode;                         // 0x38
    u8 slot;
};
```

`net_deserialize_remove_equip_server_packet` reads the one-byte slot and widens it to a 16-bit packet-object field. A receive-side trailing zero, when present, is not part of this class.

Slot values use the table on [`SAddEquip`](055-0x37-add-equip.md#equipment-slots).

## Client state

`EquipPane` converts the one-based slot to an array index, then clears the sprite, `name[0]`, current durability, and maximum durability. This is a logical clear rather than a complete wipe. The remaining name bytes and the dye byte stay in memory, but the zero sprite and empty string make the entry inactive.

Unlike the add path, this handler performs no bounds check before indexing the 18-entry arrays. The server must supply a valid slot from `1` through `18`.

`UserInfoPane` independently checks its 19-entry mapping table. It ignores slot `0` and values above `18`, then asks its child equipment view to remove the mapped entry.

See [Equipment panes](../../appendix/runtime/inventory-ui.md#equipment-panes) for the mapped arrays and [`SAddEquip`](055-0x37-add-equip.md) for insertion and login ordering.
