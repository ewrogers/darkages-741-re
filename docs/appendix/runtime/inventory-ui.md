# Inventory and character panes

The visible character UI keeps richer objects than the compact session model. These pane-owned records retain quantities, durability, casting delay, combat modifiers, and other values needed only for display or interaction.

## Item inventory panes

The exact RTTI class `ItemInventoryPane` derives from `InventoryPane_A` and inherits its packet handler. The base pane owns 60 direct item pointers.

```c
struct InventoryPaneFields {
    u8 pane_base[0x190];
    u8 unknown_190[0x0C];
    s32 selected_slot;              // +0x19C, initialized to -1
    InvItemPane *items[60];         // +0x1A0, slots 1 through 60
    u8 state_290;                   // exact purpose unknown
};

struct InvItemPaneFields {
    u8 pane_base[0x190];
    u16 sprite;                     // +0x190
    char display_name[128];         // +0x192
    u8 dye_color;                   // +0x212
    u8 padding_213;
    u8 slot;                        // +0x214, one-based
    u8 unknown_215[0x1B];
    u32 unknown_230;                // initialized to zero
    u8 state_234;                   // initialized to one
    u8 padding_235[3];
    u32 max_durability;             // +0x238
    u32 durability;                 // +0x23C
    u32 quantity;                   // +0x240
    u8 can_stack;                   // +0x244
    u8 padding_245[3];
};                                  // size 0x248
```

