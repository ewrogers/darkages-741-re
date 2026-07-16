# Draw Human Objects (`SDrawHumanObjects`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x33` (51) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **draw human objects**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x33` and installs the `SDrawHumanObjects` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SDrawHumanObjects {
    u8 opcode                 // 0x33
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
