# Merchant (`CMenuCode`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x39` (57) |
| Encoding | session key |
| Behavioral alias | `CMerchant` |
| Name provenance | Project-owner protocol name; merchant behavior confirmed by local RTTI |

## Purpose

The client sends this message for **merchant**.

The exact client protocol name is `CMenuCode`. The descriptive `CMerchant` alias came from direct local evidence: the send method occupies a slot in `MerchantDialogPane::TextMenuDialogEx`.

The client has no derived packet RTTI for `CMenuCode` itself.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CMenuCode {
    u8 opcode                 // 0x39
    u8 menu_type
    u32be object_id
    u16be selection
}
```

The exact meanings of the menu type and selection values remain to be verified.
