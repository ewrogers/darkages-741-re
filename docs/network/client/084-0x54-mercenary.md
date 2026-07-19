# Mercenary (`CMercenary`)

`CMercenary` controls an employee shop after the server opens `EmployeeDialogPane`. It can add, withdraw, reprice, or remove an employee item, fire the employee, or request the current shop information.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x54` |
| Transform | `derived` |
| Name provenance | Project-owner protocol name, supported by `EmployeeDialogPane` behavior |
| UI owner | Exact RTTI `EmployeeDialogPane` |

## What causes it to be sent

The opening trigger is [`SMercenary`](../server/079-0x4f-mercenary.md), not a preceding `CMercenary` request. Its Open message constructs `EmployeeDialogPane` from `lshop0.txt`. The constructor immediately sends action `5`, RequestInfo.

Later forms come from the employee pane and its item, quantity, and confirmation dialogs.

## Body

```text
packet CMercenary {
    u8 opcode                    // 0x54
    u8 category                  // always 1
    u32 employee_id
    u8 action

    if action == 0 {
        u8 inventory_slot
        u32 quantity
    }

    if action == 1 {
        u32 item_id
        u32 quantity
        u16 unknown_1            // normal UI sends 0
        u16 unknown_2            // normal UI sends 0
    }

    if action == 2 {
        u32 item_id
        u32 sell_price
        u32 buy_price
    }

    if action == 3 {
        u32 item_id
    }
}
```

Actions `4` and `5` end after the common header.

| Action | Executable debug name | Total body length | Behavior |
| ---: | --- | ---: | --- |
| `0` | `SendAddItem` | 12 | Add inventory quantity to the employee shop |
| `1` | `SendWithdrawItem` | 19 | Withdraw quantity from one employee item |
| `2` | `SendApplyPrice` | 19 | Apply the two price values to one employee item |
| `3` | `SendRemoveItem` | 11 | Remove an employee item by ID |
| `4` | `SendFire` | 7 | Fire the employee |
| `5` | `SendRequestInfo` | 7 | Request or refresh employee information |

The action names are embedded client debug strings. The two action-1 words remain unnamed because the reachable UI supplies zero for both.

## UI

`EmployeeDialogPane` draws the employee title, held money, capacity status, and ten visible item buttons. It also attaches OK, Dismiss, and WithdrawMoney controls. Item dialogs expose quantity and price operations, then queue the matching action through the pane's `TimerHandler` callback.
