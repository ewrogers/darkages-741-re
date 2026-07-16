# Action Delay (`SActionDelay`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3F` (63) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **action delay**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x3F` and installs the `SActionDelay` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SActionDelay {
    u8 opcode                 // 0x3F
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
