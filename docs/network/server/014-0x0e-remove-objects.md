# Remove Objects (`SRemoveObjects`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x0E` (14) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **remove objects**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x0E` and installs the `SRemoveObjects` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SRemoveObjects {
    u8 opcode                 // 0x0E
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
