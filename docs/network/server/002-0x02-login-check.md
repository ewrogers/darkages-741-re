# Lobby Account Result (`SLoginCheck` / `SNewUserCheck`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x02` (2) |
| Transform | `static` |
| Packet class | None found |
| Internal name provenance | Project-owner login and creation names; password-change use confirmed by its pane handler |

## Purpose

Opcode `0x02` is a lobby result whose meaning depends on the active UI. `MainMenuPane` handles it as `SLoginCheck`, `CreateUserDialogPane` handles it as `SNewUserCheck`, and `ChangePasswordDialogPane` handles it as the result of `CChangePassword`.

These panes route the decoded body directly, without constructing an RTTI packet object. Supplied live captures confirm its character-creation and password-change uses.

## Body

```c
struct LobbyResultBody {
    u8 opcode;                 // 0x02
    u8 status;

    // Present on login failures, first-stage creation errors,
    // and password-change responses.
    // A creation-completion response may also supply it, but the
    // client ignores that stage's bytes after status.
    u8 message_length;
    u8 message[message_length];
}
```

## Login context

Status `0` enters game-session setup. A nonzero status copies the declared message bytes, terminates the local copy, and displays them. Individual login failure-code meanings remain unknown.

### Pre-login hello timeout

The live server also uses status `0x1E` before normal lobby exchange when it does not receive the client's reply to [`SHello`](126-0x7e-hello.md) within about five seconds. The observed body declares the 65-byte message `You have been idle for too long. Your connection has been closed.`, followed by a zero byte, and the server then disconnects.

This result uses the compiled startup key because `SVersionCheck` has not yet supplied a replacement. Whether the message becomes visible depends on how far the client progressed through its initial raw-stream transition before failing to reply.

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

## Password-change context

`ChangePasswordDialogPane` uses the same raw body with these state-specific rules:

| Status | Observed meaning | Client behavior |
| --- | --- | --- |
| `0` | Success | Display localized client success text, close the password-change pane, and ignore the remaining server body |
| `5` | Invalid new-password length | Clear new password and confirmation, display the declared server message, and focus new password |
| `0x0F` | Incorrect existing password | Clear the existing-password field, display the declared server message, and focus that field |
| Other nonzero | Unresolved password-change error | Clear new password and confirmation, display the declared server message, and focus new password |

Error handling copies exactly `message_length` bytes and adds a local terminator. A wire terminator after the declared text is not required by this handler.

The paired requests are [Login (`CLogin`)](../client/003-0x03-login.md), [New User (`CNewUser`)](../client/002-0x02-new-user.md), [New User Appearance (`CNewUserAppearance`)](../client/004-0x04-new-user-appearance.md), and [Change Password (`CChangePassword`)](../client/038-0x26-change-password.md). See [Character creation](../../systems/character-creation.md) and [Changing a password](../../systems/change-password.md) for the complete UI flows.
