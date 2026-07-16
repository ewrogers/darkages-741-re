# Field Map (`SFieldMap`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x2E` (46) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **field map**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x2E` and installs the `SFieldMap` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SFieldMap {
    u8 opcode                 // 0x2E
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
