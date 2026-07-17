# Move Object (`SMoveObject`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x0C` (12) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **move object**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x0C` and installs the `SMoveObject` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SMoveObject {
    u8      opcode                    // 0x0C
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
