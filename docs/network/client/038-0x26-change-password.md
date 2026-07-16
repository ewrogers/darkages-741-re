# Change Password (`CChangePassword`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x26` (38) |
| Encoding | startup key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **change password**.

## Sent by

Known static callers lead to:

- `DialogPane::ChangePasswordDialogPane`

## Body

```text
packet CChangePassword {
    u8 opcode                 // 0x26
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
