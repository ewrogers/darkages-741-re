# Effect Layer (`SEffectLayer`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x29` (41) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **effect layer**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x29` and installs the `SEffectLayer` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SEffectLayer {
    u8 opcode                 // 0x29
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
