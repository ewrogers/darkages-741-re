# TBL lookup files

TBL is a naming convention, not one shared binary format. Most TBL assets are line-oriented text, but each loader gives its file a separate grammar.

## Palette range tables

`pal*.tbl`, `itempal.tbl`, `effpal.tbl`, `stcpal.tbl`, and `mptpal.tbl` use the same range parser. Blank lines and `//` comments are skipped.

```text
asset_id palette_id
first_asset_id last_asset_id palette_id
```

The first form maps one asset. The second maps an inclusive range. Asset IDs in the file are one-based, while the client stores them as zero-based indexes.

```text
parse_palette_line(tokens):
    if tokens.length == 2:
        first = last = tokens[0] - 1
        palette = tokens[1]
    else:
        first = tokens[0] - 1
        last = tokens[1] - 1
        palette = tokens[2]

    for id in first .. last:
        palette_for_asset[id] = palette
```

`effpal.tbl` also uses the thousands part of a value as a palette family. Keep the original numeric value if a tool does not implement that split.

## Other confirmed tables

| File | Purpose | Shape |
| --- | --- | --- |
| `Effect.tbl` | Effect frame sequences | Numeric text records described on the [Effect table](effect-table.md) page |
| `gndani.tbl`, `stcani.tbl` | Tile animation cycles | Numeric text described on the [animation table](tile-animation-tables.md) page |
| `gndattr.tbl` | Ground paint and special tile states | Structured `set_attr` records applied to tile IDs and inclusive ranges |
| `color.tbl` | Named color sets | Record ID followed by six RGB triples |
| `color*.tbl` | Variant color sets | Tuple width followed by indexed RGB records |
| [`meffect.tbl`](motion-effect-table.md) | Motion effect definitions | Structured text with numeric or compiled expression fields |
| `Skill_e.tbl`, `Skill_i.tbl` | Skill animation and behavior rows | Numeric text, semicolon comments |
| `msg.tbl` | Language messages | Line-oriented byte strings |
| `npci.tbl` | NPC information | Hierarchical text, full grammar not yet mapped |
| `trans_*.tbl` | Optional translation mappings | Reader exists, but no local samples were found |

Do not decode every text field as UTF-8. ASCII is common, while Korean text may use Windows code page 949. Preserve the original bytes when a field's language is not known.

### Variant color tables

The variant-color reader treats punctuation and whitespace alike: it skips bytes until it reaches a decimal digit. The first integer is the number of colors in every tuple. Each remaining record begins with a tuple index from 0 through 255 and contains that many RGB triples.

```text
colors_per_tuple
tuple_index red green blue [red green blue ...]
tuple_index red green blue [red green blue ...]
```

For example, a width of six means that every tuple record carries six RGB triples. The loader stops at end of input or when the next tuple index is outside the 0 through 255 range. In memory, every RGB triple becomes a six-byte entry containing the original component bytes and the renderer's packed color value.

`file_load_coloring_table` reads a named entry from the main DAT archive unless a caller supplies another archive. `file_load_variant_color_table` selects the numbered family used by renderable assets. The `ColoringTableMan` singleton then maps table IDs to parsed tables and resolves a tuple by table ID and tuple index.

### Ground attributes

`gndattr.tbl` assigns an `ATTR_gnd_paint` tuple to one or more ground tile IDs:

```text
[ set_attr:
    [ ATTR_gnd_paint: (red, green, blue, alpha), height ]
  apply_to:
    tile_id (first_id, last_id)
]
```

The Korean file comment describes `height` as how far up an object the color should be painted. The client reserves heights `1` and `2` as flags instead of ordinary paint depths. Height `1` becomes the ground-tile state used by the Human movement permission check. Items on those tiles receive a fixed translucent paint override. Height `2` becomes a second stored flag, but it does not feed that Human movement gate. See [Movement and swimming](../systems/movement-and-swimming.md#ground-tile-state).

## Writing tables

Keep comments, ordering, numeric bases, and unknown columns from a compatible source. The client generally accepts plain decimal output, but lookup order can matter when ranges overlap.

## Evidence

- `file_palette_table_parse_ranges` at `0x00547810`
- palette table loaders at `0x00546440`, `0x00546980`, `0x00546C30`, `0x00546EE0`, and `0x00547210`
- `file_load_ground_attribute_table` at `0x0058B8C0`
- `file_load_color_table` at `0x0044CD50`
- `file_load_motion_effect_table` at `0x0050E840`
- `expression_context_compile` at `0x0046D020`
- `expression_context_evaluate` at `0x0046E4F0`
- `file_parse_skill_table` at `0x00561840`
- `file_load_message_table` at `0x004A4AA0`
- `file_load_npc_info_table` at `0x005322A0`
