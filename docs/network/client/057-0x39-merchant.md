# Merchant (`CMerchant`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x39` (57) |
| Encoding | session key |
| Name provenance | Project-owner protocol name; merchant behavior confirmed by local RTTI |

## Purpose

The client sends this message for **merchant**.

The client protocol name is `CMerchant`, supplied by the project owner. Local behavior supports it: the send method occupies a slot in `MerchantDialogPane::TextMenuDialogEx`.

The client has no derived packet RTTI for `CMerchant` itself.

## Sent by

Known static callers lead to:

- `MerchantDialogPane::TextMenuDialogEx`

## Body

```text
packet CMerchant {
    u8 opcode                 // 0x39
    u8 menu_type
    u32be object_id
    u16be selection
}
```

The exact meanings of the menu type and selection values remain to be verified.
