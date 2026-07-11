# Map subsystem

The map subsystem combines a server-defined grid, local `maps/lod%d.map` cache files, palette-indexed tile banks, numbered HPF and HEA resources, and `SOTP.DAT` static-object flags.

The client keeps three `u16` tile identifiers per coordinate:

1. Ground tile
2. Static layer A
3. Static layer B

The two static fields are passed to the renderer with orientation selectors 0 and 1. Their exact company field names are not present in the binary, so this project uses neutral `static_a` and `static_b` names instead of assuming left and right.

Start with:

- [Map loading and rendering](loading-and-rendering.md)
- [Collision and SOTP flags](collision.md)
- [Graphics and animation files](../file-formats/graphics-and-animation-files.md) for HPF, HEA, palette, and raw tile-bank formats
- [Packet encryption and CRC](../client/packet-crypto-and-crc.md) for the map checksum routine

All addresses are static virtual addresses for the preferred image base `0x400000`.
