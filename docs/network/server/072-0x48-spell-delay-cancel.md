# Spell Delay Cancel (`SSpellDelayCancel`)

`SSpellDelayCancel` stops the client's pending timed spell cast. It clears the cast-active state and removes the timers that would send the remaining chant lines and the queued spell request.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x48` (72) |
| Transform | derived |
| UI owner | `SpellDelayControlPane` |
| Handler | `ui_spell_delay_control_pane_handle_network_event` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SSpellDelayCancel {
    u8      opcode                 // 0x48
}
```

The concrete deserializer returns without reading any fields. The plaintext body is exactly the opcode byte.

## Client flow

`SpellDelayControlPane` receives the typed packet through its network event handler. The handler calls `ui_cancel_spell_delay`, which performs two operations:

1. It writes zero to the pane's `cast_active` byte at complete-object offset `+0x8C94`.
2. It cancels every timer owned by the pane. The timer manager value `0x7FFFFFFF` is a wildcard, not a timer ID.

Removing the timers is what stops the cast. Without a later timer callback, the client sends no more [Spell Delay Say (`CSpellDelaySay`)](../client/078-0x4e-spell-delay-say.md) messages and never submits the queued [Use Spell (`CUseSpell`)](../client/015-0x0f-use-spell.md). The client sends no acknowledgement or other response to this packet.

The handler does not show a message, play an effect, or change another pane.

## State changes

| Pane field | Offset | Result |
| --- | ---: | --- |
| `cast_active` | `+0x8C94` | Cleared to zero |
| Owned timers | timer manager | All removed |
| `total_cast_lines` | `+0x190` | Unchanged |
| `current_cast_line` | `+0x191` | Unchanged |
| Cast-line buffers | `+0x192` | Unchanged |
| Queued `CUseSpell` body | `+0xB92` | Unchanged, but no longer submitted |
| Spell name | `+0x8B92` | Unchanged |
| Queued body length | `+0x8C92` | Unchanged |

The retained data is inert after its timers are removed. A later cast overwrites the queue and restarts the state normally. See the [Spell delay control data map](../../appendix/runtime/inventory-ui.md#spell-casting-control) for the complete layout.

## Observed server triggers

Project-owner runtime traces show the server sending this command when an active cast is interrupted by actions including moving, using an item, clicking another living object, and removing equipment.

Those triggers describe observed server behavior. The client executable proves how it handles the cancellation, but it does not contain the server's decision rules or establish that the list is exhaustive.

## Construction and dispatch

`net_spell_delay_cancel_server_packet_ctor` passes opcode `0x48` to the common server packet base and installs the exact `SSpellDelayCancel` vtable. `net_create_spell_delay_cancel_server_packet` allocates the common `0x10`-byte packet object, and `net_deserialize_spell_delay_cancel_server_packet` consumes no payload.
