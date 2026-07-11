# 025 / 0x19: Sound Effect (`SSoundEffect`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x19` |
| RTTI class | `SSoundEffect` |
| Factory | `0x59BE80` |
| Constructor | `0x59BF00` |
| Vtable | `0x688114` |
| Deserializer | `0x59BF30` |

## Preliminary payload model

```text
u8 sound_id
if sound_id == 0xFF: u8 extended_sound_id
```

## Raw reader-call trace

`u8 -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.
