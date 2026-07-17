# Add Spell (`SAddSpell`)

`SAddSpell` fills one spellbook slot and teaches the client how that spell collects its arguments. During the supplied successful-login sequence, the client requests its own appearance first, then receives the spellbook before the eventual `SSelfLook` response.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x17` (23) |
| Transform | derived |
| Session owner | RTTI class `WorldUserFunc` |
| UI owner | RTTI classes `NewSpellInventoryPane` and `SpellInvItemPane` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SAddSpell {
    u8      opcode                    // 0x17
    u8      slot
    u16     icon
    u8      spell_args_type
    string8 name
    string8 prompt
    u8      cast_lines
}
```

Both strings begin with a one-byte byte count. The class deserializer copies them into 256-byte local buffers and adds a local NUL after each value.

The RTTI-backed constructor assigns opcode `0x17`. `net_deserialize_add_spell_server_packet` reads the fields in exactly the order shown above. A receive-side trailing zero, when present, is not one of the class fields. See [Receive-side zero bytes](../packet-transforms.md#receive-side-zero-bytes).

## Argument modes

`spell_args_type` selects the UI used when the player activates the spell.

| Type | Client behavior |
| --- | --- |
| `1` | Opens `StringSpellInputPane` with the supplied prompt |
| `2` | Begins target selection with `DraggedSpellInvItemPane` |
| `3` | Opens four numeric inputs |
| `4` | Opens three numeric inputs |
| `5` | Uses the spell without an extra argument |
| `6` | Opens two numeric inputs |
| `7` | Opens one numeric input |
| `8` | Accepted into session storage, but not handled by the normal activation switch |

The string, target, and numeric paths eventually build different bodies for [Use Spell (`CUseSpell`)](../client/015-0x0f-use-spell.md). Type `8` remains unresolved in this build.

## Spellbook storage

The decoded packet reaches two consumers:

1. `net_handle_add_spell_server_packet` forwards it to `WorldUserFunc`, the world-session gameplay model.
2. `NewSpellInventoryPane` creates a `SpellInvItemPane` for display and interaction.

The session model stores 89 records beginning at `WorldUserFunc + 0x4DFA`. Each record keeps the slot-present flag, icon, argument type, name, and prompt. It accepts slots 1 through 89 and argument types 1 through 8.

The UI inventory allocates 90 pointers and accepts slots 1 through 90. Its item keeps the same visible fields plus `cast_lines`. The difference at slot 90 is real in the client, but the reason for it is not yet known. The mapped layouts are in [Spell state](../../appendix/runtime/session.md#spell-state) and [Spell inventory panes](../../appendix/runtime/inventory-ui.md#spell-inventory-panes).

## Cast lines

`cast_lines` is the number of one-second stages before the final spell request. The client keeps up to ten configurable lines per spell in the character's `SpellBook.cfg` data.

For a nonzero value, `ui_start_spell_cast`:

1. queues the completed `CUseSpell` body;
2. sends [Spell Delay Request (`CSpellDelayRequest`)](../client/077-0x4d-spell-delay-request.md) with the total count;
3. sends configured cast line zero through [Spell Delay Say (`CSpellDelaySay`)](../client/078-0x4e-spell-delay-say.md);
4. advances once per second;
5. sends the spell name and submits the queued `CUseSpell` on the final tick.

A zero value submits `CUseSpell` immediately. It does not schedule the timer, load cast text, or emit `CSpellDelayRequest` or `CSpellDelaySay`. The zero branch reaches the delay-say helper, but that helper returns before constructing a packet because the total is zero.

The client only assigns counts at or below ten. Values above ten are not handled as a safe clamp and should be treated as invalid.

## Login trace

The supplied successful-login trace contains 84 `SAddSpell` bodies before `SSelfLook`, covering slots 1 through 85. The observed argument types were `1`, `2`, and `5`; observed cast counts ranged from `0` through `8`.

Parsing each body with the layout above consumed every meaningful field. Ten bodies ended at `cast_lines`, while 74 had one additional zero. That variation supports treating the final zero as receive framing residue rather than part of `SAddSpell`.
