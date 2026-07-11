# 007 / 0x07: Draw Objects (`SDrawObjects`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x07` |
| RTTI class | `SDrawObjects` |
| Factory | `0x5989C0` |
| Constructor | `0x598A40` |
| Vtable | `0x687E70` |
| Deserializer | `0x598AB0` |

## Preliminary payload model

```text
u16be value
subreader over all remaining payload bytes
Note: the apparent loop in this method does not consume fields; detailed object records are handled downstream.
```

## Raw reader-call trace

`u16be -> subreader(remaining)`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
