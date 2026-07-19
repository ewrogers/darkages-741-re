# Cash Shop (`CCashShop`)

`CCashShop` requests the contents of the in-client cash-shop shopping bag or retrieves one selected bag record.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x6C` |
| Transform | `derived` |
| Name provenance | Project-owner protocol name; the local UI uses exact RTTI namespace `ItemShop` |
| UI owner | Exact RTTI `ItemShop::ShoppingBagDialogPane` |

## Body

```text
packet CCashShop {
    u8 opcode                    // 0x6C
    u8 action

    if action == 1 {
        u8 record_type
        u32 record_id
    }
}
```

| Action | Trigger | Total body length |
| ---: | --- | ---: |
| `0` | `ShoppingBagDialogPane` construction | 2 |
| `1` | Get the selected `SItemShop` record | 7 |

The action-1 values are copied from the selected server record. The client does not locally interpret `record_type` beyond sending it back with `record_id`.

## UI and opening behavior

`ItemShop::ShoppingBagDialogPane` loads `lshopba2.txt`. It contains a 5 by 6 icon grid, a description control, page indicator, Previous, Next, Get, and Close. Its constructor immediately sends action `0`. [`SItemShop`](../server/069-0x45-item-shop.md) only updates this pane when it already exists; it does not open the pane.

Neither `ShoppingBagDialogPane` nor the separate embedded-browser `ItemShop::ShopDialogPane` constructor has a static caller in this client. That makes the in-client shop path dormant or dependent on an unresolved external callback in this build.

There is a separate reachable shop path: pursuit type `9` can open `NPC_Pursuit_NexonIdDialog`, whose secondary action launches the configured item-shop URL with `ShellExecuteA`. That external-browser path does not send `CCashShop` and does not consume `SItemShop`.
