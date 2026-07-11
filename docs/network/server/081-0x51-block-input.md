# 081 / 0x51: Block Input (`SBlockInput`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x51` |
| RTTI class | `SBlockInput` |
| Factory | `0x597B40` |
| Constructor | `0x597BC0` |
| Vtable | `0x687D38` |
| Deserializer | `0x597BF0` |

## Preliminary payload model

```text
u8 state
if state == 0: u8
```

## Raw reader-call trace

`u8 -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
