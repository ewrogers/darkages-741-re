# 066 / 0x42: Exception (`CException`)

- Direction: client to server
- Internal name: `CException`
- Local behavioral alias: `Exception`
- Related-game enum name: `Exception`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 2 concrete builder/sender call sites
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x468b40`
- `0x468d30`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x42`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
