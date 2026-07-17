# Remove Skill (`SRemoveSkill`)

`SRemoveSkill` empties one skillbook slot. Like `SRemoveSpell`, it updates both the world-session record and the live inventory pane without sending a client response.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x2D` (45) |
| Transform | derived |
| Session owner | RTTI class `WorldUserFunc` |
| UI owner | RTTI class `NewSkillInventoryPane` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SRemoveSkill {
    u8      opcode                    // 0x2D
    u8      slot
}
```

`net_deserialize_remove_skill_server_packet` reads the single body byte into the packet object's `slot` field. A receive-side trailing zero, when present, is not part of this class.

## Session skillbook

`WorldUserFunc` accepts slots 1 through 89 and selects `skills[slot - 1]`. `session_clear_skill_entry` writes:

```c
entry->present = 0;
entry->name[0] = 0;
```

This is a logical clear rather than a full memory wipe. The old icon and remaining name-buffer bytes stay in memory, but the record is inactive and its string appears empty.

## Skill inventory UI

`NewSkillInventoryPane` accepts slots 1 through 90. It only removes a slot whose `SkillInvItemPane` pointer is non-null.

The pane converts the one-based protocol slot to a zero-based array index, releases the live item through the shared UI owner, and sets the pointer entry to null. Invalid and already-empty slots are ignored.

See [Skill state](../../appendix/runtime/session.md#skill-state) and [Skill inventory panes](../../appendix/runtime/inventory-ui.md#skill-inventory-panes) for both layouts, and [`SAddSkill`](044-0x2c-add-skill.md) for insertion behavior.
