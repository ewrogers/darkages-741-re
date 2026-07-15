# New User Check (`SNewUserCheck`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x01` (1) |
| Common transform | static |
| Registered server packet class | None found |
| Dispatcher | `net_dispatch_create_user_events` at `0x0043F780` |
| Handler | `net_handle_new_user_check` at `0x0043F820` |
| Internal name provenance | Project-owner protocol knowledge, supported by the local create-user handler |

## Current evidence

The RTTI-backed `CreateUserDialogPane` owns the dispatcher. At `0x0043F7DC` it compares the decoded body opcode with `0x01` and routes the byte buffer directly. This response belongs to the account-creation UI, so it bypasses the gameplay packet factory.

## Plaintext body

```text
opcode:u8
status:u8

if status in 3..11:
    message_length:u8
    message:bytes[message_length]
```

Status `0` advances the creation process. Error handling is state-dependent. The parser at `0x0043E360` displays the body-provided message for statuses `3` through `11`; another creation stage uses localized status text. The exact meaning of each status value remains pending.

The paired request is [New User (`CNewUser`)](../client/002-0x02-new-user.md).
