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
        u8 packed_appearance;
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

## Supplied login trace

The supplied login trace contains one `SDrawHumanObjects` record for the local player. Its packed appearance byte is `0x10`, selecting the normal M-prefix body resource `1` form.

## Known limits

Most equipment, dye, name, group, lighting, and disguise fields in the remainder of this packet still need their dedicated pass. This page names only the prefix and appearance-variant behavior required to explain self creation and swimming.
