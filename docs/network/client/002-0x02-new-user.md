# New User (`CNewUser`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x02` (2) |
| Encoding | startup key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **new user**.

## Sent by

Known static callers lead to:

- `TimerHandler::CreateUserDialogPane`

## Body

```text
packet CNewUser {
    u8 opcode                 // 0x02
    ...                         // fields pending
}
```

Remaining fields, variants, and state effects remain to be traced.

The paired response is [New User Check (`SNewUserCheck`)](../server/001-0x01-new-user-check.md).
