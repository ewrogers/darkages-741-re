# Bad Guy (`SBadGuy`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x4A` (74) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **bad guy**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x4A` and installs the `SBadGuy` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SBadGuy {
    u8 opcode                 // 0x4A
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
