# Transfer Server (`STransferServer`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x03` (3) |
| Common transform | raw |
| Constructor | `0x0059CA10` |
| Name provenance | Microsoft C++ RTTI in the target |

## Current evidence

The constructor at `0x0059CA10` calls `net_server_packet_base_ctor` with opcode `0x03` and installs the `STransferServer` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Plaintext body

```text
opcode:u8
... fields pending
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
