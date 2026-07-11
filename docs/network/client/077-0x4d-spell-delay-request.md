# 077 / 0x4d: CSpellDelayRequestPacket?

- Direction: client to server
- Internal packet name: `CSpellDelayRequestPacket?`
- Local behavioral alias: `SpellDelayRequest / BeginSpellCast`
- Related-game enum name: `SpellDelayRequest`
- Name provenance: Related-game internal enum name `SpellDelayRequest` at the same opcode matches this client's one-byte spell-delay request; the later leaked `CCastSpellPacket` remap is retained only as comparison history.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x49bab0` : `net_send_c_spell_delay_request`

## Current structural notes

The recovered body is `[u8 opcode=0x4D, u8 spell_or_slot]`.

- This is the request that begins the local delayed-cast/chant sequence.
- The related-game same-opcode name `SpellDelayRequest` is more precise here than remapping the later `CCastSpellPacket` class from opcode `0x56`.
