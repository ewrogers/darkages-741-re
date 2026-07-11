# 048 / 0x30: CChangeSlotPacket

- Direction: client to server
- Internal packet name: `CChangeSlotPacket`
- Local behavioral alias: `SwapSlot`
- Related-game enum name: `ChangeSlot`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 3 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x490f40`
- `0x492ce0`
- `0x493540`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x30`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
