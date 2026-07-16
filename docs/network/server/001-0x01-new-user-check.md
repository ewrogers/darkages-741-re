# New User Check Alias (`SNewUserCheck`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x01` (1) |
| Transform | `static` |
| Packet class | None found |
| Internal name provenance | Project-owner protocol knowledge, supported by the local create-user handler |

## Purpose

This is a compiled alias for the character-creation result. The live lobby captures use opcode `0x02`, but `CreateUserDialogPane` explicitly accepts opcode `0x01` and routes it through the same two stage handlers.

The body is handled directly as a decoded byte buffer. There is no concrete RTTI packet class.

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

During validation, status `0` sends `CNewUserAppearance`. Statuses `3` and `4` clear and focus the name field, while statuses `5` through `10` clear both password fields and focus the first. Status `11` displays its message without either reset.

The live opcode and full state-dependent behavior are documented on [Login or New User Check](002-0x02-login-check.md) and [Character creation](../../systems/character-creation.md).
