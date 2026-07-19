# Exchange (`CExchange`)

`CExchange` starts a player exchange and sends every action taken in its dialog. One shared `u32` carries the request target for a new exchange and the active exchange value for later actions.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x4A` (74) |
| Transform | derived |
| Name provenance | Related protocol vocabulary matched to the local builders |

## Body

```text
packet CExchange {
    u8      opcode                    // 0x4A
    u8      action
    u32     target_or_exchange_id

    if action == 0x01 {
        u8      slot
    }

    if action == 0x02 {
        u8      slot
        u8      quantity
    }

    if action == 0x03 {
        u32     gold_amount
    }
}
```

All multibyte values follow the packet system's big-endian rule. Actions `0x00`, `0x04`, and `0x05` end after the `u32`.

## Actions

| Value | Meaning | Extra body | Client owner |
| --- | --- | --- | --- |
| `0x00` | Start exchange | None | Isolated request builder; live UI trigger remains unresolved |
| `0x01` | Add one item | `u8 slot` | Inventory drop into `ExchangeDialog` |
| `0x02` | Add stackable item | `u8 slot`, `u8 quantity` | `AddItemWithCountDialog` |
| `0x03` | Set gold | `u32 gold_amount` | `MyMoney` edit control |
| `0x04` | Cancel | None | Cancel button and automatic refusal when a start request is blocked |
| `0x05` | Accept | None | OK button |

The item slot is one-based. Action `0x01` means a quantity of one; the quantity byte exists only for action `0x02`.

The action mapping comes from all local body builders and their callers. In particular, `ExchangeDialog` attaches OK before Cancel, then maps those action IDs to `0x05` and `0x04`. The inbound start handler also builds `0x04` when client state prevents it from opening the dialog.

Related protocol vocabulary identifies the action `0x00` value as a target ID, but this builder has no recovered live static caller in the client. A successful [`SExchange`](../server/066-0x42-exchange.md) start supplies the value retained by the dialog and echoed by actions `0x01` through `0x05`. Static client code does not prove whether the two values are the same player ID or whether the server returns a separate exchange-session ID.

## UI flow

Dragging an inventory item into the local exchange list first sends action `0x01`. The server may answer with a quantity prompt. The count dialog then sends action `0x02` with the staged slot and chosen `u8` quantity.

Gold is sent through action `0x03`. Accept and Cancel do not close the pane locally. The client waits for the matching server event, so the server remains the owner of the final exchange state.

See [Player exchange](../../systems/player-exchange.md) for the pane, acknowledgement state, and UI hook points.
