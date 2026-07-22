# Metadata files

Metadata is a small server-managed database. The client keeps compressed files under `metafile/`, checks the inflated bytes with CRC32, then parses named groups of length-prefixed values.

Local examples include item information, lighting, NPC illustrations, nation descriptions, class data, and event data. Every inspected local metadata cache file is a standard zlib stream. Their inner value meanings are table-specific.

## Decoded container

All counts and lengths are big-endian.

```text
file MetadataCache {
    compressed zlib {
        u16be group_count
        repeat group_count {
            record group {
                u8 name_length
                bytes name[name_length]
                u16be value_count
                repeat value_count {
                    record value {
                        u16be length
                        bytes data[length]
                    }
                }
            }
        }
    }
}
```

Names and values are not NUL terminated on disk. Treat value data as bytes until that table's schema proves it is text. Text may use Windows code page 949.

## Cache and update flow

The files in `metafile/` contain the original zlib stream received from the server, not the inflated table.

```text
server sends metadata inventory
    |
    +-- local file missing or CRC differs
            |
            +-- client requests the named table
                    |
                    +-- inflate zlib payload
                    +-- calculate CRC32 over inflated bytes
                    +-- save original compressed bytes
                    +-- parse groups and values
```

Inventory entries contain a one-byte name length, the name bytes, and a `u32be` CRC32. A payload response contains the name, expected `u32be` CRC32, `u16be` compressed size, and the zlib bytes. The inflate buffer is capped at `0x20000` bytes.

## Create metadata

```text
build_metadata(groups):
    decoded = encode_big_endian_group_container(groups)
    checksum = crc32(decoded)
    compressed = zlib_compress(decoded)
    return checksum, compressed
```

The cache filename and inventory name must agree. A server also needs to advertise the new CRC so the client knows whether to request the replacement.

## Class ability tables

The local character profile uses one class table to build its skill and spell reference. When [`SSelfLook`](../network/server/057-0x39-self-look.md) reports a different `character_class`, `UserInfoPane` subscribes to `SClass<character_class>`. A Wizard therefore requests `SClass3`.

```text
SClass<character_class>
    -> parse skill and spell constraints
    -> compare them with the local character
    -> build the profile's skill and spell lists
```

The table is divided by four marker groups:

```text
Skill
    ability groups...
Skill_End
Spell
    ability groups...
Spell_End
```

An ability group needs a nonempty group name and at least six values. The group name is the exact skill or spell name. The client consumes the first six values and ignores later values.

| Value | Syntax | Client use |
| ---: | --- | --- |
| `0` | `level/show_ability_metadata/ability_level` | Minimum character progression. A nonzero third number also requires `show_master_metadata`. |
| `1` | Four slash-separated integers | The first integer selects the icon frame. The other meanings remain unresolved. |
| `2` | `STR/INT/WIS/CON/DEX` | Minimum attributes in this exact order. |
| `3` | `name/level` | First prerequisite spell or skill. `0/0` disables it. |
| `4` | `name/level` | Second prerequisite spell or skill. `0/0` disables it. |
| `5` | Text split by `$` | Description and acquisition lines. |

The local check first searches the live spell or skill inventory for the exact ability name. It also returns the learned level. A learned ability is shown as learned even if its current metadata requirements would fail.

An unlearned ability is learnable only when all of these checks pass:

- character level is at least value `0.0`;
- `SSelfLook.show_ability_metadata` is at least value `0.1`;
- when value `0.2` is nonzero, `SSelfLook.show_master_metadata` is nonzero and the `SStatus.ability_level` is high enough;
- the five `SStatus` attributes meet value `2`;
- each nonzero prerequisite name is present as either a learned spell or learned skill at the requested level.

The resulting row state is `1` for learned, `2` for learnable, and `3` for locked. The newer UI uses that number to select `skill001.epf` through `skill003.epf`, or the matching `spell` file. The metadata icon number selects a frame from that file.

### Skill and spell UI

Only the local form of `UserInfoPane` constructs RTTI class `nui_SkillSpellPane`. Its `_nui_sk.txt` layout contains separate `SKILL` and `SPELL` scrollable lists.

Selecting a row opens RTTI class `SkillSpellInfoDialogPane` from `_nui_ske.txt`. The dialog has `ICON`, `LEV`, `STR`, `INT`, `WIS`, `CON`, `DEX`, `NAME`, `SUB1`, `SUB2`, and `DESC` regions. Met requirements use palette index `0xFF`; failed requirements use `0x28`.

The compiled older profile path keeps the same parsed constraint objects in `LegendInfoPane`. It shows them through `SpellSkillInfoPane` and opens `SpellSkillPropertyPane` from `llsprop.txt`. That dialog runs the same local requirement check and also marks failed lines with palette index `0x28`.

## Event tables

The local profile subscribes to `SEvent1` through `SEvent7` the first time it receives `SSelfLook`. Each table is parsed as a sequential set of records. A record starts at `<prefix>_start` and ends at `<prefix>_end`.

