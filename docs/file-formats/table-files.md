# Table files

`.tbl` is a naming convention, not one binary format. The client chooses a parser from the filename and subsystem. Confirmed tables include plain text, small fixed binary records, and files whose text fields have a reversible transform.

No table family on this page uses compression.

Writing a `.tbl` file means selecting the family from its filename and serializing that family's records. There is no universal `.tbl` encoder.

## Format families

| Filename family | Representation | Consumer |
|---|---|---|
| `Effect.tbl` | Decimal text lists terminated by 255 | Effect sequencing |
| `Efct*.tbl`, `Mefc*.tbl` | Four-byte little-endian records | Per-frame effect metadata |
| `pal*.tbl`, `itempal.tbl`, `effpal.tbl`, `stcpal.tbl`, `mptpal.tbl` | Line-oriented signed decimal mappings | Palette selection |
| `gndani.tbl`, `stcani.tbl` | Line-oriented decimal animation records | Map animation |
| `gndattr.tbl` | Commented text | Ground attributes |
| `iplookup.tbl` | Plain decimal text | Endpoint cache |
| `mServer.tbl` | Mixed decimal and pair-swapped text | Multi-server retry table |
| `msg.tbl` | Direct message-table bytes | UI language table |

The endpoint and message tables are documented in [Configuration, NFO, profile, and table files](config-and-table-files.md).

## `Effect.tbl`

`file_effect_table_load` at `0x458ED0` reads decimal values with `sscanf_s`.

The first value is a list count. The client allocates an offset array and a fixed 32-byte area per list. Each list then contains decimal byte values ending with `255` (`0xff`).

```text
<list count>
<value> <value> ... 255
<value> <value> ... 255
```

The stored terminator is part of the sequence. The original code assumes each list fits its 32-byte allocation, so an independent parser should reject longer lists.

To write `Effect.tbl`, emit the decimal list count, then one whitespace-separated list per line with a final `255`. Limit each list to 32 stored values including that terminator.

## Effect frame sidecars

When `render_decode_image_entry` at `0x48B530` loads an EPF name containing `Efct` or an SPF name containing `Mefc`, it tries a same-basename `.tbl` entry.

Each frame has one binary record:

```c
struct effect_frame_table_record {
    u16 value_00;
    u16 value_02;
};
```

The client seeks to `frame_index * 4` and copies both little-endian values into the resolved frame result. Files such as `efct001.tbl` are therefore arrays of these records. They are not text and have no header.

The corresponding encoder writes exactly two little-endian `u16` values per frame. Do not add a count or terminator.

## Palette mapping tables

The palette manager loads names including:

- `pal%d.tbl`
- `itempal.tbl`
- `effpal.tbl`
- `stcpal.tbl`
- `mptpal.tbl`

`file_palette_map_read_record` at `0x547810` reads one line at a time. It recognizes signed decimal values and stops scanning the line at a `//` comment. It accepts up to three values and requires at least two.

```text
<first> <second> [third] // optional comment
```

If only two values are present, the client copies the first into the second output before applying its normal adjustment. The first two outputs are then decremented by one. The third output is not decremented.

That behavior strongly suggests the text uses one-based palette or resource indices while runtime arrays use zero-based indices. The exact meaning of each column depends on the table family.

When writing a palette mapping, add one to the first two zero-based runtime values. Write the optional third value unchanged. Keep comments after `//` if human-readable annotations are useful.

## Map animation and attribute tables

`gndani.tbl` and `stcani.tbl` are parsed as decimal text by `map_load_animation_tables` at `0x5873A0` and its helpers. They describe ground and static-object animation records. The record fields still need semantic names.

`map_load_ground_attribute_table` at `0x58B8C0` opens `gndattr.tbl`, obtains its direct bytes and size, and passes the text to the ground-attribute parser. Commented text samples in the local archives confirm that this is not a packed binary table.

These map tables can be written as ordinary decimal text. Preserve the field count and line ordering from a compatible source table until the remaining record fields have semantic names.

## Configuration table transforms

The extension does not imply encryption:

- `iplookup.tbl` is plain decimal text.
- `msg.tbl` is copied without an additional decode step.
- `mServer.tbl` is mostly text, but two stored strings use an adjacent-byte swap beginning at byte 1. The same routine encodes and decodes those fields.

Because the adjacent-byte swap is self-inverse, an `mServer.tbl` writer applies the same transform used by the reader before storing either affected string.

See [Configuration, NFO, profile, and table files](config-and-table-files.md) for those layouts and the `mServer.tbl` transform.

## Important functions

| Function | Address | Role |
|---|---:|---|
| `file_effect_table_load` | `0x458ED0` | Parse `Effect.tbl` decimal lists |
| `render_decode_image_entry` | `0x48B530` | Read four-byte EPF and SPF sidecar records |
| `file_palette_map_read_record` | `0x547810` | Parse one palette mapping line |
| `render_load_pal_family_table` | `0x546440` | Load `pal%c.tbl` mappings |
| `render_load_item_palette_table` | `0x546980` | Load `itempal.tbl` mappings |
| `render_load_effect_palette_table` | `0x546C30` | Load `effpal.tbl` mappings |
| `render_load_static_palette_table` | `0x546EE0` | Load `stcpal.tbl` mappings |
| `render_load_map_tile_palette_table` | `0x547210` | Load `mptpal.tbl` mappings |
| `map_load_animation_tables` | `0x5873A0` | Load ground and static animation tables |
| `map_load_ground_attribute_table` | `0x58B8C0` | Load and parse `gndattr.tbl` |
