# 021 / 0x15: Map Size (`SMapSize`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x15` |
| RTTI class | `SMapSize` |
| Factory | `0x599EE0` |
| Constructor | `0x599F60` |
| Vtable | `0x687F5C` |
| Deserializer | `0x599F90` |

## Preliminary payload model

```text
1. u16be map_id
2. u8 width
3. u8 height
4. u8 map_flags
5. u8 unknown
6. u24be expected_checksum
7. string[u8 length] map_name
```

## Raw reader-call trace

`u16be -> u8 -> u8 -> u8 -> u8 -> u24be -> string[u8 length]`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: map identifier, dimensions, checksum, and name confirmed by handler use; two flag bytes remain incomplete.

## Client handling

`map_handle_s_map_size` at `0x5F1BF0` compares this state with the active grid and local `maps/lod%d.map` cache. When the cache does not match, it sends CMapCRC `0x05` with the local dimensions and checksum. See [Map loading and rendering](../../map/loading-and-rendering.md).

The map identifier, dimensions, checksum, and name uses are confirmed by the handler. The exact meanings of the two flag bytes remain incomplete.
