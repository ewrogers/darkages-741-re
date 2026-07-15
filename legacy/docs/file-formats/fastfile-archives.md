# Fastfile `.dat` archives

The common archive implementation begins at `file_fastfile_open_archive` (`0x471E00`). It first looks for a PE resource of type 10 with the requested archive name. If no resource exists, it opens the disk file read-only, creates a file mapping, and maps the entire archive.

The client supports two archive generations.

## Legacy format

If the first little-endian `u32` is not `0xFFFFFFFF`, it is treated as the entry count. The index begins immediately afterward and uses 17-byte records:

```c
struct legacy_fastfile_entry {
    u32 data_offset;
    char name[13];
};
```

Names are case-insensitive and limited to 12 visible characters plus the terminator. The index is searched with `bsearch`. An open logical entry derives its size from the next stored data offset.

Legacy archive metadata and entry bytes are not transformed by this layer.

## Extended format

An initial `0xFFFFFFFF` selects the extended format. It adds XORed metadata, compressed chunks, and variable-length entry names.

The startup calls pass an archive-specific XOR key as the fourth argument to `file_fastfile_open_archive`. Most archives in this client pass zero. The 16-byte top-level header always uses `0xFFFFFFFF` as its XOR key.

### Metadata XOR

`file_xor_u32_words` (`0x471DC0`) applies the same operation for decoding and encoding:

```c
void xor_u32_words(void *data, u32 size, u32 key)
{
    u32 *words = (u32 *)data;
    u32 i;

    for (i = 0; i < size / 4; i++) {
        words[i] ^= key;
    }
}
```

Only complete 32-bit words are processed. A non-multiple-of-four tail would remain unchanged.

The extended loader performs these steps:

1. Copy the 16-byte header at file offset 4 and XOR all four words with `0xFFFFFFFF`.
2. Use the header's index-descriptor offset to copy a 12-byte descriptor.
3. XOR the descriptor with the archive-specific key.
4. Allocate an array of eight-byte entry lookup pairs and an array of 16-byte chunk descriptors.
5. Copy and XOR every chunk descriptor with the archive-specific key.
6. Inflate each chunk.
7. Walk variable-length records from the inflated chunks and build the searchable entry lookup array.

The directly observed descriptor fields are:

```c
struct fastfile_index_descriptor {
    u32 entry_count;
    u32 chunk_count;
    u32 chunk_descriptor_offset;
};

struct fastfile_chunk_descriptor {
    u32 source_offset;
    u32 compressed_size;
    u32 uncompressed_size;
    u32 unknown_0c;
};
```

The 16-byte top-level header includes the index-descriptor offset and a base added to each entry data offset. The roles of its other two words are not yet named with confidence.

Inflated entry records begin with a relative data offset and a name length. The name follows at offset 8. The client advances by `8 + name_length` bytes and stores separate pointers to the record and its name for case-insensitive lookup.

## Compression

`file_zlib_uncompress` (`0x6043B0`) is an embedded zlib-compatible `uncompress` wrapper. Its initializer passes the literal version string `1.1.3`. The archive loader supplies the destination capacity from `uncompressed_size`, the mapped source at `source_offset`, and `compressed_size`.

Equivalent calling logic is:

```c
u32 output_size = chunk.uncompressed_size;

result = file_zlib_uncompress(
    output,
    &output_size,
    mapped_file + chunk.source_offset,
    chunk.compressed_size
);
```

This is compression, not packet encryption. No external source was used to identify the version. The version string and wrapper call pattern are both present in the client. See [Compression](compression.md) for the complete recovered chunk loop and implementation notes.

## Runtime archive interface

| Function | Address | Role |
|---|---:|---|
| `file_fastfile_ctor` | `0x471CD0` | Initialize one archive object |
| `file_fastfile_open_archive` | `0x471E00` | Map and index a resource or disk archive |
| `file_fastfile_open_entry` | `0x472470` | Find a name and reserve a logical handle |
| `file_fastfile_close_entry` | `0x472760` | Release a logical handle slot |
| `file_fastfile_read_entry` | `0x472790` | Copy bytes and advance the entry position |
| `file_fastfile_get_entry_data` | `0x472900` | Return a direct mapped or inflated pointer |
| `file_fastfile_get_entry_size` | `0x472BE0` | Return the logical entry size |
| `file_fastfile_get_main_archive` | `0x472C70` | Return the `Legend.dat` or `DarkAges.dat` singleton |

Non-main archives may redirect a missing name to the main archive before failing.
