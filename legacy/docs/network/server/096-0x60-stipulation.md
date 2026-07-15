# 096 / 0x60: Stipulation (`SStipulation`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x60` |
| RTTI class | `SStipulation` |
| Factory | `0x59C830` |
| Constructor | `0x59C8B0` |
| Vtable | `0x688178` |
| Deserializer | `0x59C8E0` |

## Preliminary payload model

```text
u8 variant
variant 0: u32be
variant 1: u16be data_length, bytes[data_length]
```

## Raw reader-call trace

`u8 -> u32be -> u16be -> view(n)`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
