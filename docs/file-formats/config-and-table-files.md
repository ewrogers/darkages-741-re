# Configuration, NFO, profile, and table files

Most small configuration files are ordinary text. The confirmed transforms are limited to extended fastfile metadata, `japan2.nfo`, and two text fields in `mServer.tbl`.

## `Darkages.cfg`

`config_read_settings_file` (`0x432660`) reads `Darkages.cfg` as plain text with labels such as `Version`, `Port`, `Speed`, `KeyBoard`, `Sound Volume`, and `Music Volume`. The version field is a configuration schema revision, not the network version reported by `CVersion`.

No descrambler is used for this file.

## Region NFO markers

`config_detect_region_from_nfo_markers` (`0x434F00`) checks marker files in a fixed order. The first match wins.

| Priority | File | Region code | Storage |
|---:|---|---:|---|
| 1 | `usa.nfo` | 1 | Disk marker |
| 2 | `singapore.nfo` | 15 | Disk marker |
| 3 | `taiwan.nfo` | 14 | Archive entry |
| 4 | `japan.nfo` | 13 | Disk text plus archived `japan2.nfo` |
| 5 | `Unitel.nfo` | 2 | Disk marker |
| 6 | `LG.nfo` | 3 | Disk marker |
| 7 | `SK.nfo` | 4 | Disk marker |
| 8 | `Thrunet.nfo` | 6 | Disk marker |
| 9 | `GameOK.nfo` | 7 | Disk marker |
| 10 | `Bixel.nfo` | 8 | Disk marker |
| 11 | `Excitegame.nfo` | 10 | Disk marker |
| 12 | `KornetWorld.nfo` | 11 | Disk marker |
| 13 | `mihosoft.nfo` | 9 | Disk marker |

No match returns region code 0. The order matters because several marker files could exist at once.

### `japan2.nfo` descrambling

`japan.nfo` contains plain text in the form `isp : <decimal>`. The client then reads archived `japan2.nfo` one byte at a time and applies bitwise NOT at `0x43504A`:

```c
u8 decode_japan2_byte(u8 encoded)
{
    return (u8)~encoded;
}
```

Decoded lines are compared with the decimal ISP number. When a line matches, the following decoded line is copied to the regional configuration buffer at static address `0x6EAFF8`.

## `iplookup.tbl`

`iplookup.tbl` is a plain numeric endpoint cache. It contains an IPv4 value and port, written as decimal integers. It is not scrambled.

The Taiwan initializer reads the two values with separate `%d` scans. The connection retry path writes them with `%d %d`. Both forms are accepted because whitespace is equivalent to `scanf`.

See [Endpoint resolution](../network/endpoint-resolution.md) for its priority and update rules.

## `mServer.tbl`

`config_load_multi_server_table` (`0x55A240`) reads this plain-text outer structure:

```text
<header byte as decimal>
<record count as decimal>
repeat record_count times:
    <u32 field_00 as decimal>
    <u32 field_04 as decimal>
    <u32 field_08 as decimal>
    <text field, up to 255 characters>
    <text field, up to 9999 characters>
<trailing byte as decimal>
```

Each record occupies `0x281C` bytes in memory. The numeric fields are at offsets `0x00`, `0x04`, and `0x08`. The text fields begin at `0x0C` and `0x10C`.

After loading, `config_swap_multi_server_text_pairs` (`0x55A650`) decodes both text fields. It leaves byte 0 in place and swaps every following adjacent pair. Saving calls the same self-inverse transform before and after writing.

```c
void swap_text_pairs(char *text)
{
    u32 i;
    char temp;

    for (i = 2; i < strlen(text); i += 2) {
        temp = text[i - 1];
        text[i - 1] = text[i];
        text[i] = temp;
    }
}
```

For example, bytes at positions `1,2` exchange places, then `3,4`, then `5,6`. Applying the function twice restores the original text.

`mServer.tbl` is a multi-server record table used by a later connection retry path. It is not the first source used by the normal US hostname resolver.

## `msg.tbl`

`ui_language_table_ctor` (`0x4A4AA0`) first opens `msg.tbl` through the archive singleton used for `national.dat`. If the entry is absent, it opens disk `msg.tbl` in binary mode. The selected bytes are copied into the language-table buffer without another decode step.

## Profile files

Startup chooses `Darkages.prf` for region code 1 and `Legend.prf` for other regions. `config_build_character_profile_path` (`0x592DE0`) rewrites the filename as:

```text
.\<player_character_name>\<profile filename>
```

`config_load_profile_file` (`0x54DA60`) reads repeated plain decimal pairs:

```text
<index> <value>
```

Each value is stored in a table indexed by the first integer. No profile-file descrambler is present in this path.
