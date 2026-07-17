# Map lighting

Map lighting combines a server-selected time step, cached `Light` metadata, a packed ambient color, and optional spatial masks. Ordinary dark maps may use an HEA mask. A map in Darkness mode instead starts from black and opens player-sized visible areas with light images attached to human objects.

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

## Darkness and lantern-style light

[`SMapSize`](../network/server/021-0x15-map-size.md) low-nibble mode `3` is the local switch for this path. The client enables its overall light mask and dynamic object-light merge, then sets ambient intensity and color to zero. It does not combine the Snow and Rain behaviors implied by the bits in the value.

On these maps, the normal-human form of [`SDrawHumanObjects`](../network/server/051-0x33-draw-human-objects.md) supplies a one-byte `light_mask_id`. The handler interprets that byte only while map mode `3` is active:

```text
light_mask_id == 0  -> remove the object's light image
light_mask_id > 0   -> load mask1%02d.epf
```

For example, selector `1` names `mask101.epf`. `render_light_bitmap_ctor` loads frame zero, and `render_set_object_light_mask` attaches it to the human. The viewport builder centers each attached image on its object and combines it with the current light mask using the brighter value at each pixel. Moving, changing, or removing the object invalidates the affected rectangle so the light follows it.

This matches the observed Andor lantern behavior: most of the view remains dark while a lantern opens a limited area around its carrier. The client does not derive the selector from [`SAddEquip`](../network/server/055-0x37-add-equip.md), an equipment slot, or an item name. The only callers that attach or remove these images are in the `SDrawHumanObjects` handler. The server therefore sends an already resolved mask choice. Which lantern maps to which selector remains server-owned behavior and is not recoverable from this client alone.

This is also separate from the blinded state in [`SStatus`](../network/server/008-0x08-status.md). The two effects may look similar in play, but Darkness uses the world light-mask compositor rather than setting the status blind flag.

## Day and clock messages

[`SChangeDay`](../network/server/030-0x1e-change-day.md) has no RTTI class or active handler in 7.41. The similarly named RTTI `ClockPane` is also unrelated: it displays the timer-driven `lodclk.epf` loading animation. No current-client sundial movement was found.
