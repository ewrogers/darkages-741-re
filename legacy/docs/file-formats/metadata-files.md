# Metadata files

The client metadata cache contains named zlib streams such as `metafile/Light`. These files are separate from the `.dat` fastfile archives and from packet encryption.

## Compression

The version-741 `Light` file begins with standard zlib bytes `78 9C`. Ordinary zlib decompression expands it from 218 bytes to 762 bytes.

```c
result = uncompress(output, &output_size, input, input_size);
```

No XOR step is applied to the decompressed metadata records.

## Record container

The decompressed format is a big-endian counted collection:

```text
u16be entry_count
repeat entry_count times:
    string[u8 length] entry_name
    u16be value_count
    repeat value_count times:
        string[u16be length] value
```

Values are text. Numeric fields in `Light` are stored as decimal ASCII rather than binary integers.

Minimal parser pseudocode:

```c
entry_count = read_u16_be(p);
p += 2;

for (i = 0; i < entry_count; i++) {
    name_length = *p++;
    name = p;
    p += name_length;

    value_count = read_u16_be(p);
    p += 2;

    for (j = 0; j < value_count; j++) {
        value_length = read_u16_be(p);
        p += 2;
        value = p;
        p += value_length;
    }
}
```

Production code must validate every length against the decompressed buffer boundary.

## `Light` schema

The current file has 34 entries:

- Twelve profile records named `Default_0` through `Default_b`.
- Twenty-two map-ID records that select the profile name `Default`.

Each profile record has six values:

```text
start_slot, end_slot, light, red, green, blue
```

Each map record has one value containing the profile name. The client converts these records into the lookup structure used by `lighting_lookup_map_profile` at `0x4AEAD0`.

See [Map lighting and masks](../map/lighting.md) for the current profile values, map list, HEA interaction, and viewport blend.
