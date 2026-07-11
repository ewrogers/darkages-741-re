# Compression

The confirmed file compression in the version-741 client is used by extended fastfile `.dat` archives. The client contains a zlib-compatible decompressor and identifies its embedded implementation with the literal version string `1.1.3`.

No separate compressor is used by the archive-loading path. The client only expands chunks that were compressed when the archive was built.

## Decompression entry point

`file_zlib_uncompress` (`0x6043B0`) is a wrapper with the following recovered signature:

```c
int file_zlib_uncompress(
    u8 *destination,
    u32 *destination_size,
    const u8 *source,
    u32 source_size
);
```

The call pattern matches the small zlib `uncompress` interface. `destination_size` is both an input capacity and an output byte count.

The wrapper returns a status code. The caller treats a nonzero result as decompression failure. Exact symbolic error names are not preserved in the client.

## Compressed chunk descriptor

Each extended archive chunk has a 16-byte descriptor. The descriptor is decoded before these fields are used:

```c
struct fastfile_chunk_descriptor {
    u32 source_offset;
    u32 compressed_size;
    u32 uncompressed_size;
    u32 unknown_0c;
};
```

`source_offset` is relative to the start of the mapped archive. The loader allocates `uncompressed_size` bytes and passes exactly `compressed_size` source bytes to the decompressor.

## Minimal chunk decompressor

This example expresses the observed client behavior without relying on modern C++ features:

```c
int decompress_fastfile_chunk(
    const u8 *archive,
    const struct fastfile_chunk_descriptor *chunk,
    u8 *output
)
{
    u32 output_size;
    int result;

    output_size = chunk->uncompressed_size;
    result = file_zlib_uncompress(
        output,
        &output_size,
        archive + chunk->source_offset,
        chunk->compressed_size
    );

    if (result != 0) {
        return 0;
    }

    if (output_size != chunk->uncompressed_size) {
        return 0;
    }

    return 1;
}
```

The size comparison is useful in an independent reader. The client supplies the descriptor's uncompressed size as the capacity, but further work is needed to confirm whether every original call site explicitly rejects a smaller successful output.

## Recovered archive loop

The extended archive loader processes each descriptor independently:

```c
int decompress_fastfile_chunks(
    const u8 *archive,
    const struct fastfile_chunk_descriptor *chunks,
    u32 chunk_count,
    u8 **outputs
)
{
    u32 i;

    for (i = 0; i < chunk_count; i++) {
        outputs[i] = allocate(chunks[i].uncompressed_size);
        if (outputs[i] == 0) {
            return 0;
        }

        if (!decompress_fastfile_chunk(
                archive,
                &chunks[i],
                outputs[i])) {
            return 0;
        }
    }

    return 1;
}
```

`allocate` is pseudocode for the client's allocation step. A real parser should also validate all source ranges before reading and release earlier allocations when a later chunk fails.

## Relationship to archive transforms

The archive operations occur in this order:

1. Decode the extended header with 32-bit XOR using `0xFFFFFFFF`.
2. Decode the index and chunk descriptors with the archive-specific 32-bit XOR key.
3. Read the compressed bytes described by each decoded chunk descriptor.
4. Decompress each chunk into a separately allocated output buffer.
5. Parse the variable-length entry records from the decompressed data.

The XOR step transforms metadata. It does not decrypt or decompress the chunk payload. No payload XOR was observed in this loader.

## Confidence and open questions

- Confirmed local: `file_zlib_uncompress` is at `0x6043B0`.
- Confirmed local: the client contains the version string `1.1.3` and uses a zlib-compatible wrapper call.
- Confirmed local: compressed and uncompressed sizes come from each decoded chunk descriptor.
- Open: the meaning of descriptor field `unknown_0c`.
- Open: whether all archives use the same zlib stream framing and compression settings.

See [Fastfile `.dat` archives](fastfile-archives.md) for the surrounding container layout and metadata XOR algorithm.
