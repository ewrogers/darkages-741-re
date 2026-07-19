# Server list and greeting

`mServer.tbl` stores an alternate server list and its greeting text. It is not the primary endpoint source in the normal connection path. The client can also update the selected greeting through `SStipulation`.

## File layout

This is a line-oriented text file. Numeric values are written as decimal lines.

```c
struct ServerTable {
    u8 version;
    u8 record_count;
    u8 trailing_value;
    ServerTableRecord *records;
};

struct ServerTableRecord {
    u32 server_id;
    u32 ipv4_value;
    u32 port;
    char name[256];
    char greeting[10000];
};                          // 0x281C bytes
```

The file begins with a decimal version and record count. Each record then stores the three numeric fields, one name line, and one greeting line. One trailing numeric byte follows all records.

Name and greeting lines use a self-inverse byte transform. Byte 0 stays in place, then byte pairs 1 and 2, 3 and 4, and so on are swapped.

```text
transform_text(bytes):
    for i = 1; i + 1 < length; i += 2:
        swap(bytes[i], bytes[i + 1])
```

Applying the transform again restores the original text. The local table contains one record whose decoded name is `Dark Ages` and whose greeting begins with `Welcome to Dark Ages`. The endpoint value is intentionally not reproduced in the book.

## Server-list synchronization

[`SVersionCheck`](server/000-0x00-version-check.md) provides a CRC32 for the list's record count, server IDs, IPv4 values, ports, and names. A missing or mismatched local list causes [`CMulti`](client/087-0x57-multi-server.md) operation `1` to request a replacement.

[`SMulti`](server/086-0x56-multi.md) returns that replacement as a zlib-compressed list. The client rebuilds the same `0x281C`-byte runtime records, initializes each greeting to a single space, and saves the result to `mServer.tbl`. A selected server's greeting is synchronized afterward through `SStipulation`.

## Greeting synchronization

The server has two `SStipulation` modes:

- Mode 0 sends a `u32be` CRC32 for the current decoded greeting. A match displays the local text. A mismatch sends an empty `CStipulation` request.
- Mode 1 sends a `u16be` zlib size followed by compressed replacement text. The client inflates at most 10,000 bytes, updates `mServer.tbl`, and displays the new greeting.

```text
receive greeting CRC
    |
    +-- matches local text -> display greeting
    |
    +-- differs -> request replacement
                       |
                       +-- inflate and save -> display greeting
```

CRC32 covers the decoded greeting bytes up to the first NUL. It does not cover the pair-swapped file representation.

## Evidence

- `net_load_server_table` at `0x0055A240`
- `net_save_server_table` at `0x0055A490`
- `net_transform_server_table_text` at `0x0055A650`
- `net_apply_multi_server_list` at `0x0055AAD0`
- `ui_server_select_dialog_handle_multi` at `0x00559E80`
- `net_handle_stipulation_raw` at `0x004B8570`
- `net_handle_stipulation` at `0x004B8890`
