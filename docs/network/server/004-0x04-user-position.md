# 004 / 0x04: User Position (`SUserPosition`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x04` |
| RTTI class | `SUserPosition` |
| Factory | `0x59CC20` |
| Constructor | `0x59CCA0` |
| Vtable | `0x6881B4` |
| Deserializer | `0x59CCD0` |

## Payload model

```text
u16be x
u16be y
```

## Raw reader-call trace

`u16be -> u16be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the payload model above and must not be interpreted as one unconditional flat structure.

## Client handling

`net_handle_s_user_position` at `0x5F2F00` finds the local `WorldObject_User`, writes `y` to object offset `+0x40` and `x` to `+0x44`, then calls `object_reindex` at `0x5C92C0`. `object_set_view_position` at `0x5EEC70` synchronizes the camera and visible map state.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Coordinate meanings: confirmed from the handler's object and view writes.
