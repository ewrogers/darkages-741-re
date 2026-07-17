# Change Password (`CChangePassword`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x26` (38) |
| Transform | `static` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The lobby client sends this request after the player enters an account name, the existing password, and a new password. The confirmation field is checked locally and is not sent.

## Sent by

`ChangePasswordDialogPane` owns the request. It loads `_npw.txt` and limits the three password controls to eight bytes.

## Body

```text
packet CChangePassword {
    u8      opcode                    // 0x26
    u8      name_length
    bytes   name[name_length]
    u8      existing_password_length
    bytes   existing_password[existing_password_length]
    u8      new_password_length
    bytes   new_password[new_password_length]
}
```

`net_send_change_password` writes all three lengths as `u8`. The common submission layer adds the transmitted trailing zero after the builder body.

Before calling the builder, `ui_change_password_submit` compares the new-password and confirmation controls. A mismatch clears both controls, focuses the new-password control, and displays localized client text without sending a request.

Distribution modes `1` and `15` use this direct request. Other distribution modes first open `InputBirthdateDialogPane` from `_npw2.txt` for an additional regional verification step.

The response is lobby opcode [`0x02`](../server/002-0x02-login-check.md). See [Changing a password](../../systems/change-password.md) for the complete UI flow.
