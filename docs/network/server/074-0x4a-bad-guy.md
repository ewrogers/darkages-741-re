# 074 / 0x4A: Bad Guy (`SBadGuy`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x4A` |
| RTTI class | `SBadGuy` |
| Factory | `0x597A10` |
| Constructor | `0x597A90` |
| Vtable | `0x687D24` |
| Deserializer | `0x597AC0` |
| Handler | `0x5F7900` (`net_handle_s_bad_guy`) |

## Payload model

```text
u8     opcode          0x4A
u8     mode            activation requires 0
u8     marker_byte     written to the persistent marker
u32be  guard           activation requires 0x7D3AFF99
```

## Raw reader-call trace

`u8 -> u8 -> u32be`

The deserializer stores the three payload fields at packet-object offsets `+0x10`, `+0x11`, and `+0x14`.

## Client behavior

When `mode` is zero and `guard` equals `0x7D3AFF99`, the handler creates or replaces `%SystemRoot%\System32\Mscfg.dll`. It writes `marker_byte` at offset zero, extends the file to `0xDB72` bytes, and deliberately crashes through a null write. The failure-to-create branch also deliberately writes through null.

On later launches, marker-file existence sets configuration byte `+0x668`. That changes the Dark Ages base connection port from `2610` to `2601` and causes the `CLogin` builder at `0x4BAA80` to crash before submission.

See [SBadGuy installation marker and login kill switch](../../security/bad-guy-installation-marker.md) for the full persistence, endpoint, registry-identifier, and login trace.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Persistent marker and deliberate crash behavior: confirmed from the handler.
- `mode` and `marker_byte` names describe local use; original member names remain unknown.
- A GM or server-policy origin cannot be established from client code alone.
