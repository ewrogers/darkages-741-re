# Damage Effect (`SDamageEffect`)

`SDamageEffect` briefly draws a server-supplied health meter over one world object. The same packet can also play a numeric sound effect. It is display feedback only: the handler does not change the object's health state.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x13` (19) |
| Transform | `derived` |
| Visual owner | `WorldPane` and exact RTTI `WorldObject_Damage` |
| Name provenance | Exact Microsoft C++ RTTI in the target |

## Body

```text
packet SDamageEffect {
    u8  opcode                    // 0x13
    u32 object_id
    u8  unknown_consumed_unused
    u8  health_percent
    u8  sound_id_or_ff
}
```

All fields are always present. `0xFF` in `sound_id_or_ff` means no sound; it does not shorten the body.

## Handling

The handler processes sound before it validates the visual:

1. If `sound_id_or_ff` is not `0xFF`, pass its signed-extended value to [`audio_play_sound_effect`](../../audio/sound-effects.md).
2. Treat `health_percent` as signed and accept only `0` through `100`.
3. Convert a valid percentage to `floor(health_percent / 4)`, producing stage `0` through `25`.
4. Resolve `object_id` in the live world and replace any existing damage overlay attached to that object.
5. Create `WorldObject_Damage`, select the stage image, and schedule its removal.

Sound can therefore play even when the percentage is invalid or the target no longer exists. Values `0x80` through `0xFE` are also sign-extended before playback; the ordinary practical sound range is not established by this handler alone.

The unknown byte is copied by the handler but never used. A missing target produces no object-data request and no delayed replay.

## Generated meter image

The client generates the meter instead of loading it from an art file. `World::DamageEffectImage` builds one `130` by `27` canvas containing 26 adjacent `5` by `27` stages. The selected stage is drawn over the target object.

| Stage | Input percentage | Palette index |
| --- | --- | --- |
| `0` through `5` | `0` through `23` | `0x28` |
| `6` through `12` | `24` through `51` | `0x97` |
| `13` through `25` | `52` through `100` | `0x89` |

These are palette indexes, not fixed RGB colors.

## Lifetime and replacement

Each overlay schedules timer ID `1` for exactly `2000 ms`. The timer carries a generation token, so an older callback cannot remove a newer replacement. A repeated packet for the same target removes the existing overlay and restarts the two-second lifetime.

The object also stores a threshold at the current dispatcher time plus `1900 ms`, which is 100 ms earlier than the removal timer. The reason for that earlier stored threshold is unresolved.

## Pairing and limits

No client reply is sent. The packet can follow attacks, spells, or other server-side damage decisions, but the client does not enforce a specific request pair.

The class factory, deserializer, world helper, generated image, overlay object, renderer, and timer functions are listed in the [function reference](../../appendix/functions.md).
