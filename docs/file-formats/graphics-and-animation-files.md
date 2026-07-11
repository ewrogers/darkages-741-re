# Graphics and animation files

The version-741 client uses several small, purpose-built image containers. Most are direct views over bytes in a fastfile archive. EFA uses zlib per frame, HPF uses a proprietary adaptive tree codec, and the other formats in this page are not compressed by their format loader.

All multibyte fields described here are little-endian.

None of these format loaders uses packet encryption or an additional XOR transform. An enclosing extended fastfile can still have transformed metadata and compressed index chunks.

| Extension | Primary use | Stored pixels | Compression |
|---|---|---|---|
| `.epf` | UI, characters, effects, and general sprites | Primary and secondary frame streams | None in the container loader |
| `.spf` | Sprites with format flags and optional embedded palettes | Direct frame stream, optional alternate stream | None |
| `.mpf` | Monster animation and directional sprites | Direct indexed frame stream | None |
| `.hpf` | `stc` and `sts` map resources | Decoded resource bytes | Proprietary adaptive binary tree |
| `.bmp` | Screenshots and a few ordinary bitmaps | Standard 16-bit DIB pixels | None in observed BMPs |
| `.bmp` tile bank | `tilea.bmp` and `tileas.bmp` map tiles | 8-bit palette indices | None |
| `.efa` | Animated effects | Per-frame decoded buffers | zlib per frame |
| `.hea` | Map spatial lookup data | `u32` lookup tables and `u16` payload | None |
| `.pal` | Render palettes | 256 RGB colors | None |

The formats are normally entries inside [fastfile `.dat` archives](fastfile-archives.md). Archive-level zlib compression is separate from any format-specific compression listed above.

Except for the screenshot BMP writer, the client does not appear to contain authoring-side encoders for these asset formats. The write paths below are derived from the confirmed readers. HPF has additionally been verified by exact binary round trip. Fields whose runtime meaning is still unknown are left explicit so an authoring tool can preserve or expose them.

## EPF

EPF is the common frame container used by UI artwork, characters, and effects. `render_decode_image_entry` at `0x48B530` reads the header, selects a 16-byte frame record, and returns direct pointers into the entry. It does not allocate or decompress the frame.

```c
struct epf_header {
    u16 frame_count;          /* +0x00 */
    u8 unknown_02[6];         /* +0x02 */
    u32 stream_size;          /* +0x08 */
    u8 streams[stream_size];  /* +0x0c */
    /* struct epf_frame frames[frame_count] follows */
};

struct epf_frame {
    s16 field_00;
    s16 field_02;
    s16 field_04;
    s16 field_06;
    u32 primary_offset;
    u32 secondary_offset;
};
```

The four signed fields form the frame bounds, but the client reorders them when it builds its internal rectangle:

```c
out.left   = frame.field_02;
out.top    = frame.field_00;
out.right  = frame.field_06;
out.bottom = frame.field_04;
```

The two frame streams are resolved as:

```c
out.primary = header.streams + frame.primary_offset;
out.secondary = header.streams + frame.secondary_offset;
out.secondary_size = next_frame.primary_offset - frame.secondary_offset;
```

The parser exposes both slices to the renderer. The secondary stream appears to describe additional transparency or span data, but that interpretation is not yet confirmed.

### Writing EPF

An encoder can place each frame's primary and secondary streams consecutively, followed by the frame descriptors. The client calculates a secondary stream's length from the next descriptor's `primary_offset`, including for the final frame. Existing files do not consistently include an explicit terminator record, so this last read can leave the entry boundary.

For newly authored files, append one extra 16-byte sentinel descriptor after the counted descriptors. Do not include it in `frame_count`. Set both sentinel offsets to `stream_size`. The loader locates the descriptor table from `stream_size` and ignores trailing bytes, while the sentinel gives the final frame a safe boundary.

