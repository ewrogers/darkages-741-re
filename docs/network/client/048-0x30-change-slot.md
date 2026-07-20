# Change Slot (`CChangeSlot`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x30` (48) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message when an item, spell, or skill is dragged from one slot to another. A category byte selects which of the three slot collections the server should change.

## Sent by

Three UI paths build the same four-byte body:

- `ItemInventoryPane` calls `net_send_inventory_change_slot` with category `0`.
- `NewSpellInventoryPane` calls `net_send_spell_change_slot` with category `1`.
- `NewSkillInventoryPane` calls `net_send_skill_change_slot` with category `2`.

Each pane maps the drop position to a destination cell and converts it to a one-based slot. The source slot is retained by the dragged item pane.

## Body

```text
packet CChangeSlot {
    u8 opcode                    // 0x30
    u8 category
    u8 source_slot
    u8 destination_slot
}
```

| Category | Slot collection |
| --- | --- |
| `0` | Item inventory |
| `1` | Spells |
| `2` | Skills |

No other category value is constructed by this client.

## Client checks

The item-inventory path rejects slot `60` for either endpoint. The pane contains 60 cells, so this makes the final one-based slot non-movable through `CChangeSlot`. The reason it is reserved remains unresolved.

The 90-slot spell and skill paths reject any endpoint divisible by `36`. For normal pane-generated values, this reserves slots `36` and `72`. They also suppress a move when the source or occupied destination entry has its [`SActionDelay`](../server/063-0x3f-action-delay.md) flag set.

[`SUserAppearance`](../server/005-0x05-user-appearance.md) action-state bit `0x01` is checked only by the item-inventory category-`0` sender. The spell and skill senders do not consult that appearance field. All three paths have additional shared client guard checks whose exact user-facing meanings remain unresolved.
