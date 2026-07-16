# Login or New User Check (`SLoginCheck` / `SNewUserCheck`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x02` (2) |
| Transform | `static` |
| Packet class | None found |
| Internal name provenance | Project-owner protocol knowledge, confirmed by the local login and creation-result behavior |

## Purpose

Opcode `0x02` is a lobby result whose meaning depends on the active UI. `MainMenuPane` handles it as `SLoginCheck`; `CreateUserDialogPane` handles it as `SNewUserCheck`.

Both panes route the decoded body directly, without constructing an RTTI packet object. The supplied live captures confirm that the lobby uses this opcode for both stages of character creation.

## Body

```c
struct LobbyResultBody {
    u8 opcode;                 // 0x02
    u8 status;

    // Present on login failures and first-stage creation errors.
    // A creation-completion response may also supply it, but the
    // client ignores that stage's bytes after status.
    u8 message_length;
    u8 message[message_length];
}
```

## Login context

Status `0` enters game-session setup. A nonzero status copies the declared message bytes, terminates the local copy, and displays them. Individual login failure-code meanings remain unknown.

## Character-creation context

The pane tracks whether it is waiting for account validation or appearance completion.

| Stage and status | Client behavior |
| --- | --- |
| Validation `0` | Send [`CNewUserAppearance`](../client/004-0x04-new-user-appearance.md) and enter completion stage |
| Validation `3` | Invalid name in the supplied capture; clear and focus name |
| Validation `4` | Taken or reserved name in the supplied captures; clear and focus name |
| Validation `5` | Invalid password length in the supplied capture; clear both password fields and focus the first |
| Validation `6` through `10` | Same password-field reset; exact meanings unknown |
| Validation `11` | Display message without those field resets |
| Completion `0` | Display localized client success text, close the creation pane, and return to the main menu |
| Completion nonzero | Consume the result without the validation-stage field resets |

The message length excludes the trailing zero seen in the supplied responses. The validation handler reads only the declared message. The completion handler reads only the status, so the server-supplied success message is not used.

The paired requests are [Login (`CLogin`)](../client/003-0x03-login.md), [New User (`CNewUser`)](../client/002-0x02-new-user.md), and [New User Appearance (`CNewUserAppearance`)](../client/004-0x04-new-user-appearance.md). See [Character creation](../../systems/character-creation.md) for the complete flow.
