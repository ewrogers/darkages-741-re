# File formats

Rendering code consumes several small game-specific formats. This section keeps container layout separate from drawing behavior so a developer can build readers and, where the evidence is complete, writers.

| Format | Purpose | Read status | Write status |
| --- | --- | --- | --- |
| [MAP](map.md) | Map tile IDs | Confirmed | Confirmed in client |
| [Raw map tile banks](map-tile-banks.md) | Isometric ground pixels | Confirmed | Fixed-record output described |
| [Tile animation tables](tile-animation-tables.md) | Ground and static animation cycles | Confirmed | Plain decimal text |
| [SOTP.DAT](sotp.md) | Static collision and render flags | Confirmed | Raw byte output described |
| [EPF](epf.md) | Indexed image frames | Container mapped | Payload encoding incomplete |
| [SPF](spf.md) | Indexed image frames | Container mapped | Generated inverse not yet tested |
| [EFA](efa.md) | Compressed effect frames | Main decode path mapped | Generated inverse incomplete |
| [Effect.tbl](effect-table.md) | Effect frame sequences | Confirmed | Straightforward text output |

`Confirmed in client` means the executable contains both reader and writer behavior. `Generated inverse` means a writer can be designed from the reader, but the client does not prove that writer and no round-trip test has been recorded yet.

All multi-byte fields on these pages are little-endian unless a page says otherwise.

File names and extensions do not prove that two formats share a layout. In particular, `tilea.bmp` and `tileas.bmp` are raw fixed-record banks rather than BMP images. CTF and DTF appear as internal tile-storage class names, but no matching extension or active constructor was confirmed.
