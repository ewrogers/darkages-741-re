# 015 / 0x0F: Add Inventory (`SAddInventory`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x0F` |
| RTTI class | `SAddInventory` |
| Factory | `0x597380` |
| Constructor | `0x597400` |
| Vtable | `0x687CC0` |
| Deserializer | `0x597430` |

## Preliminary payload model

```text
1. u8
2. u16be
3. u8
4. string[u8 length]
5. u32be
6. u8
7. u32be
8. u32be
```

## Raw reader-call trace

`u8 -> u16be -> u8 -> string[u8 length] -> u32be -> u8 -> u32be -> u32be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
