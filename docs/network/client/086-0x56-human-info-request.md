# 086 / 0x56: CHumanInfoRequestPacket

- Direction: client to server
- Internal packet name: `CHumanInfoRequestPacket`
- Local behavioral alias: `RequestUserId`
- Name provenance: Leaked company/engine class name remapped by this client's local behavior; the sibling-game opcode differs.
- Evidence: user-researched local command; fixed builder call site not yet isolated
- Send handling: not yet recovered from a concrete builder
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- Not yet isolated in the current static pass.

## Current structural notes

- Byte 0 of the untransformed body is expected to be opcode `0x56`.
- Payload layout remains to be recovered from a caller or confirmed with a runtime capture.
