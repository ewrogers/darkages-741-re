# 031 / 0x1F: Change Weather (`SChangeWeather`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x1F` |
| RTTI class | `SChangeWeather` |
| Factory | `0x598160` |
| Constructor | `0x5981E0` |
| Vtable | `0x687D9C` |
| Deserializer | `0x598210` |

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

## Local dispatch status

The packet class is registered and deserializes one byte, but `net_dispatch_game_server_message` at `0x5ED990` has no opcode `0x1F` handler branch. The current client therefore does not route this class into the recovered world-lighting pipeline. Opcode `0x20` `SChangeHour` is the active server lighting update.
