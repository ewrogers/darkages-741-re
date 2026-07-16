# Metadata files

Metadata is a small server-managed database. The client keeps compressed files under `metafile/`, checks the inflated bytes with CRC32, then parses named groups of length-prefixed values.

Local examples include item information, lighting, NPC illustrations, nation descriptions, class data, and event data. Every inspected local metadata cache file is a standard zlib stream. Their inner value meanings are table-specific.

## Decoded container

All counts and lengths are big-endian.

```c
struct MetadataTable {
    u16be group_count;
    MetadataGroup groups[group_count];
};

struct MetadataGroup {
    u8    name_length;
    u8    name[name_length];
    u16be value_count;
    MetadataValue values[value_count];
};

struct MetadataValue {
    u16be length;
    u8    bytes[length];
};
```

Names and values are not NUL terminated on disk. Treat value data as bytes until that table's schema proves it is text. Text may use Windows code page 949.

## Cache and update flow

The files in `metafile/` contain the original zlib stream received from the server, not the inflated table.

```text
server sends metadata inventory
    |
    +-- local file missing or CRC differs
            |
            +-- client requests the named table
                    |
                    +-- inflate zlib payload
                    +-- calculate CRC32 over inflated bytes
                    +-- save original compressed bytes
                    +-- parse groups and values
```

Inventory entries contain a one-byte name length, the name bytes, and a `u32be` CRC32. A payload response contains the name, expected `u32be` CRC32, `u16be` compressed size, and the zlib bytes. The inflate buffer is capped at `0x20000` bytes.

## Create metadata

```text
build_metadata(groups):
    decoded = encode_big_endian_group_container(groups)
    checksum = crc32(decoded)
    compressed = zlib_compress(decoded)
    return checksum, compressed
```

The cache filename and inventory name must agree. A server also needs to advertise the new CRC so the client knows whether to request the replacement.

## Evidence

- `net_handle_metadata` at `0x004E4EA0`
- `net_metadata_uncompress` at `0x004E54F0`
- `file_load_metadata_compressed` at `0x004E5570`
- `file_save_metadata_compressed` at `0x004E56E0`
- `net_metadata_crc32` at `0x004E5790`
- `net_parse_metadata_table` at `0x004E57C0`
