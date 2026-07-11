# 019 / 0x13: CAttackPacket

- Direction: client to server
- Internal packet name: `CAttackPacket`
- Local behavioral alias: `Assail`
- Related-game enum name: `Attack`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x5f44b0`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x13`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
