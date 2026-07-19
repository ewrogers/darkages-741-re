# Change Slot (`CChangeSlot`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x30` (48) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message when an inventory item is dragged from one slot to another.

## Sent by

`ItemInventoryPane` maps the pointer position to a zero-based cell, converts it to a one-based destination slot, and calls `net_send_change_slot`. The source slot comes from the dragged `InvItemPane`.

## Body

```text
packet CChangeSlot {
    u8 opcode                    // 0x30
    u8 zero                      // always 0
    u8 source_slot
    u8 destination_slot
}
```

The builder rejects encoded slot value `0x3C` for either endpoint. The pane hit test can produce zero-based cells `0` through `59`, but the final check makes one-based slot `60` non-movable through this packet. The reason that slot is reserved remains unresolved.

[`SUserAppearance`](../server/005-0x05-user-appearance.md) action-state bit `0x01` suppresses this packet before construction. This affects rearranging inventory slots, not ordinary [`CUse`](028-0x1c-use.md) activation.
