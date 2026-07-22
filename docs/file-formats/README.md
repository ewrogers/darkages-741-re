# File formats

The client mixes simple archives, text lookup tables, indexed images, and a few custom codecs. Each page separates the container from the way the renderer or network system uses it. See [Asset loading](../systems/asset-loading.md) for how names and archives lead to these readers.

| Format | Purpose | Read status | Write status |
| --- | --- | --- | --- |
| [DAT](dat-archives.md) | Asset archives | Legacy format confirmed | Rebuild process confirmed |
| [LFT](lft.md) | Active bitmap fonts | Layout and glyph rows confirmed | Generated inverse not yet tested |
| [FNT](fnt.md) | Dormant fixed bitmap fonts | Record sizes and code ranges confirmed | Not described |
| [HPF](hpf.md) | Static indexed images | Codec confirmed | Exact sample round trips pass |
| [HEA](hea.md) | Lighting and occlusion rows | Main layout confirmed | Generated inverse described |
| [PAL](pal.md) | 256 RGB colors | Confirmed | Direct output confirmed |
| [TBL](table-files.md) | Text lookup tables | Major families mapped | Depends on each table grammar |
| [Metadata](metadata.md) | Server-managed data cache | Container and update flow confirmed | Generated server payload described |
| [MAP](map.md) | Map tile IDs | Confirmed | Confirmed in client |
| [Raw map tile banks](map-tile-banks.md) | Isometric ground pixels | Confirmed | Fixed-record output described |
| [Tile animation tables](tile-animation-tables.md) | Ground and static animation cycles | Confirmed | Plain decimal text |
| [SOTP.DAT](sotp.md) | Static collision and render flags | Confirmed | Raw byte output described |
| [Album.dat](album.md) | Local portrait album | Container and zlib payloads confirmed | Confirmed in client |
| [EPF](epf.md) | Indexed image frames | Container mapped | Pixel encoder incomplete |
| [SPF](spf.md) | Indexed image frames | Container mapped | Generated inverse not yet tested |
| [EFA](efa.md) | Compressed effect frames | Main decode path mapped | Generated inverse incomplete |
| [Effect.tbl](effect-table.md) | Effect frame sequences | Confirmed | Straightforward text output |
| [Bulletin abuse warning list](bulletin-bang-list.md) | Per-character privileged warning history | Fixed 45-byte text records confirmed | Confirmed in client |

See [compression and checks](compression.md) for the algorithm used by each family and [exporting images](image-export.md) for PNG conversion.

`Confirmed in client` means the executable contains direct reader or writer behavior. `Generated inverse` means a writer follows naturally from the reader, but the client does not prove it and a full round trip has not been recorded.

## Binary layout notation

Binary format pages use a field-list notation similar to the packet body notation. A complete stored layout begins with `file`. A `record` is a nested group or a confirmed fragment whose complete container is not known.

```text
file Example(external_count) {
    u16le item_count
    repeat item_count {
        record item {
            u32be identifier
            bytes payload[external_count]
        }
    }
}
```

Fields appear in exact file order and have no implicit compiler padding. Integer names state their byte order, such as `u16le` or `u32be`. `bytes` preserves uninterpreted data. `repeat`, `if`, and `at offset` describe repetition, conditional fields, and an explicit absolute file position. `to end_of_file` and `to end_of_decoded_data` consume the remaining bytes in the named region. Parameters beside a file name, such as a map's width and height, come from outside the file.

`compressed codec { ... }` describes the decoded contents of a compressed stream. `decoded Name { ... }` describes bytes produced by a codec rather than another stored region. `bits_lsb_first` means the low bit of each stored byte is consumed first. Comments give sizes, offset bases, sentinels, and known meanings without adding bytes.

The layout only names fields supported by current evidence. Unknown bytes stay visible instead of being replaced with guessed values.

File names do not prove that two formats share a layout. For example, `tilea.bmp` and `tileas.bmp` are raw fixed-record banks, not BMP images.
