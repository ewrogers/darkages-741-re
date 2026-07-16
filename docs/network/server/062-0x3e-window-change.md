# Window Change (`SWindowChange`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3E` (62) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **window change**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x3E` and installs the `SWindowChange` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SWindowChange {
    u8 opcode                 // 0x3E
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
