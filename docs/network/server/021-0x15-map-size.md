# Map Size (`SMapSize`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x15` (21) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server uses this message to set up a map. It supplies the map ID, dimensions, art and weather flags, cache checksum, and display name.

The constructor calls `net_server_packet_base_ctor` with opcode `0x15` and installs the `SMapSize` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SMapSize {
    u8 opcode                  // 0x15
    u16be map_id
    u8 width
    u8 height
    u8 flags                   // low nibble: weather; 0x80: alternate art
    u8 secondary_mode          // meaning not confirmed
    u24be map_checksum
    u8 name_length
    u8 name[name_length]
}
```

`net_decode_s_map_size` confirms this layout. `net_handle_s_map_size` applies it to the world, checks the local map cache, and requests map data when needed.

## Art and weather flags

- `flags & 0x80` selects `tileas.bmp` and `stsNNNNN.hpf`, with base-art fallback.
- `flags & 0x0F` selects local weather behavior. Mode 1 creates falling snow.
- Bit `0x40` has another map setup effect, but its full meaning is not yet named.

The alternate art bit and weather mode are independent. See [Snow and weather](../../rendering/weather.md).

The client pairs this setup with `CMapRequest` when its local map data is missing or does not match the supplied checksum.
