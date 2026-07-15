# 023 / 0x17: Add Spell (`SAddSpell`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x17` |
| RTTI class | `SAddSpell` |
| Factory | `0x597640` |
| Constructor | `0x5976C0` |
| Vtable | `0x687CE8` |
| Deserializer | `0x5976F0` |

## Preliminary payload model

```text
1. u8
2. u16be
3. u8
4. string[u8 length]
5. string[u8 length]
6. u8
```

## Raw reader-call trace

`u8 -> u16be -> u8 -> string[u8 length] -> string[u8 length] -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
