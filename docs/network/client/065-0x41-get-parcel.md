# 065 / 0x41: CGetParcelPacket?

- Direction: client to server
- Internal packet name: `CGetParcelPacket?`
- Local behavioral alias: `GetParcel / DismissParcel`
- Related-game enum name: `GetParcel`
- Name provenance: Related-game internal enum name `GetParcel` at the same opcode; local behavior supports the parcel operation, but a fixed builder is not yet isolated.
- Evidence: user-researched local command; fixed builder call site not yet isolated
- Send handling: not yet recovered from a concrete builder
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- Not yet isolated in the current static pass.

## Current structural notes

- Byte 0 of the untransformed body is expected to be opcode `0x41`.
- Payload layout remains to be recovered from a caller or confirmed with a runtime capture.
