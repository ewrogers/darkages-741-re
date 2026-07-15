# Pursuit (`CMessage`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x3A` (58) |
| Common transform | static |
| Representative builder | `net_send_message_selection` at `0x004DBC90` |
| Behavioral alias | `CPursuit` |
| Name provenance | Project-owner protocol name; message behavior confirmed by local RTTI |

## Current evidence

The exact client protocol name is `CMessage`. The descriptive `CPursuit` alias came from related behavior, while the strongest local owner evidence is the `MessageDialogBase::MessageDialog` and `MessageDialog::SimpleMessageDialog` RTTI.

The client has no derived packet RTTI for `CMessage` itself.

## Known send sites

- `0x004DBC90` is referenced by the `MessageDialogBase::MessageDialog` vtable at `0x0067B0AC`.
- The same method is referenced by the `MessageDialog::SimpleMessageDialog` vtable at `0x0067B14C`.

## Plaintext body

```text
opcode:u8                 // 0x3A
message_type:u8
object_id:u32be
menu_value:u16be
selection:u16be
```

The relationship between the generic message fields and pursuit behavior remains to be traced.
