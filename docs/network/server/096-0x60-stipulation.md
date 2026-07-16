# Stipulation (`SStipulation`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x60` (96) |
| Encoding | startup key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **stipulation**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x60` and installs the `SStipulation` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SStipulation {
    u8 opcode                 // 0x60
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
