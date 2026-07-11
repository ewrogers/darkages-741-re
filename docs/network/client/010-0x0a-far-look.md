# 010 / 0x0a: CFarLookPacket?

- Direction: client to server
- Internal packet name: `CFarLookPacket?`
- Local behavioral alias: `FarLook / LookTile`
- Related-game enum name: `FarLook`
- Name provenance: Related-game internal enum name `FarLook` at the same opcode; local builder confirmation is still missing, so the C++ class spelling remains reconstructed.
- Evidence: user-researched local command; fixed builder call site not yet isolated
- Send handling: not yet recovered from a concrete builder
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- Not yet isolated in the current static pass.

## Current structural notes

- Byte 0 of the untransformed body is expected to be opcode `0x0A`.
- Payload layout remains to be recovered from a caller or confirmed with a runtime capture.
