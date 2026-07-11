# 011 / 0x0B: Move (`SMove`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x0B` |
| RTTI class | `SMove` |
| Factory | `0x59A4A0` |
| Constructor | `0x59A520` |
| Vtable | `0x687FAC` |
| Deserializer | `0x59A550` |

## Preliminary payload model

```text
1. u8
2. u16be
3. u16be
4. u16be
5. u16be
6. u8
```

## Raw reader-call trace

`u8 -> u16be -> u16be -> u16be -> u16be -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
