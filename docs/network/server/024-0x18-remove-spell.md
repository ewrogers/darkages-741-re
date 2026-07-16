# Remove Spell (`SRemoveSpell`)

`SRemoveSpell` empties one spellbook slot. The client removes both the world-session record used by gameplay code and the `SpellInvItemPane` used by the visible spell inventory.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x18` (24) |
| Transform | derived |
| Session owner | RTTI class `WorldUserFunc` |
| UI owner | RTTI class `NewSpellInventoryPane` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```c
struct SRemoveSpellBody {
    u8 opcode;                         // 0x18
    u8 slot;
};
```

`net_deserialize_remove_spell_server_packet` reads the single body byte into the packet object's `slot` field. A receive-side trailing zero, when present, is not part of this class. See [Receive-side zero bytes](../packet-transforms.md#receive-side-zero-bytes).

## Session spellbook

`net_handle_remove_spell_server_packet` forwards the decoded object to `WorldUserFunc`. The session path accepts slots 1 through 89 and calculates the record as:

```c
entry = this->spells[slot - 1];
```

`session_clear_spell_entry` then writes:

```c
entry->present = 0;
entry->spell_args_type = 0;
entry->name[0] = 0;
entry->prompt[0] = 0;
```

This is a logical clear, not a complete memory wipe. The old icon and the remaining bytes in both string buffers stay in memory, but `present == 0` and the empty strings make the record inactive. The structure is mapped in [Character spell state](../../appendix/runtime-structures.md#character-spell-state).

## Spell inventory UI

`NewSpellInventoryPane` independently handles the same packet. It accepts slots 1 through 90 and only acts when the corresponding `SpellInvItemPane` pointer is non-null.

The UI path converts the protocol slot to a zero-based index, releases the live item through the shared UI owner, and writes null into the pointer array. If the slot is invalid or already empty, it does nothing.

The 90-slot UI capacity remains one entry larger than the 89-record `WorldUserFunc` spell array. This is the same mismatch seen when processing [`SAddSpell`](023-0x17-add-spell.md); the purpose of UI slot 90 is still unknown.

## Result

The packet produces no client response. Its two local consumers return without consuming later event traversal after updating their own state.
