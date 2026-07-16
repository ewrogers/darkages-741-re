# Add Equip (`SAddEquip`)

`SAddEquip` fills one worn-equipment slot. The client copies the item into the main equipment pane and, when it is open, the separate user-information equipment view.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x37` (55) |
| Transform | derived |
| UI owners | RTTI classes `EquipPane` and `UserInfoPane` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```c
struct SAddEquipBody {
    u8 opcode;                         // 0x37
    u8 slot;
    u16be sprite;
    u8 dye_color;
    string8 name;
    u8 ignored_after_name;             // observed as 0x00
    u32be durability;
    u32be max_durability;
};
```

`name` begins with a one-byte byte count. `net_deserialize_add_equip_server_packet` copies it into a 256-byte packet-object buffer and adds a local NUL.

The next byte is part of the parsed body. The client advances over it without checking its value. It was zero in every supplied login entry, so it may be a wire-level name terminator, but that meaning is not required by the parser.

Some captured bodies have another zero after `max_durability`. That final byte is not consumed by this class. See [Receive-side zero bytes](../packet-transforms.md#receive-side-zero-bytes).

## Equipment slots

The client confirms the numeric shape of the slot table: `0` is a sentinel, and slots `1` through `18` map directly to internal indices `0` through `17`. The semantic names below are project-owner protocol vocabulary supported by observed game behavior. They were not recovered as a C++ enum.

| Value | Slot | Value | Slot |
| ---: | --- | ---: | --- |
| `0` | None | `10` | Right Gauntlet |
| `1` | Weapon | `11` | Belt |
| `2` | Armor | `12` | Greaves |
| `3` | Shield | `13` | Boots |
| `4` | Helmet | `14` | Accessory 1 |
| `5` | Earrings | `15` | Overcoat |
| `6` | Necklace | `16` | Over Helm |
| `7` | Left Ring | `17` | Accessory 2 |
| `8` | Right Ring | `18` | Accessory 3 |
| `9` | Left Gauntlet |  |  |

## Client state

`EquipPane` keeps 18 parallel entries for the sprite, dye, name, and durability pair. It converts the one-based wire slot to a zero-based index and redraws the pane after the update. The name is copied into a 128-byte UI buffer. The dye byte is retained unchanged; this path does not establish how the value maps to the shared rendering palette.

The add path only checks that the decremented index is at most 17. It does not reject the negative index produced by slot `0`, so the server must use slots `1` through `18` for this consumer.

`UserInfoPane` uses a safer 19-entry mapping table. Slot `0` maps to `-1` and is ignored. Slots `1` through `18` select view entries `0` through `17`. Its child equipment view receives the sprite, dye, name, maximum durability, and current durability. The child's exact RTTI class remains unresolved.

The mapped fields are in [Character equipment state](../../appendix/runtime-structures.md#character-equipment-state).

## Supplied login trace

The supplied successful-login trace contains 14 `SAddEquip` packets. They fill occupied slots in ascending order and skip empty slots. Every equipment packet is immediately followed by [`SStatus`](008-0x08-status.md).

Thirteen of the 14 entries are then followed by [`SMessage`](010-0x0a-message.md), which produced the observed equipment text in the message bar. The slot 16 entry instead continues to `SAddInventory` after its status update.

This ordering belongs to the server's login-load loop. The client handles `SAddEquip`, `SStatus`, and `SMessage` independently. Nothing in the equipment handler requires a status or message packet to follow, so a server can batch equipment changes and send fewer status updates.
