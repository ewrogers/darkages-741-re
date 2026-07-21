# Effect.tbl

`Effect.tbl` maps an effect ID to a sequence of image-frame numbers. `file_load_effect_frame_table` reads the first decimal integer as the number of effect entries. It then reads the frame-number groups and stores each sequence with an internal `0xFF` terminator.

At runtime, `render_update_effect_frame` advances through that sequence. The image pool then asks the active EFA or EPF session for the selected image frame.

The sequence contains frame selectors only. It does not contain timing. Ordinary effects take their effective interval from the active EFA resource when nonzero, or from the packet fallback when the resource interval is zero.

For a positive interval, the runtime index is derived from elapsed time rather than simply incremented:

```text
sequence_index = (current_tick - effect_start_tick) / frame_interval_ms
frame_number = effect_sequence[sequence_index]
```

The internal `0xFF` marker ends the sequence. A loop-enabled effect resets its start tick and index to zero. A nonlooping effect becomes inactive and is removed from the world.

## Decode

```text
effect_count = read_first_decimal_integer()

for each of effect_count entries:
    read decimal frame numbers in order
    store the sequence
    append 0xFF as the in-memory end marker
```

## Encode

Write the same decimal frame numbers and entry separators expected by the source table. The `0xFF` marker belongs to the in-memory form and should not be emitted as a decimal frame unless a source table proves otherwise.

```text
for each effect sequence:
    write each frame number as decimal text
    write the preserved entry separator
```

The exact text separators and comment rules should be copied from a known compatible `Effect.tbl` until the text grammar receives its own fixture-based test.
