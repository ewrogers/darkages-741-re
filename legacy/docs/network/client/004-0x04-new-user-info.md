# 004 / 0x04: New User Info (`CNewUserInfo`)

- Direction: client to server
- Internal name: `CNewUserInfo`
- Local behavioral alias: `CreateCharacterAppearance`
- Related-game enum name: `Login`
- Name provenance: Leaked company/engine class name remapped by this client's local behavior; the sibling-game opcode differs.
- Evidence: 1 concrete builder/sender call site
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x43e8f0`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x04`.
- This client's builder/caller behavior identifies `0x04` as new-character appearance/info, despite the related-game enum using `Login` here.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
