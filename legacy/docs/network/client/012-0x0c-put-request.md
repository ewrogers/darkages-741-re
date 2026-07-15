# 012 / 0x0c: Put Request (`CPutRequest`)

- Direction: client to server
- Internal name: `CPutRequest`
- Local behavioral alias: `RequestEntity`
- Related-game enum name: `PutGround`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x5f4430`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x0C`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
