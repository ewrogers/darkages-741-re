# 019 / 0x13: Damage Effect (`SDamageEffect`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x13` |
| RTTI class | `SDamageEffect` |
| Factory | `0x598380` |
| Constructor | `0x598400` |
| Vtable | `0x687DC4` |
| Deserializer | `0x598430` |

## Payload model

```text
u32be object_id
u8 effect_field_a
u8 health_or_damage_percent
u8 sound_id_or_sentinel
```

## Raw reader-call trace

`u32be -> u8 -> u8 -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the payload model above and must not be interpreted as one unconditional flat structure.

## Client handling

`net_handle_s_damage_effect` at `0x5F40F0` optionally plays a sound when the last byte is not `0xFF`. A middle value in the range `0..100` is divided by four and forwarded to an object-ID keyed display update. This strongly suggests a health or damage bar scale, but the exact visual meaning and the first byte remain unconfirmed.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- `object_id`, sound sentinel, and quarter-scale update: confirmed from handler use.
- Exact effect semantics: provisional.
