# 076 / 0x4C: Quit (`SQuit`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x4C` |
| RTTI class | `SQuit` |
| Factory | `0x59ACA0` |
| Constructor | `0x59AD20` |
| Vtable | `0x688010` |
| Deserializer | `0x59AD50` |

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
