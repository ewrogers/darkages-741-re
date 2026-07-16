# Map Part (`SMapPart`)

Map parts carry an uncached map to the client and drive the map-transfer progress display. This is the packet that creates and advances `MapLoadingPane`.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3C` (60) |
| Transform | `derived` |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server splits transferred map data into numbered parts. `net_handle_map_part` applies each part to the current map object and calculates a completion percentage.

The constructor calls `net_server_packet_base_ctor` with opcode `0x3C` and installs the `SMapPart` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

The world dispatcher still gives the raw decoded body to `net_handle_map_part`. On the first part of an active transfer, the handler constructs `MapLoadingPane`. Its constructor loads `_nloadm.txt` and registers the pane as a visible screen pane.

## Body

```text
packet SMapPart {
    u8 opcode                  // 0x3C
    u16be part_index

    repeat map_record_count {
        u16be value_a
        u16be value_b
        u16be value_c
    }
}
```

`map_record_count` and the total number of parts come from the map object established earlier in the transfer. The meanings of the three values in each repeated record remain unresolved.

The progress pane receives:

```text
progress = (part_index + 1) * 100 / total_parts
```

After the last part, the client closes `MapLoadingPane`, updates the map CRC, writes the local map cache, and applies the completed map.

This behavior is separate from the observed [`0x58`](088-0x58-unhandled-control.md) and [`0x67`](103-0x67-unhandled-map-transfer-control.md) controls. This client does not use either of those messages to show or hide the loading pane.