| Group suffix | Values used | Meaning |
| --- | --- | --- |
| `start` | None | Begins one event record. |
| `title` | First value | Display title. |
| `id` | First value | Exact legend key that marks this event complete. |
| `qual` | First two values | Progression-bucket digits, then class digits. |
| `sum` | First value, split by `$` | Incomplete-event summary lines. |
| `result` | First value, split by `$` | Completed-event result lines. |
| `sub` | Every value | Legend keys for prerequisite events. |
| `reward` | First value | Optional reward text. |
| `end` | None | Completes the record. |

`title`, `id`, `qual`, `sum`, `result`, `sub`, and `end` must all appear. `reward` is optional. Extra values are ignored except in `sub`, where every value is retained.

The first `qual` value is a compact set of allowed progression buckets. The parser accepts digit characters `1` through `8`, although the matching client only produces buckets `1` through `7`:

| Bucket | Local character state |
| ---: | --- |
| `1` | Level below 11 |
| `2` | Level 11 through 40 |
| `3` | Level 41 through 70 |
| `4` | Level 71 through 98 |
| `5` | Level 99 or higher |
| `6` | `show_ability_metadata` is nonzero |
| `7` | `show_master_metadata` is nonzero |

Bucket `7` takes priority over bucket `6`, and both take priority over the ordinary level buckets. The second `qual` value is a set of allowed [`CharacterClass`](../network/protocol-types.md#characterclass) digits `1` through `5`. Peasant value `0` cannot match this mask.

The client assigns each event one UI state:

1. If its `id` exactly matches a current `SSelfLook` legend key, the event is complete.
2. Otherwise it is available only when the progression and class masks match and every nonempty `sub` key is already in the legend.
3. An incomplete event that fails any check is locked.

Legend matching is case-sensitive. It compares the hidden legend key, not the visible legend text.

### Event UI

Only the local `UserInfoPane` constructs RTTI class `nui_EventPaneImpl`. `_nui_ev.txt` supplies two visible event lists plus `PREV` and `NEXT` controls. Six internal categories are shown as three pages of two lists. `SEvent1` through `SEvent5` have their own categories; `SEvent6` and `SEvent7` are both placed in the sixth category.

Rows use frames `0`, `1`, and `2` from `leicon.epf` for complete, available, and locked. A row also shows its title and a localized progression label.

Selecting a row opens `EventInfoDialogPane` from `_nui_eve.txt`. Its regions are `ICON`, `LEV`, `NAME`, `MUST`, `REWARD`, and `DESC`. An incomplete event shows `sum` lines; a complete event shows `result` lines. `MUST` resolves only the first prerequisite key to another event title, but the availability check still requires every `sub` key.

The older `EventInfoPane` keeps seven categories. It uses the same completion, qualification, and legend checks, then expands each list row with up to four `sum` or `result` lines.

### Inspected local cache

The local installation contains `SClass3` and all seven event files. These counts describe that cache, not a fixed client limit:

| File | Parsed records |
| --- | ---: |
| `SClass3` | 12 skills and 143 spells |
| `SEvent1` | 15 events |
| `SEvent2` | 6 events |
| `SEvent3` | 5 events |
| `SEvent4` | 6 events |
| `SEvent5` | 7 events |
| `SEvent6` | 0 events |
| `SEvent7` | 0 events |

One local `SClass3` ability group has a seventh value. The client ignores it, confirming that later values are not an extension of the six-value schema.

## Item, skill, and spell denial tables

The RTTI-backed `DeniedItemList` is one consumer of this metadata system. It creates three empty runtime lookup containers and subscribes to these hardcoded table names:

- `BItems`
- `BSkills`
- `BSpells`

If `MetaTableManager` is not ready when the list is constructed, the client retries the subscriptions after one second. A valid cached table can be applied locally. A missing or stale table follows the normal `SMetaData` inventory, `CMetaData` request, and `SMetaData` payload flow described above.

Applying a table replaces the current in-memory lists and routes rows tagged `Item`, `Skill`, or `Spell` into the matching lookup. Item activation, skill activation, and spell activation consult their respective list before sending the normal action packet.

The executable hardcodes the three metadata names and the parser, but not the individual denial entries. The server can replace the entries by advertising a new CRC and supplying a new table payload.

The inspected installation has 19 cached metadata files but no `BItems`, `BSkills`, or `BSpells` file. No supplied capture contains one of these table names. In that state the three runtime lists begin empty and do not block an action.

## NPC illustration table

`NPCIllustFileMan` subscribes to the metadata table named `NPCIllust`. Each group name is an exact NPC name and each value is an image filename in `npc/npcbase.dat`. The update loop clears the name's current list before each append, so only the final value survives when a group supplies several values. The dialog packet supplies an index into the retained list.

The inspected cache contains 170 groups and 26 distinct SPF filenames. Every group has one value, so the observed rows use illustration index zero. The metadata contains no image bytes. It only connects speaker names to shared art. See [NPC dialog illustrations](../systems/npc-dialog-illustrations.md) for the lookup, fallback, and draw path.

## Evidence

- `net_handle_metadata` at `0x004E4EA0`
- `net_metadata_uncompress` at `0x004E54F0`
- `file_load_metadata_compressed` at `0x004E5570`
- `file_save_metadata_compressed` at `0x004E56E0`
- `net_metadata_crc32` at `0x004E5790`
- `net_parse_metadata_table` at `0x004E57C0`
