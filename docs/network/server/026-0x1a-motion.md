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

The selected value becomes the delay for the first body-motion timer. It is not the animation's frame cadence or a guaranteed total visible lifetime:

- Table-driven human motions replace it with a client-side duration of 500, 1000, or 1500 ms.
- Human motion `0x16` divides the supplied duration by three.
- Other accepted human motions may retain the supplied duration.
- Monster motion selection leaves the supplied duration unchanged.

When motion selection succeeds, `world_living_start_motion` stores the direction, begins the object's transition state, increments a motion generation, and schedules timer event `0x02000001` using the final millisecond value. `world_living_handle_timer_event` ignores an older timer when its generation no longer matches. This keeps a previous motion from interrupting a newer one.

This is why `duration_10ms` is more precise than calling the field an unconditional on-screen duration.

The signed 16-bit conversion also means unusually large wire values can wrap after multiplication. Normal server values are expected to stay small.

### Frame ticks and transitions

After the first timer becomes due, the active human or monster image session advances its own motion data:

```c
if (timer.generation != living->motion_generation)
    return;                         // superseded motion

changed, finished, next_delay = image_session->advance_motion();

if (changed)
    rebuild_cached_sprite();

if (next_delay <= 0)
    next_delay = 80;                // shared fallback, milliseconds

schedule_motion_timer(next_delay, ++living->motion_generation);
```

The image session owns the current motion pointer, frame index, direction, and cached frame descriptor. A frame only dirties the living object when its descriptor or direction changes, so the client does not rebuild the composite sprite for an unchanged pose.

When an action sequence runs out of frames, the image session reports the transition, selects its standing motion for the same direction, and advances the first standing frame during the same callback. The living object then clears its transition state and keeps the timer chain running for any passive standing animation.

The four timed slots beginning at living-object offset `+0x194` use a different timer, `0x03000001`. They expire auxiliary motion or overlay state by absolute time and are not the body sprite's frame timeline.

### Passive standing loops

Human standing motion is normally a one-frame pose. Entering it supplies a 300 ms reset delay. The standing motion data itself has no positive per-frame delay, so the shared 80 ms fallback can be used while the first frame is advanced.

Monster standing data can produce a passive local loop without another server packet:

- If the resource has no animated standing frames, the client holds one frame for 10,000 ms.
- With one standing sequence, the cadence is the resource timing value times 100 ms, clamped to at least 100 ms.
- With distinct primary and alternate standing sequences, both use a 300 ms frame cadence.
- At each standing-segment boundary, `rand() % 100` is compared with a resource-defined threshold to select the next sequence.

The byte-sized resource accessors that supply the standing ranges, timing value, and selection threshold are confirmed, but their friendly metadata field names remain unresolved.

## Motion selection

The packet handler itself does not impose one animation range. The concrete image session decides whether the requested motion exists.

Human image sessions use fixed motions, the normal emote table, and appearance-dependent body motions in the `0x80` through `0xFF` range. An appearance-dependent motion starts only when the current body resources mark it as available.

Monster image sessions accept motion IDs `0x01`, `0x83`, `0x84`, and `0x85`, mapping them to one of the monster's cached motion resources. Other monster motion IDs are rejected.

## Relation to `CEmotion`

[`CEmotion`](../client/029-0x1d-emotion.md) sends an emotion request code. The normal client table stores that code separately from the body-motion ID expected in `SMotion`, so this is not normally a same-byte echo.

Project-owner runtime testing shows that the server accepts forged emotion requests outside the normal UI table. The receiving client has no global motion allowlist, although its image session still requires a supported animation resource.

## Sound

`SMotion` does not carry or play an optional sound in this client. Server-directed sound uses the separate [`SSoundEffect`](025-0x19-sound-effect.md) packet. A server can send that packet alongside a motion, but it is not part of the `SMotion` body.
