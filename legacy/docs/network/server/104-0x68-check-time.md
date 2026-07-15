# 104 / 0x68: Check Time (`SCheckTime`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x68` |
| RTTI class | `SCheckTime` |
| Factory | `0x598270` |
| Constructor | `0x5982F0` |
| Vtable | `0x687DB0` |
| Deserializer | `0x598320` |

## Preliminary payload model

```text
1. u32be
```

## Raw reader-call trace

`u32be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
