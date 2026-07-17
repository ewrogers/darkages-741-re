# Use Skill (`CUseSkill`)

`CUseSkill` activates the skill in one skillbook slot. `SkillInvItemPane` uses the one-based slot originally supplied by `SAddSkill`.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x3E` (62) |
| Transform | derived |
| UI owner | RTTI class `SkillInvItemPane` |
| Name provenance | Related class vocabulary matched to the locally confirmed builder |

## Body

```text
packet CUseSkill {
    u8      opcode                    // 0x3E
    u8      slot
}
```

`net_send_use_skill` writes the two meaningful bytes. The common submission helper supplies the encrypted client packet's trailing zero.

The normal activation path checks two item-state flags before sending. Their exact game-facing meanings remain unresolved. The paired skill definition is [Add Skill (`SAddSkill`)](../server/044-0x2c-add-skill.md).
