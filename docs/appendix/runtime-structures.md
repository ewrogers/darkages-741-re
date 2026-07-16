# Runtime structures

This appendix collects object layouts and dispatch tables used by the event and UI chapters. Offsets are relative to the object shown. They are not static process addresses.

## Event object

```text
struct Event {
    unknown header[0x0C]
    s8 type                     // +0x0C, starts as -1
    type-specific data[...]     // starts at +0x10
}                               // total size 0xA8
```

### Event types

| Type | Meaning |
| --- | --- |
| `0x00` | Pointer move |
| `0x01` | Left button down |
| `0x02` | Left button double click |
| `0x03` | Left button up |
| `0x04` | Right button down |
| `0x05` | Right button double click |
| `0x06` | Right button up |
| `0x07` | Mouse wheel |
| `0x08` | Key down |
| `0x09` | Key up |
| `0x0A` | IME composition text update |
| `0x0B` | Character or committed text |
| `0x0C` | Alternate translated key event, exact purpose unknown |
| `0x0D` | IME open-status change |
| `0x0E` | IME composition start |
| `0x0F` | IME composition end |
| `0x10` | IME candidate-list data |
| `0x11` | IME candidate-list close |
| `0x12` | Application event, exact purpose unknown |
| `0x13` | Decoded server packet |
| `0x14` | Intro state change |

The client creates double clicks itself. A second press must use the same button, arrive within 1000 ms, and be no more than two pixels away by Manhattan distance.

Input flags use `0x01` for Alt, `0x02` for Ctrl, `0x04` for Shift, `0x10` for left held, and `0x20` for right held. Mouse-wheel delta is divided by 120 before dispatch.

### Pane handler slots

| Event family | Primary vtable slot |
| --- | --- |
| Pointer, `0x00` to `0x07` | `+0x48` |
| Keyboard and text, `0x08` to `0x0C` | `+0x4C` |
| Network, `0x13` | `+0x50` |
| Application and IME, `0x0D` to `0x12` | `+0x54` |
| Dialog action callback | `+0x64` |

A true return value consumes the event and stops normal tree traversal.

## Decoded server event

```text
struct ServerEventFields {
    bytes *body                 // Event +0x14, command byte first
    u32 body_length             // Event +0x18
    ServerPacket *parsed        // Event +0x1C, null when no class exists
}
```

During the first TCP receive, the same event family can carry an owned copy of the complete wire bytes instead of a decoded body. `TerminalPane2` handles that raw form before the packet factory is active.

## Connection handshake fields

These fields belong to the large socket object. Only the state needed to explain the welcome transition is shown.

```text
struct SocketHandshakeFields {
    u8 transport_selector       // +0x780D8, 1..4 are modem COM ports, 5 is TCP
    bool raw_stream_mode        // +0x780DC
    bool text_framing_enabled   // +0x780DD
}
```

The constructor sets both booleans. While `raw_stream_mode` is true, the selected receiver posts the available greeting bytes without packet parsing. The observed `ESC C` welcome clears both fields, enabling binary framing on TCP. `ESC S` clears raw-stream mode but leaves printable outbound framing enabled. The serial receiver also changes from greeting bytes to printable records when raw-stream mode is cleared.

The RTTI-backed `TerminalPane2` owns the control parser:

```text
struct TerminalPane2HandshakeFields {
    u32 control_state           // +0x190
    Pane *text_output           // +0x1A0, exact derived type unknown
}
```

Important control states include normal text, escape, Telnet IAC, Telnet option, and the final connected transition. Its network-event method occupies primary-vtable slot `+0x50`.

## Startup packet objects

These are partial layouts for the RTTI-backed server packet objects used during the observed bootstrap exchange. The common `ServerPacket` base occupies the first `0x10` bytes.

