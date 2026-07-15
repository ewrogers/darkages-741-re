# 091 / 0x5B: Advertisement (`SAdvertisement`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x5B` |
| RTTI class | `SAdvertisement` |
| Factory | `0x5978B0` |
| Constructor | `0x597930` |
| Vtable | `0x687D10` |
| Deserializer | `0x597960` |

## Preliminary payload model

```text
1. u16be
2. view(n)
3. u16be
4. u16be
5. u8
```

## Raw reader-call trace

`u16be -> view(n) -> u16be -> u16be -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
