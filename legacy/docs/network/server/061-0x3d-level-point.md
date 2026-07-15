# 061 / 0x3D: Level Point (`SLevelPoint`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x3D` |
| RTTI class | `SLevelPoint` |
| Factory | `0x599940` |
| Constructor | `0x5999C0` |
| Vtable | `0x687F0C` |
| Deserializer | `0x5999F0` |

## Preliminary payload model

```text
1. u8
2. u8
```

## Raw reader-call trace

`u8 -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
