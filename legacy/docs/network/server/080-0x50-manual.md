# 080 / 0x50: Manual (`SManual`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x50` |
| RTTI class | `SManual` |
| Factory | `0x599A60` |
| Constructor | `0x599AE0` |
| Vtable | `0x687F20` |
| Deserializer | `0x599B10` |

## Preliminary payload model

```text
u8, u8
u8 variant
variant 0: u8
variant 1:
  u8, u16be
  u8 length_1, bytes[length_1]
  u16be length_2, bytes[length_2]
  u16be length_3, bytes[length_3]
  u8
```

## Raw reader-call trace

`u8 -> u8 -> u8 -> u8 -> u8 -> u16be -> u8 -> view(n) -> u16be -> view(n) -> u16be -> view(n) -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
