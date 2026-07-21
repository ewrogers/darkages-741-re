# Album.dat

`album.dat` is the local photo album for one character. It stores up to 100 rendered portraits, their captions, and the time of the last successful capture. It is not a server cache and is never sent as a whole.

The path is:

```text
.\<character>\album.dat
```

All integers are little-endian. The file has no magic value or version field.

```text
file Album {
    record header {
        u32le capacity            // +0x00, normally 100
        u32le last_capture_time   // +0x04, time_t seconds
        u32le record_table_offset // +0x08, normally 0x40
        u32le payload_base_offset // +0x0C, 0x40 + capacity * 0x60
        bytes reserved[0x30]      // +0x10
    }                             // 0x40 bytes
    at header.record_table_offset {
        repeat header.capacity {
            record entry {
                u32le flags           // +0x00, bit 0 means active
                u32le width           // +0x04
                u32le height          // +0x08
                u32le payload_offset  // +0x0C, from payload_base_offset
                u32le compressed_size // +0x10
                bytes caption[0x4C]   // +0x14, NUL-terminated local bytes
            }                         // 0x60 bytes
        }
    }
    at header.payload_base_offset {
        bytes zlib_payloads[to end_of_file]
    }
}
```

The record table always has `capacity` entries. Compressed payloads for active records follow it. The ordinary client-created file uses capacity 100, a record table at `0x40`, and a payload base at `0x25C0`.

## Pixel payloads

Each active record expands to:

```text
width * height * 2 bytes
```

`file_album_add_portrait` normalizes the client's active 16-bit pixel packing when required, then zlib-compresses the complete buffer with the library's default level. `file_album_record_replace_pixels` retains the compressed bytes and also inflates a display copy in memory.

Ordinary portrait captures are 48 pixels wide and 56 pixels high. The caption is the local `ctime` text for the capture, with its trailing newline removed.

## Load and save behavior

`file_album_load` accepts capacities from 1 through 100. It reads the complete `0x60`-byte record table, validates each active payload read, and inflates the pixels. A failed header, record, payload, allocation, or decompression step rejects the file.

`file_album_save` rewrites the complete file when the in-memory dirty flag is set:

1. Recompute each active payload offset.
2. Write the `0x40`-byte header.
3. Write `0x60` bytes for every record.
4. Append each active compressed payload in slot order.

Removing a portrait clears its record and rewrites the file. Moving a portrait copies the source record into the destination and clears the source. Neither operation changes the exported portrait file.

## Capture time

The header's second field is the source of the one-hour client cooldown. A successful normal capture writes `time(NULL)` there. The album viewer and portrait uploader do not enforce that interval.

See [Screenshots and the photo album](../systems/screenshots-and-photo-album.md) for the UI flow.
