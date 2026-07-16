# Change Weather (`SChangeWeather`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x1F` (31) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The class name says change weather, but this client does not route the packet into its main gameplay handler.

The constructor calls `net_server_packet_base_ctor` with opcode `0x1F` and installs the `SChangeWeather` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SChangeWeather {
    u8 opcode                  // 0x1F
    u8 value                   // exact meaning not confirmed
}
```

`net_decode_s_change_weather` reads the one-byte payload. The packet factory registers opcode `0x1F`, but the main gameplay dispatcher has no `0x1F` branch. No local state change or UI effect is therefore confirmed for this packet.

Active snowy art and falling snow are selected by `SMapSize` instead. See [Snow and weather](../../rendering/weather.md).
