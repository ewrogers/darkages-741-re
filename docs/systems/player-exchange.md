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

[`SUserAppearance`](../network/server/005-0x05-user-appearance.md) action-state bit `0x01` also participates when an exchange starts. If the lock is set when the server sends the Started event, the client does not create `ExchangeDialog` and replies with `CExchange` action `4`. The ordinary client-side Start request is not gated by this field, so the server remains responsible for deciding whether to offer the exchange in the first place.

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

## Item offer dialogs

Exact RTTI `AddItemDialog` loads `lexchai.txt` and embeds exact RTTI `MyItemListPane`. The list snapshots the 60 local inventory slots, draws each icon and dye with a DBCS-safe truncated name, and exposes the selected one-based slot. Confirm sends `CExchange` action `0x01`; confirm and cancel then close this temporary dialog.

If the server requests a quantity, exact RTTI `AddItemWithCountDialog` loads `litemex.txt`. Its confirmation control is enabled only while the quantity field is nonempty. Confirmation parses decimal text, clamps it to the `u8` range, sends action `0x02` with the staged slot, and closes. Both temporary dialogs also close if `SExchange` event `0x04` cancels the exchange while they are open.

Exact RTTI `ExchangeItemListPane` owns the eight-row offer view used by the main dialog. Adding a server-supplied item replaces the row with the same item ID or appends a new row, then draws its icon, palette selection, and shortened name.

## Invoking an action without pointer input

Use a main-thread action wrapper around the live, presented `ExchangeDialog`. Do not choose UI simulation or bare packet construction for every operation. The useful boundary differs by action:

| Requested action | Native entry point | Required local behavior |
| --- | --- | --- |
| Add item by slot | `net_send_exchange_add_item` | Validate a live one-based inventory slot and send action `0x01` first |
| Supply stack quantity | `net_send_exchange_add_stackable_item` | Wait for the server quantity request, use its live `AddItemWithCountDialog`, then close that temporary pane |
| Add gold | `net_send_exchange_set_gold` | Set `gold_was_sent` after submission and let the server update the displayed offer |
| Accept | `ui_exchange_dialog_handle_action` action `0` | This sends action `0x05` and sets `local_accept_sent`; refresh the controls afterward |
| Cancel | `ui_exchange_dialog_handle_action` action `1` | This sends action `0x04`; do not close the main dialog locally |

The inventory-drop UI handler is a poor slot-based API because it expects an `InvItemPane` drag source. The packet producer already accepts a one-based slot, but it performs no range or occupancy check. A wrapper should resolve the live inventory entry again, require slot `1` through `60`, and reject an item change once either party has accepted.

Stackable items keep their two-stage server handshake even when the desired quantity is already known. Send action `0x01`, wait for `SExchange` event `0x01`, then resolve the resulting `AddItemWithCountDialog`. That temporary dialog stores its exchange ID at `+0x630` and staged slot at `+0x634`. The main `ExchangeDialog` uses `+0x634` for `local_accept_sent`, so passing the main dialog to the stackable-item sender would put the wrong byte on the wire. Default an omitted quantity to `1`, require `1` through `255`, and close the temporary count pane after action `0x02` is queued.

The gold packet producer accepts the desired `u32` directly, but the normal focus-change path also sets `gold_was_sent` at `+0x637`. Mirror that write so the local field cannot be edited and submitted again. The accept packet producer similarly omits the `local_accept_sent` write, which is why the dialog action handler is the better direct entry point for confirmation.

Cancel is the simplest operation. Its dialog action and network producer have the same local effect: queue the request and wait. Keep a controller-side pending latch if duplicate external commands are possible, because the client does not mark Cancel pending or remove the pane until the server responds.

## Completion and cancellation popups

The Cancelled handler reads its `string8` message, creates a one-button alert pane, and removes the exchange. The Accepted handler updates the indicated party first. It creates the same alert and removes the exchange only when both acknowledgement flags are one.

Suppressing the alert must not skip the remaining close path. A narrow patch can make the two alert allocations return null through their existing no-allocation branches. A redirecting hook can instead append the already-decoded message through `ui_append_game_message_palette` with palette `0x58`, followed by the same newline used by `SMessage` type `0x00`.

That direct append reproduces the floating message bar only. It does not create a real [`SMessage`](../network/server/010-0x0a-message.md) or add the text to persistent history. A hook that needs both destinations should queue a bounded synthetic message event through the ordinary main-thread event path. Exchange messages can be 255 bytes, while the floating overlay is safe only through 130 bytes, so a redirect must clamp or reject longer text.

Static addresses, verified bytes, and the two no-popup patches are in [Exchange UI quality-of-life hooks](../appendix/runtime-patches/exchange-ui.md).
