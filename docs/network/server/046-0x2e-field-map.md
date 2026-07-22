# Field Map (`SFieldMap`)

`SFieldMap` opens the full-screen travel map. The server chooses the field-map artwork, identifies the player's current waypoint, and supplies every destination the client may select.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x2E` (46) |
| Transform | `derived` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SFieldMap {
    u8      opcode                    // 0x2E
    string8 field_name                // local asset stem, such as field001
    u8      node_count
    u8      current_node_index        // zero-based index into nodes

    repeat node_count {
        u16     screen_x
        u16     screen_y
        string8 name
        u16     checksum
        u16     map_id
        u16     map_x
        u16     map_y
    }
}
```

All multibyte values are big-endian. The `SFieldMap` deserializer consumes the fields in this exact order. The live `WorldPane` path then parses the decoded body again instead of using the constructed `SFieldMap` object.

`current_node_index` is not an image selector. It places the initial location marker at one of the supplied nodes. The client checks that the index is below `node_count`; an out-of-range value leaves the marker without a node position.

The screen coordinates describe where a fallback waypoint should appear. The remaining four words are travel data. The client does not interpret `checksum`; it returns that value, `map_id`, `map_x`, and `map_y` unchanged in [`CFieldMap`](../client/063-0x3f-field-map.md).

## Building the pane

The decoded packet follows this path:

```text
SFieldMap body
    -> WorldPane raw 0x2E handler
    -> FieldMapPane at 640 by 480
    -> background and local waypoint presentation
    -> one child pane per server node
```

`field_name` is the stem of three client assets:

- `<field_name>.epf` supplies frame 0 of the background.
- `<field_name>.pal` supplies an optional field-specific palette.
- `<field_name>.txt` supplies required presentation metadata, including palette names and locally styled waypoints.

The text metadata is keyed by an exact server node-name match. When a name matches, the client creates an RTTI `ImageFieldMapPointPane` using the local icon and local screen position. When no name matches, it creates an RTTI `TextFieldMapPointPane` using the server's `screen_x`, `screen_y`, and name.

This split is important for server authors. The server controls every destination, but an installed client can control the icon and visible position of a recognized waypoint. A new or unmatched name still appears as text at the server coordinates.

When `FieldMapPane` joins the live screen, it registers every point child, attaches any locally configured point animations, and creates the `FieldMapBalloonPane` marker. Its unregister path removes those children in the reverse lifetime, queues owned panes for deletion, and restores `legend.pal`. The point-pointer list owns only the child pointers; pane deletion remains part of the UI lifetime path.

## Pointer and timing flow

Moving over a point updates its hover state and redraws it. Releasing the left button over the point schedules the selection through `FieldMapPane`'s timer handler; the pointer handler does not send a packet directly.

For a different selected point, the pane moves its RTTI `FieldMapBalloonPane` marker toward the destination. The animation tick count is the screen distance divided by five and clamped to 10 through 80. The marker advances on 50 ms timer ticks, so a normal trip takes about 0.5 through 4 seconds. A target already at the marker position completes without that travel delay.

When the marker finishes, it schedules the parent's completion timer. That timer sends `CFieldMap` for the selected node. If the marker pane could not be created, the same completion is scheduled without the animation.

## Capture check

The supplied `field001` packet decodes to 12 nodes and `current_node_index = 1`. Index 1 is the second node, `Loures`:

| Field | Value |
| --- | --- |
| Screen position | `(344, 250)` |
| Checksum | `0x0000` |
| Map ID | `0x0BC4` |
| Destination | `(14, 10)` |

The later client body is:

```text
3F 00 00 0B C4 00 0E 00 0A
```

It returns those four travel values exactly. The final zero after the last node in the supplied server capture is not consumed by either client parser, so it is not part of the confirmed `SFieldMap` layout.

## Known limits

The observed packet sets every checksum to zero. The client proves only that this word is carried back to the server; its server-side validation meaning remains unknown.

The nearby server opcode [`0x67`](103-0x67-unhandled-field-map-control.md) has no client handler and does not build this pane. `SFieldMap` owns the navigation presentation, while `SMapSize` and `SMapPart` own the later destination-map loading flow.
