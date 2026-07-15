# 017 / 0x11: Change Direction (`SChangeDirection`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x11` |
| RTTI class | `SChangeDirection` |
| Factory | `0x597F30` |
| Constructor | `0x597FB0` |
| Vtable | `0x687D74` |
| Deserializer | `0x597FE0` |

## Payload model

```text
u32be object_id
u8 direction
```

## Raw reader-call trace

`u32be -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the payload model above and must not be interpreted as one unconditional flat structure.

## Client handling

`net_handle_s_change_direction` at `0x5F3BB0` finds the object, RTTI-casts it to `WorldObject_Living`, and calls `object_living_set_direction` at `0x5E0880`. The direction is stored at living-object offset `+0x192`. A missing object causes a `CPutRequest` for `object_id`.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Both field meanings: confirmed from handler use.
