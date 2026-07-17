# Quit (`SQuit`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x4C` (76) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **quit**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x4C` and installs the `SQuit` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SQuit {
    u8      opcode                    // 0x4C
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
