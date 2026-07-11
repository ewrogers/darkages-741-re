# 017 / 0x11: Change Direction (`SChangeDirection`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x11` |
| RTTI class | `SChangeDirection` |
| Factory | `0x597F30` |
| Constructor | `0x597FB0` |
| Vtable | `0x687D74` |
| Deserializer | `0x597FE0` |

## Preliminary payload model

```text
1. u32be
2. u8
```

## Raw reader-call trace

`u32be -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
