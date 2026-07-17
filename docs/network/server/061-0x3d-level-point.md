# Level Point (`SLevelPoint`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3D` (61) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **level point**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x3D` and installs the `SLevelPoint` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SLevelPoint {
    u8      opcode                    // 0x3D
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
