# 123 / 0x7b: Meta Data (`CMetaData`)

- Direction: client to server
- Internal name: `CMetaData`
- Local behavioral alias: `RequestMetadata`
- Related-game enum name: `MetaData`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 2 concrete builder/sender call sites
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4e52f0`
- `0x4e53f0`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x7B`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
