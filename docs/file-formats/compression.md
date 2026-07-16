# Compression and checks

The client uses several independent storage methods. A file extension alone does not tell you which one applies.

| Data | Storage method | Notes |
| --- | --- | --- |
| Legacy DAT entries | None at archive level | Each payload keeps its own format |
| Extended DAT index | zlib/DEFLATE | Reader exists, no local sample |
| HPF | Adaptive binary tree | Includes a raw fallback |
| HEA | Run-length rows | Not wrapped in zlib |
| EFA frame payload | zlib/DEFLATE | One compressed payload per frame |
| Metadata cache | zlib/DEFLATE | CRC32 covers inflated bytes |
| Stipulation greeting replacement | zlib/DEFLATE | Inflated into a 10,000-byte text buffer |
| EPF, SPF, PAL, raw tile banks, TBL | No common wrapper | Individual pixel modes may still differ |

The executable contains zlib 1.1.3. `file_zlib_uncompress` is the common inflate entry. zlib is a wrapper around the DEFLATE algorithm and normally starts with bytes such as `78 9C`, but readers should validate the stream instead of checking only those two bytes.

The extended DAT index also applies XOR to 32-bit words. That is obfuscation, not compression.

See [HPF static images](hpf.md) for its codec, [HEA light masks](hea.md) for row runs, [metadata files](metadata.md) for the network cache, and [checksums](../network/checksums.md) for CRC16 and CRC32.
