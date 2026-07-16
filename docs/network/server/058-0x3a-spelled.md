# Spelled (`SSpelled`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3A` (58) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **spelled**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x3A` and installs the `SSpelled` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SSpelled {
    u8 opcode                 // 0x3A
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
