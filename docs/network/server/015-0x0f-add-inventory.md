# Add Inventory (`SAddInventory`)

`SAddInventory` fills one inventory slot. The client keeps a compact session record for gameplay lookup and a larger `InvItemPane` for the visible inventory entry.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x0F` (15) |
| Transform | derived |
| State owners | RTTI classes `WorldUserFunc`, `InventoryPane_A`, and `ItemInventoryPane` |
| Item class | RTTI class `InvItemPane` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

The plaintext body begins with the command byte:

```text
packet SAddInventory {
    u8      opcode                    // 0x0F
    u8      slot                      // 1 through 60
    u16     sprite
    u8      dye_color
    string8 name                      // u8 byte length, then that many bytes
    u32     quantity
    u8      can_stack                 // protocol boolean, expected as 0 or 1
    u32     durability
    u32     max_durability
}
```

The client deserializer reads these fields in exactly this order. `string8` permits up to 255 wire bytes and appends a local null terminator. The visible item keeps a bounded 128-byte name buffer.

## Client state

Both consumers accept slots `1` through `60` and use `slot - 1` as the array index.

`WorldUserFunc` stores a compact record containing the present flag, sprite, dye color, and name. It does not retain quantity, stackability, or durability in that record.

`InventoryPane_A` owns 60 `InvItemPane` pointers. `ItemInventoryPane` inherits this implementation. If the selected slot already contains an item, the client releases the old pane and clears its pointer before creating the replacement.

The new `InvItemPane` retains every wire field. When `can_stack` is nonzero, it changes the visible label to `name[ quantity ]`. This is presentation behavior. The client does not merge inventory stacks locally.

See [Inventory state](../../appendix/runtime/session.md#inventory-state) for the compact gameplay copy and [Item inventory panes](../../appendix/runtime/inventory-ui.md#item-inventory-panes) for the UI layouts.

## Status updates and weight

An immediately following [`SStatus`](008-0x08-status.md) is a separate packet event. `SAddInventory` itself does not calculate or change character weight. `SStatus` is the path that updates maximum weight and current weight in the session state, so sending it after each inventory change keeps those values synchronized.

The inventory pane also consumes the progression block of `SStatus` to refresh its gold display. Neither status action is required for the item insertion itself.
