# Move (`SMove`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x0B` (11) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **move**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x0B` and installs the `SMove` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SMove {
    u8      opcode                    // 0x0B
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
