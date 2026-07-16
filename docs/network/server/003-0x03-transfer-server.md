# Transfer Server (`STransferServer`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x03` (3) |
| Encoding | none |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **transfer server**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x03` and installs the `STransferServer` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet STransferServer {
    u8 opcode                 // 0x03
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
