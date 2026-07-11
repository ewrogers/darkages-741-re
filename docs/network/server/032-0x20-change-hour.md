# 032 / 0x20: Change Hour (`SChangeHour`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x20` |
| RTTI class | `SChangeHour` |
| Factory | `0x598050` |
| Constructor | `0x5980D0` |
| Vtable | `0x687D88` |
| Deserializer | `0x598100` |

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
