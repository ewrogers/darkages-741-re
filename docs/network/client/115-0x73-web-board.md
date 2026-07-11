# 115 / 0x73: Web Board (`CWebBoard`)

- Direction: client to server
- Internal name: `CWebBoard`
- Local behavioral alias: `WebBoard`
- Related-game enum name: `WebBoard`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 2 concrete builder/sender call sites
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4160a0`
- `0x50c7c0`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x73`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
