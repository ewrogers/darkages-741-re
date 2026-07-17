# Motion (`SMotion`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x1A` (26) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **motion**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x1A` and installs the `SMotion` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SMotion {
    u8      opcode                    // 0x1A
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
