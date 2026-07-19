# Action Delay (`SActionDelay`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3F` (63) |
| Transform | derived |
| Class name | `SActionDelay` |
| Name provenance | Microsoft C++ RTTI in the target |
| UI owners | `NewSkillInventoryPane`, `NewSpellInventoryPane` |

## Purpose

The server uses this packet to place one spell or skill inventory slot on a client-side action delay. The selected icon is tinted and its normal pointer actions are blocked until a local timer expires.

This is separate from the spell cast-line system. [`CSpellDelayRequest`](../client/077-0x4d-spell-delay-request.md), [`CSpellDelaySay`](../client/078-0x4e-spell-delay-say.md), and [`SSpellDelayCancel`](072-0x48-spell-delay-cancel.md) coordinate multi-line spell chanting. `SActionDelay` is a server-selected cooldown applied after or independently of that process.

## Body

```text
packet SActionDelay {
    u8  opcode                    // 0x3F
    u8  selector                  // 0 = spell, 1 = skill
    u8  slot                      // one-based slot in the selected inventory
    u32 duration_seconds
}
```

The client reads the body in `net_deserialize_action_delay_server_packet`. The duration is an unsigned value on the wire. Each UI handler multiplies it by 1,000 with 32-bit arithmetic before scheduling timers.

### Selector

| Value | Target | Consuming pane |
| --- | --- | --- |
| `0` | Spell | `NewSpellInventoryPane` |
| `1` | Skill | `NewSkillInventoryPane` |

Both inventory panes receive opcode `0x3F`. The skill handler consumes only selector `1`, while the spell handler consumes only selector `0`. Other selector values are ignored by both panes.

## Slot handling

The slot is one-based. Both panes accept slots 1 through 90 and use `slot - 1` to index their item-pointer arrays.

A valid but empty slot consumes the packet without starting a timer. An out-of-range slot is rejected. The packet identifies the current slot rather than a skill or spell ID, so moving or replacing an entry does not move the delay with the original action.

## Skill delay

`ui_skill_inventory_apply_action_delay` sets `SkillInvItemPane + 0x322` to one. While this flag is set, the item activation and pointer-event paths reject use, drag start, and information actions.

Skills also receive a moving cooldown visual:

1. `ui_skill_item_start_cooldown_visual` records `timeGetTime()` as the start, calculates the end time, sets progress to zero, and schedules timer ID `0x10204` after 100 ms.
2. `ui_skill_item_cooldown_visual_timer` maps elapsed time to an integer step from 0 through 30 and requests a redraw. It schedules itself again every 100 ms while the delay flag and visual-active flag remain set.
3. `ui_skill_inventory_item_draw` tints the full icon and applies a second tint below the progress boundary. The boundary moves from the top toward the bottom in 30 steps.
4. An inventory-owned timer clears the action-delay flag after `duration_seconds * 1000` ms.

The tint arguments are palette indexes `0x58` for the full icon and `0x18` for the remaining lower region. Their final colors come from the active client palette, so they should not be documented as fixed RGB values.

## Spell delay

`ui_spell_inventory_apply_action_delay` sets `SpellInvItemPane + 0x297` to one. The same flag blocks spell activation, drag start, and information actions.

`ui_spell_inventory_item_draw` applies the palette-index `0x58` tint to the complete icon. Spells do not store start and end times and do not run the 100 ms progress timer. Their icon remains in one delayed appearance until the inventory-owned expiry timer clears the flag.

## Timing and reset behavior

The expiry timer belongs to the selected inventory pane, uses timer ID zero, and carries the one-based slot as its payload. When it fires, the pane looks up whichever item is currently in that slot and clears that item's delay flag. The timer runs through the main-thread event dispatcher. Hiding the inventory does not pause it.

The client does not cancel an older expiry timer before accepting another delay for the same slot. For a skill, it also starts another `0x10204` progress-timer chain while overwriting the shared start and end fields. Therefore overlapping packets can let the earliest expiry clear a newer delay and can temporarily leave duplicate visual update timers. Normal server behavior may avoid this case, but the client does not enforce it.

Replacing a delayed item before expiry has a similar slot-based edge case: the old timer resolves the current pointer and can clear the replacement item's flag. A zero-second delay is set first and then expires when the dispatcher processes the due timer, rather than being skipped inline.

## Client traffic

`SActionDelay` sends no acknowledgement or dedicated client response. It can accompany the action flows begun by [`CUseSpell`](../client/015-0x0f-use-spell.md) or [`CUseSkill`](../client/062-0x3e-use-skill.md), but the packet itself is downstream-only and the server can select any valid slot.

The complete UI flow is described in [Skill and spell action delays](../../systems/action-delays.md).
