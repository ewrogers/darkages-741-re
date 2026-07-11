# 067 / 0x43: Object Info Request (`CObjectInfoRequest`)

- Direction: client to server
- Internal name: `CObjectInfoRequest`
- Local behavioral alias: `Interact`
- Related-game enum name: `RequestBubbleInfo`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 5 concrete builder/sender call sites
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4cd350`
- `0x534a90`
- `0x5aa0e0`
- `0x5f4730`
- `0x5f47f0`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x43`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
