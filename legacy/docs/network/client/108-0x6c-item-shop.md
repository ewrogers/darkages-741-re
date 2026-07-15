# 108 / 0x6c: Item Shop (`CItemShop`)

- Direction: client to server
- Internal name: `CItemShop`
- Local behavioral alias: `ItemShop`
- Related-game enum name: `CashShop`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 3 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4a03b0`
- `0x4a0430`
- `0x4a1400`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x6C`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
