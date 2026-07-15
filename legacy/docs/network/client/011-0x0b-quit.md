# 011 / 0x0b: Quit (`CQuit`)

- Direction: client to server
- Internal name: `CQuit`
- Local behavioral alias: `RequestExit`
- Related-game enum name: `Quit`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 3 concrete builder/sender call sites
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4b79c0`
- `0x544100`
- `0x544280`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x0B`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
