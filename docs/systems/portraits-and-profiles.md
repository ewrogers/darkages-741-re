# Portraits and profiles

The game keeps each character's portrait and profile text in that character's local folder. The server asks for both with one empty packet. The client answers with one packet that contains the image bytes followed by the profile text.

```text
server                                  client
  |                                       |
  |  SRequestPortrait                     |
  |  opcode 0x49, no body                  |
  |-------------------------------------->|
  |                                       | find local portrait
  |                                       | read profile.txt
  |  CSendPortrait                        |
  |  opcode 0x4F, image + profile          |
  |<--------------------------------------|
```

`ui_user_info_handle_server_packet` receives the request. It calls `net_send_portrait_profile`, which asks `net_build_send_portrait` to build the response and submits it through the normal packet path.

## Local files

`file_build_character_path` places files under the current character directory:

```text
.\<character>\<file>
```

The portrait builder tries these names in order:

1. `<character>` with no extension
2. `<character>.jpg`
3. `<character>.epf`
4. The first `*.epf` returned from the character directory

There is no hardcoded `Face.epf` name. A file with that name works through the final wildcard step. Do not rely on that step when the folder contains several EPF files because directory enumeration order is not a useful file priority rule. Use `<character>.epf` for a predictable legacy portrait.

The bundled portrait helper contains `face.jpg` as its default output name. The client does not have a general `*.jpg` fallback, so that file must be placed or renamed to one of the names the client checks.

The profile is always named `profile.txt` in the same character folder.

## Album Save output

The current photo album Save action writes the first, extensionless portrait name in the list above. It copies any existing file to `<character>.bak`, composites transparent portrait pixels over `_nportbk.spf`, and overwrites the portrait with JFIF JPEG bytes. The older `AlbumViewPane` Save action reaches the same JPEG writer.

`file_write_jpeg_from_rgb16` uses the bundled IJG version 62 defaults. The effective quality is 75, and its YCbCr output uses 4:2:0 chroma sampling. There is no quality choice in the UI.

There is also no EPF or PCX branch in either album Save implementation. EPF support in this client is limited to loading, displaying, and uploading an already-created portrait-sized EPF. Because the extensionless JPEG has first priority, remove or rename it before expecting `<character>.epf` to be selected.

The capture cooldown, album panes, and exact save and remove flow are documented in [Screenshots and the photo album](screenshots-and-photo-album.md).

## Accepted portraits

The response carries the complete source file without converting it.

JPEG portraits must contain `JFIF` at file offset 6 and be smaller than 8,000 bytes. The local display decoder also expects an image 48 pixels wide and 56 pixels high. That is therefore the safe size to create.

The legacy EPF path is stricter:

- Total file size is exactly `0xB1C` bytes.
- The little-endian table displacement at file offset 8 is `0xAF0`.
- The first frame bounds describe a portrait 48 pixels wide and 56 pixels high.

These checks describe a portrait-sized EPF profile. See [EPF images](../file-formats/epf.md) for the general container.

If no candidate passes its checks, the client still sends the packet with a zero portrait length. Profile text may still be present.

## Display palette

The legacy portrait EPF stores palette indexes. `file_decode_portrait_image` marks it with palette selector 0, and the drawing path resolves that selector through `legend.pal`. This is the `.pal` file to use when converting a portrait EPF outside the client.

JPEG portraits do not use a `.pal` file. The JPEG decoder produces display pixels directly.

## Legend and profile dialogs

The legacy RTTI class `LegendDialogPane` loads `llegends.txt`. It combines a title with an eight-image list control and parses the server's counted legend entries.

`NewLegendDialogPane` loads `llegend2.txt`. It adds a `PortraitControlPane`, profile text, and an optional Change action. The constructor supports read-only and editable forms. Its packet handler decodes the nested portrait/profile body, reloads the profile text, enables Change when editing is allowed, and either renders or clears the portrait control.

Both dialogs parse the counted legend list independently of the portrait and profile fields.

## Profile text

The client reads at most 370 bytes from `profile.txt`. `ui_text_truncate_dbcs_safe` makes sure the byte limit does not split a Windows double-byte character. There is no Unicode conversion in the packet builder. The stored local text bytes are copied to the packet.

The profile editor is `PortraitTextInputDialogPane`. It loads `_nui_pi.txt`, reads `profile.txt`, and saves it when the user chooses OK. A separate `NewLegendDialogPane` save path normalizes carriage returns to line feeds and ends the text when it reaches a fifth line break.

Saving changes the local file and refreshes the local `UserInfoPane` preview through timer `0x1241`. It does not immediately submit `CSendPortrait`. The next `SRequestPortrait` causes the network upload.

Profile text may contain the client's inline color codes. The packet keeps those bytes unchanged. `UserInfoPane` later inserts the profile through the formatted text path, where the codes are interpreted. See [Text color markup](text-color-markup.md).

## Response body

```text
packet CSendPortrait {
    u8    opcode            // 0x4F
    u16be content_length    // 4 + portrait_length + profile_length
    u16be portrait_length
    u8    portrait[portrait_length]
    u16be profile_length
    u8    profile[profile_length]
}
```

`content_length` counts both nested `u16be` length fields and both byte strings. It does not count the opcode or its own two bytes. The full plaintext packet size is `7 + portrait_length + profile_length`.

The image and profile fields are independent. Either length may be zero.

## Known limits

- The client-side checks do not prove which additional rules the server applies.
- JPEG EXIF data without a JFIF marker does not enter the JPEG path.
- The builder accepts a small JFIF file before checking its dimensions. The local decoder still requires 48 pixels wide by 56 pixels high.
- The profile is a byte string. Its displayed language depends on the text's encoding and the Windows environment.
