# Map Size (`SMapSize`)

`SMapSize` begins a map change. It tells the client which map is coming, how large a local grid to prepare, whether the Tab map is allowed, which seasonal and weather modes to use, and whether a cached map file still matches the server.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x15` (21) |
| Transform | derived |
| Name provenance | Microsoft C++ RTTI in the target |

## Body as parsed by client 7.41

```c
struct SMapSizeBody741 {
    u8 opcode;                  // 0x15
    u16be map_number;
    u8 width;
    u8 height;
    u8 flags;
    u8 unknown_after_flags;     // parsed, then ignored
    u24be cache_value;          // observed as 0x00 || crc16
    string8 name;
};
```

`net_deserialize_map_size_server_packet` performs exactly this sequence:

```text
u16be, u8, u8, u8, u8, u24be, string8
```

`net_handle_map_size_server_packet` zero-extends the first two dimension bytes and uses them as the width and height. The fourth byte is loaded but never used. The main world handler also does not read the parsed map name.

## The unused byte and cache slot

The byte after `flags` is real packet data, but its purpose is unresolved. The parser stores it at `SMapSize + 0x15`. The active handler copies it into a local variable and never reads that variable again. No change to map loading, rendering, weather, lighting, collision, or the Tab map depends on this byte in the traced client path.

The two dimensions are one byte each in client 7.41. Its map-grid resize routine has no second live-network caller that supplies wider dimensions, so one loaded grid is limited to 255 tiles on either axis through this path. This does not rule out a larger game area being divided across several map numbers or another client version interpreting the wire bytes differently.

Other packets still use wider coordinate fields. In particular, [`SUserPosition`](004-0x04-user-position.md) carries `u16be x` and `u16be y`, but its handler sign-extends them and local movement compares them against these same byte-derived map bounds. Wider position fields therefore do not increase the grid size in client 7.41.

The client does not implement a CRC24 algorithm. `map_update_crc16` returns exactly 16 bits. Both the `SMapSize` comparison and the paired `CMapRequest` use a three-byte storage slot whose normal value is:

```text
00 crc_high crc_low
```

The reader consumes those bytes with a generic `u24be` helper, while the writer zero-extends the CRC16 through `net_write_u24be`. Every supplied observation has a zero leading byte, and the 7.41 cache comparison requires it to be zero. Its original purpose remains unknown.

## Map flags

The client keeps the low nibble as a single weather or lighting mode. Bits `0x40` and `0x80` are independent options that may be combined with it.

| Value | Project vocabulary | Client 7.41 behavior |
| ---: | --- | --- |
| `0x00` | None | No weather setup |
| `0x01` | Snow | Creates the falling-snow overlay |
| `0x02` | Rain | Recognized explicitly, but performs no local setup |
| `0x03` | Darkness | Forces black ambient light and enables human-centered light masks; does not combine snow and rain effects |
| `0x40` | NoMap | Disables the Tab map overlay for every class |
| `0x80` | Winter | Selects alternate ground and static art |

`NoMap` is checked before the Rogue class branch. A Rogue therefore cannot open or zoom the Tab map when `flags & 0x40` is set. Map setup also disables an overlay that was already open.

`Winter` selects `tileas.bmp` and the `stsNNNNN.hpf` static-art family, with fallback to the ordinary art. It is independent of falling snow. See [Snow and weather](../../rendering/weather.md).

`Darkness` is the lantern-style Andor path. While it is active, [`SDrawHumanObjects`](051-0x33-draw-human-objects.md) may attach a server-selected `mask1%02d.epf` light image to a human. See [Map lighting](../../rendering/lighting.md).

The executable contains a nearby constant for bit `0x20`, but no code references it. Its protocol meaning remains unknown.

## Cache validation and map request

The client computes a CRC16 over the local six-byte map-cell records. It zero-extends that result before comparing it with the packet's parsed `u24be cache_value`.

If the map number, dimensions, or checksum do not match the local cache, the handler prepares the new grid and sends [`CMapRequest`](../client/005-0x05-map-request.md). That request carries the one-byte dimensions and serializes the zero-extended CRC16 as three big-endian bytes.
