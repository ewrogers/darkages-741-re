# Map lighting

Map lighting combines a server-selected time step, cached `Light` metadata, a packed ambient color, and an optional HEA spatial mask. The HEA file does not decide the time of day by itself. It supplies map-shaped light data only when the active profile asks for it.

```text
SChangeHour time_step
        |
        v
min(time_step * 2, 24)
        |
        v
Light metadata entry for map and time
        |
        +-- ambient RGB and intensity
        |
        +-- HEA permitted and intensity below 0x20
                    |
                    v
             load %06d.hea
```

## Selecting the profile

[`SChangeHour`](../network/server/032-0x20-change-hour.md) stores its one meaningful byte in `WorldPane`. `world_update_map_lighting` doubles it and clamps the result to `24`. The exact RTTI class `LightList` then finds an entry whose map and inclusive time range match the current state.

The server value behaves like a coarse half-day clock position rather than a literal 24-hour value. For example, value `7` selects profile coordinate `14`.

## Light metadata entry

The selected entry supplies:

- an inclusive starting and ending profile coordinate
- ambient intensity
- red, green, and blue bytes, packed into the renderer's 16-bit color
- flags, where bit `0` prevents the HEA path when set

If no matching metadata is available, the client uses black color, intensity `0x20`, disables the HEA mask, and retries the lookup one second later. Map setup also creates `LightList` when needed and reapplies the stored time after the map changes.

## HEA relationship

When the entry permits HEA and ambient intensity is below `0x20`, `map_load_hea_resource` opens the current map ID as `%06d.hea`. A successful load enables the spatial mask and rebuilds its visible region. At intensity `0x20` or above, the client disables that mask and redraws with ambient lighting alone.

The [HEA format](../file-formats/hea.md) stores run-length rows and bands. The time profile selects whether the mask participates; it does not select a different HEA filename for each hour.

## Day and clock messages

[`SChangeDay`](../network/server/030-0x1e-change-day.md) has no RTTI class or active handler in 7.41. The similarly named RTTI `ClockPane` is also unrelated: it displays the timer-driven `lodclk.epf` loading animation. No current-client sundial movement was found.
