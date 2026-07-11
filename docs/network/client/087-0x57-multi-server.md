# 087 / 0x57: CMultiServerPacket

- Direction: client to server
- Internal packet name: `CMultiServerPacket`
- Local behavioral alias: `RequestServerTable`
- Related-game enum name: `Multi`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 2 concrete builder/sender call sites
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x55a090`
- `0x55a150`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x57`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
