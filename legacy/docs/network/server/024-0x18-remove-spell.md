# 024 / 0x18: Remove Spell (`SRemoveSpell`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x18` |
| RTTI class | `SRemoveSpell` |
| Factory | `0x59B1F0` |
| Constructor | `0x59B270` |
| Vtable | `0x688074` |
| Deserializer | `0x59B2A0` |

## Preliminary payload model

```text
1. u8
```

## Raw reader-call trace

`u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
