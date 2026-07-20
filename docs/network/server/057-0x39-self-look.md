# Self Look (`SSelfLook`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x39` (57) |
| Encoding | derived |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server uses this packet to fill the local character profile. One response supplies the visible nation, guild and title text, group settings, recruiting advertisement, character class, and legend marks.

It normally answers the empty [Self Look (`CSelfLook`)](../../network/client/045-0x2d-self-look.md) request. During login, the client can request it before the rest of the character UI has finished opening.

## Body

```text
packet SSelfLook {
    u8      opcode                    // 0x39
    u8      nation                    // Nation
    string8 guild_rank
    string8 title
    string8 group_members
    u8      is_group_open
    u8      is_recruiting

    if is_recruiting == 1 {
        string8 leader
        string8 group_name
        string8 note
        u8      minimum_level
        u8      maximum_level

        repeat 5 ordered class rows {
            u8      wanted
            u8      current
        }
    }

    u8      character_class           // CharacterClass
    u8      show_ability_metadata
    u8      show_master_metadata
    string8 display_class
    string8 guild
    u8      legend_mark_count

    repeat legend_mark_count {
        u8      icon                  // LegendMarkIcon
        u8      color
        string8 key
        string8 text
    }
}
```

Only the exact recruiting value `1` enables the optional block. The five class rows are Warrior, Wizard, Rogue, Priest, then Monk. Each wire pair is wanted or maximum first and current or occupied second. The client calculates the two displayed totals by summing those same columns.

## Nation and class

When `nation` is nonzero, the equipment pane draws frame `nation - 1` from `nation.epf`. The matching asset contains 13 frames.

`nation` uses the shared [`Nation`](../protocol-types.md#nation) type. `character_class` uses [`CharacterClass`](../protocol-types.md#characterclass).

`UserInfoPane` reloads its `SClass<value>` metadata when the class changes. The two metadata flags are parsed and retained by `EquipPane`, but no read of those saved bytes was found in the matched UI paths. Their descriptive names therefore remain protocol vocabulary rather than confirmed version-741 behavior.

## Recruiting group box

The recruiting block feeds the RTTI-backed `GroupAdPane` and `GroupAdDialogPane`. The group name becomes the title, the note fills the extra text area, and the level and class counts fill the requested and current columns. The UI uses `_ngcdlg1.txt`; its background art supplies the five class labels.

The client parses `leader`, but `ui_group_ad_pane_apply_self_look` starts its copy at `group_name`. It leaves the temporary leader buffer uninitialized before applying the model. This is a client bug, not evidence that the wire field is absent.

## Legend marks

`icon` uses the shared [`LegendMarkIcon`](../protocol-types.md#legendmarkicon) type. Values `0` through `7` are drawable; value `8` is the non-drawable sentinel.

`color` is an index into palette slot 0. The client loads that slot from `legend.pal`, which is also the palette used by rich text colors. The `key` supports legend lookup, while `text` is the visible line. The parser appends a carriage return to each text string before the list receives it.

The local legend record reserves 70 bytes each for `key` and `text`. A key of at most 69 bytes fits with its NUL. Text is safely limited to 68 bytes because the client adds both a carriage return and a new NUL. The packet reader does not enforce those smaller record limits.

Both the older legend dialog and RTTI class `nui_LegendPane` rebuild their lists from these records.

## Other UI effects

`ui_equip_pane_apply_self_look` copies the title, guild, guild rank, display class, and group-member text into `EquipPane`. The group-member string enters the formatted text path, so inline color codes are interpreted. `is_group_open` also changes the group button skin.

`WorldUserFunc` also parses `group_members` into a fixed cache used by the world pane. Each accepted line begins with `"* "` or two spaces. The client strips those two bytes, stores up to 64 bytes of name storage plus a `starred` byte, and uses `IsDBCSLeadByte` while scanning. The world refresh path clamps its iteration to 64 cached entries and matches each name against live user objects. The parser itself does not separately enforce the 64-record or 64-byte destination limits.

`BtmButtonsPane_A` treats this packet as the response to `CSelfLook`. It updates the group-button state, cancels the one-second request retry, and clears the pending-profile flag. After `CGroupToggle`, this response supplies the authoritative `is_group_open` value. The click path does not change the icon optimistically.

The newer `UserInfoPane` keeps the same identity fields and nation value for its profile view. The packet object is large because it reserves room for all 255 possible legend records, not because every response is normally that large.
