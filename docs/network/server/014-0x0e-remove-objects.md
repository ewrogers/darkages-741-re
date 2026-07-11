# 014 / 0x0E: Remove Objects (`SRemoveObjects`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x0E` |
| RTTI class | `SRemoveObjects` |
| Factory | `0x59AFD0` |
| Constructor | `0x59B050` |
| Vtable | `0x68804C` |
| Deserializer | `0x59B080` |

## Preliminary payload model

```text
1. u32be
```

## Raw reader-call trace

`u32be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
