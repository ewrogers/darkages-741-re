# Effect.tbl

`Effect.tbl` maps an effect ID to a sequence of image-frame numbers. `file_load_effect_frame_table` reads the first decimal integer as the number of effect entries. It then reads the frame-number groups and stores each sequence with an internal `0xFF` terminator.

At runtime, `render_update_effect_frame` advances through that sequence. The image pool then asks the active EFA or EPF session for the selected image frame.

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
