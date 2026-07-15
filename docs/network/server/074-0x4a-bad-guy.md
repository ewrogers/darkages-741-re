# Bad Guy (`SBadGuy`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x4A` (74) |
| Common transform | derived |
| Constructor | `0x00597A90` |
| Name provenance | Microsoft C++ RTTI in the target |

## Current evidence

The constructor at `0x00597A90` calls `net_server_packet_base_ctor` with opcode `0x4A` and installs the `SBadGuy` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Behavioral lead

The project owner identifies this as the banned-client packet that creates the local `Mscfg.dll` marker. Later startups detect that marker and change the connection port from `2610` to `2601`. The marker and port behavior are verified in [Command line and initial connection](../initial-connection.md); the packet handler and file-creation path still need to be connected in Binary Ninja.

## Plaintext body

```text
opcode:u8
... fields pending
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.
