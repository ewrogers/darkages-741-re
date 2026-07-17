# Cash Shop (`CCashShop`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x6C` (108) |
| Encoding | session key |
| Name provenance | Project-owner protocol name; local UI RTTI uses `ItemShop` |

## Purpose

The client sends this message for **cash shop**.

The builder sends the two-byte body `6C 00` while constructing `ItemShop::ShoppingBagDialogPane`. This exact local RTTI is why the first reconstruction used `CItemShop`. The project protocol name is `CCashShop`, which better distinguishes the real-money shop from ordinary in-game merchants.

Server opcode `0x45` has exact RTTI name `SItemShop`. Its relationship to this request is likely but still needs a handler trace.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CCashShop {
    u8      opcode                    // 0x6C
    u8      reserved                  // 0
}
```
