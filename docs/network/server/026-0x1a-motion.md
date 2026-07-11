# 026 / 0x1A: Motion (`SMotion`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x1A` |
| RTTI class | `SMotion` |
| Factory | `0x59A370` |
| Constructor | `0x59A3F0` |
| Vtable | `0x687F98` |
| Deserializer | `0x59A420` |

## Payload model

```text
u32be object_id
u8 motion
u16be duration_10ms
```

## Raw reader-call trace

`u32be -> u8 -> u16be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the payload model above and must not be interpreted as one unconditional flat structure.

## Client handling

`net_handle_s_motion` at `0x5F3C80` accepts living human/user and monster categories. It uses the object's current direction at `+0x192` and calls the motion virtual method with `duration_10ms * 10` milliseconds.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- All field meanings: strong from the animation call.
