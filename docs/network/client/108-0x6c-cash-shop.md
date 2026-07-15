# Cash Shop (`CCashShop`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x6C` (108) |
| Common transform | derived |
| Representative builder | `net_request_cash_shop` at `0x004A03B0` |
| Name provenance | Project-owner protocol name; local UI RTTI uses `ItemShop` |

## Current evidence

The builder sends the two-byte body `6C 00` while constructing `ItemShop::ShoppingBagDialogPane`. This exact local RTTI is why the first reconstruction used `CItemShop`. The project protocol name is `CCashShop`, which better distinguishes the real-money shop from ordinary in-game merchants.

Server opcode `0x45` has exact RTTI name `SItemShop`. Its relationship to this request is likely but still needs a handler trace.

## Known send sites

- `0x0049F7B4` in the `ItemShop::ShoppingBagDialogPane` constructor at `0x0049F450`.

## Plaintext body

```text
opcode:u8                 // 0x6C
reserved:u8               // 0
```
