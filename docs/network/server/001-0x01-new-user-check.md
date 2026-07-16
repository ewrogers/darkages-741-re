# New User Check (`SNewUserCheck`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x01` (1) |
| Encoding | startup key |
| Packet class | None found |
| Internal name provenance | Project-owner protocol knowledge, supported by the local create-user handler |

## Purpose

The server sends this message for **new user check**.

`CreateUserDialogPane` compares the decoded command with `0x01` and routes the body directly. This response belongs to the character-creation UI, so it bypasses the gameplay packet factory.

## Body

```text
packet SNewUserCheck {
    u8 opcode                 // 0x01
    u8 status

    if status in 3..11:
        u8 message_length
        bytes message[message_length]
}
```

Status `0` advances the creation process. Error handling is state-dependent. The parser displays the body-provided message for statuses `3` through `11`; another creation stage uses localized status text. The exact meaning of each status value remains pending.

The paired request is [New User (`CNewUser`)](../client/002-0x02-new-user.md).
