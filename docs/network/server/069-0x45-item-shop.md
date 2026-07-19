# Item Shop (`SItemShop`)

`SItemShop` supplies records to an already-open cash-shop shopping bag. It does not create the shopping-bag pane.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x45` |
| Concrete class | Exact RTTI `SItemShop` |
| Transform | `derived` |
| UI owner | Exact RTTI `ItemShop::ShoppingBagDialogPane` |

## Body

```text
packet SItemShop {
    u8 opcode                    // 0x45
    u8 variant

    if variant == 0 {
        u8 record_count

        repeat record_count {
            u8 record_type
            u32 record_id
            u16 sprite
            u8 color
            string8 name
            string8 description
            u32 quantity
            u8 description_mode

            if description_mode == 1 {
                string8 alternate_description
            }
        }
    }
}
```

Nonzero variants have no body fields after `variant` in the concrete deserializer.

## Variants

| Variant | Shopping-bag behavior |
| ---: | --- |
| `0` | Replace the complete record list, load icons, recalculate pages, and clear the busy state |
| `1` | Clear the busy state without replacing records |
| `2` | Not consumed by the pane |

Variant `0` can carry up to 255 records. The pane displays 30 records per page. It uses `description` normally; when `description_mode` is `1`, it displays `alternate_description`. Quantities greater than one are appended to the displayed item text.

## Request flow

Constructing `ShoppingBagDialogPane` sends [`CCashShop`](../client/108-0x6c-cash-shop.md) action `0`. Pressing Get sends action `1` with the selected record's `record_type` and `record_id`.

The packet reaches the pane through its network-event vtable slot. There is no central `SItemShop` handler that constructs a dialog, so sending `SItemShop` while no shopping-bag pane exists has no recovered UI consumer.
