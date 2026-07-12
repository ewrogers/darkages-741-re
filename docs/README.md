# Dark Ages 7.41 Reverse Engineering

These notes document the version-741 client and its packet-processing behavior.

- [Combined SPacket/CPacket opcode master list](network/README.md)
- [Friendly function index](functions/README.md)
- [Client startup and subsystem order](client/startup.md)
- [File formats, transforms, and compression](file-formats/README.md)
- [User interface layouts, runtime, and pane classes](ui/README.md)
- [Objects, view range, refresh, and self-player initialization](objects/README.md)
- [Map lighting, HEA masks, time profiles, and lantern light sources](map/lighting.md)
- [Chat, speech balloons, message overlays, and look popups](chat/README.md)
- [Win32, keyboard, mouse, modal, and world input routing](input/README.md)
- [Endpoint resolution and fallback order](network/endpoint-resolution.md)
- [Client receive pipeline](client/network-receive.md)
- [Client send pipeline](client/network-send.md)
- [Packet encryption, decryption, and CRC reconstruction](client/packet-crypto-and-crc.md)
- [Client security behavior](security/README.md)
- [Server packet registry](network/server/README.md)
- [Client packet send index](network/client/README.md)

SPacket names come from Microsoft Visual C++ RTTI in this client. CPacket documentation combines leaked registered class names with user-provided related-engine terminology. Concrete names omit the redundant class suffix, so the docs use forms such as `SUserPosition` and `CVersion`. The generic terms `SPacket` and `CPacket` remain unchanged. The version-741 builders and callers remain authoritative. Each page records its provenance. A trailing `?` marks a reconstructed C++ class spelling, even when a related-engine symbol provides strong terminology evidence.

## Address convention

Code and global addresses are static virtual addresses from the IDA database. The executable's preferred image base is `0x400000`. If Windows relocates the module, compute a runtime address as:

```text
runtime_address = module_base + (static_address - 0x400000)
```

Object-relative values such as `this + 0x638` are offsets inside an allocated object, not static process addresses.
