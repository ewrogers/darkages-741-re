# Exchange (`SExchange`)

`SExchange` opens and updates the player-exchange dialog. Its event byte selects one of six small bodies for starting, adding an offer, changing gold, cancelling, or acknowledging a party.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x42` (66) |
| Transform | derived |
| Name provenance | Exact Microsoft C++ RTTI in the target |

The constructor binds opcode `0x42`, and the packet factory registers the same concrete class. The deserializer stores the event at object offset `+0x10` and reads only the fields belonging to that event.

## Body

```text
packet SExchange {
    u8      opcode                    // 0x42
    u8      event

    if event == 0x00 {
        u32     exchange_id
        string8 target_name
    }

    if event == 0x01 {
        u8      slot
    }

    if event == 0x02 {
        u8      party
        u8      item_index
        u16     tagged_item_sprite
        u8      item_color
        string8 item_name
    }

    if event == 0x03 {
        u8      party
        u32     gold_amount
    }

    if event == 0x04 {
        u8      party
        string8 message
    }

    if event == 0x05 {
        u8      party
        string8 message
    }
}
```

## Events

| Value | Meaning | Client behavior |
| --- | --- | --- |
| `0x00` | Started | Create `ExchangeDialog` for the supplied ID and name |
| `0x01` | Quantity prompt | Open `AddItemWithCountDialog` for the supplied inventory slot |
| `0x02` | Item added | Add or replace one row in that party's offer list |
| `0x03` | Gold added | Replace that party's displayed gold amount |
| `0x04` | Cancelled | Show the message and close the exchange immediately |
| `0x05` | Accepted | Mark one party accepted; show the message and close only after both parties are accepted |

The two final event names are easy to reverse. Event `0x04` ignores the party for state purposes and always takes the close path. Event `0x05` updates the per-party acknowledgement flags and closes only when both are set. This client therefore identifies `0x04` as Cancelled and `0x05` as Accepted.

## Party values

| Value | Meaning | Dialog control |
| --- | --- | --- |
| `0x00` | You | `MyExchange` or `MyMoney` |
| Nonzero | Them | `YourExchange` or `YourMoney` |

The deserializer retains `tagged_item_sprite` exactly as a big-endian `u16`; it does not call a generic flag-clearing helper. The exchange-item display record also keeps the raw value. Its draw path subtracts `0x8001` when selecting item artwork, which interprets the client-specific tag and one-based sprite numbering later in the UI flow.

## Dispatch and closure

Event `0x00` is handled before an exchange pane exists. If the client is in a state that blocks the new dialog, it answers with [`CExchange`](../client/074-0x4a-exchange.md) Cancel and creates no pane. Otherwise it constructs the exact RTTI class `ExchangeDialog` from `_nexch.txt`.

Events `0x01` through `0x05` reach the open dialog through its primary-vtable network-event slot. Cancelled and final Accepted both remove the exchange only after processing their message. Earlier Accepted events update the acknowledgement image and leave the pane open.

See [Player exchange](../../systems/player-exchange.md) for the complete UI flow and popup behavior.
