# Raw map tile banks

Ground art comes from two resources named `tilea.bmp` and `tileas.bmp`. Despite their names, they are not Windows BMP files. They have no file header, size fields, or embedded palette.

The names are best read as base and alternate banks:

| Resource | Role |
| --- | --- |
| `tilea.bmp` | Base ground art |
| `tileas.bmp` | Alternate ground art, used for snowy or seasonal maps |

The server selects the alternate bank with bit `0x80` in the `SMapSize` flags byte. If an alternate tile is missing, the client falls back to the same tile ID in the base bank.

The local banks contain 19,415 base records and 19,243 alternate records. The different counts are safe because of that fallback.

## Record layout

Each tile is one fixed-size record:

```text
file RawMapTileBank {
    repeat to end_of_file {
        record tile {
            repeat 27 {
                bytes palette_index_row[56]
            }
        }                     // 0x5E8 bytes
    }
}
```

Only the diamond inside the 56 by 27 rectangle is visible.

```text
row widths:
  4, 8, 12, ... 52, 56, 52, ... 12, 8, 4

visible pixels per tile:
  784
```

`file_decode_raw_map_tile` reads the record, ignores padding outside the diamond, and converts each palette index to the renderer's 16-bit color format. The palette choice comes from the bank type rather than the file itself.

## Decode

```text
record = file_bytes + tile_id * 0x5E8
output = []

for row in 0 .. 26:
    left = abs(13 - row) * 2
    width = 56 - left * 2

    for x in left .. left + width - 1:
        output.push(palette_to_u16(record.rows[row][x]))
```

The result is 784 packed pixels, or 1,568 bytes in the 16-bit render format.

## Storage and cache

`MapTileImageLib` owns two RTTI-backed `BMPMapTileStorage` objects. The constructor resolves `tilea.bmp` and `tileas.bmp` through the map-tile archive, and each storage object retains the archive entry, byte size, and palette selector used by `file_decode_raw_map_tile`.

The library also contains a decoded-tile cache API. One cache entry holds a valid flag and a reusable 0x620-byte pixel buffer. The code can grow the entry array, allocate buffers in batches, invalidate one entry, or reset all entries without freeing their buffers. No local code or data reference reaches the cache store and invalidate methods, so this analysis does not treat that cache path as active gameplay behavior.

## Create a bank

Write records back to back with no header. Set padding bytes to zero and place the visible indexes into the same diamond shape.

```text
for each tile:
    record = 0x5E8 zero bytes
    copy 784 palette indexes into the diamond rows
    write record
```

An alternate bank may be shorter than the base bank. Missing alternate records use base art at runtime.

For PNG output, place the 784 visible palette indexes in a 56 by 27 RGBA image and set padding outside the diamond to alpha 0. The ground pixels inside the diamond are opaque. See [Exporting images](image-export.md).

## Static art uses the same map mode

The same `SMapSize` bit also changes fixed map objects:

- Base mode opens `stcNNNNN.hpf`.
- Alternate mode first tries `stsNNNNN.hpf`.
- A missing `sts` resource falls back to `stc`.

This lets the ground and walls change together without changing the tile IDs stored in the map.

RTTI also exposes `CTFMapTileStorage` and `DTFMapTileStorage`. Their constructors use the same archive-entry ownership pattern, and their readers accept different in-memory tile layouts. No active caller constructs either class in this client.
