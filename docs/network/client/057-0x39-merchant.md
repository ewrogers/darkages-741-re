# 057 / 0x39: CMerchantPacket

- Direction: client to server
- Internal packet name: `CMerchantPacket`
- Local behavioral alias: `DialogMenuChoice`
- Related-game enum name: `MenuCode`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 16 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4cfe60`
- `0x4d0020`
- `0x4d0c30`
- `0x4d12a0`
- `0x4d2060`
- `0x4d2b20`
- `0x4d3b80`
- `0x4d3d30`
- `0x4d3ee0`
- `0x4d77d0`
- `0x535590`
- `0x5359d0`
- `0x5362a0`
- `0x536620`
- `0x536d60`
- `0x538710`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x39`.
- Common builder header: `u8 opcode, u8 subtype/state, u32be context/id, u16be argument`.
- `net_submit_client_packet` adds a special random/checksum wrapper before common transformation.
