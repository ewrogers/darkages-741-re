# Pursuit Message (`SPursuitMessage`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x30` (48) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends this message for **pursuit message**.

The constructor calls `net_server_packet_base_ctor` with opcode `0x30` and installs the `SPursuitMessage` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SPursuitMessage {
    u8      opcode                    // 0x30
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.

## NPC illustration owner

`NPCSession` handles this packet and reads a speaker name plus an illustration index from its decoded object. It uses the same `NPCIllustFileMan` lookup and tile fallback as `SScreenMenu`. See [NPC dialog illustrations](../../systems/npc-dialog-illustrations.md). The full wire field order remains unresolved.
