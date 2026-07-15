# Browser (`SBrowser`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x66` (102) |
| Common transform | static |
| Constructor | `0x00597E20` |
| Name provenance | Microsoft C++ RTTI in the target |

## Current evidence

The constructor at `0x00597E20` calls `net_server_packet_base_ctor` with opcode `0x66` and installs the `SBrowser` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Plaintext body

```text
opcode:u8
... fields pending
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
