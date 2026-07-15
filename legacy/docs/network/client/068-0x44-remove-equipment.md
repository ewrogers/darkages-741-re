# 068 / 0x44: Remove Equipment (`CRemoveEquipment`)

- Direction: client to server
- Internal name: `CRemoveEquipment`
- Local behavioral alias: `UnequipItem`
- Related-game enum name: `RemoveEquip`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 3 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x460330`
- `0x5b1690`
- `0x5f4170`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x44`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
