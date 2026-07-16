# Message (`SMessage`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x0A` (10) |
| Encoding | startup key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **message**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x0A` and installs the `SMessage` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SMessage {
    u8 opcode                 // 0x0A
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
