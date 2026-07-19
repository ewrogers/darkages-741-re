# File formats

The client mixes simple archives, text lookup tables, indexed images, and a few custom codecs. Each page separates the container from the way the renderer or network system uses it.

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

See [compression and checks](compression.md) for the algorithm used by each family and [exporting images](image-export.md) for PNG conversion.

`Confirmed in client` means the executable contains direct reader or writer behavior. `Generated inverse` means a writer follows naturally from the reader, but the client does not prove it and a full round trip has not been recorded.

All multi-byte fields on these pages are little-endian unless a page says otherwise. Metadata and packet fields are notable big-endian exceptions.

File names do not prove that two formats share a layout. For example, `tilea.bmp` and `tileas.bmp` are raw fixed-record banks, not BMP images.
