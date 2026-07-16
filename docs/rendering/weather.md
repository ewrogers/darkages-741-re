# Snow and weather

Snowy ground and falling snow are separate systems. The server can enable either one through the flags in `SMapSize`.

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

The local weather setup behaves as follows:

| Mode | Local behavior |
| ---: | --- |
| 0 | No weather session |
| 1 | Create falling snow |
| 2 | No local setup |
| 3 | Change lighting-related state, not particles |

The server can also create normal world effects with `SEffectLayer`. That path could display rain-like art, but no direct link to rain is confirmed.

`SChangeWeather` exists as an RTTI-backed packet and contains one byte. The main gameplay dispatcher has no handler for its opcode in this client, so it does not control the active map weather path described above.
