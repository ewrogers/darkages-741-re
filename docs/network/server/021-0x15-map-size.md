# 021 / 0x15: Map Size (`SMapSize`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x15` |
| RTTI class | `SMapSize` |
| Factory | `0x599EE0` |
| Constructor | `0x599F60` |
| Vtable | `0x687F5C` |
| Deserializer | `0x599F90` |

## Preliminary payload model

```text
1. u16be
2. u8
3. u8
4. u8
5. u8
6. u24be
7. string[u8 length]
```

## Raw reader-call trace

`u16be -> u8 -> u8 -> u8 -> u8 -> u24be -> string[u8 length]`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
