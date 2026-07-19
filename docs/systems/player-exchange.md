# Player exchange

The exchange window is a server-owned dialog for offering items and gold to another player. The client builds the pane, reports local actions, and waits for server events before it changes the shared offer or closes the window.

## Flow

```text
CExchange Start
       |
       v
SExchange Started --> ExchangeDialog
                         |  item or gold actions
                         v
                      CExchange
                         |
                         v
              SExchange offer updates
                         |
             Cancelled or both Accepted
                         |
                         v
                 message popup + close
```

[`CExchange`](../network/client/074-0x4a-exchange.md) contains the local action. [`SExchange`](../network/server/066-0x42-exchange.md) contains the server event. The two acknowledgement flags are updated only by server event `0x05`; clicking OK merely sends the request and records that it was sent.

## ExchangeDialog

The exact RTTI class `ExchangeDialog` derives from `DialogPane` and loads `_nexch.txt`. It attaches controls in this order:

| Action ID | Named control | Role |
| --- | --- | --- |
| `0` | `OK` | Send Accept |
| `1` | `Cancel` | Send Cancel |
| `2` | `MyID` | Local name |
| `3` | `MyExchange` | Local item list and drop target |
| `4` | `MyMoney` | Local gold edit |
| `5` | `YourID` | Other player's name |
| `6` | `YourExchange` | Other player's item list |
| `7` | `YourMoney` | Other player's gold |

The layout also supplies the other party's acknowledgement image. As with other dialogs, these action IDs come from constructor attachment order rather than layout definition order.

The useful trailing fields are:

```c
struct ExchangeDialogFields {
    u8  dialog_pane[0x62C];
    u32 movable;                 // +0x62C, constructor writes 0
    u32 exchange_id;             // +0x630
    u8  local_accept_sent;       // +0x634
    u8  local_accepted;          // +0x635
    u8  other_accepted;          // +0x636
    u8  gold_was_sent;           // +0x637
};
```

`ExchangeDialog` inherits `ui_dialog_handle_pointer_event` at primary-vtable slot `+0x48`. That base handler already implements window movement, but only when `movable` is nonzero. Setting this field to one after construction makes the existing dialog draggable without replacing its pointer handler. Empty dialog background starts the drag; controls keep their normal event handling.

The quality-of-life patch leaves the small or large main-UI layout and the inventory's expansion state alone. Making the dialog draggable is sufficient because the player can move it away from the inventory. No exchange lifecycle tracking or layout restoration is needed.

## Completion and cancellation popups

The Cancelled handler reads its `string8` message, creates a one-button alert pane, and removes the exchange. The Accepted handler updates the indicated party first. It creates the same alert and removes the exchange only when both acknowledgement flags are one.

Suppressing the alert must not skip the remaining close path. A narrow patch can make the two alert allocations return null through their existing no-allocation branches. A redirecting hook can instead append the already-decoded message through `ui_append_game_message_palette` with palette `0x58`, followed by the same newline used by `SMessage` type `0x00`.

That direct append reproduces the floating message bar only. It does not create a real [`SMessage`](../network/server/010-0x0a-message.md) or add the text to persistent history. A hook that needs both destinations should queue a bounded synthetic message event through the ordinary main-thread event path. Exchange messages can be 255 bytes, while the floating overlay is safe only through 130 bytes, so a redirect must clamp or reject longer text.

Static addresses, verified bytes, and the two no-popup patches are in [Exchange UI quality-of-life hooks](../appendix/runtime-patches/exchange-ui-quality-of-life.md).
