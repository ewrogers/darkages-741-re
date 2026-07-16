# Self Save OK (`SSelfSaveOK`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x21` (33) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **self save ok**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x21` and installs the `SSelfSaveOK` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SSelfSaveOK {
    u8 opcode                 // 0x21
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
