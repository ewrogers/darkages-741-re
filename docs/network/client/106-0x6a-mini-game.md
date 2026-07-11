# 106 / 0x6a: Mini Game (`CMiniGame`)

- Direction: client to server
- Internal name: `CMiniGame`
- Local behavioral alias: `MiniGame`
- Related-game enum name: `MiniGame`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 4 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x50c600`
- `0x50c670`
- `0x50c890`
- `0x5ef850`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x6A`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
