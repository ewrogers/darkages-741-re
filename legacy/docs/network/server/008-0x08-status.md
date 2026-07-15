# 008 / 0x08: Status (`SStatus`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x08` |
| RTTI class | `SStatus` |
| Factory | `0x59C360` |
| Constructor | `0x59C3E0` |
| Vtable | `0x688164` |
| Deserializer | `0x59C410` |

## Payload model

The first payload byte is both a group-presence mask and a two-bit client state. Groups are read in the order below. Optional groups do not have fixed wire offsets because an absent earlier group shortens the packet.

```c
uint8_t flags = read_u8();
uint8_t client_state = (flags >> 6) & 3;

if (flags & 0x20) read_fixed_character_data();
if (flags & 0x10) read_current_vitals();
if (flags & 0x08) read_experience_and_currency();
if (flags & 0x04) read_extended_status();

/* 0x02 sets two packet-state booleans but consumes no bytes. */
/* 0x01 marks packed parcel/mail state valid but consumes no bytes. */
```

The names `client_state`, `weight_value_a`, and `weight_value_b` remain descriptive until their internal company names are recovered.

### Flag byte

| Bits | Meaning | Wire data |
|---:|---|---|
| `7..6` | Client movement/state value, range 0 through 3 | None |
| `0x20` | Fixed character data present | Fixed character group |
| `0x10` | Current vitality and mental present | Two `u32be` values |
| `0x08` | Experience and currency present | Six `u32be` values |
| `0x04` | Extended status present | Thirteen `u8` values |
| `0x02` | Sets two internal packet booleans | None |
| `0x01` | Packed parcel/mail state is valid when `0x04` is also present | None |

The state value affects movement. `map_can_move_direction` at `0x5EFFE0` gives states 1 and 2 special handling that bypasses the normal collision result. The exact internal names of the four states are not yet known.

### `0x20`: fixed character data

| Order | Type | Field | Confirmed use |
|---:|---|---|---|
| 0 | `u8` | `fixed_unknown_0` | Cached by `WorldUserFunc` |
| 1 | `u8` | `fixed_unknown_1` | Cached by `WorldUserFunc` |
| 2 | `u8` | `fixed_unknown_2` | Cached by `WorldUserFunc` |
| 3 | `u8` | `level` | `s_Lev` |
| 4 | `u8` | `ability` | `s_Ab` |
| 5 | `u32be` | `maximum_vitality` | `s_HPMax`, bottom HP orb |
| 6 | `u32be` | `maximum_mental` | `s_MPMax`, bottom MP orb |
| 7 | `u8` | `strength` | `s_Str`, self profile |
| 8 | `u8` | `intelligence` | `s_Int`, self profile |
| 9 | `u8` | `wisdom` | `s_Wis`, self profile |
| 10 | `u8` | `constitution` | `s_Con`, self profile |
| 11 | `u8` | `dexterity` | `s_Dex`, self profile |
| 12 | `u8` | `fixed_unknown_11` | Stored by the status pane |
| 13 | `u8` | `level_up_points` | Stored by the status pane and `WorldUserFunc` |
| 14 | `u16be` | `weight_value_a` | `SZ_WEIGHT` |
| 15 | `u16be` | `weight_value_b` | `SZ_WEIGHT` |
| 16 | `u32be` | `fixed_unknown_tail` | Cached by the status pane and `WorldUserFunc` |

The weight display proves that the two `u16be` values are the current and maximum weight pair. Their order is still provisional.

### `0x10`: current vitals

| Order | Type | Field | Confirmed use |
|---:|---|---|---|
| 0 | `u32be` | `vitality` | `s_HP`, `NUM_HP`, bottom HP orb |
| 1 | `u32be` | `mental` | `s_MP`, `NUM_MP`, bottom MP orb |

The executable's retained diagnostic string calls these values `vit` and `ment`.

### `0x08`: experience and currency

| Order | Type | Field | Confirmed use |
|---:|---|---|---|
| 0 | `u32be` | `experience` | `s_EXP` |
| 1 | `u32be` | `next_experience` | `s_nextLev` |
| 2 | `u32be` | `ability_experience` | `s_AEXP`, diagnostic name `ABP` |
| 3 | `u32be` | `next_ability_experience` | `s_nextAb` |
| 4 | `u32be` | `game_points` | `s_GP`, diagnostic name `GP` |
| 5 | `u32be` | `gold` | `s_Gold` and several gold displays |

The retained format string is `VariableData2 exp %u next %u ABP %u next %u GP %u gold %u`. This is strong local-binary evidence for the ordering.

### `0x04`: extended status