The item pane initially receives the wire name. If `can_stack` is nonzero, the constructor replaces the display buffer with `name[ quantity ]`. Adding to an occupied slot releases the old item before inserting the replacement. Removing a live item destroys it and writes null to the slot pointer. See [Inventory state](session.md#inventory-state) for the compact gameplay copy.

## Spell inventory panes

The UI retains `cast_lines`, which is absent from the session spell record.

```c
struct SpellInvItemPaneFields {
    u8 pane_base[0x190];
    u8 slot;                        // +0x190
    u8 padding_191;
    u16 icon;                       // +0x192
    u8 spell_args_type;             // +0x194
    char name[128];                 // +0x195
    char prompt[128];               // +0x215
    u8 cast_lines;                  // +0x295
    u8 state_296;                   // exact purpose unknown
    u8 action_delay_active;         // +0x297, set by SActionDelay selector 0
};

struct NewSpellInventoryPaneFields {
    u8 pane_base[0x190];
    s32 capacity;                   // +0x190, initialized to 90
    SpellInvItemPane **items;       // +0x194, 90 pointers
};

struct SkillSpellInventoryPaneFields {
    u8 pane_base[0x224];
    NewSkillInventoryPane *skills;  // +0x224
    NewSpellInventoryPane *spells;  // +0x228
};
```

The UI accepts slots 1 through 90, one more than `WorldUserFunc`. Removing a live spell releases its `SpellInvItemPane` and sets the corresponding pointer to null. No use for slot 90 has been established.

`action_delay_active` blocks spell activation and ordinary item pointer actions. The draw path tints the full icon while it is set. The owning `NewSpellInventoryPane` clears it with a slot-keyed expiry timer. See [Skill and spell action delays](../../systems/action-delays.md).

### Spell casting control

Timed casting is owned by the RTTI class `SpellDelayControlPane`.

```c
struct SpellDelayControlPaneFields {
    u8 pane_base[0x190];
    u8 total_cast_lines;            // +0x190
    u8 current_cast_line;           // +0x191
    char cast_lines[10][256];       // +0x192, loaded from SpellBook.cfg
    u8 queued_use_spell_body[0x8000]; // +0xB92, includes opcode
    char spell_name[256];           // +0x8B92
    u16 queued_use_spell_length;    // +0x8C92
    u8 cast_active;                 // +0x8C94
    u8 trailing[3];                 // +0x8C95
};                                  // size 0x8C98
```

Its timer callback receives the usual adjusted `TimerHandler` pointer at `this + 0x11C`. It converts that pointer back to the complete pane before advancing the cast sequence.

Starting a timed cast copies the completed opcode-first `CUseSpell` body into `queued_use_spell_body`, stores its length and spell name, resets `current_cast_line`, and sets `cast_active` to one. Each one-second timer advances the line index. The final timer sends the spell name, submits the queued body, and clears `cast_active`.

[`SSpellDelayCancel`](../../network/server/072-0x48-spell-delay-cancel.md) clears only `cast_active` and cancels every timer owned by this pane. It does not erase or reset the line count, current index, text buffers, queued body, spell name, or queued length. Those retained values cannot advance without a timer and are overwritten by a later cast.

## Skill inventory panes

```c
struct SkillInvItemPaneFields {
    u8 pane_base[0x190];
    u16 icon;                       // +0x190
    char name[128];                 // +0x192
    u8 unknown_212[0x100];
    u8 slot;                        // +0x312, one-based
    u8 unknown_313;
    u32 cooldown_progress;          // +0x314, integer 0 through 30
    u32 cooldown_start_ms;          // +0x318, timeGetTime value
    u32 cooldown_end_ms;            // +0x31C
    u8 cooldown_visual_active;      // +0x320
    u8 state_321;                   // exact purpose unknown
    u8 action_delay_active;         // +0x322, set by SActionDelay selector 1
    u8 state_323;                   // exact purpose unknown
    u8 unknown_324[0x24];
};                                  // size 0x348

struct NewSkillInventoryPaneFields {
    u8 pane_base[0x190];
    s32 capacity;                   // +0x190, initialized to 90
    SkillInvItemPane **items;       // +0x194, 90 pointers
};
```

The UI replaces an existing item before insertion. Removal releases the live `SkillInvItemPane` and writes null to its pointer entry. As with spells, the UI accepts slot 90 while the session model stops at slot 89.

`action_delay_active` blocks skill activation and ordinary item pointer actions. Skills also update `cooldown_progress` every 100 ms with timer ID `0x10204`, producing a 30-step vertical tint boundary. The owning `NewSkillInventoryPane` separately clears the flag at the requested duration. See [Skill and spell action delays](../../systems/action-delays.md).

## Equipment panes

Worn equipment is represented in two UI-owned models. No third gameplay-session copy was found in the `SAddEquip` or `SRemoveEquip` receive paths.

The RTTI class `EquipPane` keeps 18 parallel entries selected by `slot - 1`.

```c
struct EquipmentDurability {
    u32 maximum;                    // +0x00
    u32 current;                    // +0x04
};                                  // size 0x08

struct EquipPaneEquipmentFields {
    u8 unknown_0000[0x111C];
    u16 sprites[18];                // +0x111C
    u8 dye_colors[18];              // +0x1140
    char names[18][128];            // +0x1152
    u8 unknown_1A52[2];
    EquipmentDurability values[18]; // +0x1A54
};
```

[`SAddEquip`](../../network/server/055-0x37-add-equip.md) writes all five values and redraws the pane. [`SRemoveEquip`](../../network/server/056-0x38-remove-equip.md) clears the sprite, first name byte, maximum durability, and current durability. It leaves the dye byte and remaining name-buffer bytes untouched.

The RTTI class `UserInfoPane` owns a second view.

```c
struct UserInfoEquipmentFields {
    u8 unknown_0000[0x588];
    void *equipment_view;           // +0x588, exact derived class unresolved
};
```

The static `equipment_slot_to_ui_index` table contains 19 signed entries. Slot `0` maps to `-1`; slots `1` through `18` map to indices `0` through `17`. The child view receives maximum durability before current durability, matching the order stored by `EquipPane` even though the wire packet sends current first.

## Status and mail panes

`StatusInfoPane` keeps the broad character-sheet view of [`SStatus`](../../network/server/008-0x08-status.md).

```c
struct StatusInfoPaneStatusFields {
    u8 pane_base[0x198];
    u32 gold;                        // +0x198
    u32 health;                      // +0x19C
    u32 max_health;                  // +0x1A0
    u32 mana;                        // +0x1A4
    u32 max_mana;                    // +0x1A8
    u32 total_experience;            // +0x1AC
    u32 opaque_status_word;          // +0x1B0
    u16 retained_stats_0;            // +0x1B4
    u16 retained_stats_1;            // +0x1B6
    u16 retained_stats_2;            // +0x1B8
    u16 level;                       // +0x1BA
    u16 strength;                    // +0x1BC
    u16 dexterity;                   // +0x1BE
    u16 wisdom;                      // +0x1C0
    u16 constitution;                // +0x1C2
    u16 intelligence;                // +0x1C4
    u8 unrelated_1C6[2];
    u16 attack_element;              // +0x1C8
    u16 defense_element;             // +0x1CA
    u16 magic_resist_units;          // +0x1CC
    u8 unrelated_1CE[2];
    u32 to_next_level;               // +0x1D0
    u32 game_points;                 // +0x1D4
    u32 to_next_ability;             // +0x1D8
    u32 ability_level;               // +0x1DC
    u32 total_ability;               // +0x1E0
    u32 max_weight;                  // +0x1E4
    u32 weight;                      // +0x1E8
    u8 stat_points;                  // +0x1EC
    bool has_stat_points;            // +0x1ED
    s8 selected_stat_index;          // +0x1EE, -1 when none
    u8 stat_selectors[5];            // +0x1EF: 01 04 08 10 02
    s32 stat_button_rects[5][4];     // +0x1F4
    u8 blink_phase;                  // +0x244, zero or one
};
```

`has_stat_points` gates drawing all five stat-increase controls. `stat_points` supplies the displayed count and controls whether the dedicated [`SLevelPoint`](../../network/server/061-0x3d-level-point.md) path keeps a 500 ms timer running. The timer toggles `blink_phase`, redraws the pane, and alternates the count and normal button artwork. `SStatus` writes the same two values but does not manage this timer.

The selected control indexes `stat_selectors` when the pane builds [`CAddStat`](../../network/client/071-0x47-add-stat.md). Sending the request does not decrement `stat_points` locally.

`ExtraStatusInfoPane` owns the compact combat view.

```c
struct ExtraStatusInfoPaneStatusFields {
    u8 pane_base[0x4F8];
    s8 armor_class;                  // +0x4F8
    u8 damage_modifier;              // +0x4F9
    u8 hit_modifier;                 // +0x4FA
    u8 unrelated_4FB;
    u16 attack_element;              // +0x4FC
    u16 defense_element;             // +0x4FE
    u16 magic_resist_units;          // +0x500
};
```

`BtmButtonsPane_A` keeps the mail indicator state at `+0x1C4` and its blink phase at `+0x1C5`. When the high nibble of an active `mail_state` is nonzero, it runs timer `0x01000000` every 500 ms and alternates the mailbox image.
