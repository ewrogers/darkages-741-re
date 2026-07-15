# Login Check (`SLoginCheck`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x02` (2) |
| Common transform | static |
| Registered server packet class | None found |
| Dispatcher | `net_dispatch_main_menu_events` at `0x004B8B70` |
| Handler | `net_handle_login_check` at `0x004B8420` |
| Internal name provenance | Project-owner protocol knowledge, confirmed by the local login-result behavior |

## Current evidence

The RTTI-backed `MainMenuPane` owns the dispatcher. At `0x004B8C00` it compares the decoded body opcode with `0x02` and routes the byte buffer directly. This authentication response is consumed before the gameplay packet factory is active.

## Plaintext body

```text
opcode:u8
status:u8

if status != 0:
    message_length:u8
    message:bytes[message_length]
```

Status `0` enters the game-session setup path. A nonzero status displays the body-provided message. Individual failure-code meanings remain unknown.

The paired request is [Login (`CLogin`)](../client/003-0x03-login.md).
