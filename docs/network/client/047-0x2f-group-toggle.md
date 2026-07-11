# 047 / 0x2f: Group Toggle (`CGroupToggle?`)

- Direction: client to server
- Internal name: `CGroupToggle?`
- Local behavioral alias: `GroupToggle / ToggleGroup`
- Related-game enum name: `GroupToggle`
- Name provenance: Related-game internal enum name `GroupToggle` at the same opcode, corroborated by this client's three local builders; the C++ class spelling remains reconstructed.
- Evidence: 3 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x41b8e0`
- `0x4604a0`
- `0x5b1690`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x2F`.
- Payload layout is documented only where recovered from local code; remaining fields still require caller analysis or runtime confirmation.
