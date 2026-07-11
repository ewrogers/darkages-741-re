# 069 / 0x45: Item Shop (`SItemShop`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x45` |
| RTTI class | `SItemShop` |
| Factory | `0x599640` |
| Constructor | `0x5996C0` |
| Vtable | `0x687EF8` |
| Deserializer | `0x599730` |

## Preliminary payload model

```text
u8 variant
if variant == 0:
  u8
  subreader over remaining payload
```

## Raw reader-call trace

`u8 -> u8 -> subreader(remaining)`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
