# Self Save OK (`SSelfSaveOK`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x21` (33) |
| Common transform | derived |
| Constructor | `0x0059BE00` |
| Name provenance | Microsoft C++ RTTI in the target |

## Current evidence

The constructor at `0x0059BE00` calls `net_server_packet_base_ctor` with opcode `0x21` and installs the `SSelfSaveOK` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Plaintext body

```text
opcode:u8
... fields pending
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
