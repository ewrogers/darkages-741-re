# 005 / 0x05: CMapCRCPacket

- Direction: client to server
- Internal packet name: `CMapCRCPacket`
- Local behavioral alias: `RequestMapData`
- Related-game enum name: `MapRequest`
- Name provenance: Leaked company/engine class name remapped by this client's local behavior; the sibling-game opcode differs.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `map_handle_s_map_size` at `0x5F1BF0`: emitted when the cached map identifier, dimensions, or checksum do not match

## Current structural notes

The recovered untransformed body is 10 bytes:

| Offset | Type | Meaning |
|---:|---|---|
| 0 | `u8` | opcode `0x05` |
| 1 | `u16be` | reserved/currently zero |
| 3 | `u16be` | reserved/currently zero |
| 5 | `u8` | map width |
| 6 | `u8` | map height |
| 7 | `u24be` | locally cached map checksum |

- The checksum is recovered through `net_calculate_map_crc16` at `0x5B9180` and serialized by `net_write_u24_be` at `0x5641A0`.
- Although the local checksum value is held as a 16-bit value at this call site, the wire field is explicitly three bytes wide.
- This strongly supports the leaked internal name `CMapCRCPacket` despite its opcode moving from `0x35` in the sibling game to `0x05` here.
- The complete cache selection and download flow is documented in [Map loading and rendering](../../map/loading-and-rendering.md).
