# HEA light masks

HEA files store run-length rows used by the map lighting and occlusion system. They are not ordinary pictures, and they do not use zlib.

All 34 HEA files found in the inspected client data use the layout below.

## Layout

```text
file Hea {
    record header {
        u32le unknown_00      // observed as 0
        u32le screen_width    // 640, logical screen width
        u32le screen_height   // 480, logical screen height
        u32le unknown_0c      // observed as 640
        u32le unknown_10      // observed as 480
        u32le map_width
        u32le map_height
        u32le canvas_width    // padded mask width in pixels
        u32le canvas_height   // pixel scanlines and offsets per band
        u32le band_count
    }                         // 0x28 bytes
    repeat header.band_count {
        u32le band_start_x    // horizontal canvas pixel
    }
    repeat header.band_count {
        repeat header.canvas_height {
            u32le row_offset // measured in 16-bit words from runs
        }
    }
    repeat to end_of_file {
        record run {
            u8 intensity_and_flags // low 6 bits are intensity
            u8 length              // number of output pixels
        }
    }
}
```

## Header fields

| Field | Meaning |
| --- | --- |
| `unknown_00` | Zero in all inspected files. No confirmed reader use. |
| `screen_width`, `screen_height` | The fixed 640 by 480 logical screen dimensions. The projection uses them as canvas margins. |
| `unknown_0c`, `unknown_10` | Also 640 and 480 in every inspected file, but unused by the confirmed reader path. |
| `map_width`, `map_height` | Map dimensions in tiles. |
| `canvas_width`, `canvas_height` | Dimensions of the padded isometric mask in pixels. `canvas_height` is also the number of row offsets stored per band. |
| `band_count` | Number of horizontal RLE seek checkpoints. |

## Screen-space padding

The first `640` and `480` match the client's fixed [logical screen dimensions](../rendering/lifecycle.md). `file_hea_project_map_position` adds them as horizontal and vertical margins when it projects map axes into the HEA mask canvas:

```text
canvas_x = (axis_a - axis_b + map_height) * 28 + screen_width
canvas_y = (axis_a + axis_b) * 14 + screen_height
```

The complete mask canvas keeps one screen of padding on every side:

```text
canvas_width  = (map_width + map_height) * 28 + 2 * screen_width
canvas_height = (map_width + map_height) * 14 + 2 * screen_height
```

These equations hold for all 34 inspected HEA files. The duplicated `640` and `480` at `unknown_0c` and `unknown_10` are not read by the confirmed open, projection, clipping, or decoding path, so their purpose remains unknown.

## Bands and row offsets

A band is a horizontal seek checkpoint in the mask canvas. It is not a lighting level, animation stage, or map-tile row. Each band stores one `band_start_x` value and a complete table of `canvas_height` row offsets:

```text
canvas_x:     0               1000            2000
              | band 0        | band 1         | band 2

scanline y:   row_offset[0][y] row_offset[1][y] row_offset[2][y]
              |               |                |
              +------ pointers into the shared run stream ------+
```

For a given pixel scanline, `row_offset[band][y]` points to the first run at `band_start_x[band]`. The offset is a count of 16-bit run words from the start of `runs`, not a byte offset.

All 34 inspected files use ascending checkpoints beginning at zero and spaced 1000 pixels apart. Their count follows:

```text
band_count = ceil(canvas_width / 1000)
band_start_x[i] = i * 1000
```

Every one of the 698,240 inspected nonzero-band row offsets lands after runs that decode to exactly its `band_start_x`. This confirms that the later tables are horizontal shortcuts into the same decoded scanline.

The natural lookup is:

```text
band = largest i where band_start_x[i] <= requested_left_x
cursor = &runs[row_offset[band][canvas_y]]
skip = requested_left_x - band_start_x[band]
```

Client 7.41 scans the checkpoint array and computes that band index, but does not use it. `file_hea_build_row_views` always reads row pointers from band 0 and measures the horizontal skip from `band_start_x[0]`. It is the only caller-backed row-view path in this binary. Later band tables are valid seek data in the files, but this client does not use their acceleration.

## Decode a row

The decoder starts at one scanline pointer, consumes runs until it reaches the requested horizontal position, then emits the requested number of pixels. There is no row terminator.

```text
decode_hea_row(file, band, canvas_y, start_x, width):
    cursor = &runs[row_offset[band][canvas_y]]
    skip = start_x - band_start_x[band]

    while skip >= cursor.length:
        skip -= cursor.length
        cursor++

    output = []

    while output.length < width:
        available = cursor.length - skip
        append cursor.intensity up to available times
        skip = 0
        cursor++

    return first width values
```

Each stored run is still the two-byte record shown in the layout: the high byte is its pixel length and the low six bits are its intensity. `render_hea_decode_mask` caps or masks that intensity for the requested render path. The meaning of the top two low-byte bits is not confirmed.

For example, an inspected 40 by 40 map records a 3520 by 2080 pixel mask canvas and four checkpoints at 0, 1000, 2000, and 3000. Its height follows `(40 + 40) * 14 + 2 * 480 = 2080`, so each of its four bands stores 2080 row offsets.

## Runtime selection

[`SChangeHour`](../network/server/032-0x20-change-hour.md) does not select a band or a separate HEA file directly. Bands only organize horizontal seek points inside one mask. The packet selects a `Light` metadata profile for the current map. When that profile permits HEA and its ambient intensity is below `0x20`, `map_load_hea_resource` opens the current map ID as `%06d.hea` and enables the spatial mask. Brighter profiles disable the mask.

See [Map lighting](../rendering/lighting.md) for the complete update flow.

## Create a compatible file

A generated writer can split each pixel scanline into runs of at most 255 pixels, record the current run-word offset, and write the packed words. To reproduce the local form, split runs at each 1000-pixel checkpoint and record a row offset there. The band count then follows `ceil(canvas_width / 1000)`. Preserve `unknown_00`, `unknown_0c`, and `unknown_10` from a compatible file until their roles are understood.

## Evidence

- RTTI class `HEASession`
- `file_hea_open` at `0x004875B0`
- `file_hea_project_map_position` at `0x004876D0`
- `file_hea_build_row_views` at `0x00487380`
- `map_load_hea_resource` at `0x005C7870`
- `render_hea_decode_mask` at `0x005C8540`
