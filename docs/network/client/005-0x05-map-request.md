# Map Request (`CMapRequest`)

The client sends `CMapRequest` when the map announced by `SMapSize` is missing or does not match the local cache. It reports the dimensions it prepared and the CRC it calculated, allowing the server to begin a map transfer.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x05` (5) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed against the local builder behavior |

## Body

```c
struct CMapRequestBody {
    u8 opcode;                  // 0x05
    u16be reserved_0;           // 0
    u16be reserved_1;           // 0
    u8 width;
    u8 height;
    u24be cache_value;          // normally 0x00 || crc16
};
```

The body is ten bytes including the opcode. `net_handle_map_size_server_packet` builds it inline after cache validation fails.

The dimensions are the same zero-extended low bytes used to allocate the 7.41 map grid. `map_update_crc16` computes a 16-bit value, while `net_write_u24be` places it in a three-byte big-endian slot with a zero high byte. This is a padded CRC16 value, not a CRC24 algorithm.

The paired server packet is [Map Size (`SMapSize`)](../server/021-0x15-map-size.md). The server responds with map-transfer data rather than another setup packet.
