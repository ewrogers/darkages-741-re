# 058 / 0x3a: CPursuitPacket

- Direction: client to server
- Internal packet name: `CPursuitPacket`
- Local behavioral alias: `DialogChoice`
- Related-game enum name: `Message`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 22 concrete builder/sender call sites
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4dbc90`
- `0x4dd1a0`
- `0x4dd300`
- `0x4dd460`
- `0x4ddee0`
- `0x4de040`
- `0x4de1a0`
- `0x4df050`
- `0x4df1b0`
- `0x4e05b0`
- `0x4e0710`
- `0x4e0870`
- `0x4e1540`
- `0x4e16a0`
- `0x52a590`
- `0x52a760`
- `0x53d940`
- `0x53d9d0`
- `0x53da90`
- `0x53dc30`
- `0x53e070`
- `0x53f060`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x3A`.
- Common builder header: `u8 opcode, u8 subtype/state, u32be context/id, u16be object/value, u16be argument`.
- `net_submit_client_packet` adds a special random/checksum wrapper before common transformation.
