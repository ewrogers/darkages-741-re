# 042 / 0x2a: CGiveGoldPacket?

- Direction: client to server
- Internal packet name: `CGiveGoldPacket?`
- Local behavioral alias: `GiveGold`
- Related-game enum name: `GiveGold`
- Name provenance: Internal-style local name inferred from this client's behavior; no exact leaked class match is known yet.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x497b10`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x2A`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
