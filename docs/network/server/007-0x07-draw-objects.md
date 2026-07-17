# Draw Objects (`SDrawObjects`)

`SDrawObjects` adds creatures, NPC-style actors, and ground items to the current map. One packet may contain any number of records, and creature and item records may be mixed in the same body.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x07` (7) |
| Encoding | derived |
| Runtime classes | `WorldObject_Monster`, `WorldObject_Item`, `MonsterObjectImageSession`, and `WorldObject_Name_Pane` |
| Name provenance | `SDrawObjects` is exact Microsoft C++ RTTI from the target |

## Body

```text
packet SDrawObjects {
    u8      opcode                    // 0x07
    u16     entity_count

    repeat entity_count {
        u16     x
        u16     y
        u32     entity_id
        u16     tagged_sprite

        if tagged_sprite in 0x4000..0x7FFF {
            u8      palette_selectors[4]
            u8      direction         // Direction
            u8      unused
            u8      creature_type     // CreatureType

            if creature_type == 2 {
                string8 name
            }
        }

        if tagged_sprite in 0x8000..0xBFFF {
            u8      dye_color
            u8      unused[2]
        }
    }
}
```

The client recognizes only those two tagged sprite ranges. Values outside them still consume the common record prefix, but the handler does not create an object. Unlike the supplied application model, the client does not throw an invalid-entity error.

The complete body is not flattened into a fixed array. The packet deserializer reads `entity_count`, retains a reader over the remaining bytes, and `net_read_draw_object_record` consumes one variable-length record for each handler iteration. This permits creature and item variants to be interleaved without a per-record length.

## Sprite namespaces

The high sprite bits select the local object class. The tag is removed before the sprite is given to the renderer. These values are also summarized under [Tagged world sprites](../protocol-types.md#tagged-world-sprites).

| Tagged value | Local class | Sprite sent to renderer |
| --- | --- | --- |
| `0x4000..0x7FFF` | `WorldObject_Monster` | `tagged_sprite - 0x4000` |
| `0x8000..0xBFFF` | `WorldObject_Item` | `tagged_sprite - 0x8000` |

`WorldObject_Monster` represents both monsters and Mundanes, the game's term for NPCs. There is no separate `WorldObject_NPC` RTTI class in this client. The shared [`Direction`](../protocol-types.md#direction) values control the creature's initial facing.

## Creature records

The four bytes previously treated as one unknown `u32` are palette selectors. The client copies up to four 16-byte color-range descriptions from the monster sprite resource, replaces each description's palette selector with the corresponding packet byte, and saves them in `MonsterObjectImageSession`. Rendering then uses those descriptions to remap the indexed monster pixels.

The sprite resource may define fewer than four replaceable ranges. The client therefore uses:

```c
palette_count = min(4, sprite_resource.palette_range_count);
```

Extra packet selectors remain consumed but have no visible effect for that sprite.

The byte after `direction` is read into the temporary record and never used by the handler. It does not survive in `WorldObject_Monster` or its image session.

The shared [`CreatureType`](../protocol-types.md#creaturetype) table records all five project names and the behavior this client confirms. Most importantly, value `1`, Passable, is explicitly ignored by the destination-object blocking check. Value `2`, Mundane, identifies an NPC and is the only value followed by `name`. Values `1`, `2`, and `3` also select distinct per-object collision levels; values `0` and `4` share the default.

The optional name is not copied into the living object's `+0x112` character buffer. Instead, the client creates an RTTI `WorldObject_Name_Pane`, retains up to 63 name bytes plus a NUL, and attaches that pane at the common world-object `+0x58` field. This is the reliable place to read an NPC-style label in memory.

## Ground-item records

`dye_color` and the untagged sprite are retained in `WorldObject_Item` and select the ground image. The two following bytes are read separately and discarded. They do not affect construction, insertion, drawing, or the retained item object in this build.

After insertion, the handler calls the item's class-specific refresh method. That resolves its cached image and any local ground-item visual state from the sprite and dye. It does not use the discarded bytes.

### Dropped gold

A successful [`CDropGold`](../client/036-0x24-drop-gold.md) returns as an ordinary `WorldObject_Item` record beneath the character. The server chooses the sprite to communicate the relative size of the dropped amount, with observed representations such as a silver coin, gold coin, silver pile, and gold pile.

There is no numeric gold amount in this item record. The client does not choose the visual tier from an amount. It removes the `0x8000` item tag and renders the sprite supplied by the server. The exact amount thresholds and sprite IDs for the observed representations remain unconfirmed.

## World state

Creature and item creation follows the same identity rules as human objects:

1. Remove an existing object with the same `entity_id`.
2. Allocate the concrete RTTI class.
3. Store the 32-bit ID and widen the packet coordinates into signed 32-bit Y, X fields.
4. Insert the object into the shared ID and coordinate indexes.
5. Build the class-specific image session or cached item image.

The ID index is an ordered tree, not a flat entity array. `WorldPane + 0x194` points to `WorldObjectList`; its ID-tree nodes pair the server ID with a reference-counted `WorldObject` pointer. Creatures, items, other players, and the local player therefore share one lookup namespace.

The packet object is temporary. Useful retained layouts for the ID index, `WorldObject_Monster`, `MonsterObjectImageSession`, `WorldObject_Item`, and the name pane are in [World objects](../../appendix/runtime/world.md#dynamic-object-index).

## Related updates

Later packets operate on the shared `entity_id`:

- [`SMoveObject`](012-0x0c-move-object.md) moves a living creature.
- [`SChangeDirection`](017-0x11-change-direction.md) changes its facing.
- [`SMotion`](026-0x1a-motion.md) starts a living-object animation.
- [`SRemoveObjects`](014-0x0e-remove-objects.md) removes a creature, item, or human from the indexes.

If a later living-object update refers to an ID the client does not have, the client can request that the server send the object's description again.
