# Remove Inventory (`SRemoveInventory`)

`SRemoveInventory` clears one inventory slot. It removes both the compact session record and the visible `InvItemPane` for that slot.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x10` (16) |
| Transform | derived |
| State owners | RTTI classes `WorldUserFunc`, `InventoryPane_A`, and `ItemInventoryPane` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

The plaintext body has one field after the command:

```text
packet SRemoveInventory {
    u8      opcode                    // 0x10
    u8      slot                      // 1 through 60
}
```

## Client state

Both receive paths reject slot `0` and values above `60`.

`WorldUserFunc` logically clears its compact record. It sets the present flag and sprite to zero and writes a null only to `name[0]`. The old dye byte and the rest of the name buffer remain in memory, but the cleared present flag makes the record inactive.

`InventoryPane_A` checks whether the slot has a live `InvItemPane`. If it does, the pane is detached, released, destroyed, and its pointer is set to null. Removing an already empty slot has no visible effect.

As with [`SAddInventory`](015-0x0f-add-inventory.md), a separate [`SStatus`](008-0x08-status.md) carries any resulting weight change. Removal does not adjust weight locally.

See [Inventory state](../../appendix/runtime/session.md#inventory-state) and [Item inventory panes](../../appendix/runtime/inventory-ui.md#item-inventory-panes) for the mapped fields.
