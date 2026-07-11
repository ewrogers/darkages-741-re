# 078 / 0x4e: CSpellDelaySayPacket?

- Direction: client to server
- Internal packet name: `CSpellDelaySayPacket?`
- Local behavioral alias: `SpellDelaySay / SpellChant`
- Related-game enum name: `SpellDelaySay`
- Name provenance: Related-game internal enum name `SpellDelaySay` at the same opcode is corroborated by this client's length-prefixed chant text; the C++ class spelling remains reconstructed.
- Evidence: 3 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x499330` : `net_send_c_spell_delay_say`
- `0x49b870` : `net_advance_spell_delay_say_sequence`
- `0x49bb40` : `net_build_c_spell_delay_say_step`

## Current structural notes

- Recovered builders emit `[u8 opcode=0x4E, u8 text_length, bytes[text_length]]`.
- The text comes from the active spell-delay chant sequence; another helper advances the chant index and submits the accumulated body.
- This directly corroborates the related-game internal enum name `SpellDelaySay`.