```c
stream_size = 0;

for (i = 0; i < frame_count; i++) {
    frames[i].primary_offset = stream_size;
    append_bytes(streams, primary[i], primary_size[i]);
    stream_size += primary_size[i];

    frames[i].secondary_offset = stream_size;
    append_bytes(streams, secondary[i], secondary_size[i]);
    stream_size += secondary_size[i];
}

sentinel.primary_offset = stream_size;
sentinel.secondary_offset = stream_size;

write_u16_le(frame_count);
write_bytes(header_unknown_02, 6);
write_u32_le(stream_size);
write_bytes(streams, stream_size);
write_bytes(frames, frame_count * 16);
write_bytes(&sentinel, 16);
```

The unknown header bytes, signed bounds, and secondary stream encoding should be copied from a compatible source asset until their meanings are confirmed.

Effect EPFs named `Efct*.epf` can have a same-basename `.tbl` sidecar. The client reads one four-byte sidecar record per frame. See [Table files](table-files.md).

## SPF

SPF adds explicit format bytes, optional embedded 16-bit palettes, 32-byte frame records, and an alternate pixel offset. `file_spf_view_init` at `0x4021D0` builds a zero-copy view, and `file_spf_resolve_frame` at `0x4022A0` selects a frame.

```c
struct spf_header {
    u32 unknown_00;
    u32 unknown_04;
    u8 format[4];

    /* Present only when format[0] == 0 and format[1] == 0. */
    u16 embedded_palette_a[256];
    u16 embedded_palette_b[256];

    u32 frame_count;
    struct spf_frame frames[frame_count];
    u32 pixel_data_size;
    u8 pixel_data[pixel_data_size];
};

struct spf_frame {
    u16 field_00;
    u16 field_02;
    u16 field_04;
    u16 field_06;
    u16 optional_08;
    u16 optional_0a;
    u32 flags;
    u32 pixel_offset;
    u32 stride_or_size;
    u32 unknown_18;
    u32 alternate_pixel_offset;
};
```

`flags & 1` enables the two optional `u16` values. The normal pointer is `pixel_data + pixel_offset`. When `format[0] == 2` and the active display mode is 2, the client also adds `alternate_pixel_offset`.

When the embedded palettes are present, the caller selects palette A or B according to display mode. No palette conversion, decompression, or byte scrambling occurs in the SPF parser.

### Writing SPF

SPF encoding is direct serialization. Write the two 512-byte palette blocks only when both leading format bytes are zero. Offsets in every frame record are relative to the start of the final pixel block.

```c
write_u32_le(header_unknown_00);
write_u32_le(header_unknown_04);
write_bytes(format, 4);

if (format[0] == 0 && format[1] == 0) {
    write_u16_array_le(palette_a, 256);
    write_u16_array_le(palette_b, 256);
}

write_u32_le(frame_count);
write_bytes(frames, frame_count * 32);
write_u32_le(pixel_data_size);
write_bytes(pixel_data, pixel_data_size);
```

If a frame does not use the display-mode alternate image, set `alternate_pixel_offset` to zero. Preserve the opaque header and frame fields from a working asset with the same pixel mode while new content is being tested.

SPFs named `Mefc*.spf` can use the same four-byte-per-frame `.tbl` sidecar convention as effect EPFs.

## MPF

MPF stores monster animation frames and directional grouping metadata. `file_mpf_load` at `0x50F490` reads the container. `render_select_mpf_frame` at `0x48D0E0` combines motion and direction state to choose a frame.

An optional envelope can precede the normal header:

```c
struct mpf_envelope {
    u32 marker;       /* 0xffffffff */
    u32 flags;
};
```

When `flags & 4` is set, the envelope is followed by a `u32` record count and that many four-byte records. The client retains at most four of these records in its fixed object fields, but it advances over the full stored count.

The core header is 17 bytes. Byte 0 is the frame count. Bytes 11 and 12 normally provide animation or direction grouping values. If byte 11 is `0xff`, six extension bytes follow the core header and supply three explicit byte pairs. Otherwise the client repeats bytes 11 and 12 for all three pairs.

