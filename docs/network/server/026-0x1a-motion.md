# 026 / 0x1A: Motion (`SMotion`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x1A` |
| RTTI class | `SMotion` |
| Factory | `0x59A370` |
| Constructor | `0x59A3F0` |
| Vtable | `0x687F98` |
| Deserializer | `0x59A420` |

## Preliminary payload model

```text
1. u32be
2. u8
3. u16be
```

## Raw reader-call trace

`u32be -> u8 -> u16be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
