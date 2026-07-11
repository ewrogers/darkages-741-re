# 004 / 0x04: User Position (`SUserPosition`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x04` |
| RTTI class | `SUserPosition` |
| Factory | `0x59CC20` |
| Constructor | `0x59CCA0` |
| Vtable | `0x6881B4` |
| Deserializer | `0x59CCD0` |

## Preliminary payload model

```text
1. u16be
2. u16be
```

## Raw reader-call trace

`u16be -> u16be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