```c
struct STransferServerFields {
    u8 base[0x10];
    u32 ipv4_value;              // +0x10, decoded from u32be
    u16 port;                    // +0x14, decoded from u16be
    u32 token_length;            // +0x18
    u8 token[];                  // +0x1C, inline and locally NUL-terminated
};

struct SStipulationFields {
    u8 base[0x10];
    u8 mode;                     // +0x10
    u32 greeting_crc32;          // +0x14, mode 0
    u32 compressed_size;         // +0x18, mode 1
    u8 *compressed_data;         // +0x1C, mode 1
};

struct SBrowserFields {
    u8 base[0x10];
    u8 subtype;                  // +0x10
    u16 first_size;              // +0x12, subtypes 1 and 2
    u8 *first_data;              // +0x14
    u16 second_size;             // +0x18
    u8 *second_data;             // +0x1C
    char homepage_url[];         // +0x20, subtype 3 inline string
};
```

The apparent overlap is variant storage. A subtype or mode determines which fields are valid. Packet wire layouts remain on the individual packet pages.

## Character spell state

The logged-in world keeps a gameplay copy of each spell and a separate UI copy. `WorldPane + 0x2CC` points to the RTTI class `WorldUserFunc`, which owns fixed arrays for inventory items, spells, and skills.

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

