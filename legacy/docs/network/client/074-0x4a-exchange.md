# 074 / 0x4a: Exchange (`CExchange`)

- Direction: client to server
- Internal name: `CExchange`
- Local behavioral alias: `ExchangeAction`
- Related-game enum name: `Exchange`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 7 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x46a390`
- `0x46a440`
- `0x46a4f0`
- `0x46a5c0`
- `0x46b690`
- `0x46c2a0`
- `0x5f2190`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x4A`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
