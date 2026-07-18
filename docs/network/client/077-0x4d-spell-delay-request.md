# Spell Delay Request (`CSpellDelayRequest`)

`CSpellDelayRequest` tells the server that a spell is entering its timed cast sequence. It is sent once, before the client begins sending the configured cast lines.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x4D` (77) |
| Transform | derived |
| UI owner | RTTI class `SpellDelayControlPane` |
| Name provenance | Project protocol vocabulary matched to the locally confirmed builder |

## Body

```text
packet CSpellDelayRequest {
    u8      opcode                    // 0x4D
    u8      cast_lines
}
```

`net_send_spell_delay_request` writes the two meaningful bytes. The common submission helper supplies the encrypted client packet's trailing zero.

## Cast flow

When an [Add Spell (`SAddSpell`)](../server/023-0x17-add-spell.md) UI item has a nonzero `cast_lines` value, `ui_start_spell_cast` queues the completed [Use Spell (`CUseSpell`)](015-0x0f-use-spell.md), schedules a one-second timer, sends this request, and sends cast line zero through [Spell Delay Say (`CSpellDelaySay`)](078-0x4e-spell-delay-say.md).

The client submits the queued spell on the final timer tick. A zero-line spell skips this packet and is submitted immediately.

The server can interrupt the sequence with [Spell Delay Cancel (`SSpellDelayCancel`)](../server/072-0x48-spell-delay-cancel.md). The client then removes the cast timers and does not submit the queued `CUseSpell` body.
