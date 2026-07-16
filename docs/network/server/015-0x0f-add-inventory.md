# Add Inventory (`SAddInventory`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x0F` (15) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **add inventory**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x0F` and installs the `SAddInventory` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SAddInventory {
    u8 opcode                 // 0x0F
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
