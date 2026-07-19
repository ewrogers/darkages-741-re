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

## Detecting an open exchange

`ExchangeDialog` is not a singleton. The global count changed by its constructor and destructor counts modal dialogs in general, so it cannot identify exchange by itself.

A hook should retain the object pointer after `ui_exchange_dialog_ctor` returns and clear it in `ui_exchange_dialog_dtor`. A read-only pane-tree walk can instead compare the primary vtable with the exact `ExchangeDialog` vtable, but lifecycle tracking is simpler and avoids scanning live containers.

## Main UI size and inventory expansion

`GUIBackPane` owns the main interface and keeps these states separately:

```c
struct GUIBackPaneExchangeState {
    u8  unrelated_0000[0x4DF0];
    s32 layout_index;             // +0x4DF0: 0 small, 1 large
    u8  unrelated_4DF4[0x1B4];
    s32 current_page;             // +0x4FA8: 0 is item inventory
    u8  unrelated_4FAC[4];
    u8  page_is_expanded;         // +0x4FB0
};
```

Layout index `0` selects `_nbk_s.txt`, the small or minimal main UI. Index `1` selects `_nbk_l.txt`, the large UI. The constructor initializes the small layout first, and `ui_gui_back_apply_layout` records the selected index while applying its named geometry.

The item inventory is visibly in its extra-row state when `current_page == 0` and `page_is_expanded != 0`. These fields are stronger evidence than measuring the current pane rectangle. Expansion and main-UI size are independent. The item page can use its expanded geometry in the small layout even though several other pages are forced to their compact form there.

Changing the size layout applies the page's normal rectangle first. To preserve an expanded item inventory, call `ui_gui_back_select_page_mode` afterward with page `0` and expanded `1`. This re-applies the selected layout's expanded inventory rectangle.

## Completion and cancellation popups

The Cancelled handler reads its `string8` message, creates a one-button alert pane, and removes the exchange. The Accepted handler updates the indicated party first. It creates the same alert and removes the exchange only when both acknowledgement flags are one.

Suppressing the alert must not skip the remaining close path. A narrow patch can make the two alert allocations return null through their existing no-allocation branches. A redirecting hook can instead append the already-decoded message through `ui_append_game_message_palette` with palette `0x58`, followed by the same newline used by `SMessage` type `0x00`.

That direct append reproduces the floating message bar only. It does not create a real [`SMessage`](../network/server/010-0x0a-message.md) or add the text to persistent history. A hook that needs both destinations should queue a bounded synthetic message event through the ordinary main-thread event path. Exchange messages can be 255 bytes, while the floating overlay is safe only through 130 bytes, so a redirect must clamp or reject longer text.

## Force minimal while exchanging

The quality-of-life flow is feasible with two lifecycle hooks:

1. At exchange construction, read `GUIBackPane` through `ui_get_gui_back_pane`.
2. If the item page is expanded and the layout is large, save that state, call `ui_gui_back_apply_layout(gui, 0)`, then re-apply page `0` with expanded mode `1`.
3. Construct and position `ExchangeDialog` in the now-small layout, set its inherited `movable` field to one, and retain its pointer with a generation token.
4. After that exact dialog is destroyed, restore layout `1` and re-apply expanded item page `0` only if the UI still matches the state installed by the hook.

The constructor hook runs only after the native start handler has decided that a dialog may open. This avoids changing the UI when the client automatically refuses an exchange. Restoring from the destructor covers server cancellation, completion, local cancellation after the server reply, and other teardown paths.

The restore check should fail open. If the player changes layout, page, or expansion while the exchange is open, leave the newer state alone. All calls already occur on the main event thread, and no hook should wait for IPC or another process.

Static addresses, verified bytes, and the two no-popup patches are in [Exchange UI quality-of-life hooks](../appendix/runtime-patches/exchange-ui-quality-of-life.md).
