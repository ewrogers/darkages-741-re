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
    string8 name
    string8 existing_password
    string8 new_password
    if distribution_mode != 1 && distribution_mode != 15 {
        u32 birthdate
    }
}
```

`net_send_change_password` writes the direct three-string form. `net_send_change_password_with_birthdate` writes the same strings and appends the birthdate text parsed as a decimal `u32`. The common submission layer adds the transmitted trailing zero after either builder body.

Before calling the builder, `ui_change_password_submit` compares the new-password and confirmation controls. A mismatch clears both controls, focuses the new-password control, and displays localized client text without sending a request.

Distribution modes `1` and `15` use the direct request. Other distribution modes first open `InputBirthdateDialogPane` from `_npw2.txt`. Its submit path copies at most 15 input bytes, parses them as a decimal number, and uses the birthdate-bearing request variant.

The response is lobby opcode [`0x02`](../server/002-0x02-login-check.md). See [Changing a password](../../systems/change-password.md) for the complete UI flow.