The frame table follows:

```c
struct mpf_frame {
    s16 field_00;
    s16 field_02;
    s16 field_04;
    s16 field_06;
    s16 anchor_08;
    s16 anchor_0a;
    u32 pixel_offset;
};
```

Pixel data begins after `frame_count * 16` bytes of descriptors. A frame points directly to `pixel_data + pixel_offset`. No MPF decompression step was found.

### Writing MPF

The smallest accepted form omits the `0xffffffff` envelope. Write the 17-byte core header, the optional six extension bytes, all frame descriptors, then the indexed pixel block. Every `pixel_offset` is relative to the pixel block, not the file start.

```c
write_bytes(core_header, 17);

if (core_header[11] == 0xff) {
    write_bytes(direction_pairs, 6);
}

write_bytes(frames, core_header[0] * 16);
write_bytes(pixel_data, pixel_data_size);
```

Use the envelope only when its extra records are needed. Set `marker` to `0xffffffff`; if `flags & 4`, write the record count and all four-byte records before the core header. Several core-header fields remain semantic unknowns, so an authoring tool should expose them rather than invent defaults.

## HPF

HPF is used for map resources named `stc%05d.hpf` and `sts%05d.hpf`. `map_load_hpf_resource` at `0x5FD700` loads the entry and calls `file_hpf_decompress` at `0x4319B0`.

Compressed input begins with little-endian magic `0xff02aa55`. If the magic is absent, the routine copies the entry unchanged. If it is present, the bitstream begins at offset 4 and is read least-significant bit first.

The decoder starts with a complete binary tree:

```c
void hpf_tree_init(struct hpf_tree *tree)
{
    u32 node;
    u32 symbol;

    for (node = 1; node <= 512; node++) {
        tree->parent[node] = (node - 1) / 2;
    }

    for (symbol = 0; symbol < 256; symbol++) {
        tree->left[symbol] = symbol * 2 + 1;
        tree->right[symbol] = symbol * 2 + 2;
    }
}
```

Each bit chooses the left or right child until the node is greater than 255. The decoded symbol is `node - 256`. Symbol `0x100` ends the stream. Every symbol, including the terminator, updates the tree with this rotation:

```c
void hpf_update_tree(struct hpf_tree *tree, u32 symbol)
{
    u32 node;
    u32 parent;
    u32 grandparent;
    u32 other_child;

    node = symbol + 256;

    for (;;) {
        parent = tree->parent[node];
        if (parent == 0) {
            break;
        }

        grandparent = tree->parent[parent];
        other_child = tree->left[grandparent];

        if (other_child == parent) {
            other_child = tree->right[grandparent];
            tree->right[grandparent] = node;
        } else {
            tree->left[grandparent] = node;
        }

        if (tree->left[parent] == node) {
            tree->left[parent] = other_child;
        } else {
            tree->right[parent] = other_child;
        }

        tree->parent[node] = grandparent;
        tree->parent[other_child] = parent;
        node = grandparent;
    }
}
```

A minimal decode loop is:

```c
while (1) {
    node = 0;

    while (node <= 255) {
        bit = read_lsb_first_bit(&bits);
        node = bit ? tree.right[node] : tree.left[node];
    }

    symbol = node - 256;
    hpf_update_tree(&tree, symbol);

    if (symbol == 0x100) {
        break;
    }

    output[output_size++] = (u8)symbol;
}
```

### Writing HPF

HPF encoding is the exact inverse of tree traversal. Before updating the tree for a symbol, walk from leaf `symbol + 256` to the root through the parent table. A left edge emits zero and a right edge emits one. Reverse that collected path, write it least-significant bit first, then perform the same tree update used by the decoder. Encode terminator symbol `0x100` after the final data byte.

