# 085 / 0x55: Black Smith (`CBlackSmith`)

- Direction: client to server
- Internal name: `CBlackSmith`
- Local behavioral alias: `Manufacture`
- Related-game enum name: `Manual`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 2 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4c26d0`
- `0x4c27c0`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x55`.
- The related-game enum labels `0x55` as `Manual`, but this client's local manufacture/blacksmith behavior and the leaked registered `CBlackSmith` class agree with each other. The current `CBlackSmith` name is therefore retained.
- Remaining payload fields still require caller analysis or runtime confirmation.
