# 046 / 0x2e: CPartyPacket

- Direction: client to server
- Internal packet name: `CPartyPacket`
- Local behavioral alias: `GroupInvite`
- Related-game enum name: `Group`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 10 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x462dc0`
- `0x5107d0`
- `0x513960`
- `0x513a40`
- `0x513b30`
- `0x514140`
- `0x54ca50`
- `0x5b1c90`
- `0x5f4340`
- `0x5f8620`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x2E`.
- Multiple builders emit a subtype byte followed by a one-byte-length string or related variable data.
