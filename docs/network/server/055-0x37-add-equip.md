# Add Equip (`SAddEquip`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x37` (55) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **add equip**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x37` and installs the `SAddEquip` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SAddEquip {
    u8 opcode                 // 0x37
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
