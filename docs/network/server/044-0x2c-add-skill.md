# 044 / 0x2C: Add Skill (`SAddSkill`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x2C` |
| RTTI class | `SAddSkill` |
| Factory | `0x597510` |
| Constructor | `0x597590` |
| Vtable | `0x687CD4` |
| Deserializer | `0x5975C0` |

## Preliminary payload model

```text
1. u8
2. u16be
3. string[u8 length]
```

## Raw reader-call trace

`u8 -> u16be -> string[u8 length]`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
