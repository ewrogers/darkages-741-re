# 011 / 0x0B: Move (`SMove`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x0B` |
| RTTI class | `SMove` |
| Factory | `0x59A4A0` |
| Constructor | `0x59A520` |
| Vtable | `0x687FAC` |
| Deserializer | `0x59A550` |

## Payload model

```text
u8 direction_or_result
u16be x
u16be y
u16be unknown_05
u16be unknown_07
u8 timing_token
```

## Raw reader-call trace

`u8 -> u16be -> u16be -> u16be -> u16be -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the payload model above and must not be interpreted as one unconditional flat structure.

## Client handling

`net_handle_s_move` at `0x5F2FC0` is the local-player movement path. A `direction_or_result` value of `4` is treated as an authoritative position result. If it disagrees with local state, the client sends `CRefresh` (`0x38`) through `net_send_c_refresh` at `0x5F4640`.

Other direction values advance the view from the supplied coordinates. When `timing_token` matches the pending movement token, the handler records `timeGetTime()` minus the stored send time as round-trip latency.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Coordinates, result branch, and timing token: strong from handler use.
- Two middle `u16be` fields: unknown.
