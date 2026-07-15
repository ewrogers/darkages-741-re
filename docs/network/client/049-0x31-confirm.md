# Confirm (`CConfirm`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x31` (49) |
| Common transform | derived |
| Representative builder | `net_send_confirm` at `0x005922A0` |
| Name provenance | Project-owner protocol name, confirmed against `UserConfirmPane` |

## Current evidence

Both known calls come from `AlertPane::UserConfirmPane`. The body includes three control bytes and a length-prefixed value, but what the user is confirming remains unknown.

The client has no derived packet RTTI for this name.

## Known send sites

- `0x0059226C` in `sub_592260`, a `UserConfirmPane` virtual method.
- `0x0059228C` in `sub_592280`, a second `UserConfirmPane` virtual method.

## Plaintext body

```text
opcode:u8                 // 0x31
dialog_value_0:u8
choice:u8
dialog_value_1:u8
value_length:u8
value:u8[value_length]
```

The field roles and the confirmed operation require further investigation.
