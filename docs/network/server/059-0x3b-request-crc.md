# Request CRC (`SRequestCRC`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3B` (59) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **request crc**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x3B` and installs the `SRequestCRC` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SRequestCRC {
    u8 opcode                 // 0x3B
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