```c
void hpf_write_symbol(
    struct hpf_tree *tree,
    struct lsb_writer *bits,
    u32 symbol
)
{
    u8 path[512];
    u32 path_size;
    u32 node;
    u32 parent;

    path_size = 0;
    node = symbol + 256;

    while (node != 0) {
        parent = tree->parent[node];
        path[path_size++] = tree->right[parent] == node;
        node = parent;
    }

    while (path_size != 0) {
        write_lsb_first_bit(bits, path[--path_size]);
    }

    hpf_update_tree(tree, symbol);
}

void hpf_encode(const u8 *input, u32 input_size, struct output *out)
{
    struct hpf_tree tree;
    struct lsb_writer bits;
    u32 i;

    write_u32_le(out, 0xff02aa55);
    init_lsb_writer(&bits, out);
    hpf_tree_init(&tree);

    for (i = 0; i < input_size; i++) {
        hpf_write_symbol(&tree, &bits, input[i]);
    }

    hpf_write_symbol(&tree, &bits, 0x100);
    flush_partial_byte(&bits);
}
```

This encoder was round-trip tested against `stc00000.hpf` from the local `ia.dat`. The 59-byte stored file decoded to 400 bytes and re-encoded to the exact same 59 bytes, including its final partial byte.

The client allocates `compressed_size * 10` output bytes but does not visibly enforce that capacity inside the symbol loop. An independent decoder should validate both input exhaustion and output capacity.

After decoding, `map_load_hpf_resource` strips an eight-byte resource header. A local verification decoded `stc00000.hpf` from 59 stored bytes to 400 bytes and consumed the entire entry.

## BMP

There are two unrelated `.bmp` conventions.

### Standard Windows BMP

The loose `lodNNN.bmp` files are ordinary Windows bitmaps. `render_write_screenshot_bmp` at `0x5537F0` writes them as uncompressed 640 by 480, 16-bit, bottom-up DIBs. It emits a `BITMAPFILEHEADER`, a 40-byte `BITMAPINFOHEADER`, and raw scanlines. The pixel conversion accounts for the active 16-bit display masks.

Standard archive BMPs were also observed. For example, `rs_bg00.BMP` is a 320 by 240, 16-bit `BI_RGB` image. These files use normal Windows BMP headers and have no additional client scrambling.

### Raw `tilea.bmp` and `tileas.bmp`

These two entries in `seo.dat` are not BMP files. They have no `BM` header. They are fixed-record banks of palette-indexed isometric map tiles:

```c
#define MAP_TILE_ROWS         27
#define MAP_TILE_ROW_BYTES    56
#define MAP_TILE_RECORD_SIZE  0x5e8

tile = bank + tile_index * MAP_TILE_RECORD_SIZE;
```

`map_decode_palette_tile` at `0x4C7390` walks all 27 rows. Static row-start and row-width tables choose the visible diamond-shaped span within each 56-byte row. Every source byte is an index into a selected 256-entry 16-bit palette.

Both observed bank sizes are exact multiples of `0x5e8`. There is no per-tile header or compression.

### Writing BMP and tile banks

A standard BMP writer can emit the normal 14-byte file header, 40-byte `BITMAPINFOHEADER`, and bottom-up 16-bit rows padded to a four-byte boundary. Use `BI_RGB` for compatibility with the observed files.

For `tilea.bmp` and `tileas.bmp`, do not write a BMP header or palette. Allocate exactly `tile_count * 0x5e8` bytes. Each tile is 27 rows of 56 palette indices. Fill bytes outside the visible row span with zero, then copy each visible diamond row to the start and width selected by the same static shape tables used by `map_decode_palette_tile` at `0x4C7390`.

## EFA

EFA is the compressed effect-animation format. `render_effect_resource_ctor` at `0x4575B0` tries `EfctNNNm.efa`, `EfctNNNb.efa`, and `EfctNNN.efa`, then falls back to equivalent EPF names. `render_effect_load_frame` at `0x457FD0` loads frames lazily.

The file starts with a 64-byte header and has one 64-byte descriptor per frame:

