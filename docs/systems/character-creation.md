# Character creation

Character creation happens on the lobby connection before the client enters the game world. The client first asks the server to validate the name, password, and account text. If that succeeds, it automatically sends the appearance already selected in the preview.

```text
fill in the form and choose an appearance
  -> CNewUser validates the account fields
  -> SNewUserCheck returns the first result
  -> CNewUserAppearance submits the selected appearance
  -> SNewUserCheck returns the completion result
  -> close the creation pane and return to the main menu
```

The RTTI-backed owner is `CreateUserDialogPane`. It loads `_ncreate.txt`, builds the form controls, draws the character preview, and handles both server replies as decoded byte buffers. There is no concrete RTTI packet class for either reply.

## Lobby context

The bootstrap connection selects an endpoint and transfers the client to the lobby. This second connection owns the main create-or-login screen, stipulation check, homepage URL, account creation, login, password changes, and the later transfer into a game server.

Opcode `0x02` is state-dependent on this connection. `MainMenuPane` reads it as `SLoginCheck`, while `CreateUserDialogPane` reads it as `SNewUserCheck`. The creation pane also accepts opcode `0x01` as a compiled alias, but the supplied live captures use `0x02` for both creation stages.

The pane is process-local singleton state. Its constructor registers the complete object, its destructor clears the slot, and small `get` and `exists` helpers let the main menu and shutdown paths avoid opening or destroying a second copy.

A nearby compiler-split fragment can construct server message dialog variants 0 through 5 and store the shared message-dialog pointer. Binary Ninja recovers no incoming control-flow edge to that fragment, so it remains a medium-confidence dormant or split path rather than established live character-creation behavior.

## Form submission

The form contains separate name, password, and password-confirmation controls. The confirmation is checked locally and is not sent. A mismatch clears both password controls, focuses the first password control, and displays a localized client message.

The submit button is enabled only when the required name and password fields are nonempty. Distribution-specific paired account fields must either both be empty or both contain text. Password and other sensitive fields explicitly enable the text control's masked-input mode.

The active USA distribution does not show an email field. It sends the literal text `none` in the third length-prefixed field. Dormant [distribution branches](../application/distribution-markers.md) can use this field for an email address or NexonClub account text. Japan mode 13 also appends a two-byte ISP selector to the request.

After local validation, the pane waits 200 milliseconds and sends [`CNewUser`](../network/client/002-0x02-new-user.md):

```c
packet CNewUser {
    u8 opcode;                 // 0x02
    u8 name_length;
    u8 name[name_length];
    u8 password_length;
    u8 password[password_length];
    u8 account_text_length;
    u8 account_text[account_text_length];

    // Japan distribution mode 13 only
    u16be isp_selector;
}
```

The ordinary client submission path adds its common zero byte after this logical body.

## Validation result

The first [`SNewUserCheck`](../network/server/002-0x02-login-check.md) response begins with a status byte. Error responses then carry a one-byte message length and exactly that many message bytes. The trailing zero seen after the messages is not included in the declared length, and the handler does not read it.

| Status | Observed result |
| --- | --- |
| `0` | Send `CNewUserAppearance` and wait for the completion result |
| `3` | Clear and focus the name field; display the server message |
| `4` | Clear and focus the name field; display the server message |
| `5` | Clear both password fields, focus the first, and display the server message |
| `6` through `10` | Same password-field handling as status `5`; exact meanings are not known |
| `11` | Display the server message without clearing those fields |

The supplied captures identify status `3` as an invalid name, status `4` as a taken or reserved name, and status `5` as an invalid password length.

## Appearance submission

A successful validation response immediately calls `net_send_new_user_appearance`:

```c
packet CNewUserAppearance {
    u8 opcode;                 // 0x04
    u8 hair_style;
    u8 gender;                 // 1 male, 2 female
    u8 hair_color;
}
```

Male styles range from `1` through `18`; female styles range from `1` through `17`. The preview starts with a time-based random gender and style, so the visible initial selection is not necessarily style `1`.

While the pane is open, its preview timer advances a five-frame animation and invalidates only the preview rectangle.

The observed body `04 09 01 01` therefore means hair style `9`, male, hair color `1`. The client passes the first value directly to its character renderer as the hair-style ID.

Hair color is a palette index from `0` through `13`. The 2-by-7 swatch grid presents those indexes in this order:

```text
5, 9, 8, 4, 10, 2, 7,
0, 13, 6, 12, 3, 11, 1
```

This confirms that the wire field is a palette index rather than the swatch position. The creation code alone does not yet prove that every item-dye interface uses the same table.

One dormant NexonClub branch displays exact RTTI `NoNexonClubIDWarningPane` when the optional account identifier is missing. Its confirm and cancel hooks schedule configured owner timers after 200 ms. In the observed construction, confirm selects the normal delayed creation path and cancel has no timer.

## Completion result

When the second result has status `0`, the client displays its own localized success text, closes `CreateUserDialogPane`, and returns to the main menu. The live server also supplies a length-prefixed success message, but this second-stage handler ignores everything after the status byte.

A nonzero second-stage status is consumed without the first-stage field-reset behavior. Its server-side meanings remain unknown.

## Useful object fields

These fields explain how the UI state becomes the two client packets:

```c
struct CreateUserDialogPane {
    // Pane and DialogPane fields come first.
    s16 gender_index;          // +0x674: 0 male, 1 female
    s16 hair_style;            // +0x676
    s16 hair_color;            // +0x678: palette index 0..13
    s32 creation_stage;        // +0x684: 1 validation, 2 completion
    char name[16];             // +0x6A0
    char password[16];         // +0x6B0
    char password_confirm[16]; // +0x6C0, local only
    char account_text[64];     // +0x6F0
};
```
