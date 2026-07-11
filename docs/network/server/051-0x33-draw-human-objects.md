# 051 / 0x33: Draw Human Objects (`SDrawHumanObjects`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x33` |
| RTTI class | `SDrawHumanObjects` |
| Factory | `0x5984C0` |
| Constructor | `0x598540` |
| Vtable | `0x687DD8` |
| Deserializer | `0x598570` |

## Preliminary payload model

```text
u16be, u16be, u8, u32be, u16be appearance_id
if appearance_id != special_appearance_constant:
  packed/variant fields: u8, u16be, u8, u16be, u8, u16be, u8, u8, u8, u16be, u8, u16be, u8, u16be, u8, u8, u8, u16be, u8, u8, u8, u8, u8
else:
  u16be, u8, u8, u8, skip/view 5 bytes, u8
string[u8 length]
string[u8 length]
Several packed appearance bits are normalized after reading.
```

## Raw reader-call trace

`u16be -> u16be -> u8 -> u32be -> u16be -> u8 -> u16be -> u8 -> u16be -> u8 -> u16be -> u8 -> u8 -> u8 -> u16be -> u8 -> u16be -> u8 -> u16be -> u8 -> u8 -> u16be -> u8 -> u8 -> u8 -> u8 -> u8 -> u16be -> u8 -> u8 -> u8 -> view(n) -> u8 -> string[u8 length] -> string[u8 length]`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
