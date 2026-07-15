# 060 / 0x3C: Map Part (`SMapPart`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x3C` |
| RTTI class | `SMapPart` |
| Factory | `0x599DC0` |
| Constructor | `0x599E40` |
| Vtable | `0x687F48` |
| Deserializer | `0x599E70` |

## Preliminary payload model

```text
1. u16be
2. remaining-view
```

## Raw reader-call trace

`u16be -> remaining-view`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.

## Client handling

`map_handle_s_map_part` at `0x5F2840` applies this packet as a rectangular update. Its data view begins with four `u8` rectangle values, followed by three `u16be` tile identifiers per cell in row-major order. The client stores the values as ground, static A, and static B. See [Map loading and rendering](../../map/loading-and-rendering.md).

The existing `u16be` field in the packet class appears to cover the first two byte-sized rectangle components. Exact names for all four rectangle values still need a capture or server-side definition.
