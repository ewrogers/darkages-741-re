# 109 / 0x6D: Family Name (`SFamilyName`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x6D` |
| RTTI class | `SFamilyName` |
| Factory | `0x599100` |
| Constructor | `0x599180` |
| Vtable | `0x687EAC` |
| Deserializer | `0x5991B0` |

## Preliminary payload model

```text
1. string[u8 length]
```

## Raw reader-call trace

`string[u8 length]`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
