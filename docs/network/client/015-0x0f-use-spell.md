# Use Spell (`CUseSpell`)

`CUseSpell` asks the server to cast the spell in one spellbook slot. The selected slot determines how the trailing bytes must be interpreted because the packet does not carry an argument type or argument count.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x0F` (15) |
| Transform | derived |
| UI owner | RTTI class `SpellInvItemPane` |
| Name provenance | Project-owner protocol vocabulary, confirmed by the local builders |

## Body

```text
packet CUseSpell {
    u8      opcode                    // 0x0F
    u8      slot                     // one-based

    if spell_args_type == 1 {
        bytes   text[remaining]
    }

    if spell_args_type == 2 {
        u32     target_id
        u16     target_x
        u16     target_y
    }

    if spell_args_type == 3 {
        repeat 4 {
            u16 value
        }
    }

    if spell_args_type == 4 {
        repeat 3 {
            u16 value
        }
    }

    if spell_args_type == 6 {
        repeat 2 {
            u16 value
        }
    }

    if spell_args_type == 7 {
        u16     value
    }
}
```

Type 5 is the slot-only form, so it has no trailing fields. Type 8 is retained from `SAddSpell`, but the normal activation dispatcher has no case for it.

`SAddSpell` supplies `spell_args_type`, the one-based slot, the input prompt, and the cast-line count. The type-to-body mapping is:

| Type | Trailing body |
| --- | --- |
| 1 | Raw text bytes with no length or terminator |
| 2 | Target ID, X, and Y, exactly 8 bytes |
| 3 | Four `u16` numeric values |
| 4 | Three `u16` numeric values |
| 5 | No arguments |
| 6 | Two `u16` numeric values |
| 7 | One `u16` numeric value |

## Why a generic reader is ambiguous

The wire body alone cannot distinguish text from numeric or target arguments. A server normally resolves the slot against the character's spellbook and uses that spell definition to choose the correct interpretation.

Without that state, a diagnostic reader can only expose possible interpretations. Eight remaining bytes can be read as `target_id`, `target_x`, and `target_y`; every remaining byte can be viewed as text; and each complete two-byte pair can be viewed as a numeric input. These interpretations may overlap and should not be presented as independently confirmed fields.

## Cast timing

All four builders pass the completed body to `ui_start_spell_cast`. A zero cast-line count submits `CUseSpell` immediately. A positive count starts the one-second spell-delay sequence and holds the body until its final timer tick. See [Spell Delay Request (`CSpellDelayRequest`)](077-0x4d-spell-delay-request.md) and [Spell Delay Say (`CSpellDelaySay`)](078-0x4e-spell-delay-say.md).

If the server sends [Spell Delay Cancel (`SSpellDelayCancel`)](../server/072-0x48-spell-delay-cancel.md), the client removes the pending timers. It leaves this queued body in memory but does not submit it.

The text form is also built by a separate bulletin batch flow. It uses the same opcode, slot, and unprefixed trailing text layout rather than a distinct packet format.

## Local denial check

Each normal builder checks the spell name in `DeniedItemList` mode 2 before starting the cast delay. This object subscribes to the server-managed `BItems`, `BSkills`, and `BSpells` metadata names, then routes rows tagged `Spell` into this lookup. A match suppresses the delay packets and `CUseSpell`. The current local metadata cache has none of those tables, so the list remains empty unless the server supplies one.

This remains a client-side convenience or policy check. The server must validate the cast and produce the spell-specific result.

The paired spell definition is [Add Spell (`SAddSpell`)](../server/023-0x17-add-spell.md). Metadata delivery is described in [Metadata](../../file-formats/metadata.md).
