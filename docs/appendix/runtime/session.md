# Session and character state

`WorldUserFunc` owns the compact gameplay copy of the logged-in character. Inventory, spells, and skills use fixed arrays. Status and local appearance packets update fields elsewhere in the same large object. The richer objects used for drawing panes are documented separately in [Inventory and character panes](inventory-ui.md).

The three slot arrays are contiguous. Their record definitions are expanded below.

```c
struct WorldUserFuncCharacterFields {
    u8 unknown_0000[0x1092];
    SessionInventoryEntry inventory[60]; // +0x1092
    SessionSpellEntry spells[89];        // +0x4DFA
    SessionSkillEntry skills[89];        // +0x10210
};
```

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

struct WorldUserFuncInventoryFields {
    u8 unknown_0000[0x1092];
    SessionInventoryEntry items[60]; // +0x1092, slots 1 through 60
};
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

struct WorldUserFuncSpellFields {
    u8 unknown_0000[0x4DFA];
    SessionSpellEntry spells[89];   // +0x4DFA, slots 1 through 89
};
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

struct WorldUserFuncSkillFields {
    u8 unknown_0000[0x10210];
    SessionSkillEntry skills[89];   // +0x10210, slots 1 through 89
};
```

[`SAddSkill`](../../network/server/044-0x2c-add-skill.md) sets `present`, stores the icon, and copies the name. [`SRemoveSkill`](../../network/server/045-0x2d-remove-skill.md) clears `present` and `name[0]` without overwriting the icon or remaining name bytes.

## Status state

[`SStatus`](../../network/server/008-0x08-status.md) is a partial update, so each present block updates part of the long-lived session object.

```c
struct WorldUserStatusFields {
    u8 unrelated_0000[0x104C];
    s32 privilege_level;             // +0x104C
    u32 self_object_id;              // +0x1050, SUserAppearance-owned
    u8 appearance_facing;            // +0x1054, stored but no reader found
    u8 retained_stats[3];            // +0x1055
    u8 level;                        // +0x1058
    u8 ability_level;                // +0x1059
    u8 unrelated_105A[2];
    u32 gold;                        // +0x105C
    u32 total_experience;            // +0x1060
    u16 strength;                    // +0x1064
    u8 unrelated_1066[2];
    u16 dexterity;                   // +0x1068
    u16 wisdom;                      // +0x106A
    u16 constitution;                // +0x106C
    u16 intelligence;                // +0x106E
    u16 stat_points;                 // +0x1070
    u8 unrelated_1072[2];
    u32 opaque_status_word;          // +0x1074
    u32 health;                      // +0x1078
    u32 max_health;                  // +0x107C
    u32 mana;                        // +0x1080
    u32 max_mana;                    // +0x1084
    u8 appearance_guild_value;       // +0x1088, raw u8
    u8 character_class;              // +0x1089, raw u8
    u8 appearance_unknown_final;     // +0x108A, raw u8
    u8 unrelated_108B;
    u8 retained_modifier_0;          // +0x108C
    u8 blind_code;                   // +0x108D
    u8 retained_modifiers[3];        // +0x108E
    u8 mail_state;                   // +0x1091
    u8 unrelated_1092[0x14BEE];
    u32 max_weight;                  // +0x15C80
    u32 weight;                      // +0x15C84
    u8 appearance_action_state;      // +0x15C88, SUserAppearance-owned
};
```

The wire values for attributes, stat points, and weight are widened in this model. `has_stat_points`, experience-to-next values, ability totals, game points, elements, magic resistance, the unknown byte after magic resistance, armor class, damage, hit, and the derived mail booleans are not copied here. Their pane-owned copies are mapped in [Status and mail panes](inventory-ui.md#status-and-mail-panes).

The retained stats bytes, retained modifier bytes, and `opaque_status_word` have no identified readers in the traced status paths. They remain named by storage behavior rather than an assumed game meaning.

## Local user action state

[`SUserAppearance`](../../network/server/005-0x05-user-appearance.md) owns the self-object and action-state fields embedded in `WorldUserFunc`. A full update writes `self_object_id`, cached facing, the raw guild value, character class, the final unknown byte, and `appearance_action_state`. A state-only update writes only the action state.

The stored action state is `wire_appearance_state & 0x7F`. Bit `0x01` rejects local movement and several other actions. The wire bit `0x80` is not retained; it tells the updater to leave the other self fields unchanged. The visible human appearance stored on world objects is mapped in [World objects](world.md#human-appearance).

`WorldPane_Impl` exposes virtual getters for every field above except cached facing. The guild value is returned without boolean normalization, while the final byte has no identified gameplay consumer. The packet page records the limits on the supplied guild, class, and direction labels.

The constructor clears `appearance_action_state`, and `session_update_from_user_appearance_packet` is its only runtime writer. `SStatus` does not update it. The server can change it during play by resending `SUserAppearance`; wire bit `0x80` lets that resend change only the action state.
