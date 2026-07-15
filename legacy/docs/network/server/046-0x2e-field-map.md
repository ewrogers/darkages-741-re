# 046 / 0x2E: Field Map (`SFieldMap`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x2E` |
| RTTI class | `SFieldMap` |
| Factory | `0x599210` |
| Constructor | `0x599290` |
| Vtable | `0x687EC0` |
| Deserializer | `0x5992C0` |

## Preliminary payload model

```text
string[u8 length] name
u8 record_count
u8 mode_or_flags
repeat record_count times:
  u16be
  u16be
  u8 data_length
  bytes[data_length]
  u16be
  u16be
  u16be
  u16be
```

## Raw reader-call trace

`string[u8 length] -> u8 -> u8 -> u16be -> u16be -> u8 -> view(n) -> u16be -> u16be -> u16be -> u16be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
