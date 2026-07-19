# Map Size (`SMapSize`)

`SMapSize` begins a map change. It tells the client which map is coming, how large a local grid to prepare, whether the Tab map is allowed, which seasonal and weather modes to use, and whether a cached map file still matches the server.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x15` (21) |
| Transform | derived |
| Name provenance | Microsoft C++ RTTI in the target |

## Body as parsed by client 7.41

```text
packet SMapSize {
    u8      opcode                    // 0x15
    u16     map_number
    u8      width
    u8      height
    u8      flags                     // MapFlags
    u8      unknown_after_flags       // parsed, then ignored
    u24     cache_value               // observed as 0x00 || crc16
    string8 name
}
```

`net_deserialize_map_size_server_packet` performs exactly this sequence:

```text
u16, u8, u8, u8, u8, u24, string8
```

`net_handle_map_size_server_packet` zero-extends the first two dimension bytes and uses them as the width and height. The fourth byte is loaded but never used. The main world handler also does not read the parsed map name.

## The unused byte and cache slot

The byte after `flags` is real packet data, but its purpose is unresolved. The parser stores it at `SMapSize + 0x15`. The active handler copies it into a local variable and never reads that variable again. No change to map loading, rendering, weather, lighting, collision, or the Tab map depends on this byte in the traced client path.

The two dimensions are one byte each in client 7.41. Its map-grid resize routine has no second live-network caller that supplies wider dimensions, so one loaded grid is limited to 255 tiles on either axis through this path. This does not rule out a larger game area being divided across several map numbers or another client version interpreting the wire bytes differently.

Other packets still use wider coordinate fields. In particular, [`SUserPosition`](004-0x04-user-position.md) carries `u16 x` and `u16 y`, but its handler sign-extends them and local movement compares them against these same byte-derived map bounds. Wider position fields therefore do not increase the grid size in client 7.41.

The client does not implement a CRC24 algorithm. `map_update_crc16` returns exactly 16 bits. Both the `SMapSize` comparison and the paired `CMapRequest` use a three-byte storage slot whose normal value is:

```text
00 crc_high crc_low
```

The reader consumes those bytes with a generic `u24` helper, while the writer zero-extends the CRC16 through `net_write_u24be`. Every supplied observation has a zero leading byte, and the 7.41 cache comparison requires it to be zero. Its original purpose remains unknown.

## Map flags

`flags` uses the shared [`MapFlags`](../protocol-types.md#mapflags) type. The client keeps the low nibble as a single weather or lighting mode. Bits `0x40` and `0x80` are independent options that may be combined with it.

`NoMap` is checked before the Rogue class branch. A Rogue therefore cannot open or zoom the Tab map when `flags & 0x40` is set. Map setup also disables an overlay that was already open. [Allow map](../../appendix/runtime-patches/allow-map.md) disables both client checks, while [Map zoom](../../appendix/runtime-patches/map-zoom.md) selects the zoom-enabled configuration for every class.

`Winter` selects `tileas.bmp` and the `stsNNNNN.hpf` static-art family, with fallback to the ordinary art. It is independent of falling snow. See [Snow and weather](../../rendering/weather.md).

`Darkness` is the lantern-style Andor path. While it is active, [`SDrawHumanObjects`](051-0x33-draw-human-objects.md) may attach a server-selected `mask1%02d.epf` light image to a human. See [Map lighting](../../rendering/lighting.md). The [No darkness](../../appendix/runtime-patches/no-darkness.md) runtime patch disables all three client comparisons with this mode.

The executable contains a nearby constant for bit `0x20`, but no code references it. Its protocol meaning remains unknown.

## Cache validation and map request

The client first checks whether the map already held in memory has the same map number, dimensions, and CRC16. If not, it prepares a grid for the incoming dimensions and synchronously tries `maps\lod<map_number>.map`. A disk cache is accepted only after the complete expected cell array was read and its CRC16 matches.

The CRC16 is zero-extended before comparison with the packet's parsed `u24 cache_value`. If either cache source matches, the map is applied immediately without constructing `MapLoadingPane`.

If neither source matches, the handler marks a transfer active, sets progress to zero, and sends [`CMapRequest`](../client/005-0x05-map-request.md). That request carries the one-byte dimensions and serializes the zero-extended CRC16 as three big-endian bytes. The loading pane is still not shown at this point.

A cache-file sharing violation is also treated as a miss. The handler does not retry the local file before sending the request. This can occur when another client process is inside its short exclusive map-cache write; see [Map loading and cache](../../systems/map-loading.md#multiple-client-processes).

## Transfer data after setup

`SMapSize` does not carry map cells. It either accepts the local cache or marks a map transfer active and requests data from the server.

The client has two handlers for incoming transfer data:

- [`SMap`](006-0x06-map.md) applies an arbitrary `u8`-bounded rectangle of map cells. It does not finish the transfer by itself.
- [`SMapPart`](060-0x3c-map-part.md) applies one complete row. It updates the loading percentage and completes the transfer when the final row arrives.

This separation explains the similar names. `SMapSize` establishes the destination grid and transfer state; the other messages fill that grid.

See [Map loading and cache](../../systems/map-loading.md) for the cache, pane, persistence, and world-activation lifecycle.
