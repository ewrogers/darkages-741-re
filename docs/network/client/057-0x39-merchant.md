# Merchant (`CMenuCode`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x39` (57) |
| Common transform | derived |
| Representative builder | `net_send_merchant_menu_code` at `0x004CFE60` |
| Behavioral alias | `CMerchant` |
| Name provenance | Project-owner protocol name; merchant behavior confirmed by local RTTI |

## Current evidence

The exact client protocol name is `CMenuCode`. The descriptive `CMerchant` alias came from direct local evidence: the send method occupies a slot in `MerchantDialogPane::TextMenuDialogEx` at `0x00679DEC`.

The client has no derived packet RTTI for `CMenuCode` itself.

## Known send sites

- `0x004CFE60` is the virtual send method referenced by the `MerchantDialogPane::TextMenuDialogEx` vtable at `0x00679DEC`.

## Plaintext body

```text
opcode:u8                 // 0x39
menu_type:u8
object_id:u32be
selection:u16be
```

The exact meanings of the menu type and selection values remain to be verified.
