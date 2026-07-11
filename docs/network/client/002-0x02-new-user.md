# 002 / 0x02: CNewUserPacket

- Direction: client to server
- Internal packet name: `CNewUserPacket`
- Local behavioral alias: `CreateCharacterName`
- Related-game enum name: `NewUser`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 1 concrete builder/sender call site
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x43d820`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x02`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
