# 079 / 0x4f: Send Portrait (`CSendPortrait?`)

- Direction: client to server
- Internal name: `CSendPortrait?`
- Local behavioral alias: `SendPortrait / UserPortrait`
- Related-game enum name: `SendPortrait`
- Name provenance: Related-game internal enum name `SendPortrait` at the same opcode is corroborated by this client's JPEG/EPF and `profile.txt` upload builder; the C++ class spelling remains reconstructed.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x5b1160` : `net_send_c_portrait`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x4F`.
- Tentative semantic identification: profile/portrait upload.
- The recovered builder can include JPEG or legacy EPF portrait bytes and the contents of `profile.txt`.
