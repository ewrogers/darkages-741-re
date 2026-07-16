# New User Appearance (`CNewUserAppearance`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x04` (4) |
| Transform | `static` |
| Name provenance | Project-owner protocol name, confirmed against the accepted character-creation path |

## Purpose

This packet finalizes character creation with the appearance already selected in `CreateUserDialogPane`.

After the first `SNewUserCheck` returns status `0`, `net_handle_new_user_validation_result` calls `net_send_new_user_appearance`. The pane then waits for a second result before closing.

The client has no derived packet RTTI for this name.

## Sent by

- `CreateUserDialogPane`

## Body

```c
packet CNewUserAppearance {
    u8 opcode;                 // 0x04
    u8 hair_style;             // male 1..18, female 1..17
    u8 gender;                 // 1 male, 2 female
    u8 hair_color;             // palette index 0..13
}
```

The captured body `04 09 01 01` selects hair style `9`, male, and hair color `1`. The client stores gender internally as `0` or `1` and adds one for the wire value.

The hair-color swatch grid maps its 14 positions to palette indexes rather than sending the clicked position directly. The full mapping and response behavior are in [Character creation](../../systems/character-creation.md).

The ordinary submission path adds a fifth plaintext byte, `0x00`, before applying the static transform.
