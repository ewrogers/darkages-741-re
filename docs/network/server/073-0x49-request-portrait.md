# 073 / 0x49: Request Portrait (`SRequestPortrait`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x49` |
| RTTI class | `SRequestPortrait` |
| Factory | `0x59B410` |
| Constructor | `0x59B490` |
| Vtable | `0x68809C` |
| Deserializer | `0x59B4C0` |

## Preliminary payload model

```text
No payload fields are consumed by this packet deserializer.
```

## Raw reader-call trace

`no packet-reader calls`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
