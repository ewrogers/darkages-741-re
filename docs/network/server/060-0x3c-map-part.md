# 060 / 0x3C: Map Part (`SMapPart`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x3C` |
| RTTI class | `SMapPart` |
| Factory | `0x599DC0` |
| Constructor | `0x599E40` |
| Vtable | `0x687F48` |
| Deserializer | `0x599E70` |

## Preliminary payload model

```text
1. u16be
2. remaining-view
```

## Raw reader-call trace

`u16be -> remaining-view`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
