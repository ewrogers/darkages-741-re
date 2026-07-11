# 008 / 0x08: Status (`SStatus`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x08` |
| RTTI class | `SStatus` |
| Factory | `0x59C360` |
| Constructor | `0x59C3E0` |
| Vtable | `0x688164` |
| Deserializer | `0x59C410` |

## Preliminary payload model

```text
u8 presence_flags
if flags[group A]: 5 x u8, 2 x u32be, 7 x u8, 2 x u16be, u32be
if flags[group B]: 2 x u32be
if flags[group C]: 6 x u32be
if flags[group D]: 13 x u8
other decoded bits toggle state without consuming additional bytes
Flag-mask semantic names are still provisional.
```

## Raw reader-call trace

`u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> u32be -> u32be -> u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> u16be -> u16be -> u32be -> u32be -> u32be -> u32be -> u32be -> u32be -> u32be -> u32be -> u32be -> u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
