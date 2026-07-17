# Add Skill (`SAddSkill`)

`SAddSkill` fills one skillbook slot with its icon and display name. The client stores one copy in the world-session model and creates a separate `SkillInvItemPane` for the visible skill inventory.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x2C` (44) |
| Transform | derived |
| Session owner | RTTI class `WorldUserFunc` |
| UI owner | RTTI classes `NewSkillInventoryPane` and `SkillInvItemPane` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SAddSkill {
    u8      opcode                    // 0x2C
    u8      slot
    u16     icon
    string8 name
}
```

`name` begins with a one-byte byte count. `net_deserialize_add_skill_server_packet` copies it into a 256-byte packet-object buffer and adds a local NUL.

A receive-side trailing zero, when present, is not one of the class fields. See [Receive-side zero bytes](../packet-transforms.md#receive-side-zero-bytes).

## Session skillbook

`net_handle_add_skill_server_packet` forwards the decoded object to `WorldUserFunc`. The session path accepts slots 1 through 89 and stores a `0x104`-byte record at:

```c
entry = &this->skills[slot - 1];
entry->present = 1;
entry->icon = icon;
copy(entry->name, name, 256);
```

The mapped record is in [Skill state](../../appendix/runtime/session.md#skill-state).

## Skill inventory UI

`NewSkillInventoryPane` independently accepts slots 1 through 90. If the target slot already has an item, the pane releases that `SkillInvItemPane` before constructing its replacement.

The UI item keeps:

- the icon in a 16-bit field;
- the name in a 128-byte buffer;
- the original one-based slot used by [Use Skill (`CUseSkill`)](../client/062-0x3e-use-skill.md).

The 90-slot UI capacity is one entry larger than the 89-record session array, matching the discrepancy already seen in the spell inventory. The purpose of UI slot 90 is unknown.

## Supplied login trace

The supplied successful-login trace contains 28 `SAddSkill` packets before `SSelfLook`, covering occupied slots from 1 through 86. Every body matches the structure above. Five end immediately after the name and 23 have one additional zero.

The exact observed order is 47 `SAddSpell`, 28 `SAddSkill`, then another 37 `SAddSpell`. This confirms that skills follow an initial spell block, but the server does not keep all spell and skill additions in two strictly separated groups in this capture.
