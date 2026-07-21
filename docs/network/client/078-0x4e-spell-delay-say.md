# Spell Delay Say (`CSpellDelaySay`)

`CSpellDelaySay` carries visible chant text. The timed spell path sends configured cast lines and then the spell name. The normal skill path can also send one configured line through this packet immediately before activating the skill.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x4E` (78) |
| Transform | derived |
| UI owner | RTTI class `SpellDelayControlPane`; `SkillInvItemPane` activation path |
| Name provenance | Project protocol vocabulary matched to the locally confirmed builder |

## Body

```text
packet CSpellDelaySay {
    u8      opcode                    // 0x4E
    string8 text
}
```

`text` begins with a one-byte byte count. The common submission helper adds the encrypted client packet's trailing zero after the meaningful body.

## Cast flow

`SpellDelayControlPane` loads up to ten per-spell lines from the character's `SpellBook.cfg` data. It sends line zero immediately after [Spell Delay Request (`CSpellDelayRequest`)](077-0x4d-spell-delay-request.md), then sends the next line on each one-second timer tick. The on-disk format is described in [Per-character configuration](../../application/configuration.md#per-character-configuration).

When the current line reaches the total from [Add Spell (`SAddSpell`)](../server/023-0x17-add-spell.md), the client sends the spell name in this packet and submits the queued [Use Spell (`CUseSpell`)](015-0x0f-use-spell.md).

Project-owner runtime behavior confirms that the server presents these lines to nearby clients as [`SSay`](../server/013-0x0d-say.md) mode `2`, Chant. That receive path draws blue text over the caster without the ordinary speech-balloon frame.

A zero-line spell reaches the sender helper, but its zero-total guard returns before constructing this packet. The client submits `CUseSpell` immediately instead.

[Spell Delay Cancel (`SSpellDelayCancel`)](../server/072-0x48-spell-delay-cancel.md) removes the pending timers. No later cast line, final spell name, or queued `CUseSpell` is sent for that sequence.

## Skill flow

After a skill passes its local activation checks, `SkillInvItemPane` looks up that skill in the character's `SkillBook.cfg`. A nonempty `Skill:` value is sent once through this packet, followed immediately by [Use Skill (`CUseSkill`)](062-0x3e-use-skill.md). A missing or empty value skips this packet and does not prevent the skill packet.
