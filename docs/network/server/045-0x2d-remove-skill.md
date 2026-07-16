# Remove Skill (`SRemoveSkill`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x2D` (45) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **remove skill**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x2D` and installs the `SRemoveSkill` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SRemoveSkill {
    u8 opcode                 // 0x2D
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
