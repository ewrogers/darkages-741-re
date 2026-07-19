# Skill and spell action delays

The game can put one spell or skill slot on a local cooldown at the server's request. During that time the icon is tinted and the client refuses its normal pointer actions. Skills show a moving progress wipe, while spells use a fixed delayed appearance.

The feature is owned by the two inventory panes. It is not a global character timer and it is not part of the spell cast-line controller.

```text
SActionDelay (0x3F)
        |
        +-- selector 0 --> NewSpellInventoryPane --> fixed tint + input block
        |
        +-- selector 1 --> NewSkillInventoryPane --> 30-step wipe + input block
```

## Packet routing

[`SActionDelay`](../network/server/063-0x3f-action-delay.md) carries a selector, a one-based slot, and a duration in whole seconds. `ui_skill_inventory_handle_network_event` and `ui_spell_inventory_handle_network_event` both recognize opcode `0x3F`, but their delay helpers accept opposite selector values.

| Selector | Inventory | Valid slots | Item flag |
| --- | --- | --- | --- |
| `0` | Spell | 1 through 90 | `SpellInvItemPane + 0x297` |
| `1` | Skill | 1 through 90 | `SkillInvItemPane + 0x322` |

The first matching pane consumes the event. Unknown selectors reach neither delay path. A valid empty slot is treated as handled but has no item to change.

## What the flag controls

The delay flag is checked by more than the drawing code. The skill and spell activation functions return without building [`CUseSkill`](../network/client/062-0x3e-use-skill.md) or [`CUseSpell`](../network/client/015-0x0f-use-spell.md) while the corresponding flag is set. Their item pointer handlers also refuse drag start and information actions.

This makes the feature a client-enforced slot lock with visual feedback. It is not only an overlay. The server does not receive an acknowledgement when the lock starts or ends.

## Skill progress

A skill item keeps a small visual clock:

```c
progress = 0;
start_ms = timeGetTime();
end_ms = start_ms + duration_seconds * 1000;
visual_active = 1;

every 100 ms:
    progress = clamp((now - start_ms) * 30 / (end_ms - start_ms), 0, 30);
```

Timer ID `0x10204` owns the 100 ms updates. The callback uses the `TimerHandler` secondary base at `SkillInvItemPane + 0x11C`, so its received `this` pointer is adjusted from the complete item object.

The draw method first renders the ordinary skill icon. While delayed, it applies a palette-index `0x58` tint across the full icon. It also applies palette index `0x18` from the current vertical boundary to the bottom. Progress advances the boundary from top to bottom in 30 integer steps. The palette resolves both indexes at runtime.

The visual timer stops rescheduling after progress reaches 30 or after the inventory expiry timer clears the action-delay flag. Its 100 ms cadence is the update rate, not the cooldown duration.

## Spell appearance

Spell items do not keep a start time, end time, progress value, or repeating visual timer for this feature. Their draw method applies palette index `0x58` to the full icon whenever the delay flag is set. The appearance changes back when the inventory expiry timer clears the flag.

## Expiry ownership

Both inventory handlers convert seconds to milliseconds and schedule timer ID zero on their own `NewSkillInventoryPane` or `NewSpellInventoryPane`. The timer payload is the one-based slot. At expiry, the callback resolves the current item pointer in that slot and clears its delay flag.

This has several consequences:

- The delay continues while the inventory is hidden because neither timer callback tests visibility.
- The delay follows the slot timer, not the original item object.
- Removing and replacing an item can make an old timer clear the replacement's flag.
- Repeating a delay before the previous one expires does not cancel the older timer. The earliest expiry can therefore clear the newer delay.
- Repeating a skill delay also creates another 100 ms timer chain against the same overwritten start and end fields.
- The duration multiplication and timer arithmetic have no range check and use 32-bit values.

These are client behavior limits, not recommended server semantics. A server should avoid overlapping delays for the same slot unless it intentionally accounts for the earliest outstanding expiry.

## Different from cast-line delay

`SpellDelayControlPane` queues a spell body, sends chant lines once per second, and submits the spell when all configured lines are complete. That system uses [`CSpellDelayRequest`](../network/client/077-0x4d-spell-delay-request.md), [`CSpellDelaySay`](../network/client/078-0x4e-spell-delay-say.md), and [`SSpellDelayCancel`](../network/server/072-0x48-spell-delay-cancel.md).

`SActionDelay` does none of that work. It arrives as a server message, targets an already populated inventory slot, and controls only the local slot lock and its icon feedback.
