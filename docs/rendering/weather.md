# Snow and weather

Version 7.41 can create falling snow and dark-map lighting during map setup, but it drops later `SChangeWeather` updates. Snow-covered ground is a separate art choice.

```text
SMapSize flags
  |
  +-- bit 0x80 ---- alternate ground and static art
  |
  +-- low nibble -- local weather mode
```

## Snow-covered maps

Bit `0x80` calls `map_apply_seasonal_tile_mode` during map setup.

Alternate mode uses:

- `tileas.bmp` for ground, with `tilea.bmp` fallback
- `stsNNNNN.hpf` for static art, with `stcNNNNN.hpf` fallback

This is server-controlled map state. It normally changes when the server sends new map setup, such as during a map transition. It is not driven by the `SChangeWeather` packet.

## Falling snow

Weather mode 1 creates `WeatherSession_SnowParticle`. The session adds several `SnowParticlePane` image panes over the world view.

Each particle uses a resource named like `snowaNN.epf`. A 100 ms timer moves the particles downward, removes those below the pane, and creates replacements above the view.

Because the particles are panes, they join the normal UI render tree. They are not special DirectDraw primitives.

The seasonal bit and weather mode are independent. A map may use snowy art without falling snow, falling snow without snowy art, or both.

## Rain and other modes

No dedicated rain particle class, rain filename, or rain setup path was found.

The low-nibble mode values are defined by the shared [`MapFlags`](../network/protocol-types.md#mapflags) type. Locally, None creates no weather session, Snow creates falling snow, Rain performs no setup, and Darkness forces black ambient light with human-centered light masks.

The Rain and Darkness names are project-owner protocol vocabulary. The client contains an explicit mode-2 branch but performs no work in it, so rain may be server-driven through another effect or simply unsupported here.

Mode 3 writes the [world lighting state](lighting.md) directly by enabling the overall and object-light mask flags and setting ambient intensity and color to zero. `SDrawHumanObjects` can then attach a server-selected `mask1%02d.epf` light image to each human. Although the mode's numeric value is `Snow | Rain`, the client treats `3` as the exact Darkness mode. It does not combine the snow and rain behaviors or create a weather particle class.

The server can also create normal world effects with `SEffectLayer`. That path could display rain-like art, but no direct link to rain is confirmed.

## Why live weather changes are broken

[`SChangeWeather`](../network/server/031-0x1f-change-weather.md) is only partly connected:

1. The server packet factory registers opcode `0x1F`.
2. `net_decode_s_change_weather` reads its one-byte value.
3. `net_dispatch_server_packet` never checks for opcode `0x1F`.

The decoded object therefore reaches the gameplay dispatcher and is discarded. The existing `map_apply_weather_mode` routine is called only from `SMapSize`, so its snow and Darkness behavior normally changes only with map setup.

This looks like an incomplete packet integration, but the binary does not reveal why it shipped that way.

The [Weather packet runtime patch](../appendix/runtime-patches/weather-packet.md) adds the missing dispatch step. It interprets values `0` through `3` as the same modes used by `SMapSize`, applies the native weather routine, redraws the world, and refreshes map lighting. The lighting refresh matters when leaving Darkness because the weather routine alone does not restore the normal ambient color.

The patch does not add rain art. Value `2` still follows the client's native no-op branch.
