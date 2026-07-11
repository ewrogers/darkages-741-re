# 012 / 0x0C: Move Object (`SMoveObject`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x0C` |
| RTTI class | `SMoveObject` |
| Factory | `0x59A600` |
| Constructor | `0x59A680` |
| Vtable | `0x687FC0` |
| Deserializer | `0x59A6B0` |

## Preliminary payload model

```text
1. u32be
2. u16be
3. u16be
4. u8
```

## Raw reader-call trace

`u32be -> u16be -> u16be -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
