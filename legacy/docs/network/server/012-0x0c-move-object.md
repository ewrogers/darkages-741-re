# 012 / 0x0C: Move Object (`SMoveObject`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x0C` |
| RTTI class | `SMoveObject` |
| Factory | `0x59A600` |
| Constructor | `0x59A680` |
| Vtable | `0x687FC0` |
| Deserializer | `0x59A6B0` |

## Payload model

```text
u32be object_id
u16be x
u16be y
u8 direction
```

## Raw reader-call trace

`u32be -> u16be -> u16be -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the payload model above and must not be interpreted as one unconditional flat structure.

## Client handling

`net_handle_s_move_object` at `0x5F3930` finds `object_id`, accepts human/user and monster categories, and RTTI-casts the instance to `WorldObject_Living`. A source-position disagreement writes the packet coordinates and calls `object_reindex` at `0x5C92C0`. The handler then computes the adjacent destination and invokes the living-object movement virtual method.

If the object is missing or is not a living actor, the client sends `CPutRequest` (`0x0C`) through `net_send_c_put_request` at `0x5F4430`.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- All field meanings: confirmed from handler lookup, coordinate writes, and movement call.
