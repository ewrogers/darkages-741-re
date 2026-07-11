# 045 / 0x2d: CSelfLookPacket

- Direction: client to server
- Internal packet name: `CSelfLookPacket`
- Local behavioral alias: `RequestProfile`
- Related-game enum name: `SelfLook`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 4 concrete builder/sender call sites
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x41b840`
- `0x510380`
- `0x5138f0`
- `0x5f42d0`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x2D`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
