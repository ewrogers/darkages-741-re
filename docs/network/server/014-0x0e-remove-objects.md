# 014 / 0x0E: Remove Objects (`SRemoveObjects`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x0E` |
| RTTI class | `SRemoveObjects` |
| Factory | `0x59AFD0` |
| Constructor | `0x59B050` |
| Vtable | `0x68804C` |
| Deserializer | `0x59B080` |

## Payload model

```text
u32be object_id
```

## Raw reader-call trace

`u32be`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the payload model above and must not be interpreted as one unconditional flat structure.

## Client handling

`net_handle_s_remove_objects` at `0x5F3100` removes exactly one object through `object_remove_by_id` at `0x5C9FA0`. Despite the plural RTTI class name, this build has no count or loop in the packet.

The removal path may insert a class-provided temporary removal visual before `object_detach` at `0x5C9450` erases the original from spatial, render, coordinate, and ID indexes.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- `object_id` and single-record behavior: confirmed.
