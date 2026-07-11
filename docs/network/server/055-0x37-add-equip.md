# 055 / 0x37: Add Equip (`SAddEquip`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x37` |
| RTTI class | `SAddEquip` |
| Factory | `0x597210` |
| Constructor | `0x597290` |
| Vtable | `0x687CAC` |
| Deserializer | `0x5972C0` |

## Preliminary payload model

```text
1. u8
2. u16be
3. u8
4. string[u8 length]
5. view(n)
6. u32be
7. u32be
```

## Raw reader-call trace

`u8 -> u16be -> u8 -> string[u8 length] -> view(n) -> u32be -> u32be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
