# 016 / 0x10: CTransferServerPacket

- Direction: client to server
- Internal packet name: `CTransferServerPacket`
- Local behavioral alias: `Authenticate`
- Related-game enum name: `TransferServer`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 2 concrete builder/sender call sites
- Send handling: no common encryption transform
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4b9510`
- `0x5f7bb0`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x10`.
- The payload is the `u8`-length transfer token received in `STransferServer 0x03`, copied verbatim without adding a new length field.
- Recovered body: `u8 opcode 0x10, byte transfer_token[token_length], u8 queued NUL sentinel`.
- The handler reconnects to the supplied `u32be` address and `u16be` port, then submits this raw CPacket.
- This packet does not consume the rolling sequence and does not directly install the salt selector or replacement primary key. The new server's raw `SVersionCheck 0x00` subtype-0 message performs that setup.
