# 071 / 0x47: Num Users (`SNumUsers`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x47` |
| RTTI class | `SNumUsers` |
| Factory | `0x59A870` |
| Constructor | `0x59A8F0` |
| Vtable | `0x687FE8` |
| Deserializer | `0x59A920` |

## Preliminary payload model

```text
1. u16be
```

## Raw reader-call trace

`u16be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
