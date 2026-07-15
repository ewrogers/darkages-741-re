# Static Object State (`SStaticObjectState`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x32` (50) |
| Common transform | derived |
| Constructor | `0x0059C260` |
| Name provenance | Microsoft C++ RTTI in the target |

## Current evidence

The constructor at `0x0059C260` calls `net_server_packet_base_ctor` with opcode `0x32` and installs the `SStaticObjectState` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Plaintext body

```text
opcode:u8
... fields pending
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
