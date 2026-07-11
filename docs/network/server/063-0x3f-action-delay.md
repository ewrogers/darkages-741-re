# 063 / 0x3F: Action Delay (`SActionDelay`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x3F` |
| RTTI class | `SActionDelay` |
| Factory | `0x5970E0` |
| Constructor | `0x597160` |
| Vtable | `0x687C98` |
| Deserializer | `0x597190` |

## Preliminary payload model

```text
1. u8
2. u8
3. u32be
```

## Raw reader-call trace

`u8 -> u8 -> u32be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
