# Map Part (`SMapPart`)

Map parts carry an uncached map to the client one complete row at a time and drive the map-transfer progress display. This is the packet that creates and advances `MapLoadingPane`.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3C` (60) |
| Transform | `derived` |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends each row with its zero-based Y coordinate. `net_handle_map_part` applies exactly the current map width in cells and calculates progress against the current map height.

One row is the packet's transfer unit, not a confirmed standalone row-update operation. Supplied runtime observations show `SMapPart` being sent as the complete set of rows needed to save an entire map after a cache miss. No isolated partial-update use has been observed.

The implementation would accept one non-final row while a transfer is active, but it would only change the prepared in-memory grid and leave the transfer unfinished. Outside an active transfer it is ignored. A final-index row is the only completion signal, so sending that row without the preceding rows would make the client commit an incomplete grid rather than perform a well-defined partial update.

The constructor calls `net_server_packet_base_ctor` with opcode `0x3C` and installs the `SMapPart` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

The world dispatcher still gives the raw decoded body to `net_handle_map_part`. The handler ignores it unless [`SMapSize`](021-0x15-map-size.md) previously marked a cache-miss transfer active. On the first accepted part, it constructs `MapLoadingPane`. Its constructor loads `_nloadm.txt` and registers the pane as a visible screen pane.

## Body

```text
packet SMapPart {
    u8      opcode                    // 0x3C
    u16     row_index

    repeat map_width {
        u16     ground_tile
        u16     left_static_tile
        u16     right_static_tile
    }
}
```

The plaintext body size is `3 + map_width * 6` bytes. The three values match the six-byte [MAP cell](../../file-formats/map.md). The handler writes each record at X positions `0` through `map_width - 1` and Y position `row_index`.

These writes update the allocated in-memory map. The client does not append or seek within the cache file as each row arrives.

The progress pane receives:

```text
progress = (row_index + 1) * 100 / map_height
```

When `row_index == map_height - 1`, the client clears the active-transfer flag, updates the CRC across the complete in-memory map, and writes the entire map cache with one `width * height * 6` write. It then destroys and unregisters `MapLoadingPane` before applying the prepared grid to the world. The cache writer's result is ignored, so a failed save does not prevent activation.

Completion is based only on receiving the final row index. The client has no received-row count or bitmap. Duplicate and out-of-order rows are accepted, and an early final-index row can cause unchanged earlier cells to be saved and activated. `map_set_cell` rejects an out-of-grid row, but the handler does not visibly check the decoded body length before reading `map_width` records.

[`SMap`](006-0x06-map.md) can also write map cells during an active transfer, but it carries an arbitrary rectangle and has no corresponding progress or completion step.

This behavior is separate from the observed [`0x58`](088-0x58-unhandled-control.md) and [`0x67`](103-0x67-unhandled-map-transfer-control.md) controls. This client does not use either of those messages to show or hide the loading pane.

See [Map loading and cache](../../systems/map-loading.md) for the complete cache and pane lifecycle.
