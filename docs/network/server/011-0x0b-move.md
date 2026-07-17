# Move (`SMove`)

`SMove` acknowledges a local movement request. A normal reply advances the world view from the server's previous position. A direction value of `4` takes a no-step correction path instead. The echoed step byte also supplies the client's movement round-trip sample.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x0B` (11) |
| Transform | derived |
| Runtime owner | `WorldPane` and `GUIBackPane` |
| Name provenance | Microsoft C++ RTTI in the target |

The constructor calls `net_server_packet_base_ctor` with opcode `0x0B` and installs the `SMove` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SMove {
    u8      opcode                    // 0x0B
    u8      direction                 // Direction; 4 selects correction
    u16     previous_x
    u16     previous_y
    u16     unknown_x                 // parsed, then ignored by client 7.41
    u16     unknown_y                 // parsed, then ignored by client 7.41
    u8      step                      // echoed CMove step
}
```

`direction` uses the shared [`Direction`](../protocol-types.md#direction) values for `0` through `3`. This packet alone also handles `4` as a control value rather than passing it to the direction helper.

`net_deserialize_move_server_packet` reads all six fields in this exact order. The two unresolved words have packet-object fields, so they are different from unconsumed trailing bytes. The only typed `SMove` handler reads `direction`, `previous_x`, `previous_y`, and `step`; it never reads `unknown_x` or `unknown_y`. No other registered server-packet consumer checks for opcode `0x0B`.

The binary therefore confirms that both words have no effect in client 7.41. Their server-side purpose cannot be recovered from this client. Visible-range coordinates remain a possible protocol explanation, but there is no local evidence for that name.

The client's logical display is 640 by 480, with an optional nearest-neighbor 2x presentation at 1280 by 960. No `SMove` path compares these words with either display size, pane bounds, tile visibility, or camera range. The supported display sizes therefore do not resolve the fields.

## Accepted movement

For directions `0` through `3`, `net_handle_move_server_packet` adds the cardinal delta to `previous_x` and `previous_y`, then publishes the result as the new world-view position:

```c
next = previous + direction_delta(direction);
world_set_view_position(next.y, next.x, false);
```

The local player object already moved when the client sent [`CMove`](../client/006-0x06-move.md). This reply advances the view from the server-supplied source coordinate. It does not move the object a second time.

## Rejected or corrected movement

Direction `4` skips the coordinate-delta helper. The client treats `previous_x` and `previous_y` as the server's current position:

1. If the local player object has different coordinates, send [`CRefreshUser`](../client/056-0x38-refresh-user.md).
2. Otherwise refresh the object's current motion and facing state.
3. Reset the `WorldPane` movement state.
4. Force the world view to `previous_y`, `previous_x`.

[`SUserPosition`](004-0x04-user-position.md) is the authoritative position packet used to replace the local object's coordinates and rebuild the view. The client-side control flow supports the observed server validation model: a refused or desynchronized step reaches direction `4`, and a coordinate mismatch requests a full refresh.

## Network indicator

Before sending `CMove`, the client increments `step` and records `timeGetTime()`. On `SMove`, it compares the echoed byte with the current movement counter. A mismatch still processes movement, but it does not update latency.

For a match, the sample is:

```c
round_trip_ms = timeGetTime() - last_move_send_time;
```

`GUIBackPane` stores that raw value, invalidates the indicator area, and chooses one of four images:

| Round trip | Indicator band |
| ---: | --- |
| `< 250 ms` | 1 |
| `250..349 ms` | 2 |
| `350..449 ms` | 3 |
| `450 ms or more` | 4 |

There is no moving average or other smoothing calculation in this path. The indicator can appear steadier because stale step replies are excluded and the raw result is reduced to four broad bands. Each new `CMove` replaces the one saved timestamp, so only a reply echoing the latest step can update the display.
