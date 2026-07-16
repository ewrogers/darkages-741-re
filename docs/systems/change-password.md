# Changing a password

Password changes happen on the lobby server, before the client enters the game world. The client collects the account name and passwords, checks the confirmation locally, and lets the server validate the existing password and the new-password rules.

## Dialog controls

`ChangePasswordDialogPane` loads `_npw.txt`. Controls are attached in this order, which also supplies their action and focus indexes:

| Index | Layout name | Role |
| --- | --- | --- |
| `0` | `OK` | Submit |
| `1` | `Cancel` | Close the pane |
| `2` | `Name` | Account name |
| `3` | `Password` | Existing password |
| `4` | `NewPassword` | Requested password |
| `5` | `Confirm` | Local confirmation |

The three password controls accept at most eight bytes. The dialog initially focuses the name control.

## Submitting the form

The submit path first compares `NewPassword` with `Confirm`. If they differ, the client clears both controls, focuses `NewPassword`, and displays a localized message. Nothing is sent.

When they match, [`CChangePassword`](../network/client/038-0x26-change-password.md) carries three `u8`-length strings:

```text
name
existing password
new password
```

The confirmation value never leaves the client.

Distribution modes `1` and `15` send this request directly. Other distribution modes open `InputBirthdateDialogPane` from `_npw2.txt` before continuing. The direct three-string form is the variant confirmed by the supplied live captures.

## Handling the result

The lobby answers with state-dependent opcode [`0x02`](../network/server/002-0x02-login-check.md). `net_dispatch_change_password_events` routes it to `net_handle_change_password_result` while this pane is active.

| Status | Client response |
| --- | --- |
| `0` | Show localized client success text and close the pane |
| `0x0F` | Clear and focus the existing-password field; show the server message |
| Other nonzero | Clear new password and confirmation, focus new password, and show the server message |

Status `5` was observed for a new password that failed the server's length rule. Status `0x0F` was observed for an incorrect existing password.

The success handler reads only the status. Although the observed success response includes text, the client ignores it and obtains the displayed success message from its local string resources. Error handlers read the declared message bytes and terminate their local copy themselves.
