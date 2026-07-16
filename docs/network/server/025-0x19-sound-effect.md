# Sound Effect (`SSoundEffect`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x19` (25) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **sound effect**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x19` and installs the `SSoundEffect` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SSoundEffect {
    u8 opcode                 // 0x19
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
