# Screen Shot (`SScreenShot`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x6B` (107) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **screen shot**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x6B` and installs the `SScreenShot` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SScreenShot {
    u8      opcode                    // 0x6B
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
