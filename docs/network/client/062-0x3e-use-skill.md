# Use Skill (`CUseSkill`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x3E` (62) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **use skill**.

## Sent by

Known static callers lead to:

- `Pane::SkillInvItemPane`

## Body

```text
packet CUseSkill {
    u8 opcode                 // 0x3E
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
