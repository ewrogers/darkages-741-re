# Confirm (`CConfirm`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x31` (49) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed against `UserConfirmPane` |

## Purpose

The client sends this message for **confirm**.

Both known calls come from `AlertPane::UserConfirmPane`. The body includes three control bytes and a length-prefixed value, but what the user is confirming remains unknown.

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CConfirm {
    u8 opcode                 // 0x31
    u8 dialog_value_0
    u8 choice
    u8 dialog_value_1
    u8 value_length
    u8 value[value_length]
}
```

The field roles and the confirmed operation require further investigation.
