# Shared protocol types

Several packets carry the same one-byte game concepts. This page is the canonical value reference for those shared wire types. Packet pages link here and keep only behavior specific to that packet.

These are protocol values, not C++ memory layouts. Each value is stored as a `u8` unless its section says otherwise.

## Direction

`Direction` is shared by movement, facing, and visible-world updates.

| Value | Name | Coordinate change |
| ---: | --- | --- |
| `0` | Up | `y - 1` |
| `1` | Right | `x + 1` |
| `2` | Down | `y + 1` |
| `3` | Left | `x - 1` |

The common coordinate helper defines only values `0` through `3`. Active keyboard and pointer movement also produce only those values. `SMove` handles value `4` separately as a no-step correction signal, so it is not a fifth coordinate direction. The client does not give that control value an enum name.

Used by [`CMove`](client/006-0x06-move.md), [`SMove`](server/011-0x0b-move.md), [`CChangeDirection`](client/017-0x11-change-direction.md), [`SUserAppearance`](server/005-0x05-user-appearance.md), [`SDrawObjects`](server/007-0x07-draw-objects.md), and [`SDrawHumanObjects`](server/051-0x33-draw-human-objects.md).

## CreatureType

`CreatureType` describes the kind of `WorldObject_Monster` carried by `SDrawObjects`. The names are project-owner protocol vocabulary. The client confirms several value-specific behaviors, but it does not contain a friendly enum table.

| Value | Name | Client 7.41 evidence |
| ---: | --- | --- |
| `0` | Monster | Uses the default collision level and normally blocks movement |
| `1` | Passable | The destination-object check explicitly skips blocking for this value |
| `2` | Mundane | An NPC; the only value followed by a `string8` name, which becomes a visible name pane |
| `3` | Solid | Uses a distinct collision level and normally blocks movement; the friendly name is not independently recovered |
| `4` | Aisling | Uses the default client branches; the friendly name is not independently recovered |

Construction stores the type on `WorldObject_Monster` and selects collision levels `0x96`, `0x8C`, and `0x82` for values `1`, `2`, and `3`. Other values use `0x78`. The map's collision cache retains the highest object level in each tile, but the proposed-movement check also tests `creature_type` directly.

Living objects have a separate nonblocking state at `+0xD4`. Normal monster construction clears it. If another runtime path sets it, type `3` is the only non-Passable creature allowed through that special branch. No active packet path that sets this state on a monster has been confirmed.

Used by [`SDrawObjects`](server/007-0x07-draw-objects.md).

## Tagged world sprites

Some world-object records use the high bits of a `u16` sprite value as a namespace tag.

| Tagged range | Namespace | Untagged value |
| --- | --- | --- |
| `0x4000..0x7FFF` | Monster or creature | `tagged_sprite - 0x4000` |
| `0x8000..0xBFFF` | Ground item | `tagged_sprite - 0x8000` |

The target performs explicit range tests. Values outside these ranges are not valid creature or ground-item selectors for `SDrawObjects`, and `0xC000..0xFFFF` is not treated as a combination of both tags.

Used by [`SDrawObjects`](server/007-0x07-draw-objects.md) and the monster-disguise form of [`SDrawHumanObjects`](server/051-0x33-draw-human-objects.md).

## CharacterClass

| Value | Name |
| ---: | --- |
| `0` | Peasant |
| `1` | Warrior |
| `2` | Rogue |
| `3` | Wizard |
| `4` | Priest |
| `5` | Monk |

The names are project-owner protocol vocabulary. The client independently confirms that `2` selects the Rogue-only Tab-map configuration, including its zoom controls. It does not contain a complete local table naming all six values.

Used by [`SUserAppearance`](server/005-0x05-user-appearance.md) and [`SSelfLook`](server/057-0x39-self-look.md).

## EquipmentSlot

| Value | Name | Value | Name |
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

The client confirms the numeric shape: `0` is a sentinel, and wire values `1` through `18` map directly to internal indices `0` through `17`. The slot names are project-owner protocol vocabulary supported by observed equipment behavior, not a recovered C++ enum.

Used by [`SAddEquip`](server/055-0x37-add-equip.md) and [`SRemoveEquip`](server/056-0x38-remove-equip.md).

## Element

| Value | Name | Value | Name |
| ---: | --- | ---: | --- |
| `0` | None | `5` | Light |
| `1` | Fire | `6` | Dark |
| `2` | Water | `7` | Wood |
| `3` | Wind | `8` | Metal |
| `4` | Earth | `9` | Undead |

The extra-status pane contains and indexes this exact ten-entry string table. The lookup is not range-checked, so valid packet values are `0` through `9`.

Used by the attack and defense fields in [`SStatus`](server/008-0x08-status.md).

## MapFlags

`MapFlags` combines a low-nibble weather or lighting mode with independent high-bit options.

| Value | Name | Client 7.41 behavior |
| ---: | --- | --- |
| `0x00` | None | No weather setup |
| `0x01` | Snow | Creates the falling-snow overlay |
| `0x02` | Rain | Recognized explicitly, but performs no local setup |
| `0x03` | Darkness | Forces black ambient light and enables human-centered light masks |
| `0x40` | NoMap | Disables the Tab map overlay for every class |
| `0x80` | Winter | Selects alternate ground and static art |

`Darkness` is an exact mode, even though its numeric value equals `Snow | Rain`. The client does not combine the snow and rain behaviors. Bit `0x20` appears in nearby constants but has no code reference or confirmed protocol meaning.

Used by [`SMapSize`](server/021-0x15-map-size.md).

## Nation

| Value | Name | Value | Name |
| ---: | --- | ---: | --- |
| `0` | None | `7` | Noes |
| `1` | Suomi | `8` | Unknown |
| `2` | Unknown | `9` | Piet |
| `3` | Loures | `10` | Unknown |
| `4` | Mileth | `11` | Abel |
| `5` | Tagor | `12` | Undine |
| `6` | Rucesion | `13` | Unknown |

Local `NationDesc` metadata confirms Suomi and values `3` through `7` by name. Piet, Abel, and Undine are project-owner protocol vocabulary. No matching local name was recovered for values `2`, `8`, `10`, or `13`.

Used by [`SSelfLook`](server/057-0x39-self-look.md).

## LegendMarkIcon

| Value | Name | Value | Name |
| ---: | --- | ---: | --- |
| `0` | Aisling | `5` | Monk |
| `1` | Warrior | `6` | Heart |
| `2` | Rogue | `7` | Victory |
| `3` | Wizard | `8` | None sentinel |
| `4` | Priest |  |  |

The names are project-owner protocol vocabulary. `LegendListPane` loads exactly eight drawable frames, values `0` through `7`. Value `8` is a sentinel and is not a ninth drawable icon.

Used by legend records in [`SSelfLook`](server/057-0x39-self-look.md).

## Byte domains that are not enums yet

Some shared byte fields look enum-like but do not have a verified value table:

- `dye_color` is a palette or dye index used by inventory and equipment.
- Legend `color` and human `name_style` are palette indexes, not named enums.
- `rest_position` changes standing-motion setup, but its value-to-pose mapping is unresolved.
- `light_mask_id` selects `mask1%02d.epf` while Darkness mode is active. It is an asset selector, not a recovered lantern enum.
- `spell_args_type` selects spell targeting or prompt behavior, but the complete value mapping is not yet established.

Keep these fields as `u8` values until direct client behavior supports stable names.
