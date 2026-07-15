# 063 / 0x3f: Field Map (`CFieldMap?`)

- Direction: client to server
- Internal name: `CFieldMap?`
- Local behavioral alias: `FieldMap / WorldMapClick`
- Related-game enum name: `FieldMap`
- Name provenance: Related-game internal enum name `FieldMap` at the same opcode, corroborated by this client's coordinate-based local builders; the C++ class spelling remains reconstructed.
- Evidence: 2 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x430d30` : `net_send_c_field_map_request`
- `0x476390` : `net_send_c_field_map_selection`

## Current structural notes

- Both recovered builders emit a 9-byte body: opcode `0x3F` followed by four `u16be` fields.
- The `0x430D30` form writes a zero discriminator followed by three caller-supplied values.
- The `0x476390` form writes four values from the active field-map UI object.
- Exact field semantics remain open, but the related-game enum name `FieldMap` is a better internal description than the former behavioral label `WorldMapClick`.
