# Field Map (`CFieldMap`)

`CFieldMap` selects one destination from the field map currently displayed by the client. It returns the travel values attached to that server-provided waypoint.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x3F` (63) |
| Transform | `derived` |
| Name provenance | Project-owner protocol vocabulary; local builders confirm the opcode and body |

## Body

```text
packet CFieldMap {
    u8      opcode                    // 0x3F
    u16     checksum
    u16     map_id
    u16     x
    u16     y
}
```

All four words are big-endian. The normal UI builder copies them from the selected [`SFieldMap`](../server/046-0x2e-field-map.md) node without changing their order or values.

## Sent by the field-map UI

Both image and text waypoints inherit the same `FieldMapPointPane` pointer handler. A left-button release over a point asks the parent `FieldMapPane` to select its node index. The parent moves the field-map marker, waits for the timer-driven animation to complete, and then calls `net_send_field_map_selection`.

The pointer event therefore does not cause an immediate network send. Depending on screen distance, the marker animation normally adds about 0.5 through 4 seconds. A selection at the marker's current position can complete without that travel delay.

There is also a separate command-line builder. It accepts `map_id`, `x`, and `y`, writes a zero checksum, and submits the same nine-byte body. This is not the normal clickable-waypoint path.

## Capture check

The supplied selection is:

```text
3F 00 00 0B C4 00 0E 00 0A
```

It means checksum `0`, map `0x0BC4`, and destination `(14, 10)`. These values match the `Loures` node in the preceding `SFieldMap` exactly.

## Server continuation

There is no direct RTTI response class paired only with this request. In the supplied successful sequence, the server follows it with unhandled control opcode `0x67`, then [`SMapSize`](../server/021-0x15-map-size.md) and the normal map-entry packets. The server must still validate the returned destination because the client body can be forged.