struct WorldUserFuncCharacterFields {
    u8 unknown_0000[0x1092];
    u8 inventory[60][0x106];        // +0x1092
    SessionSpellEntry spells[89];   // +0x4DFA, slots 1 through 89
    u8 skills[89][0x104];           // +0x10210
};
```

`session_store_spell_entry` calculates a spell address as `this + 0x4DFA + (slot - 1) * 0x206`. It stores the fields supplied by [`SAddSpell`](../network/server/023-0x17-add-spell.md) except `cast_lines`.

[`SRemoveSpell`](../network/server/024-0x18-remove-spell.md) performs a logical clear of the same record. It sets `present`, `spell_args_type`, `name[0]`, and `prompt[0]` to zero. It does not overwrite `icon` or the remaining bytes in either string buffer.

The UI representation keeps that missing value:

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
    u8 state_296;                   // exact purposes unknown
    u8 state_297;
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

The UI accepts slots 1 through 90, one more than `WorldUserFunc`. Removing a live UI spell releases its `SpellInvItemPane` and sets the corresponding pointer to null. No use for slot 90 has been established.

Timed casting is owned by the RTTI class `SpellDelayControlPane`:

```c
struct SpellDelayControlPaneFields {
    u8 pane_base[0x190];
    u8 total_lines;                 // +0x190
    u8 current_line;                // +0x191
    char cast_text[10][256];        // +0x192, loaded from SpellBook.cfg
    u8 queued_use_spell[0x8000];    // +0xB92
    char spell_name[256];           // +0x8B92
    u16 queued_body_length;         // +0x8C92
    bool pending;                   // +0x8C94
};
```

Its timer callback receives the usual adjusted `TimerHandler` pointer at `this + 0x11C`. It converts that pointer back to the complete pane before advancing the cast sequence.

## Character skill state

`WorldUserFunc` stores 89 skill records immediately after its spell array. The session record contains only the fields needed by gameplay lookup:

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

[`SAddSkill`](../network/server/044-0x2c-add-skill.md) sets `present`, stores the icon, and copies the name. [`SRemoveSkill`](../network/server/045-0x2d-remove-skill.md) clears `present` and `name[0]` without overwriting the icon or remaining name bytes.

The skill inventory UI holds a larger object for each visible entry:

```c
struct SkillInvItemPaneFields {
    u8 pane_base[0x190];
    u16 icon;                       // +0x190
    char name[128];                 // +0x192
    u8 unknown_212[0x100];
    u8 slot;                        // +0x312, one-based
    u8 unknown_313[0x0F];
    u8 state_322;                   // exact purpose unknown
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

## Character equipment state

Worn equipment is represented in two UI-owned models. No third gameplay-session copy was found in the `SAddEquip` or `SRemoveEquip` receive paths.

The RTTI class `EquipPane` keeps 18 parallel entries selected by `slot - 1`:

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

[`SAddEquip`](../network/server/055-0x37-add-equip.md) writes all five values and redraws the pane. [`SRemoveEquip`](../network/server/056-0x38-remove-equip.md) clears the sprite, first name byte, maximum durability, and current durability. It leaves the dye byte and remaining name-buffer bytes untouched.

The RTTI class `UserInfoPane` owns a second view:

```c
struct UserInfoEquipmentFields {
    u8 unknown_0000[0x588];
    void *equipment_view;           // +0x588, exact derived class unresolved
};
```

The static `equipment_slot_to_ui_index` table contains 19 signed entries. Slot `0` maps to `-1`; slots `1` through `18` map to indices `0` through `17`. The child view receives maximum durability before current durability, matching the order stored by `EquipPane` even though the wire packet sends current first.

## Character status state

[`SStatus`](../network/server/008-0x08-status.md) is a partial-update packet, so its fields are copied into several long-lived objects according to the packet's block flags. `WorldUserFunc` is the main session-owned copy:

```c
struct WorldUserStatusFields {
    u8 unrelated_0000[0x104C];
    s32 privilege_level;             // +0x104C
    u32 self_object_id;              // +0x1050, SUserAppearance-owned
    u8 appearance_unknown_0;         // +0x1054, SUserAppearance-owned
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
    u8 appearance_unknown_1;         // +0x1088, SUserAppearance-owned
    u8 appearance_unknown_2;         // +0x1089, SUserAppearance-owned
    u8 appearance_unknown_3;         // +0x108A, SUserAppearance-owned
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

The wire values for attributes, stat points, and weight are widened in this model. `has_stat_points`, experience-to-next values, ability totals, game points, elements, magic resistance, the unknown byte after magic resistance, armor class, damage, hit, and the derived mail booleans are not copied here. The `SUserAppearance` fields shown in the same range are owned by a separate updater and are not changed by `SStatus`.

`StatusInfoPane` keeps the broader character-sheet view:

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
};
```

`ExtraStatusInfoPane` owns the compact combat view:

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

The retained stats bytes, retained modifier bytes, and `opaque_status_word` are written into these models but have no identified readers in the traced status paths. They remain named by storage behavior rather than an assumed game meaning.

## Local user appearance and swimming state

[`SUserAppearance`](../network/server/005-0x05-user-appearance.md) owns the self-object and action-state fields embedded in `WorldUserFunc`. A full update writes `self_object_id`, the four unknown appearance bytes, and `appearance_action_state`. A state-only update writes only the action state.

The stored action state is `wire_appearance_state & 0x7F`. Bit `0x01` rejects local movement and several other actions. The wire bit `0x80` is not retained; it tells the updater to leave the other self fields unchanged.

Visible human appearance is stored separately in each world object:

```c
struct HumanAppearanceRecord {
    u8 gender_resource_prefix;       // +0x00, 0 = M and 1 = W
    u8 unknown_01[5];
    u16 body_resource;               // +0x06
    u8 unknown_08[0x27];
    u8 additional_appearance_flag;   // +0x2F
};                                  // size 0x30

struct WorldObjectHumanAppearanceFields {
    u8 world_object_base[0x90];
    HumanObjectImageSession *image_session; // +0x90
    u8 unknown_094[0x10];
    HumanAppearanceRecord appearance;       // +0xA4
    bool nonblocking_human;                 // +0xD4
    bool unknown_appearance_flag;           // +0xD5
};
```

`WorldObject_User` and `WorldObject_Human` both use this appearance record. Packed [`SDrawHumanObjects`](../network/server/051-0x33-draw-human-objects.md) variants `8` and `9` decode to body resource `5` with M and W prefixes. `HumanObjectImageSession` then loads the small `MM005` or `WM005` motion family used for the swimming form.

Body resource `2` sets `nonblocking_human`; swimming body resource `5` does not. This dynamic-object collision flag is separate from the self action lock and from static `SOTP.DAT` collision.

## Event pane tree

`EventHandlerList` stores a flattened preorder tree. The dispatcher owns it at offset `+0x60`.

```text
struct EventHandlerEntry {
    Pane *pane                  // +0x00
    u32 depth                   // +0x04
    u32 identity_or_generation  // +0x08, exact purpose uncertain
}                               // size 0x0C
```

Example storage:

```text
depth 0  root A
depth 1    child A.1
depth 2      child A.1.a
depth 1    child A.2
depth 0  root B
```

Removing an entry also removes the following entries with greater depth. Child iterators use one of 16 tracked slots so a handler can change the tree without leaving a raw array pointer behind.

## Pane fields

```text
struct PaneFields {
    TimerHandler timer          // +0x11C, secondary base object
    s32 origin_x                // +0x128
    s32 origin_y                // +0x12C
    bool visible                // +0x130
    s32 input_priority          // +0x184
}
```

The dispatcher stores the captured pane at `+0x40` and the active minimum input priority at `+0x50`. The priority threshold provides modal-style input blocking without removing lower panes from the event tree.

## Timer entry

```text
struct TimerEntry {
    TimerHandler *handler       // +0x00
    u32 timer_id                // +0x04
    u32 due_time                // +0x08
    u32 payload_1               // +0x0C
    u32 payload_2               // +0x10
}                               // size 0x14
```

The dispatcher removes a due entry before calling the timer handler. It processes at most 40 due entries per game-loop pass. Cancellation removes matching entries and uses a separate notification callback.

## Dialog pane fields

```text
struct DialogPaneFields {
    ControlList *controls       // +0x594
    s32 setup_index_a           // +0x598, exact purpose uncertain
    s32 setup_index_b           // +0x59C, exact purpose uncertain
    s32 focused_control         // +0x5AC
    s32 hovered_control         // +0x5BC
    s32 hover_zone              // +0x5C0
    s32 pointer_control_2       // +0x5C4
    s32 pointer_zone_2          // +0x5C8
}
```

Control indexes follow attachment order. They are used for focus, hit testing, and the parent dialog action callback.

## Video system fields

This is the confirmed part of the renderer owner. Unlisted fields remain unmapped.

```text
struct VideoSystemFields {
    bool initialized           // +0x10
    s32 logical_width          // +0x1C
    s32 logical_height         // +0x20
    Canvas *main_canvas        // +0x24
    Canvas *output_canvas      // +0x28
    u32 display_format         // +0x2C
    u32 output_pixel_size      // +0x30
    u32 scale                  // +0x38
    HWND window                // +0x3C
}
```

The main canvas uses 16-bit software pixels. The output canvas is used when the final Windows surface needs conversion or scaling.

## DirectDraw wrapper fields

```text
struct DirectDrawFields {
    bool initialized                // +0x0C
    s32 width                       // +0x10
    s32 height                      // +0x14
    u32 mode                        // +0x24
    IDirectDraw *direct_draw        // +0x28
    IDirectDrawSurface *primary     // +0x2C
    IDirectDrawSurface *backbuffer  // +0x30, optional
    IDirectDrawClipper *clipper     // +0x34, optional
}
```

DirectDraw presents the completed canvas. Sprite and effect blends happen before these surfaces receive the frame.

## Canvas fields

Only the fields needed by the mapped drawing paths are listed here.

```text
struct CanvasFields {
    u32 storage_mode       // +0x6C, memory or wrapped surface kind
    void *pixel_allocation // +0x98, owned memory in storage mode 4
    s32 row_pitch          // +0x9C, bytes between pixel rows
    bool drawing_active    // +0xD4, set by begin and cleared by end
    s32 logical_width      // +0xE8
    s32 logical_height     // +0xEC
    s32 storage_width      // +0xF0, aligned to four pixels for memory canvases
    s32 storage_height     // +0xF4
}
```

## Static world object fields

These fields are useful for wall and occluder hooks:

```text
struct WorldObjectStaticFields {
    u32 tile_id                 // +0x7C
    u8 map_side                 // +0x80, one of the two static cell layers
    StaticTileCache *cache      // +0x84
    Canvas *image               // +0x88
    bool hidden                 // +0xAC, skips drawing when set
    u32 image_tile_id           // +0xB0, input to static animation mapping
    u8 sotp_render_flags        // +0xB9
}
```

The constructor initially copies the same static tile ID into `tile_id` and `image_tile_id`. The image path applies the current `stcani.tbl` mapping to `image_tile_id` before it opens an `stc` or `sts` resource.

Function addresses and evidence notes are in the [function reference](functions.md) and YAML exports.
