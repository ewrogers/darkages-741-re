# Login Check (`SLoginCheck`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x02` (2) |
| Encoding | startup key |
| Packet class | None found |
| Internal name provenance | Project-owner protocol knowledge, confirmed by the local login-result behavior |

## Purpose

The server sends this message for **login check**.

`MainMenuPane` compares the decoded command with `0x02` and routes the body directly. This login response is handled before the gameplay packet factory is active.

## Body

```text
packet SLoginCheck {
    u8 opcode                 // 0x02
    u8 status

    if status != 0:
        u8 message_length
        bytes message[message_length]
}
```

Status `0` enters the game-session setup path. A nonzero status displays the body-provided message. Individual failure-code meanings remain unknown.

The paired request is [Login (`CLogin`)](../client/003-0x03-login.md).
