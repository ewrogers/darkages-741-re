# New User Appearance (`CNewUserAppearance`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x04` (4) |
| Common transform | static |
| Representative builder | `net_send_new_user_appearance` at `0x0043E8F0` |
| Name provenance | Project-owner protocol name, confirmed against the accepted character-creation path |

## Current evidence

After `SNewUserCheck` accepts opcode `0x02` character creation, `net_handle_new_user_check` reaches `0x0043E3E9` and calls this builder. The four-byte body finalizes creation with three appearance-related bytes read from the create-user dialog.

The client has no derived packet RTTI for this name.

## Known send sites

- `0x0043E3E9` in `sub_43E360`. This accepted-result path is called by `net_handle_new_user_check` at `0x0043F83A` and belongs to `CreateUserDialogPane`.

## Plaintext body

```text
opcode:u8                 // 0x04
appearance_value_0:u8
appearance_value_1:u8
appearance_value_2:u8
```

The exact meaning of the three appearance values remains to be named.
