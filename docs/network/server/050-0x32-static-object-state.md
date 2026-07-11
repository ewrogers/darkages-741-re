# 050 / 0x32: Static Object State (`SStaticObjectState`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x32` |
| RTTI class | `SStaticObjectState` |
| Factory | `0x59C1E0` |
| Constructor | `0x59C260` |
| Vtable | `0x688150` |
| Deserializer | `0x59C290` |

## Preliminary payload model

```text
u8 record_count
repeat record_count times:
  u8
  u8
  u8
  u8
```

## Raw reader-call trace

`u8 -> u8 -> u8 -> u8 -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
