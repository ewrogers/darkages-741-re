# Map Size (`SMapSize`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x15` (21) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **map size**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x15` and installs the `SMapSize` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SMapSize {
    u8 opcode                 // 0x15
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