```c
struct efa_header {
    u32 marker;             /* observed 0x00001000 */
    u32 frame_count;
    u32 frame_delay_ms;     /* inferred from values such as 55 and 70 */
    u32 pixel_mode;         /* observed value 2 */
    u32 unknown_10;
    u8 reserved_14[0x2c];
};

struct efa_frame {
    u32 unknown_00;
    u32 compressed_offset;
    u32 compressed_size;
    u32 decoded_size;
    u32 frame_type;
    u32 primary_offset;
    u32 row_stride;
    u32 storage_mode;
    u32 secondary_offset;
    u32 secondary_stride_or_size;
    u16 auxiliary_28;
    u16 auxiliary_2a;
    u16 rectangle_a[4];
    u16 rectangle_b[4];
    u32 unknown_3c;
};
```

Compressed frame data begins after the complete descriptor table. Offsets are relative to that payload base:

```c
int efa_decode_frame(const u8 *file, u32 frame_index, u8 *output)
{
    const struct efa_header *header;
    const struct efa_frame *frames;
    const struct efa_frame *frame;
    const u8 *payload;
    u32 output_size;

    header = (const struct efa_header *)file;
    frames = (const struct efa_frame *)(file + 0x40);
    frame = &frames[frame_index];
    payload = file + 0x40 + header->frame_count * 0x40;

    output_size = frame->decoded_size;
    if (file_zlib_uncompress(
            output,
            &output_size,
            payload + frame->compressed_offset,
            frame->compressed_size) != 0) {
        return 0;
    }

    return output_size == frame->decoded_size;
}
```

This is ordinary zlib framing through `file_zlib_uncompress` at `0x6043B0`. It is not XOR-encrypted. A local check of `efct231.efa` found 12 frames. Frame 0 begins with zlib bytes `78 9c` and expands from 529 bytes to 41,040 bytes.

### Writing EFA

Compress every decoded frame as a separate zlib stream. First build the 64-byte header and all 64-byte descriptors. Concatenate the compressed streams after the descriptor table and store offsets relative to the beginning of that payload.

```c
payload_offset = 0;

for (i = 0; i < frame_count; i++) {
    compressed[i] = zlib_compress(decoded[i], decoded_size[i]);
    frames[i].compressed_offset = payload_offset;
    frames[i].compressed_size = compressed[i].size;
    frames[i].decoded_size = decoded_size[i];
    payload_offset += compressed[i].size;
}

write_bytes(&header, 0x40);
write_bytes(frames, frame_count * 0x40);

for (i = 0; i < frame_count; i++) {
    write_bytes(compressed[i].data, compressed[i].size);
}
```

The client accepts ordinary zlib framing. The exact compressed bytes can vary with compression level while decoding to the same frame. Preserve the remaining descriptor fields from a compatible frame type until their render semantics are named.

## HEA

HEA is a map-side spatial lookup resource loaded as `%06d.hea` by `map_load_hea_resource` at `0x5C7870`. The exact expansion of the name is not present in RTTI or strings, so the project keeps the extension as its format name.

`file_hea_load` at `0x4875B0` creates three direct views:

```c
header = file;
table_a = file + 0x28;
table_b = table_a + header_u32[0x24 / 4];
payload = table_b + header_u32[0x20 / 4] * header_u32[0x24 / 4];
```

In byte-oriented form:

```c
table_a = (u32 *)(file + 0x28);
table_b = table_a + read_u32_le(file + 0x24);
payload = table_b
        + read_u32_le(file + 0x20)
        * read_u32_le(file + 0x24);
```

The first table partitions a coordinate range. The second is a `u32` matrix of indices into the following `u16` payload. Map routines use these tables to build pointers for a clipped rectangle. Some payload helpers treat the high byte as a level or magnitude and the low six bits as flags. More semantic field names need runtime confirmation.

The observed `000108.hea` header contains values including 640, 480, 40, 3520, 2080, and a table-A count of 4. The parser does not decompress, decrypt, or copy the stored tables.

