# Pursuit (`CMessage`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x3A` (58) |
| Encoding | startup key |
| Behavioral alias | `CPursuit` |
| Name provenance | Project-owner protocol name; message behavior confirmed by local RTTI |

## Purpose

The client sends this message for **pursuit**.

The exact client protocol name is `CMessage`. The descriptive `CPursuit` alias came from related behavior, while the strongest local owner evidence is the `MessageDialogBase::MessageDialog` and `MessageDialog::SimpleMessageDialog` RTTI.

The client has no derived packet RTTI for `CMessage` itself.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CMessage {
    u8 opcode                 // 0x3A
    u8 message_type
    u32be object_id
    u16be menu_value
    u16be selection
}
```

The relationship between the generic message fields and pursuit behavior remains to be traced.
