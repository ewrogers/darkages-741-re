# Change Weather (`SChangeWeather`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x1F` (31) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The packet is named for a live weather update, but version 7.41 decodes and then drops it before it can change the world.

The constructor calls `net_server_packet_base_ctor` with opcode `0x1F` and installs the `SChangeWeather` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SChangeWeather {
    u8      opcode                    // 0x1F
    u8      value                     // native meaning not confirmed
}
```

`net_decode_s_change_weather` stores `value` in the derived packet object. The packet factory registers opcode `0x1F`, but `net_dispatch_server_packet` has no `0x1F` branch. The unmodified client therefore produces no state change or UI effect.

The packet's exact value table cannot be confirmed from a native consumer because that consumer is missing. The [Weather packet runtime patch](../../appendix/runtime-patches/weather-packet.md) deliberately maps values `0` through `3` to the modes already implemented for `SMapSize`:

| Value | Patched behavior |
| ---: | --- |
| `0` | Stop the weather overlay and restore normal map lighting |
| `1` | Create the native falling-snow overlay |
| `2` | Follow the native Rain branch, which performs no setup |
| `3` | Enable native Darkness lighting |

Active snowy art and falling snow are selected by `SMapSize` instead. See [Snow and weather](../../rendering/weather.md).

The optional patch changes only dispatch after decoding. Framing, the derived transform, and packet construction remain native.
