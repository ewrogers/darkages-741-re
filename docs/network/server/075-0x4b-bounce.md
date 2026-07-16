# Bounce (`SBounce`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x4B` (75) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **bounce**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x4B` and installs the `SBounce` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SBounce {
    u8 opcode                 // 0x4B
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
