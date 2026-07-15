# Draw Objects (`SDrawObjects`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x07` (7) |
| Common transform | derived |
| Constructor | `0x00598A40` |
| Name provenance | Microsoft C++ RTTI in the target |

## Current evidence

The constructor at `0x00598A40` calls `net_server_packet_base_ctor` with opcode `0x07` and installs the `SDrawObjects` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Plaintext body

```text
opcode:u8
... fields pending
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
