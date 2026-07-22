# Session and character state

`WorldUserFunc` owns the compact gameplay copy of the logged-in character. Its large size comes from fixed records and one embedded `UserInfo` object, not an opaque binary payload. The richer objects used for drawing panes are documented separately in [Inventory and character panes](inventory-ui.md).

The object begins with a parsed group-member cache and the current [`UserState`](../../network/protocol-types.md#userstate). Status and local appearance fields follow, then the three contiguous slot arrays. Three widened [`SSelfLook`](../../network/server/057-0x39-self-look.md) metadata bytes sit between the skill array and weight fields. The final `0xB44` bytes are an exact RTTI `UserInfo` object.

```c
struct WorldUserFuncGroupMemberEntry {
    char name[64];                   // +0x00
    u8 starred;                      // +0x40, source line began with "* "
};                                   // size 0x41

struct WorldUserFuncStatusBlock {
    s32 privilege_level;             // object +0x104C
    u32 self_object_id;              // object +0x1050, SUserAppearance-owned
    u8 appearance_facing;            // object +0x1054, stored but no reader found
    u8 retained_stats[3];            // object +0x1055
    u8 level;                        // object +0x1058
    u8 ability_level;                // object +0x1059
    u8 unrelated_105A[2];
    u32 gold;                        // object +0x105C
    u32 total_experience;            // object +0x1060
    u16 strength;                    // object +0x1064
    u8 unrelated_1066[2];
    u16 dexterity;                   // object +0x1068
    u16 wisdom;                      // object +0x106A
    u16 constitution;                // object +0x106C
    u16 intelligence;                // object +0x106E
    u16 stat_points;                 // object +0x1070
    u8 unrelated_1072[2];
    u32 opaque_status_word;          // object +0x1074
    u32 health;                      // object +0x1078
    u32 max_health;                  // object +0x107C
    u32 mana;                        // object +0x1080
    u32 max_mana;                    // object +0x1084
    u8 appearance_guild_value;       // object +0x1088, raw u8
    u8 character_class;              // object +0x1089, raw u8
    u8 appearance_unknown_final;     // object +0x108A, raw u8
    u8 unrelated_108B;
    u8 retained_modifier_0;          // object +0x108C
    u8 blind_code;                   // object +0x108D
    u8 retained_modifiers[3];        // object +0x108E
    u8 mail_state;                   // object +0x1091
};                                   // size 0x46

struct WorldUserFuncFields {
    void **vtable;                                      // +0x0000
    WorldUserFuncGroupMemberEntry group_members[64];   // +0x0004
    u32 group_member_count;                             // +0x1044
    u32 user_state;                                     // +0x1048, low byte is UserState
    WorldUserFuncStatusBlock status;                    // +0x104C
    SessionInventoryEntry inventory[60];                // +0x1092
    SessionSpellEntry spells[89];                       // +0x4DFA
    SessionSkillEntry skills[89];                       // +0x10210
    u32 self_look_show_master_metadata;                 // +0x15C74
    u32 self_look_show_ability_metadata;                // +0x15C78
    u32 self_look_character_class;                      // +0x15C7C
    u32 max_weight;                                     // +0x15C80
    u32 weight;                                         // +0x15C84
    u8 appearance_action_state;                         // +0x15C88
    u8 padding_15C89[3];
    UserInfo user_info;                                 // +0x15C8C, size 0xB44
};                                                      // size 0x167D0

typedef WorldUserFuncFields WorldUserFuncCharacterFields;
typedef WorldUserFuncFields WorldUserFuncInventoryFields;
typedef WorldUserFuncFields WorldUserFuncSpellFields;
typedef WorldUserFuncFields WorldUserFuncSkillFields;
typedef WorldUserFuncFields WorldUserStatusFields;
```

The five aliases preserve the older analysis-view names while giving each one the same complete layout. Their former large byte arrays are the named regions above.

`session_update_from_self_look_packet` parses the `SSelfLook.group_members` text into the 64 fixed records. A valid source line begins with `"* "` or two spaces. The parser removes that prefix, preserves whether the first byte was `*`, and uses `IsDBCSLeadByte` so a Korean double-byte character is not split. The world refresh path clamps its iteration to 64 and matches each cached name against live user objects. The parser itself does not separately clamp the record count or copied name length.

The `WorldPane` allocation site requests exactly `0x167D0` bytes. `session_world_user_func_ctor` installs the `WorldUserFunc` vtable, constructs exact RTTI class `UserInfo` at `+0x15C8C`, and clears the three slot arrays. This establishes the full object boundary and the embedded tail type.

The three fields at `+0x15C74` through `+0x15C7C` come from consecutive `SSelfLook` bytes. The packet stores them as widened values in the order `show_master_metadata`, `show_ability_metadata`, then `character_class`.

The world-pane interface exposes these values to the class and event metadata checks. `show_ability_metadata` selects event progression bucket 6. `show_master_metadata` selects bucket 7 and gates nonzero `SClass` ability-level requirements. The live character class supplies the `SEvent` class mask and selects the `SClass<value>` table.

The record definitions used by the arrays are expanded below.

## Inventory state

```c
struct SessionInventoryEntry {
    u8 present;                     // +0x000
    u8 padding_001;
    u16 sprite;                     // +0x002
    u8 dye_color;                   // +0x004
    char name[256];                 // +0x005
    u8 padding_105;
};                                  // size 0x106

```

[`SAddInventory`](../../network/server/015-0x0f-add-inventory.md) marks the compact record present and copies its sprite, dye color, and name. Quantity, stackability, and durability are not stored here. [`SRemoveInventory`](../../network/server/016-0x10-remove-inventory.md) clears `present`, `sprite`, and `name[0]` without overwriting the retained dye byte or remaining name bytes.

[`SStatus`](../../network/server/008-0x08-status.md) updates weight independently. Neither inventory packet derives weight from the item fields.

## Spell state

`WorldPane + 0x2CC` points to `WorldUserFunc`. Its spell array follows the inventory array.

```c
struct SessionSpellEntry {
    u8 present;                     // +0x000
    u8 padding_001;
    u16 icon;                       // +0x002
    u8 spell_args_type;             // +0x004
    char name[256];                 // +0x005
    char prompt[256];               // +0x105
    u8 padding_205;
};                                  // size 0x206

```

`session_store_spell_entry` calculates an address as `this + 0x4DFA + (slot - 1) * 0x206`. It stores the fields supplied by [`SAddSpell`](../../network/server/023-0x17-add-spell.md) except `cast_lines`.

[`SRemoveSpell`](../../network/server/024-0x18-remove-spell.md) sets `present`, `spell_args_type`, `name[0]`, and `prompt[0]` to zero. It does not overwrite `icon` or the remaining bytes in either string buffer.

## Skill state

`WorldUserFunc` stores 89 skill records immediately after its spell array.

```c
struct SessionSkillEntry {
    u8 present;                     // +0x000
    u8 padding_001;
    u16 icon;                       // +0x002
    char name[256];                 // +0x004
};                                  // size 0x104

```

[`SAddSkill`](../../network/server/044-0x2c-add-skill.md) sets `present`, stores the icon, and copies the name. [`SRemoveSkill`](../../network/server/045-0x2d-remove-skill.md) clears `present` and `name[0]` without overwriting the icon or remaining name bytes.

## Status state

[`SStatus`](../../network/server/008-0x08-status.md) is a partial update, so each present block updates part of the long-lived session object.

`WorldUserFuncStatusBlock` above covers the compact status region at `+0x104C`. The inventory, spell, and skill arrays account for the former `+0x1092` through `+0x15C73` blob. The three `SSelfLook` metadata fields then lead directly into weight and action state.

The wire values for attributes, stat points, and weight are widened in this model. `has_stat_points`, experience-to-next values, ability totals, game points, elements, magic resistance, the unknown byte after magic resistance, armor class, damage, hit, and the derived mail booleans are not copied here. Their pane-owned copies are mapped in [Status and mail panes](inventory-ui.md#status-and-mail-panes).

The retained stats bytes, retained modifier bytes, and `opaque_status_word` have no identified readers in the traced status paths. They remain named by storage behavior rather than an assumed game meaning.

`privilege_level` has four direct readers: `map_can_move_direction`, `map_has_special_movement_permission`, and the two `MapUserInterface` getters `ui_world_pane_is_privileged` and `ui_world_pane_get_privilege_level`. The boolean getter fans out to bulletin, line-input, and dormant screenshot behavior. The raw getter has one exact-level consumer in the event dispatcher. The complete value matrix is on the [`SStatus` privilege page](../../network/server/008-0x08-status.md#privilege-behavior).

## Local user action state

[`SUserAppearance`](../../network/server/005-0x05-user-appearance.md) owns the self-object and action-state fields embedded in `WorldUserFunc`. A full update writes `self_object_id`, cached facing, the raw guild value, character class, the final unknown byte, and `appearance_action_state`. A state-only update writes only the action state.

The stored action state is `wire_appearance_state & 0x7F`. Bit `0x01` rejects local movement and several other actions. The wire bit `0x80` is not retained; it tells the updater to leave the other self fields unchanged. The visible human appearance stored on world objects is mapped in [World objects](world.md#human-appearance).

`WorldPane_Impl` exposes virtual getters for every field above except cached facing. The guild value is returned without boolean normalization, while the final byte has no identified gameplay consumer. The packet page records the limits on the supplied guild, class, and direction labels.

The constructor clears `appearance_action_state`, and `session_update_from_user_appearance_packet` is its only runtime writer. `SStatus` does not update it. The server can change it during play by resending `SUserAppearance`; wire bit `0x80` lets that resend change only the action state.

Direct field readers are `ui_world_pane_handle_drop_event`, `map_can_move_direction`, and `net_handle_exchange_started`. `ui_world_pane_get_local_action_state` exposes the same byte through `MapUserInterface`; its only identified caller is `net_send_change_slot`. Every consumer masks bit `0x01`. See [`SUserAppearance`](../../network/server/005-0x05-user-appearance.md#action-state-and-partial-updates) for the resulting client behavior.
