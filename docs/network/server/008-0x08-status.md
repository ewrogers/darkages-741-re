# Status (`SStatus`)

`SStatus` updates one or more parts of the player's character sheet. A flag byte lets the server send a full snapshot during login or a small update after an equipment change, a health change, or new mail.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x08` (8) |
| Transform | derived |
| Session owner | RTTI class `WorldUserFunc` |
| UI owners | `StatusInfoPane`, `ExtraStatusInfoPane`, `GUIBackPane`, inventory and menu panes, and `BtmButtonsPane_A` |
| Name provenance | Microsoft C++ RTTI in the target |

## Field flags

The byte after the opcode selects the blocks that follow. The high two bits are different: together they form a two-bit privilege level.

| Mask | Meaning in this client |
| ---: | --- |
| `0xC0` | Privilege level, stored as `(fields & 0xC0) >> 6` |
| `0x20` | Core stats block |
| `0x10` | Current health and mana block |
| `0x08` | Experience and currency block |
| `0x04` | Combat modifiers block |
| `0x02` | Standalone state bit; called `Swimming` in project protocol vocabulary, but no 7.41 consumer has been found |
| `0x01` | Makes the mail-state byte in the modifiers block active |

The privilege value is not reduced to a single administrator boolean. `WorldUserFunc` keeps all four possible values. Several helpers treat any nonzero value as privileged, while map movement has a special bypass for values `1` and `2`. The exact player-facing distinction among values `1`, `2`, and `3` remains unresolved.

The standalone `0x02` status bit is separate from the action state carried by [`SUserAppearance`](005-0x05-user-appearance.md). No `SStatus` handler copies it to the saved movement/action lock. Runtime changes to that lock require another opcode `0x05`, normally using its state-only form.

## Body

All multi-byte integers are big-endian.

```text
packet SStatus {
    u8      opcode                    // 0x08
    u8      fields

    if fields & 0x20 {
        u8      retained_stats_0
        u8      retained_stats_1
        u8      retained_stats_2
        u8      level
        u8      ability_level
        u32     max_health
        u32     max_mana
        u8      strength
        u8      intelligence
        u8      wisdom
        u8      constitution
        u8      dexterity
        u8      has_stat_points
        u8      stat_points
        u16     max_weight
        u16     weight
        u32     opaque_status_word
    }

    if fields & 0x10 {
        u32     health
        u32     mana
    }

    if fields & 0x08 {
        u32     total_experience
        u32     to_next_level
        u32     total_ability
        u32     to_next_ability
        u32     game_points
        u32     gold
    }

    if fields & 0x04 {
        u8      retained_modifier_0
        u8      blind_code
        u8      retained_modifier_1
        u8      retained_modifier_2
        u8      retained_modifier_3
        u8      mail_state
        u8      attack_element        // Element
        u8      defense_element       // Element
        u8      magic_resist_units
        u8      unknown_modifier_4
        s8      armor_class
        u8      damage_modifier
        u8      hit_modifier
    }
}
```

The first three stats bytes are parsed and retained. They must not be skipped merely because the visible panes do not label them. Every stats block in the supplied login trace used `02 00 00`, not the `01 00 00` seen in some other implementations.

A receive-side zero may follow the selected blocks. It is not consumed by `net_deserialize_status_server_packet`. See [Receive-side zero bytes](../packet-transforms.md#receive-side-zero-bytes).

## Character and UI updates

`net_handle_status_server_packet` handles the global effects, then the registered panes independently consume the same decoded object.

- `WorldUserFunc` retains privilege, core stats, current vitals, total experience, gold, weight, and several unknown bytes.
- `StatusInfoPane` updates the main character sheet. `has_stat_points` controls its stat-up buttons, while `stat_points` supplies the displayed count.
- `ExtraStatusInfoPane` updates attack and defense element, magic resistance, signed armor class, damage, and hit.
- `GUIBackPane` updates the health and mana bar targets.
- Inventory and merchant-style menu panes update their local gold displays.
- `UserInfoPane` updates the five attributes and signed armor class in its secondary character view.
- `BtmButtonsPane_A` updates the flashing mailbox indicator.

The combat-modifier block also sets the global blinded state. Only `blind_code == 0x08` is treated as blinded. The renderer stores that boolean and redraws the world view.

`unknown_modifier_4` is copied to an application field at `+0x444`, but no read of that destination has been confirmed. Its meaning remains unknown.

The mapped fields are in [Status state](../../appendix/runtime/session.md#status-state) and [Status and mail panes](../../appendix/runtime/inventory-ui.md#status-and-mail-panes).

## Mail and parcel state

The client does not decode `mail_state` as a set of individually named bits. It derives two booleans:

```c
low_nibble_present  = (mail_state & 0x0F) != 0;
high_nibble_present = (mail_state & 0xF0) != 0;
```

Those values are valid only when both `fields & 0x04` and `fields & 0x01` are set. The bottom-button pane uses the high-nibble result to start or stop its 500 ms mailbox flash. No consumer of the low-nibble result has been identified.

Dormant debug strings in the executable describe the same branches as “parcel” and `hasNewMail`. They support the mail interpretation, but they are not referenced by the live handler and do not prove names for individual bits.

## Elements

`attack_element` and `defense_element` use the shared [`Element`](../protocol-types.md#element) type.

The attack and defense values are not range-checked before this lookup, so valid senders must keep them between `0` and `9`. Magic resistance is displayed as `magic_resist_units * 10` followed by a percent sign.

## Supplied login trace

The supplied successful-login trace contains 49 status packets. Their flag combinations were:

| Fields | Count | Blocks present |
| ---: | ---: | --- |
| `0x04` | 13 | Modifiers |
| `0x05` | 5 | Modifiers and active mail state |
| `0x24` | 30 | Stats and modifiers |
| `0x3C` | 1 | Stats, vitals, progression, and modifiers |

All 49 included the modifiers block. None set the standalone `0x02` state bit. Five set the mail-state gate and used raw `mail_state == 0x30`.

The `opaque_status_word` has a repeatable but incomplete pattern. Across the 31 supplied stats blocks, its high byte matched the signed armor-class byte and its low two bytes were zero. Its remaining byte was `0x05` after equipment additions and `0x00` after inventory additions. This looks more like a packed legacy or update word than one scalar stat, but the client only stores it and no reader has been found. The field remains deliberately unnamed.

## Known limits

The exact meanings of the three retained stats bytes, five retained or unknown modifier bytes, `opaque_status_word`, privilege sublevels, and standalone `0x02` state are not yet established. The game does have a skill named Swimming, but the client does not use this `SStatus` bit in its movement or swimming-render paths. The value remains preserved without assigning it that behavior.

No client request is required before an ordinary status update. During the supplied login flow the server sends one full snapshot, then smaller packets as its load loop adds equipment and inventory entries.
