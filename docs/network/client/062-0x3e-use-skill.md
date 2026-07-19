# Use Skill (`CUseSkill`)

`CUseSkill` activates the skill in one skillbook slot. `SkillInvItemPane` sends the one-based slot originally supplied by `SAddSkill`.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x3E` (62) |
| Transform | derived |
| UI owner | RTTI class `SkillInvItemPane` |
| Name provenance | Project-owner protocol vocabulary, confirmed by the local builder |

## Body

```text
packet CUseSkill {
    u8      opcode                    // 0x3E
    u8      slot
}
```

`net_send_use_skill` writes the two meaningful bytes. The common submission helper supplies the encrypted client packet's trailing zero.

## Local checks

The normal activation path first checks `SkillInvItemPane + 0x322`. [`SActionDelay`](../server/063-0x3f-action-delay.md) sets this flag for selector `1` and clears it with a local expiry timer. A nonzero value blocks activation before this packet is built. The second checked state byte at `+0x323` remains unresolved.

It then looks up the skill name in `DeniedItemList` mode 1. This object subscribes to the server-managed `BItems`, `BSkills`, and `BSpells` metadata names, then routes rows tagged `Skill` into this lookup. The names of denied skills are not hardcoded. A match suppresses `CUseSkill` locally. The current 19-file metadata cache contains none of those three tables, so this check has no entries unless the server advertises and supplies one.

This is only a client-side restriction. The server must still decide whether the skill can be used and apply its effect.

The paired skill definition is [Add Skill (`SAddSkill`)](../server/044-0x2c-add-skill.md). The action-delay UI flow is described in [Skill and spell action delays](../../systems/action-delays.md). Metadata delivery is described in [Metadata](../../file-formats/metadata.md).
