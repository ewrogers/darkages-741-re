# Motion (`SMotion`)

`SMotion` starts a body animation on an existing living world object. The packet identifies the object, selects a motion, and supplies a timing value in 10 ms units.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x1A` (26) |
| Transform | `derived` |
| Concrete class | RTTI class `SMotion` |
| Gameplay owner | RTTI class `WorldPane` |
| Name provenance | Exact client RTTI |

## Body

```text
packet SMotion {
    u8      opcode                    // 0x1A
    u32     object_id
    u8      animation                 // body-motion ID
    u16     duration_10ms             // initial duration in 10 ms units
}
```

`net_deserialize_motion_server_packet` consumes exactly these fields. All multibyte values follow the packet layer's big-endian rule.

There is no sound byte in the version 741 reader. A trailing byte would remain unconsumed and cannot select a sound through this handler.

## Object handling

`net_handle_motion_server_packet` finds `object_id` in the current world and accepts only common object kinds `1` and `2`. It then requires an RTTI cast to `WorldObject_Living` and checks that the living object has a usable image session.

If those checks pass, the handler keeps the object's current facing direction and calls its class-specific body-motion method with the animation and timing values. A missing object, a nonliving object, or an unavailable image session is ignored. Unlike several other object packets, this path does not send [`CRequestObject`](../client/012-0x0c-request-object.md) when the object is missing.

## Timing behavior

The handler converts the wire value to milliseconds before starting the motion:

```c
duration_ms = (s16)((s16)packet.duration_10ms * 10);
living->start_motion(packet.animation, living->direction, duration_ms);
```

The final duration is an animation lifetime, but the wire value is only its initial value:

- Table-driven human motions replace it with a client-side duration of 500, 1000, or 1500 ms.
- Human motion `0x16` divides the supplied duration by three.
- Other accepted human motions may retain the supplied duration.
- Monster motion selection leaves the supplied duration unchanged.

When motion selection succeeds, `world_living_start_motion` increments a motion generation and schedules timer event `0x02000001` using the final millisecond value. `world_living_handle_timer_event` ignores an older timer when its generation no longer matches, then advances the living animation for the current timer. This keeps a previous motion from interrupting a newer one.

This is why `duration_10ms` is more precise than calling the field an unconditional on-screen duration.

The signed 16-bit conversion also means unusually large wire values can wrap after multiplication. Normal server values are expected to stay small.

## Motion selection

The packet handler itself does not impose one animation range. The concrete image session decides whether the requested motion exists.

Human image sessions use fixed motions, the normal emote table, and appearance-dependent body motions in the `0x80` through `0xFF` range. An appearance-dependent motion starts only when the current body resources mark it as available.

Monster image sessions accept motion IDs `0x01`, `0x83`, `0x84`, and `0x85`, mapping them to one of the monster's cached motion resources. Other monster motion IDs are rejected.

## Relation to `CEmotion`

[`CEmotion`](../client/029-0x1d-emotion.md) sends an emotion request code. The normal client table stores that code separately from the body-motion ID expected in `SMotion`, so this is not normally a same-byte echo.

Project-owner runtime testing shows that the server accepts forged emotion requests outside the normal UI table. The receiving client has no global motion allowlist, although its image session still requires a supported animation resource.

## Sound

`SMotion` does not carry or play an optional sound in this client. Server-directed sound uses the separate [`SSoundEffect`](025-0x19-sound-effect.md) packet. A server can send that packet alongside a motion, but it is not part of the `SMotion` body.
