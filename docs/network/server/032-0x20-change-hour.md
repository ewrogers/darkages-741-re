# Change Hour (`SChangeHour`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x20` (32) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends a coarse time step that selects the current map-lighting profile. The client changes ambient color and darkness immediately, then enables or disables the map's HEA spatial light mask as needed.

The constructor calls `net_server_packet_base_ctor` with opcode `0x20` and installs the `SChangeHour` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SChangeHour {
    u8 opcode                  // 0x20
    u8 time_step               // scaled by two and clamped to 24
    u8 unread_tail[]           // optional server bytes ignored by this client
}
```

`net_deserialize_change_hour_server_packet` reads exactly one byte after the opcode. A supplied decoded body was `20 07 27`, so the client uses `0x07` and leaves `0x27` unread. The common parser allows unread bytes at the end of a body. The extra byte therefore cannot affect the 7.41 client, and its server-side meaning remains unknown.

## Lighting update

`net_handle_change_hour_server_packet` stores `time_step` in `WorldPane`, then calls `world_update_map_lighting`. The lighting coordinate is:

```text
profile_time = min(time_step * 2, 24)
```

The observed value `7` therefore selects coordinate `14`. Values `0` through `11` select the even coordinates `0` through `22`; `12` and larger select `24`.

The exact RTTI class `LightList` searches the cached `Light` metadata for an entry covering the current map and profile coordinate. That entry supplies ambient red, green, blue, intensity, and a flag that can prevent HEA use. If HEA is permitted and intensity is below `0x20`, the client loads the current map's `%06d.hea` mask. Otherwise it renders without that spatial mask.

The same update runs after [`SMapSize`](021-0x15-map-size.md), so a newly loaded map uses the latest stored time step.

## Clock UI

No current sundial update was found. The RTTI-backed `ClockPane` loads `lodclk.epf` and advances it on its own timer as a loading animation. It is not called by this packet. The older sundial behavior is useful historical context, but it is not present in the traced 7.41 path.

See [Map lighting](../../rendering/lighting.md), [HEA light masks](../../file-formats/hea.md), the mapped [world lighting state](../../appendix/runtime/world.md#world-lighting-state), and the related unhandled [`SChangeDay`](030-0x1e-change-day.md).
