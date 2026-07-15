# 027 / 0x1b: User Status (`CUserStatus`)

- Direction: client to server
- Internal name: `CUserStatus`
- Local behavioral alias: `ToggleSetting`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x542e60`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x1B`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
