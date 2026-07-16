# HEA light masks

HEA files store run-length rows used by the map lighting and occlusion system. They are not ordinary pictures, and they do not use zlib.

All 34 HEA files found in the inspected client data use the layout below.

## Layout

```c
struct HeaHeader {
    u32le unknown_00;        // observed as 0
    u32le unknown_04;        // observed as 640
    u32le unknown_08;        // observed as 480
    u32le unknown_0c;        // observed as 640
    u32le unknown_10;        // observed as 480
    u32le map_width;
    u32le map_height;
    u32le world_width;
    u32le row_count;         // matches world height in inspected files
    u32le band_count;
};                          // 0x28 bytes

u32le band_y[band_count];
u32le row_offset[band_count][row_count];
u16le runs[];
```

Each row offset is measured in 16-bit run words from the start of `runs`.

```c
struct HeaRun {
    u8 intensity_and_flags;  // low 6 bits are intensity
    u8 length;               // number of output pixels
};
```

`render_hea_decode_mask` caps or masks the intensity for the requested render path. The meaning of the top two low-byte bits is not confirmed.

## Decode a row

There is no row terminator. Stop when the requested output width has been filled.

```text
decode_hea_row(file, band, y, width):
    cursor = runs + row_offset[band][y]
    output = []

    while output.length < width:
        word = read_u16_le(cursor)
        length = word >> 8
        intensity = word & 0x3F
        append intensity length times

    return first width values
```

An inspected 40 by 40 map records a 3520 by 2080 world and four band thresholds at 0, 1000, 2000, and 3000. The client stores all bands. One confirmed view-building path ultimately selects band 0, so the live choice of later bands still needs runtime checking.

## Create a compatible file

A generated writer can split each row into runs of at most 255 pixels, record the current run-word offset, and write the packed words. Preserve the ten header values and band thresholds from a compatible map until their remaining roles are understood.

## Evidence

- RTTI class `HEASession`
- `file_hea_open` at `0x004875B0`
- `file_hea_build_row_views` at `0x00487380`
- `render_hea_decode_mask` at `0x005C8540`
