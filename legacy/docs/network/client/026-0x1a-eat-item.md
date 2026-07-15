# 026 / 0x1a: Eat Item (`CEatItem?`)

- Direction: client to server
- Internal name: `CEatItem?`
- Local behavioral alias: `EatItem`
- Name provenance: Internal-style local name inferred from this client's behavior; no exact leaked class match is known yet.
- Evidence: user-researched local command; fixed builder call site not yet isolated
- Send handling: not yet recovered from a concrete builder
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- Not yet isolated in the current static pass.

## Current structural notes

- Byte 0 of the untransformed body is expected to be opcode `0x1A`.
- Payload layout remains to be recovered from a caller or confirmed with a runtime capture.
