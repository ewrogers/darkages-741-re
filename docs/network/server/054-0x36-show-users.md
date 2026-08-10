# Show Users (`SShowUsers`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x36` (54) |
| Encoding | session key |
| Name provenance | Project protocol vocabulary, confirmed against the local raw opcode handler and `ShowUsersPane` behavior. |

## Purpose

`SShowUsers` supplies the rows shown by the world-user list. It is the response to [`CWho`](../client/024-0x18-who.md). The handler replaces the current lists, rebuilds their filters, and opens or reveals `ShowUsersPane`.

Opcode `0x36` is handled directly from the decoded body. It does not have a server packet-factory class in this client.

## Body

```text
packet SShowUsers {
    u8 opcode                    // 0x36
    u16 world_count
    u16 country_count
    repeat country_count {
        u8 class_and_flags
        u8 color                 // legend.pal index before local overrides
        u8 user_state            // UserState
        string8 title
        u8 is_master
        string8 name
    }
}
```

All multibyte integers are big-endian. `country_count`, not `world_count`, controls the row loop. The pane retains `world_count` as the larger displayed population value.

The parser consumes a complete row before validating its text sizes. A title longer than 48 bytes or a name longer than 24 bytes causes that row to be skipped.

## Class and flag byte

The client splits `class_and_flags` into three independent values:

| Bits | Client use |
| --- | --- |
| `0..2` | [`CharacterClass`](../protocol-types.md#characterclass), used for class-filter tabs |
| `3` | Same guild or family marker, used to include the row in that filtered list |
| `4..7` | Retained as a separate nibble; meaning unresolved |

Every valid row enters the all-users list. `is_master > 0` also places it in the master list. The low class bits select the matching class list. Bit 3 is consulted only when the local character has guild or family state, then routes the row into that special list.

The upper nibble is not used by the final visible-row builder or row renderer. It may support behavior elsewhere, but this client does not provide enough evidence to name the individual bits.

## Filter collections

The Who pane does not have twenty fixed user slots. Every accepted packet row is copied into dynamic `List` storage. The pane creates nine filter collections with a `0x60`-byte source-row stride, then rebuilds a separate visible `ListPane` whose row stride is `0x50` bytes and whose row height is 12 pixels.

| Filter index | Rows included |
| ---: | --- |
| `0` | Every accepted country row |
| `1` | `is_master > 0` |
| `2` | Class `1`, Warrior |
| `3` | Class `2`, Rogue |
| `4` | Class `3`, Wizard |
| `5` | Class `4`, Priest |
| `6` | Class `5`, Monk |
| `7` | Class `0`, Peasant |
| `8` | Same family or guild when the local character has that feature enabled |

Dialog actions 1 through 9 select filter indexes 0 through 8. The list is rebuilt from the selected collection, so the on-screen capacity comes from the `UsersList` control height and scrolling, not from the twenty friend slots.

The normal class range is 0 through 5. Mechanically, an unexpected class value `6` also enters filter 7 and value `7` enters filter 8 because the client uses `class + 1` for every nonzero three-bit value.

The pane allocates one additional `0x60`-byte list and inserts every accepted row into it. In the traced client this duplicate list is only inserted, cleared, and destroyed. Visible rebuilding selects one of the nine filter lists instead.

### Source row

Only the fields below are read after insertion. Unlisted bytes in the `0x60`-byte record have no established meaning.

```c
partial struct ShowUsersSourceRow {
    s32 order_key;          // +0x00, packet row index + 50
    u8 unknown_04;          // +0x04
    u8 upper_nibble;        // +0x05, class_and_flags bits 4..7
    u8 same_family_mask;    // +0x06, either 0x00 or 0x08
    u8 unknown_07;          // +0x07
    u32 palette_index;      // +0x08, widened from the wire byte
    u32 character_class;    // +0x0C, class_and_flags bits 0..2
    u8 unknown_10[5];       // +0x10
    u8 is_master;           // +0x15
    u8 user_state;          // +0x16
    char title[48];         // +0x17
    char name[25];          // +0x47, up to 24 bytes plus zero
};                          // 0x60 bytes
```

The visible projection discards the filter fields and keeps only:

```c
struct ShowUsersVisibleRow {
    u8 user_state;          // +0x00
    u8 padding_01[3];
    u32 palette_index;      // +0x04, renderer consumes the low byte
    char title[48];         // +0x08
    char name[24];          // +0x38
};                          // 0x50 bytes
```

On a replacement response, the pane finds the local character in the selected filter and asks the scrolling list to reveal the row ten positions after it, capped to the final row. Filter-button rebuilds preserve the current scroll position instead.

### Text boundaries

The packet parser accepts a title length of 48 and a name length of 24. The later visible-row copy uses destination capacities of exactly 48 and 24 with `strcpy_s` behavior. A source string equal to either capacity cannot include its terminator, so that destination is cleared. The effective nonempty visible-row limits are therefore 47 title bytes and 23 name bytes.

The row drawer then displays at most the first 21 title bytes and first 15 name bytes. These cuts are byte counts and are not DBCS-safe. The configured playable-name limit normally keeps character names below this renderer boundary.

## State

`user_state` uses the shared [`UserState`](../protocol-types.md#userstate) values `0` through `7`. The row renderer has exactly eight state visuals and displays state `0` for an out-of-range value.

## Color and local highlighting

The packet `color` byte is an index into palette slot 0, which the client loads from `legend.pal`. It is not a recovered `WorldListColor` enum.

Before drawing a row, the client compares its name with two local 20-entry lists:

| Match | Final palette index | Matching `legend.pal` RGB |
| --- | ---: | --- |
| No local match | Server `color` | Server-selected |
| `Friendlist.cfg` | `0x80` | `#00FF00` |
| `Familylist.cfg` | `0x24` | `#F75B8F` |

The family or guild check runs second, so `0x24` wins when a name appears in both lists. These highlights are client-side display overrides. They do not modify the packet row or the server's stored list.

Each scan checks all twenty slots, skipping blank entries. Comparison is case-insensitive through the client CRT: the normal path folds ASCII letters and compares the remaining bytes, while an active CRT locale supplies its byte-wise lowercase mapping. Commas, color suffixes, and surrounding spaces have no special syntax.

Matching occurs against the `0x60`-byte source row before its name is copied into the visible row. A 24-byte packet name can therefore receive a friend or family color even though the exact-capacity visible copy later clears its displayed name.

The row stores the final palette index as a byte. Values `0x00` through `0xFF` therefore fit the client path, although the visible result depends on the corresponding entry in `legend.pal`.

Both files are twenty-line local name lists stored in the active character's directory. Their complete layout is described in [Per-character configuration](../../application/configuration.md#per-character-configuration).

The compatible runtime extension keeps these stock checks as a fallback and consults a separate colored-name table first. See [Extended friend highlights](../../appendix/runtime-patches/extended-friend-highlights.md).

`Familylist.cfg` is the target client's filename. The game behavior and project vocabulary call this the guild or family list; the binary does not expose a separate English enum that resolves the naming difference.
