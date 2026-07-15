# 071 / 0x47: Add Stat (`CAddStat?`)

- Direction: client to server
- Internal name: `CAddStat?`
- Local behavioral alias: `AddStat / RaiseStat`
- Related-game enum name: `AddStat`
- Name provenance: Related-game internal enum name `AddStat` at the same opcode matches this client's stat-selector payload better than the later leaked `CGrowSkill` remap; the C++ class spelling remains reconstructed.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x5755c0` : `net_send_c_add_stat`

## Current structural notes

The recovered body is two bytes:

| Offset | Type | Meaning |
|---:|---|---|
| 0 | `u8` | opcode `0x47` |
| 1 | `u8` | selected stat identifier |

- The builder accepts one of five local stat selections (index 0 through 4) and sends the corresponding selector byte.
- The same-opcode internal enum name `AddStat` therefore fits better than the later-game `CGrowSkill` class remap.
