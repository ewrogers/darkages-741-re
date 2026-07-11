# 049 / 0x31: User Confirm (`CUserConfirm`)

- Direction: client to server
- Internal name: `CUserConfirm`
- Local behavioral alias: `ConfirmUser`
- Related-game enum name: `Confirm`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x5922a0`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x31`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
