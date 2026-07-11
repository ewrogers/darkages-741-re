# 038 / 0x26: CChangePasswordPacket

- Direction: client to server
- Internal packet name: `CChangePasswordPacket`
- Local behavioral alias: `ChangePassword`
- Related-game enum name: `ChangePassword`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 2 concrete builder/sender call sites
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4bc050`
- `0x4bc730`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x26`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
