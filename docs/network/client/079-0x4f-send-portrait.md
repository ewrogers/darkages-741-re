# Send Portrait (`CSendPortrait`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x4F` (79) |
| Encoding | session key |
| Name provenance | Verified project protocol name, matched to the local portrait builder. |

## Purpose

The client sends its local portrait and profile text after the server asks for them with `SRequestPortrait`.

`net_send_portrait_profile` calls `net_build_send_portrait`, then submits the completed buffer through the normal client packet path.

## Sent by

Known static callers lead to:

- `UserInfoPane::UserInfoPane_ForUser`

`ui_user_info_handle_server_packet` is the confirmed sender. Its `0x49` branch answers the request immediately. Saving the local profile only refreshes the local preview. It does not send this packet on its own.

## Body

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

The full plaintext packet size is `7 + portrait_length + profile_length`. The portrait is a complete JFIF JPEG or portrait-sized EPF file. The profile is at most 370 local text bytes. Either nested length may be zero.

The packet uses the derived session transform. Its encrypted sequence advances through the normal client send path.

See [Portraits and profiles](../../systems/portraits-and-profiles.md) for local filenames, image checks, profile editing, and format limits.
