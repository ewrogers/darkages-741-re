# DAT archives

The asset DAT archives handled by `file_archive_open` are simple containers. Other files such as `sotp.dat` only share the extension. The local archives use a legacy format with a fixed-size name index followed by raw file payloads. The archive layer does not compress those payloads.

`file_archive_open` can open a loose DAT file or a Windows resource of type 10. All 22 DAT archives inspected in the local client installation use the legacy layout below.

## Legacy layout

```c
struct DatHeader {
    u32le index_count;       // includes the final blank sentinel
};

struct DatIndexEntry {
    u32le data_offset;       // absolute file offset
    char  name[13];          // at most 12 visible bytes, NUL padded
};                          // 17 bytes
```

The entries are sorted without regard to ASCII letter case. The final entry has a blank name. Its offset marks the end of the last real payload.

```text
size(entry[i]) = entry[i + 1].data_offset - entry[i].data_offset
```

Some archives have eight unused bytes after the last payload. The client does not include them in an entry. A new writer does not need to add them.

## Read an archive

```text
count = read_u32_le(file)
index = read_exactly(count * 17)

for i in 0 .. count - 2:
    name = nul_terminated(index[i].name)
    begin = index[i].data_offset
    end = index[i + 1].data_offset
    entry[name] = file[begin : end]
```

Validate every offset before slicing. Names should be unique after case folding and the index should remain sorted.

## Create or extend an archive

Rebuild the archive instead of inserting bytes into it. Adding one index row moves the start of every payload by 17 bytes.

```text
build_dat(entries):
    sort entries by lowercase ASCII name
    reject names longer than 12 bytes
    reject duplicate names after case folding

    count = entries.length + 1
    next_offset = 4 + count * 17

    write_u32_le(count)
    for entry in entries:
        write_u32_le(next_offset)
        write_fixed_name(entry.name, 13)
        next_offset += entry.data.length

    write_u32_le(next_offset)       // blank sentinel
    write_zero_bytes(13)

    for entry in entries:
        write(entry.data)
```

Replacing an entry uses the same process because later offsets may change. A round trip should compare every extracted payload, not necessarily the complete DAT byte for byte.

## UI layouts in setoa.dat

`setoa.dat` contains the underscore-prefixed text layouts used by many panes. A custom UI skin can replace one of those text entries and its referenced SPF or EPF art when the rebuilt archive keeps the normal name and offset rules.

Adding a new layout entry does not make the client load it. A pane constructor must request that filename and must construct controls for its named definitions. See [UI layout files](../systems/ui-layouts.md) for the grammar and code-to-control mapping.

## Extended layout

The reader also recognizes an extended format when the first word is `0xFFFFFFFF`. No matching local archive was found, so this path is useful evidence but not yet a safe writer target.

The extended header and index descriptors are XOR-obfuscated in 32-bit words. The index is split into chunks, and each chunk is inflated with zlib. Its decoded records use this shape:

```c
struct ExtendedDatNameRecord {
    u32le relative_data_offset;
    u32le name_length;
    u8    name[name_length];
};
```

`file_archive_open` adds a decoded data-base value to each relative offset. Several header fields and one chunk descriptor field remain unknown. Do not generate this variant until a real sample can be checked.

## Evidence

- `file_archive_open` at `0x00471E00`
- `file_archive_xor_words` at `0x00471DC0`
- `file_archive_find_entry` at `0x00472470`
- `file_archive_get_entry_data` at `0x00472900`
- `file_zlib_uncompress` at `0x006043B0`

Addresses are collected in the [function reference](../appendix/functions.md).
