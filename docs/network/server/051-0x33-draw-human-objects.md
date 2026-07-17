# Draw Human Objects (`SDrawHumanObjects`)

`SDrawHumanObjects` creates or refreshes a human in the world. A record matching the saved self-object ID becomes `WorldObject_User`; other records become `WorldObject_Human`.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x33` (51) |
| Transform | derived |
| Runtime classes | `WorldObject_User`, `WorldObject_Human`, and `HumanObjectImageSession` |
| Name provenance | Microsoft C++ RTTI in the target |

## Confirmed prefix

The complete appearance record is large and will be documented with the wider login sequence. The prefix needed to identify the object and its body variant is confirmed:

```c
struct SDrawHumanObjectsPrefix {
    u8 opcode;                         // 0x33
    u16be coordinate_0;
    u16be coordinate_1;
    u8 orientation_or_motion;
    u32be object_id;
    u16be appearance_id;

    if (appearance_id != 0xFFFF) {
        u8 packed_appearance;          // body offset 0x0C
        u8 appearance_fields[19];      // individually unresolved here
        u8 light_mask_id;              // body offset 0x20
        // remaining normal-human appearance fields
    } else {
        // disguised or monster-form fields
    }
};
```

The two coordinate names and the one-byte orientation field remain deliberately generic here. The handler proves how they reach world-object construction, but this focused pass did not need to settle their public protocol names.

`appearance_id == 0xFFFF` selects a disguised or monster-form path. Other values use the normal human appearance decoder and `HumanObjectImageSession`.

## Packed appearance variant

The high nibble of `packed_appearance` selects a gender prefix, a body-resource ID, and two related flags. The low nibble is retained separately and is not needed for the swimming selection.

| High nibble | Gender prefix | Body resource | Other confirmed effect |
| ---: | --- | ---: | --- |
| `0` | M | `0` | None identified |
| `1` | M | `1` | Normal male form in the supplied login trace |
| `2` | W | `1` | Normal female resource family |
| `3` | M | `2` | Human does not block local dynamic-object collision |
| `4` | W | `2` | Human does not block local dynamic-object collision |
| `5` | M | `1` | Sets an additional unresolved appearance flag |
| `6` | W | `1` | Sets an additional unresolved appearance flag |
| `7` | M | `4` | Exact purpose unresolved |
| `8` | M | `5` | Swimming body |
| `9` | W | `5` | Swimming body |

The M and W prefixes are literal bytes in the client's resource-name table. They are used here as resource selectors rather than translated gender labels.

## Swimming body

Variants `8` and `9` select body resource `5`. `render_format_human_part_filename` resolves its first motion files through the `MM005` and `WM005` EPF families.

The local matching assets support the in-game observation that this is swimming art. Their first-motion frames are roughly 15 to 17 pixels wide and 11 to 14 pixels high, while normal body resource `1` frames are roughly 48 to 54 pixels wide and 17 to 27 pixels high. Resource `5` is therefore a small head-level body layer rather than a standing character body.

`render_human_apply_appearance_record` copies the decoded appearance into `HumanObjectImageSession`, which builds the body and equipment filenames used by the normal living-object renderer. No special water renderer is involved.

The client does not derive variants `8` or `9` from a local skill check. The server supplies the packed variant. See [Movement and swimming](../../systems/movement-and-swimming.md).

## Darkness light mask

The normal-human record carries `light_mask_id` at decoded-body offset `0x20`, counting the opcode as offset zero. The client uses it only when the active [`SMapSize`](021-0x15-map-size.md) low-nibble mode is `3`, Darkness.

| Value | Client behavior |
| ---: | --- |
| `0` | Remove any light image attached to the human |
| `1` through `255` | Load frame zero from `mask1%02d.epf` and attach it to the human |

The image is centered on the human and merged into the world light mask. This produces the limited visible area associated with lanterns on Andor. The client does not inspect worn equipment to choose the number, so the server must resolve the character's current lantern or other light source before sending this appearance record.

The disguised `appearance_id == 0xFFFF` variant does not read this byte. Its packet object keeps the constructor's default selector of `1`.

See [Map lighting](../../rendering/lighting.md) for mask composition and the distinction from `SStatus` blindness.

## Supplied login trace

The supplied login trace contains one `SDrawHumanObjects` record for the local player. Its packed appearance byte is `0x10`, selecting the normal M-prefix body resource `1` form. Its `light_mask_id` is `0`, so that appearance carries no object light image.

## Known limits

Most equipment, dye, name, group, and disguise fields in the remainder of this packet still need their dedicated pass. This page currently names the prefix, appearance variant, and Darkness light selector.
