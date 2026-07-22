# Draw Human Objects (`SDrawHumanObjects`)

`SDrawHumanObjects` creates or refreshes a player-shaped world object. It is also how the server draws the local player. A record whose entity ID matches the saved self ID becomes `WorldObject_User`; every other record becomes `WorldObject_Human`.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x33` (51) |
| Transform | derived |
| Runtime classes | `WorldObject_User`, `WorldObject_Human`, `HumanObjectImageSession`, and `MonsterObjectImageSession` |
| Name provenance | `SDrawHumanObjects` is exact Microsoft C++ RTTI from the target |

## Body layout

The packet has a normal human form and a monster-disguise form. Both end with the same name fields.

```text
packet SDrawHumanObjects {
    u8      opcode                    // 0x33
    u16     x
    u16     y
    u8      direction                 // Direction
    u32     entity_id
    u16     head_sprite

    if head_sprite != 0xFFFF {
        u8      packed_body           // high nibble body, low nibble pants dye
        u16     arms_sprite
        u8      boots_sprite
        u16     armor_sprite
        u8      shield_sprite
        u16     weapon_sprite
        u8      hair_color
        u8      boots_color

        u8      accessory1_color
        u16     accessory1_sprite
        u8      accessory2_color
        u16     accessory2_sprite
        u8      accessory3_color
        u16     accessory3_sprite

        u8      light_mask_id
        u8      rest_position
        u16     overcoat_sprite
        u8      overcoat_color
        u8      skin_color
        u8      is_translucent
        u8      face_shape
    } else {
        u16     tagged_monster_sprite
        u8      monster_color
        u8      ignored_color
        bytes   unknown[6]
    }

    u8      name_style
    string8 name
    string8 group_ad_text
}
```

`boots_sprite` and `shield_sprite` are one byte on the wire, then widened to 16 bits in the packet object. Fixed normal-form fields through `name_style` occupy 41 bytes, counting the opcode. Two `string8` values follow; with both empty, the complete body is 43 bytes. Each string can carry at most 255 bytes.

## Coordinates, identity, and direction

The wire order is X, then Y. The packet object sign-extends both 16-bit coordinates to 32 bits. A live world object stores them in the opposite memory order:

```c
object->tile_y = packet->y;          // WorldObject +0x40
object->tile_x = packet->x;          // WorldObject +0x44
```

The handler compares `entity_id` with the self ID retained from [`SUserAppearance`](005-0x05-user-appearance.md). It allocates a 0x200-byte `WorldObject_User` for a matching ID and a 0x1F0-byte `WorldObject_Human` otherwise. Existing objects are refreshed instead of duplicated.

The direction byte uses the shared [`Direction`](../protocol-types.md#direction) type. It is passed to the living-object motion system and retained at human-object offset `+0x192`. No additional direction value is handled here.

## Packed body and pants color

The client shifts the high nibble down by four to select the body form. The low nibble becomes `pants_color`. When it is nonzero, the client also creates pants part sprite `1`; zero removes that part.

| Packed high bits | Project protocol name | Client prefix | Body sprite | Additional effect |
| ---: | --- | --- | ---: | --- |
| `0x00` | `None` | M | `0` | No base-body resource |
| `0x10` | `Male` | M | `1` | Normal male form in the supplied login trace |
| `0x20` | `Female` | W | `1` | Normal female form |
| `0x30` | `MaleGhost` | M | `2` | Sets the nonblocking-human state |
| `0x40` | `FemaleGhost` | W | `2` | Sets the nonblocking-human state |
| `0x50` | `MaleInvisible` | M | `1` | Forces translucency on |
| `0x60` | `FemaleInvisible` | W | `1` | Forces translucency on |
| `0x70` | `MaleJester` | M | `4` | No additional state flag |
| `0x80` | `MaleHead` | M | `5` | Head-only form used by the observed swimming appearance |
| `0x90` | `FemaleHead` | W | `5` | Head-only form used by the observed swimming appearance |
| `0xA0` | `MaleBlank` | M | `10` | Keeps the shifted selector as the body ID |
| `0xB0` | `FemaleBlank` | M default | `11` | Keeps the shifted selector as the body ID |

The friendly names are project-owner protocol vocabulary. They are not compiler-recovered strings. The parser has explicit switch cases only for shifted selectors 0 through 9. Selectors `0xA` and `0xB` bypass that switch, retain raw body IDs 10 and 11, and leave the zero-filled prefix at its M value. `FemaleBlank` is therefore distinguished by body ID 11 rather than a W prefix in client 741.

For the explicit cases, M and W are literal resource-name prefixes used by the renderer. Packed `MaleInvisible` and `FemaleInvisible` overwrite the later `is_translucent` field with `1` after the whole record has been read.

Body sprite `2` sets `WorldObject_Human + 0xD4`. Local dynamic-object collision checks treat that human as nonblocking. This is separate from translucency at `+0xD5`.

The project protocol calls the paired body-sprite-2 forms `MaleGhost` and `FemaleGhost`. This agrees with the client marking both nonblocking. `MaleJester` instead selects body sprite `4` and sets no additional collision or translucency state.

`is_translucent` does not make the player invisible. It tells the living-object renderer to draw the supplied human sprite layers translucently. The server uses this viewer-facing form when the receiving player is allowed to see someone who would otherwise be invisible, commonly because the viewer has See Invisible. Packed variants `5` and `6` force the same translucent state even if the later wire byte was zero.

`MaleHead` and `FemaleHead` load the small `MM005` and `WM005` motion families used for the observed swimming appearance. The client does not choose this form from a local skill check. The server must send the packed variant. See [Movement and swimming](../../systems/movement-and-swimming.md).

## Equipment and appearance layers

The normal form is converted into a 0x30-byte `HumanAppearanceRecord`. The renderer selects body, head, arms, boots, armor, shield, weapon, three accessories, overcoat, and face layers from that record.

An overcoat suppresses the ordinary pants, armor, and arms layers while it is present. Sprite ID zero suppresses the corresponding part filename. The packet also initializes two internal appearance slots to zero because this wire format does not supply them.

Ghost body sprite `2` does not itself suppress equipment. The human image session still attempts all 21 categories, and the part selector reads armor independently of the body. An observed unarmored ghost is therefore most likely a record with zero equipment selectors. Private art availability could also affect whether a selected overlay has a usable frame, but there is no Ghost-dependent armor-clearing branch in this client.

`rest_position` is retained at appearance offset `+0x2D` and changes the standing-motion setup. The exact value-to-pose enum is not yet established. `face_shape` is used as the sprite selector for human part `0x14`.

The client does not create a separate `is_hidden` field from `body_sprite == 0 && !is_translucent`. Individual zero sprite IDs simply omit their own layers. The server uses that behavior for the invisible-player form described below.

## Invisible player form

Invisible players are still sent as normal human records so they remain part of local world state and collision. The server keeps the real entity ID, coordinates, and direction, but supplies zero for the human appearance fields and sends empty name and group-ad strings.

The client still creates or refreshes the player's `WorldObject_User` or `WorldObject_Human`. Body sprite `0` does not set `nonblocking_human`, so another local player can still collide with the invisible object. Zero body, head, equipment, accessory, and face selectors produce no visible part resources, while the empty name produces no visible name text.

Later movement updates can change the invisible object's coordinates and direction normally. There are no visible sprite layers to animate, so the movement is represented in world and collision state without a visible walking animation. A later nonzero `SDrawHumanObjects` record for the same entity restores its visible appearance.

When the receiving player can see invisible entities, the server instead sends the real nonzero appearance with `is_translucent` enabled. `MaleInvisible` and `FemaleInvisible` force exactly this translucent normal-body form. The entity is then visible with its normal sprite layers in the translucent render mode. A fully hidden all-zero record and the protocol-named Invisible form are therefore distinct receiving-client representations, not one persistent local visibility flag.

## Monster disguise form

`head_sprite == 0xFFFF` makes the human use `MonsterObjectImageSession` instead of `HumanObjectImageSession`. The handler subtracts `0x4000` from `tagged_monster_sprite` and loads `mns%03d.mpf` for the result.

This is the client mechanism used when an event transforms a player into a monster or creature sprite. The object does not become `WorldObject_Monster`: it keeps the same entity ID and remains `WorldObject_User` for the local player or `WorldObject_Human` for another player. Only its living-object image session changes to the monster form. Sending a later normal record for the same entity restores the layered human appearance.

The packet does not say why the transformation happened or how long it lasts. Those rules belong to the server-side event or effect that chooses which `SDrawHumanObjects` form to send.

The first following color byte is forwarded to the monster image session. The second is parsed but not used by this handler. The next six bytes have no identified behavior: the parser retains the first in a reused packet-object field and skips the remaining five.

The `0x4000` value is a sprite namespace tag, not a general flag cleared from every appearance field. The broader ranges are defined under [Tagged world sprites](../protocol-types.md#tagged-world-sprites). Only the `0x4000` monster namespace is used by the disguise branch of opcode `0x33`.

## Names and group advertisements

The name is used to build a `WorldObject_Name_Pane`. For other players it is also copied into the human object at `+0x112`. The packet buffer accepts 255 bytes, the retained human name buffer is 128 bytes including its terminator, and the name pane keeps 64 bytes including its terminator. Normal character-name limits are much smaller than all three buffers.

`name_style` selects a palette index for the visible name. The client does not store friendly labels for these styles.

| `name_style` | Name palette index |
| ---: | ---: |
| `0` | `0x14` |
| `1` | `0x28` |
| `2` | `0x80` |
| Other | Same default path as `0` |

The second string is not a guild name. RTTI and nearby configuration name it as a group advertisement. A nonempty string creates `WorldObject_GroupAd` only when the local `GroupObjectOption` setting is enabled. An empty string, or a disabled option, removes the object's existing group advertisement.

## Darkness light mask

The normal form carries `light_mask_id` at body offset `0x20`, counting the opcode as offset zero. Other protocol implementations may call this field `Lantern`, but the client uses the value directly as a light-mask resource selector.

| Value | Client behavior in Darkness mode `3` |
| ---: | --- |
| `0` | Remove any light image attached to the human |
| `1` through `255` | Load frame zero from `mask1%02d.epf` and attach it to the human |

The server therefore resolves worn lanterns or other light sources before sending the appearance. The monster-disguise form has no wire field here. Its packet object retains the parser's default selector of `1`, which the common handler uses in Darkness mode.

See [Map lighting](../../rendering/lighting.md) for mask composition and the distinction from `SStatus` blindness.

## Runtime copies

The transient RTTI packet object is 0x264 bytes. Normal appearance fields are rearranged into one stable 0x30-byte record, then copied to two live locations:

| Owner | Offset | Purpose |
| --- | ---: | --- |
| `WorldObject_Human` or `WorldObject_User` | `+0xA4` | Current logical appearance |
| `HumanObjectImageSession` | `+0x0C` | Rendering and motion resource selection |

The object ID remains at world-object offset `+0x24`; Y and X remain at `+0x40` and `+0x44`. The full layouts are in [World objects](../../appendix/runtime/world.md#human-appearance).

## Supplied login trace

The supplied login record decodes completely with this layout. It places the local player at `(43, 40)`, facing down, with packed body `0x10`. That selects the M-prefix body sprite `1`, pants color zero, no translucency, no group advertisement, and light-mask selector zero. The two strings consume the remainder exactly, with no unexplained bytes.

## Known limits

The six monster-form bytes remain unresolved. The client confirms that `rest_position` changes standing-motion setup, but the value names still need runtime examples. Palette indexes are recorded as indexes because their final colors depend on the active palette.
