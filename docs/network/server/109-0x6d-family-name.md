# Family Name (`SFamilyName`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x6D` (109) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **family name**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x6D` and installs the `SFamilyName` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SFamilyName {
    u8      opcode                    // 0x6D
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
