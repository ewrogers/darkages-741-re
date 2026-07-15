# 059 / 0x3b: Bulletin (`CBulletin`)

- Direction: client to server
- Internal name: `CBulletin`
- Local behavioral alias: `BoardAction`
- Related-game enum name: `Bulletin`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 15 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x41cbc0`
- `0x41e350`
- `0x420d00`
- `0x420e40`
- `0x420f80`
- `0x421090`
- `0x4220d0`
- `0x422210`
- `0x422c00`
- `0x424a40`
- `0x424b80`
- `0x424cc0`
- `0x425df0`
- `0x425f30`
- `0x4268f0`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x3B`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
