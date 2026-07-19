# Object Info (`SObjectInfo`)

`SObjectInfo` supplies another character's equipment appearance, identity, legend marks, portrait, and biography. It is the response paired with [`CRequestObjectInfo`](../client/067-0x43-request-object-info.md).

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x34` |
| Transform | `derived` |
| Name provenance | Provisional project-owner protocol name |
| RTTI | No concrete server-packet RTTI class |
| UI owner | Exact RTTI `UserInfoPane_ForOthers` |

## Body

```text
packet SObjectInfo {
    u8 opcode                    // 0x34
    u32 entity_id

    repeat 18 {                   // implicit EquipmentSlot order below
        u16 sprite
        u8 dye_color
    }

    u8 social_status
    string8 name
    u8 nation                     // Nation
    string8 title
    u8 is_group_open
    string8 guild_rank
    string8 display_class
    string8 guild

    u8 legend_mark_count
    repeat legend_mark_count {
        u8 icon                   // LegendMarkIcon
        u8 color
        string8 key
        string8 text
    }

    u16 content_length
    if content_length != 0 {
        u16 portrait_length
        bytes portrait[portrait_length]
        string16 bio
    }
}
```

The supplied field names match the client layout. The same `UserInfoPane` fields receive `nation`, `title`, `is_group_open`, `guild_rank`, `display_class`, and `guild` from [`SSelfLook`](057-0x39-self-look.md). `social_status` is project-owner protocol vocabulary. The client stores the byte, but no value table or later read of that stored field was found, so it remains a plain `u8` rather than a shared enum.

`nation` uses the shared [`Nation`](../protocol-types.md#nation) type. Legend `icon` uses [`LegendMarkIcon`](../protocol-types.md#legendmarkicon). `dye_color` and legend `color` are palette indexes; the client does not prove named `DyeColor` or `LegendMarkColor` enums.

## Equipment order

The equipment records have no slot byte. Their positions imply these [`EquipmentSlot`](../protocol-types.md#equipmentslot) values:

| Record | Slot |
| ---: | --- |
| `1` | Weapon |
| `2` | Armor |
| `3` | Shield |
| `4` | Helmet |
| `5` | Earrings |
| `6` | Necklace |
| `7` | Left Ring |
| `8` | Right Ring |
| `9` | Left Gauntlet |
| `10` | Right Gauntlet |
| `11` | Belt |
| `12` | Greaves |
| `13` | Accessory 1 |
| `14` | Boots |
| `15` | Overcoat |
| `16` | Over Helm |
| `17` | Accessory 2 |
| `18` | Accessory 3 |

The client mapping table is internal indices `0..11, 13, 12, 14..17`. Accessory 1 therefore appears before Boots instead of following numeric `EquipmentSlot` order.

Each `sprite` remains the exact `u16` read from the wire. The client widens and stores it without masking any high bits. A server library may expose `SpriteFlags.ClearFlags(...)` as a normalized API value, but that transformation is not part of this client's packet parser and should not replace the literal wire field in the schema.

## Portrait and biography tail

The tail uses the same nested length convention as [`CSendPortrait`](../client/079-0x4f-send-portrait.md). For a valid nonempty tail, `content_length` is `4 + portrait_length + bio_length`. Either nested length may be zero.

When `content_length` is zero, the client consumes no nested fields and clears the pane's portrait and biography. For any nonzero value, it tries to decode both nested lengths. It does not check `content_length >= 4` or use that field to bound the nested reads. A stricter implementation may reject values `1` through `3`, as in a `remaining < 4` guard, but that is defensive validation rather than the matched client's exact branch.

## UI routing

The decoded body bypasses the server packet factory. Its handler first finds `entity_id` in the current world and requires that object to be a living object. It then creates or refreshes exact RTTI `UserInfoPane_ForOthers`, applies the equipment and identity fields, rebuilds the legend list, and decodes the portrait and biography.

If the object is absent or is not a living object, the client consumes the packet without opening the pane.
