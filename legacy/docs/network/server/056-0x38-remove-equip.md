# 056 / 0x38: Remove Equip (`SRemoveEquip`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x38` |
| RTTI class | `SRemoveEquip` |
| Factory | `0x59ADB0` |
| Constructor | `0x59AE30` |
| Vtable | `0x688024` |
| Deserializer | `0x59AE60` |

## Preliminary payload model

```text
1. u8
```

## Raw reader-call trace

`u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
