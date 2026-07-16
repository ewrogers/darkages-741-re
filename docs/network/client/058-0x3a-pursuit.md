# Pursuit (`CPursuit`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x3A` (58) |
| Encoding | startup key |
| Name provenance | Project-owner protocol name; pursuit flow supported by local dialog RTTI |

## Purpose

The client sends this message for **pursuit**.

The client protocol name is `CPursuit`, supplied by the project owner. Local behavior supports it through the `MessageDialogBase::MessageDialog` and `MessageDialog::SimpleMessageDialog` selection paths.

The client has no derived packet RTTI for `CPursuit` itself.

## Sent by

Known static callers lead to:

- `MessageDialogBase::MessageDialog`
- `MessageDialog::SimpleMessageDialog`

## Body

```text
packet CPursuit {
    u8 opcode                 // 0x3A
    u8 message_type
    u32be object_id
    u16be menu_value
    u16be selection
}
```

The exact meaning of each pursuit selection value remains to be traced.
