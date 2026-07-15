# User Position (`SUserPosition`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x04` (4) |
| Common transform | derived |
| Constructor | `0x0059CCA0` |
| Name provenance | Microsoft C++ RTTI in the target |

## Current evidence

The constructor at `0x0059CCA0` calls `net_server_packet_base_ctor` with opcode `0x04` and installs the `SUserPosition` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Plaintext body

```text
opcode:u8
... fields pending
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
