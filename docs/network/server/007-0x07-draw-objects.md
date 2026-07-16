# Draw Objects (`SDrawObjects`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x07` (7) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **draw objects**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x07` and installs the `SDrawObjects` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SDrawObjects {
    u8 opcode                 // 0x07
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