### Writing HEA

HEA encoding is direct. Write the 40-byte header, `header[0x24]` little-endian `u32` values for table A, `header[0x20] * header[0x24]` little-endian `u32` values for table B, then the little-endian `u16` payload.

```c
write_bytes(header, 0x28);
write_u32_array_le(table_a, read_u32_le(header + 0x24));
write_u32_array_le(
    table_b,
    read_u32_le(header + 0x20) * read_u32_le(header + 0x24)
);
write_u16_array_le(payload, payload_count);
```

The client does not store an explicit payload count at this layer. The enclosing fastfile entry size provides the final boundary, so a standalone tool must calculate it from the bytes remaining after both tables.

## PAL

The normal client palette is exactly 768 bytes:

```c
struct raw_palette {
    u8 rgb[256][3];
};
```

`render_register_rgb24_palette` at `0x548650` sends all 256 RGB triples to `render_convert_rgb24_palette` at `0x593B00`. Each color is converted through the active display-format callback into a `u16` pixel. For palette entries 1 through 255, a converted value of zero is replaced with one so pixel value zero remains reserved for transparency.

Some archives also contain standard 1,048-byte RIFF PAL files:

```text
RIFF <u32 size> PAL  data <u32 size> <u16 version=0x0300>
<u16 count=256> <256 entries of red, green, blue, flags>
```

The raw-palette registration path does not inspect RIFF headers and expects RGB triples at byte 0. RIFF PAL entries therefore need their standard container removed and their four-byte entries converted to three-byte RGB entries before use with that path. A separate client consumer for the RIFF variant has not yet been confirmed.

Neither palette representation is compressed or scrambled.

### Writing PAL

The client-facing raw form is simply 256 red, green, blue triples in palette-index order:

```c
for (i = 0; i < 256; i++) {
    write_u8(colors[i].red);
    write_u8(colors[i].green);
    write_u8(colors[i].blue);
}
```

This always produces 768 bytes. A RIFF PAL writer instead uses the standard 24-byte RIFF header and four bytes per color, but that form should not be supplied to the raw registration path without conversion.

## Important functions

| Function | Address | Role |
|---|---:|---|
| `file_spf_view_init` | `0x4021D0` | Build an SPF view |
| `file_spf_resolve_frame` | `0x4022A0` | Resolve one SPF frame |
| `file_hpf_decompress_stub` | `0x431840` | Unreferenced stub that returns no decoded data |
| `file_hpf_decompress_legacy` | `0x431860` | Older unreferenced HPF-only decoder |
| `file_hpf_decompress` | `0x4319B0` | Decode HPF or copy an uncompressed entry |
| `file_hpf_codec_singleton` | `0x4AE480` | Return the codec object called `Compressor` by RTTI |
| `file_efa_read_header` | `0x456F30` | Read EFA count and timing fields |
| `file_efa_decode_frame` | `0x457030` | Inflate and interpret one EFA frame |
| `render_effect_resource_ctor` | `0x4575B0` | Select EFA or EPF effect resources |
| `file_hea_load` | `0x4875B0` | Build a zero-copy HEA view |
| `render_decode_image_entry` | `0x48B530` | Resolve EPF and SPF image entries |
| `render_select_mpf_frame` | `0x48D0E0` | Select an MPF directional animation frame |
| `map_decode_palette_tile` | `0x4C7390` | Decode a raw map tile to 16-bit pixels |
| `file_mpf_load` | `0x50F490` | Parse and retain an MPF entry |
| `render_register_rgb24_palette` | `0x548650` | Register and convert a 768-byte palette |
| `render_write_screenshot_bmp` | `0x5537F0` | Write a standard 16-bit screenshot BMP |
| `map_load_hea_resource` | `0x5C7870` | Load the current numbered HEA map resource |
| `map_load_hpf_resource` | `0x5FD700` | Load and decode an `stc` or `sts` HPF entry |
