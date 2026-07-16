# Spell Delay Say (`CSpellDelaySay`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x4E` (78) |
| Encoding | session key |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

The client sends this message for **spell delay say**.

## Sent by

Known static callers lead to:

- `Pane::SkillInvItemPane`

## Body

```text
packet CSpellDelaySay {
    u8 opcode                 // 0x4E
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
