# 041 / 0x29: Effect Layer (`SEffectLayer`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x29` |
| RTTI class | `SEffectLayer` |
| Factory | `0x598D30` |
| Constructor | `0x598DB0` |
| Vtable | `0x687E84` |
| Deserializer | `0x598DE0` |

## Preliminary payload model

```text
u32be discriminator
if discriminator != 0: u32be
u16be
if discriminator != 0: u16be
u16be
if discriminator == 0: u16be, u16be
```

## Raw reader-call trace

`u32be -> u32be -> u16be -> u16be -> u16be -> u16be -> u16be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
