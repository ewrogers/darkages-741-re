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

## State

`user_state` uses the shared [`UserState`](../protocol-types.md#userstate) values `0` through `7`. The row renderer has exactly eight state visuals and displays state `0` for an out-of-range value.

## Color and local highlighting

The packet `color` byte is an index into palette slot 0, which the client loads from `legend.pal`. It is not a recovered `WorldListColor` enum.

Before drawing a row, the client compares its name with two local 20-entry lists:

| Match | Final palette index |
| --- | ---: |
| No local match | Server `color` |
| `Friendlist.cfg` | `0x80` |
| `Familylist.cfg` | `0x24` |

The family or guild check runs second, so `0x24` wins when a name appears in both lists. These highlights are client-side display overrides. They do not modify the packet row or the server's stored list.

The row stores the final palette index as a byte. Values `0x00` through `0xFF` therefore fit the client path, although the visible result depends on the corresponding entry in `legend.pal`.

Both files are twenty-line local name lists stored in the active character's directory. Their complete layout is described in [Per-character configuration](../../application/configuration.md#per-character-configuration).

The compatible runtime extension keeps these stock checks as a fallback and consults a separate colored-name table first. See [Extended friend highlights](../../appendix/runtime-patches/extended-friend-highlights.md).

`Familylist.cfg` is the target client's filename. The game behavior and project vocabulary call this the guild or family list; the binary does not expose a separate English enum that resolves the naming difference.
