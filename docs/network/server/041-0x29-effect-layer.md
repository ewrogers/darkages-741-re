# Effect Layer (`SEffectLayer`)

`SEffectLayer` creates a temporary world visual in one of three ways: at a map tile, attached to one or two existing objects, or moving between two objects. The first object ID selects the packet form.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x29` (41) |
| Transform | `derived` |
| Concrete class | RTTI class `SEffectLayer` |
| Gameplay owner | RTTI class `WorldPane` |
| Name provenance | Exact client RTTI |

## Body

```text
packet SEffectLayer {
    u8      opcode                    // 0x29
    u32     target_id

    if target_id == 0 {
        u16 target_animation
        u16 frame_interval            // fallback timer value
        u16 target_x
        u16 target_y
    } else {
        u32 source_id
        u16 target_animation
        u16 source_animation
        u16 frame_interval            // fallback timer value
    }
}
```

The coordinate form is `X` then `Y` on the wire. The parser stores these two values in reversed internal offsets, but the creation path restores their meaning: the first value becomes the static effect's common `tile_x` field and the second becomes `tile_y`.

## Object and coordinate modes

When `target_id` is zero, `net_handle_effect_layer_server_packet` creates one RTTI `WorldObject_StaticEffect` at `(target_x, target_y)`. Both coordinates must be inside the current map. An out-of-range position is ignored.

When `target_id` is nonzero, the handler creates an RTTI `WorldObject_ObjectEffect` attached to that object. If `source_id` is also nonzero and `source_animation` is greater than zero, it creates a second, independent object-attached effect on the source. These IDs are attachment anchors, not drawing coordinates.

The target animation must be greater than zero before either ordinary effect is created. Object IDs that are absent from the current world are ignored. This path does not request missing objects from the server.

Ordinary animation selectors are one-based packet values. The client subtracts one before selecting an `Effect.tbl` resource.

## Moving effect mode

Target animation values from `10000` through `11999` have a separate meaning. They require both object IDs and create one RTTI `WorldObject_MovingEffect` traveling from `source_id` to `target_id`:

```c
effect_index = target_animation - 10000;
create_moving_effect(source_id, target_id, effect_index);
```

The client computes the path from the two objects' current world positions. In this mode it ignores `source_animation` and the packet's `frame_interval`; client effect data supplies the movement style and step timing. The moving object uses the separate timer event `0x00010001` and schedules it with the path step interval stored on the object.

## Timing and special values

For ordinary static and attached effects, `frame_interval` is read as a signed 16-bit timer value. It is not the total effect duration. When the chosen effect resource has a nonzero client-side interval, `world_effect_start_animation` replaces the packet value with that resource interval. The packet value remains in use only when the resource interval is zero.

Ordinary effects use timer event `0x01000001`. The effect records its start time, effective interval, sequence index, selected frame, and active resource. For a positive interval, each tick derives the sequence position from elapsed time:

```c
sequence_index = (dispatcher_now - effect_start) / frame_interval;
```

This lets a delayed main-thread timer skip to the appropriate frame instead of slowing the entire effect. A zero interval advances the stored sequence index by one per callback.

The `0xFF` terminator in the in-memory `Effect.tbl` sequence marks completion. A loop-enabled static effect resets its start time and sequence index and selects frame zero again. An object-attached effect is constructed as nonlooping. When a nonlooping sequence ends, the client clears its active flag and detaches the effect.

The start routine computes a local `max(resource_interval, 50)`, but that result is not written to the timer field. The original resource or packet interval is what gets scheduled, so this path does not enforce an effective 50 ms minimum.

`target_animation == 0x00FF` is an explicit no-op sentinel. A zero target animation also creates nothing, including a possible source effect.

See [world rendering](../../rendering/world.md#effects), the [`Effect.tbl` frame table](../../file-formats/effect-table.md), and the [EFA effect format](../../file-formats/efa.md) for the client-side resources used after the packet is handled.