| Order | Type | Field | Confirmed use |
|---:|---|---|---|
| 0 | `u8` | `extended_control_0` | Cached by `WorldUserFunc` |
| 1 | `u8` | `extended_control_1` | Compared with 8 by the world handler |
| 2 | `u8` | `extended_control_2` | Cached by `WorldUserFunc` |
| 3 | `u8` | `extended_control_3` | Cached by `WorldUserFunc` |
| 4 | `u8` | `extended_control_4` | Cached by `WorldUserFunc` |
| 5 | `u8` | `packed_parcel_mail_flags` | Split into low and high nibbles when flag `0x01` is set |
| 6 | `u8` | `attack_element` | `e_attack` |
| 7 | `u8` | `defense_element` | `e_defense` |
| 8 | `u8` | `magic_percent_steps` | `e_magic`, displayed as value times 10 percent |
| 9 | `u8` | `extended_unknown_9` | Copied into shared world state |
| 10 | `i8` | `armor_class` | `e_AC`, self profile |
| 11 | `u8` | `damage` | `e_DMG` |
| 12 | `u8` | `hit` | `e_HIT` |

Element values are resolved through internal strings: 0 None, 1 Fire, 2 Water, 3 Wind, 4 Earth, 5 Light, 6 Dark, 7 Wood, 8 Metal, and 9 Undead.

The high nibble of `packed_parcel_mail_flags` drives the bottom-button new-mail effect. The low nibble likely reports parcel presence because retained diagnostics refer to both parcel and `hasNewMail`, but that half remains provisional.

## Decoded packet object

`net_s_status_deserialize` stores the conditional groups in the temporary `SStatus` object. These offsets are useful when following a handler in IDA:

| Object offset | Value |
|---:|---|
| `+0x14` | Fixed character group present |
| `+0x15..+0x3B` | Fixed character fields |
| `+0x3C` | Current-vitals group present |
| `+0x40`, `+0x44` | Current vitality and mental |
| `+0x48` | Experience/currency group present |
| `+0x4C..+0x60` | Experience, next experience, ABP, next ABP, GP, and gold |
| `+0x64` | Extended-status group present |
| `+0x65..+0x75` | Extended fields, with natural alignment gaps in the C++ object |
| `+0x76` | First boolean derived from flag `0x02` |
| `+0x7A` | Second boolean derived from flag `0x02` |
| `+0x7B` | Flag `0x01` marker |
| `+0x77` | Packed parcel/mail nibbles are valid |
| `+0x78` | Low packed nibble is nonzero |
| `+0x79` | High packed nibble is nonzero, used as `hasNewMail` |

The object offsets are not wire offsets. Padding appears between some byte fields because this is the decoded C++ packet instance.

## Client consumers

| Consumer | Address | Effect |
|---|---:|---|
| `net_handle_s_status` | `0x5F1A10` | Main game-server handler and world forwarding |
| `world_user_func_apply_s_status` | `0x5FCFD0` | Updates the local player state cache |
| `ui_status_info_apply_s_status` | `0x574B30` | Updates the main `_nstatus.txt` character values |
| `ui_extra_status_apply_s_status` | `0x575FB0` | Updates elements, magic, AC, damage, and hit |
| `ui_bottom_status_apply_s_status` | `0x59D6C0` | Updates weight, numeric HP/MP, and the HP/MP orbs |
| `ui_bottom_buttons_apply_s_status` | `0x41BB80` | Updates the new-mail bottom-button effect |
| `ui_self_profile_apply_s_status` | `0x5B0C40` | Updates attributes and armor class in the self profile |

The primary and extended status panes both use `setoa.dat:_nstatus.txt`. See the [UI pane class catalog](../../ui/pane-classes.md).

## Local player cache

`WorldUserFunc` is confirmed by Visual C++ RTTI. The main controller owns its pointer at controller offset `+0x2CC`. Its status handler stores these values at stable object offsets:

| Offset | Value |
|---:|---|
| `+0x104C` | Two-bit client state |
| `+0x1055..+0x1057` | Three leading fixed-group bytes |
| `+0x1058` | Level |
| `+0x1059` | Ability |
| `+0x105C` | Gold |
| `+0x1060` | Experience |
| `+0x1064` | Strength |
| `+0x1068` | Dexterity |
| `+0x106A` | Wisdom |
| `+0x106C` | Constitution |
| `+0x106E` | Intelligence |
| `+0x1070` | Level-up points |
| `+0x1074` | Fixed-group trailing `u32` |
| `+0x1078` | Current vitality |
| `+0x107C` | Maximum vitality |
| `+0x1080` | Current mental |
| `+0x1084` | Maximum mental |
| `+0x108C..+0x1091` | First six extended-group bytes |
| `+0x15C80`, `+0x15C84` | Weight pair |

The status pane keeps the four `next`, ABP, and GP values that are not copied into these nearby `WorldUserFunc` fields.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Conditional group masks: confirmed from the deserializer.
- Level, ability, attributes, HP, MP, experience, ABP, GP, gold, elements, AC, damage, and hit: confirmed from local UI controls and retained diagnostic strings.
- State names, leading fixed bytes, weight order, several extended controls, and the parcel low nibble: provisional.
