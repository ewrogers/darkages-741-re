# 058 / 0x3A: Spelled (`SSpelled`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x3A` |
| RTTI class | `SSpelled` |
| Factory | `0x59C0C0` |
| Constructor | `0x59C140` |
| Vtable | `0x68813C` |
| Deserializer | `0x59C170` |

## Preliminary payload model

```text
1. u16be
2. u8
```

## Raw reader-call trace

`u16be -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
