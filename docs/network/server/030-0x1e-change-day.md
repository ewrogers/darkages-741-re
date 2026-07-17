# Change Day (`SChangeDay`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x1E` (30) |
| Encoding | session key |
| Name provenance | Project-owner protocol vocabulary; no RTTI class exists in this client |

## Purpose

The server sends this message as a day or clock update, but no 7.41 consumer was found. The packet remains useful as a compatibility clue because older clients reportedly used this update for a sundial-style clock.

## Observed body

One supplied decoded body was:

```text
1E 06 00 00
```

The client provides no parser from which to recover field boundaries. The three bytes after the opcode therefore remain opaque:

```text
packet SChangeDay {
    u8      opcode                    // 0x1E
    bytes   data[3]                   // observed as 06 00 00; meaning unresolved
}
```

## Client handling

`net_server_packet_factory_ctor` has no registration for opcode `0x1E`, so no parsed server packet object is created. `net_dispatch_server_packet` also has no parsed or raw `0x1E` branch. No pane handler or state write for the raw body was found, so current evidence says the decoded event falls through unused.

There is an RTTI class named `ClockPane`, but it displays the independent `lodclk.epf` loading animation. It is timer-driven and has no `SChangeDay` connection in this client.

The related [`SChangeHour`](032-0x20-change-hour.md) remains active and controls [map lighting](../../rendering/lighting.md).
