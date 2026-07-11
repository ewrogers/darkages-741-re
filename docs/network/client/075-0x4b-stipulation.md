# 075 / 0x4b: Stipulation (`CStipulation`)

- Direction: client to server
- Internal name: `CStipulation`
- Local behavioral alias: `RequestLoginNotice`
- Related-game enum name: `Stipulation`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 2 concrete builder/sender call sites
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4b8570`
- `0x4b8890`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x4B`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
