# Action Delay (`SActionDelay`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x3F` (63) |
| Common transform | derived |
| Constructor | `0x00597160` |
| Name provenance | Microsoft C++ RTTI in the target |

## Current evidence

The constructor at `0x00597160` calls `net_server_packet_base_ctor` with opcode `0x3F` and installs the `SActionDelay` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Plaintext body

```text
opcode:u8
... fields pending
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
