# 072 / 0x48: Spell Delay Cancel (`SSpellDelayCancel`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x48` |
| RTTI class | `SSpellDelayCancel` |
| Factory | `0x59BFC0` |
| Constructor | `0x59C040` |
| Vtable | `0x688128` |
| Deserializer | `0x59C070` |

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
