# Extended friend highlights

The client can highlight more locally classified names without changing its stock friend dialog. The least intrusive design keeps the original twenty friend fields and their file exactly as they are, then lets a launcher add a separate read-only table used only while choosing an online-user row's color.

This is a compatibility layer, not a larger in-game editor. `Friendlist.cfg` remains owned by the client. An extension file remains owned by the launcher, so opening or saving the stock dialog cannot erase extended names.

## Why the stock array cannot grow

The friend and family lists are inline arrays at the end of `UserInfo`. There is no spare record after either list.

```c
partial struct UserInfo {
    u8 other[0x504];
    char friend_names[20][40];  // +0x504 through +0x823
    char family_names[20][40];  // +0x824 through +0xB43
};                              // size 0xB44
```

Changing a comparison from 20 to 40 would make the friend loop consume the family array. Extending the family loop would run beyond `UserInfo`. The loaders, writers, friend dialog, family dialog, and row-highlighting code also contain their own fixed bounds. A real inline-array expansion would therefore require a new object layout and changes across every owner.

The fixed owners are:

| Current Binary Ninja symbol | Static address | RVA | Role |
| --- | ---: | ---: | --- |
| `file_read_dbcs_line` | `0x00592680` | `0x00192680` | Read one DBCS-aware text line into a fixed slot |
| `user_info_load_friend_list` | `0x00592800` | `0x00192800` | Clear and load twenty friend slots |
| `user_info_save_friend_list` | `0x00592920` | `0x00192920` | Write twenty friend slots |
| `user_info_load_family_list` | `0x00592560` | `0x00192560` | Clear and load twenty family slots |
| `user_info_save_family_list` | `0x00592730` | `0x00192730` | Write twenty family slots |
| `ui_family_list_dialog_ctor` | `0x00471320` | `0x00071320` | Construct the twenty-field `FamilyListDialogPane` |
| `ui_family_list_dialog_commit_fields` | `0x00471810` | `0x00071810` | Copy, truncate, and save all twenty family fields |
| `ui_friend_list_dialog_ctor` | `0x005435F0` | `0x001435F0` | Construct the twenty-field `FriendListDialog` |
| `ui_friend_list_dialog_handle_action` | `0x00543C70` | `0x00143C70` | Handle OK/Cancel and save on OK |
| `ui_show_users_rebuild_visible_list` | `0x0055C3E0` | `0x0015C3E0` | Apply server, friend, and family row colors |

## Length and color limits

The client exposes several different limits:

| Context | Confirmed limit |
| --- | ---: |
| Safe `Friendlist.cfg` or `Familylist.cfg` line payload | 39 bytes |
| Runtime slot including its terminating zero | 40 bytes |
| Family dialog value retained on commit | 30 DBCS-safe bytes |
| Name retained by `SShowUsers` | 24 bytes |
| Playable character name reported by the project owner | Effectively 13 characters |
| Row palette index | `0x00` through `0xFF` |

The file reader receives a capacity of 40, reads bytes until a newline, and then writes the terminating zero at the current index. A 40-byte payload can therefore write its terminator into the following slot. Keep every stock line at 39 bytes or less.

The stock friend dialog has a related mismatch. Its commit handler asks a text field for up to 64 bytes while giving it a 40-byte destination slot. An extension should not depend on packed text surviving this path.

The family dialog is more conservative but still fixed. Its commit path applies a DBCS-safe 30-byte truncation to each of exactly twenty fields before calling `user_info_save_family_list`. It cannot preserve packed data beyond that limit.

The 24-byte Show Users limit is a parser boundary, not evidence that the game permits a 24-character playable name. The extension table should still use 24-byte name storage so it matches the row representation. Keep names as the client's original bytes, including code page 949 bytes when present. Do not convert them to UTF-8 inside the lookup table.

The renderer consumes the low byte of the selected palette value. Every byte value fits structurally, but not every `legend.pal` entry is guaranteed to be readable against the pane background.

## Why comma packing is only a prototype

Comma packing can produce more logical names without a new allocation, but it still needs a matcher patch because the stock client compares the complete line literally. A suffix such as `#4` also needs the matcher to remove and parse it.

With the project owner's 13-character maximum, two maximum-length names with one-character color suffixes use 31 bytes without spaces:

```text
ThirteenChars#4,ThirteenChars#5
```

That would allow forty logical names across the twenty stock slots. Shorter names can sometimes fit three to a slot. The packed syntax remains visible in the stock dialog, spaces consume the same 39-byte budget, and an edit can accidentally damage several logical entries at once. The dialog's 64-byte copy request makes the boundary especially unfriendly. This is useful for proving the matcher but is not the recommended user-facing format.

## Separate extension data

The launcher should parse the per-character extension file `<character>\\Friendlist.ini`. The client has no JSON or YAML parser, and neither format is needed here. A small INI-style grammar is enough:

```ini
[Rangers]
color=1
members=CharacterA,CharacterB,CharacterC

[Clerics]
color=0x24
members=HealerA,HealerB
members=HealerC
```

The grammar is intentionally small:

| Form | Meaning |
| --- | --- |
| `[GroupName]` | Begin one named color group |
| `color=<value>` | Set the required group palette byte in decimal or `0x` hexadecimal |
| `members=<name>,<name>` | Add one or more comma-separated members |
| `; comment` | Ignore the rest of a comment line |

Each section requires exactly one `color` and at least one nonempty `members` value. More than one `members` line is allowed and avoids an unnecessarily long physical line. Surrounding ASCII spaces are ignored around keys, values, commas, and names. Group names are labels for people editing the file and are not stored in the injected table. Quoting, escapes, inheritance, dotted keys, and multiline values are not supported.

Unknown keys, malformed values, overlong input lines, missing colors, empty member tokens, and unreasonable counts should reject that character's extension profile without affecting the stock list. `color` accepts decimal or hexadecimal values from `0x00` through `0xFF`. A semicolon begins a comment only when it is the first non-space character on a line.

Duplicate names across groups are an error because a name can have only one final row color. Names remain raw client bytes and may not exceed 24 bytes. The launcher resolves group names to flat name and palette records before injection. The hook therefore knows nothing about INI sections, commas, or group names.

The injected table uses one fixed-size record per colored name. Repeating the character name in each record makes lookup linear and removes runtime offsets or nested allocations:

```c
struct ExtendedFriendEntry {
    u8 character_length;  // 1 through 24
    u8 name_length;       // 1 through 24
    u8 palette;
    u8 reserved;
    u8 character_name[24];
    u8 name[24];          // raw client text bytes, not zero-terminated
};

struct ExtendedFriendTable {
    u32 magic;            // "FCLR", 0x524C4346
    u16 version;          // 1
    u16 entry_count;      // 0 through 1,024
    u32 byte_size;        // 12 + entry_count * 52
    ExtendedFriendEntry entries[];
};
```

The launcher can scan all character directories for `Friendlist.ini` before resuming the game and place every valid entry in one allocation. This avoids needing to know the selected character at launch. The hook compares each entry's character name with the live `session_character_name` when Show Users rows are rebuilt.

Reject names longer than 24 bytes, palette values outside one byte, duplicate names for one character, unsupported table versions, a `byte_size` other than `12 + entry_count * 52`, and counts above 1,024. This keeps a simple linear lookup bounded while remaining far beyond the stock list.

## Compatible lookup flow

The extension check sits before the two original scans:

```c
color = server_color;

if (extended_table_is_valid()) {
    profile = find_profile(session_character_name);
    if (profile != NULL && find_extended_name(profile, row_name, &color)) {
        goto color_selected;
    }
}

if (stock_friend_list_contains(row_name))
    color = 0x80;

if (stock_family_list_contains(row_name))
    color = 0x24;

color_selected:
add_visible_row(row, color);
```

An extension match wins because it represents an explicit custom color. On a miss, the client executes its original friend and family loops. Edits made through the stock friend dialog therefore remain live. A missing, invalid, or unmatched extension table follows the original path without changing behavior.

The final priority is:

| Priority | Color source |
| ---: | --- |
| 1 | Matching `Friendlist.ini` group color |
| 2 | Stock `Familylist.cfg` color `0x24` |
| 3 | Stock `Friendlist.cfg` color `0x80` |
| 4 | Server-provided row color |

The two stock checks retain their original order on an extension miss. The custom lookup skips both only after a positive match, so a configured group color cannot be overwritten by either stock list or by the server value.

The extension file is intentionally not serialized by the client and is not displayed in `FriendListDialog`. Changing it requires a relaunch in the first version. A later live-reload design should build an immutable replacement table and atomically publish its pointer, but the row-building hook must never perform file I/O or wait for the launcher.

## Hook site

Target fingerprint:

```text
Size: 3,112,960 bytes
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
Preferred image base: 0x00400000
```

`ui_show_users_rebuild_visible_list` initializes the stock friend-loop index immediately before both local scans. A seven-byte jump at that boundary can enter the extension stub without splitting an instruction.

| Purpose | Static address | RVA | Original bytes | Replacement template |
| --- | ---: | ---: | --- | --- |
| Enter extension lookup | `0x0055C500` | `0x0015C500` | `C7 45 FC 00 00 00 00` | `E9 rr rr rr rr 90 90` |

`rr rr rr rr` is the signed little-endian displacement from `loaded_base + 0x0015C505` to the allocated stub. It must be calculated after the launcher chooses the remote allocation.

```diff
- 0015C500: C7 45 FC 00 00 00 00 | mov dword [ebp-0x4], 0
+ 0015C500: E9 rr rr rr rr 90 90 | jmp extended_friend_hook
```

At this point the function has a stable frame and the values needed by the stub:

| Value | Location |
| --- | --- |
| Current decoded row | `[ebp-0x18]` |
| Row name | `[ebp-0x18] + 0x47` |
| Current server palette index | `[ebp-0x7C]` |
| Active character name | `0x0073D910`, RVA `0x0033D910` |

The stub has two continuations:

| Result | Static continuation | RVA | Required action |
| --- | ---: | ---: | --- |
| No extension match or invalid table | `0x0055C507` | `0x0015C507` | Replay `mov dword [ebp-0x4], 0`, then run both stock loops |
| Extension match | `0x0055C5D2` | `0x0015C5D2` | Store the chosen byte in `[ebp-0x7C]`, then skip both stock loops |

The stub must preserve the caller's nonvolatile registers and stack frame. It should compare names case-insensitively for ASCII letters while retaining non-ASCII bytes exactly. The launcher should keep executable code and table data in separate pages, with final protections of execute-read and read-only rather than a writable-executable page.

## Injected stub template

Allocate exactly 348 bytes, or `0x15C`, for the code template. The four zeroed `abs32` operands are filled from the relocation table. All internal branches and calls are relative within the blob and are already complete. Before relocation, the byte template has SHA-256 `E67525FEDD1B1B1AAC528086BA6ABD1E7FCA2E8EDA161D2F5121D91B868B2725`.

```text
000: 60                         | pushad
001: 8B 55 E8                   | mov edx, [ebp-0x18]          ; decoded row
004: 83 C2 47                   | add edx, 0x47                ; row name
007: 52                         | push edx
008: 68 00 00 00 00             | push active_character_abs32  ; relocated
00D: 68 00 00 00 00             | push table_abs32             ; relocated
012: E8 20 00 00 00             | call stub+0x037
017: 83 C4 0C                   | add esp, 12
01A: 85 C0                      | test eax, eax
01C: 74 0B                      | jz stub+0x029
01E: 48                         | dec eax                       ; color_plus_one to color
01F: 89 45 84                   | mov [ebp-0x7C], eax           ; custom color wins
022: 61                         | popad
023: 68 00 00 00 00             | push custom_match_abs32       ; relocated
028: C3                         | ret

029: 61                         | popad
02A: C7 45 FC 00 00 00 00       | mov dword [ebp-0x4], 0       ; replay displaced instruction
031: 68 00 00 00 00             | push stock_fallback_abs32     ; relocated
036: C3                         | ret

037: 55                         | push ebp
038: 89 E5                      | mov ebp, esp
03A: 83 EC 0C                   | sub esp, 12
03D: 53                         | push ebx
03E: 56                         | push esi
03F: 57                         | push edi
040: 8B 75 08                   | mov esi, [ebp+8]              ; table
043: 85 F6                      | test esi, esi
045: 0F 84 C1 00 00 00          | jz stub+0x10C
04B: 81 3E 46 43 4C 52          | cmp dword [esi], 0x524C4346  ; "FCLR"
051: 0F 85 B5 00 00 00          | jne stub+0x10C
057: 66 83 7E 04 01             | cmp word [esi+4], 1           ; version
05C: 0F 85 AA 00 00 00          | jne stub+0x10C
062: 0F B7 46 06                | movzx eax, word [esi+6]       ; entry count
066: 3D 00 04 00 00             | cmp eax, 1024
06B: 0F 87 9B 00 00 00          | ja stub+0x10C
071: 6B D0 34                   | imul edx, eax, 52
074: 83 C2 0C                   | add edx, 12
077: 0F 82 8F 00 00 00          | jc stub+0x10C
07D: 39 56 08                   | cmp [esi+8], edx              ; exact table byte size
080: 0F 85 86 00 00 00          | jne stub+0x10C
086: 89 45 F4                   | mov [ebp-0x0C], eax           ; remaining entries
089: 8B 7D 0C                   | mov edi, [ebp+0x0C]           ; active character
08C: 85 FF                      | test edi, edi
08E: 74 7C                      | jz stub+0x10C
090: 31 C0                      | xor eax, eax

092: 83 F8 18                   | cmp eax, 24
095: 77 75                      | ja stub+0x10C
097: 80 3C 07 00                | cmp byte [edi+eax], 0
09B: 74 03                      | je stub+0x0A0
09D: 40                         | inc eax
09E: EB F2                      | jmp stub+0x092

0A0: 89 45 FC                   | mov [ebp-0x04], eax           ; character length
0A3: 8B 5D 10                   | mov ebx, [ebp+0x10]           ; row name
0A6: 85 DB                      | test ebx, ebx
0A8: 74 62                      | jz stub+0x10C
0AA: 31 C0                      | xor eax, eax

0AC: 83 F8 18                   | cmp eax, 24
0AF: 77 5B                      | ja stub+0x10C
0B1: 80 3C 03 00                | cmp byte [ebx+eax], 0
0B5: 74 03                      | je stub+0x0BA
0B7: 40                         | inc eax
0B8: EB F2                      | jmp stub+0x0AC

0BA: 89 45 F8                   | mov [ebp-0x08], eax           ; row-name length
0BD: 83 C6 0C                   | add esi, 12                   ; first entry

0C0: 83 7D F4 00                | cmp dword [ebp-0x0C], 0
0C4: 74 46                      | je stub+0x10C
0C6: 8B 45 FC                   | mov eax, [ebp-0x04]
0C9: 38 06                      | cmp [esi], al                 ; character length
0CB: 75 37                      | jne stub+0x104
0CD: 8B 45 F8                   | mov eax, [ebp-0x08]
0D0: 38 46 01                   | cmp [esi+1], al               ; row-name length
0D3: 75 2F                      | jne stub+0x104
0D5: FF 75 FC                   | push dword [ebp-0x04]
0D8: 8D 46 04                   | lea eax, [esi+4]              ; stored character
0DB: 50                         | push eax
0DC: 57                         | push edi
0DD: E8 33 00 00 00             | call stub+0x115
0E2: 83 C4 0C                   | add esp, 12
0E5: 85 C0                      | test eax, eax
0E7: 74 1B                      | jz stub+0x104
0E9: FF 75 F8                   | push dword [ebp-0x08]
0EC: 8D 46 1C                   | lea eax, [esi+28]             ; stored member name
0EF: 50                         | push eax
0F0: 53                         | push ebx
0F1: E8 1F 00 00 00             | call stub+0x115
0F6: 83 C4 0C                   | add esp, 12
0F9: 85 C0                      | test eax, eax
0FB: 74 07                      | jz stub+0x104
0FD: 0F B6 46 02                | movzx eax, byte [esi+2]       ; palette
101: 40                         | inc eax                        ; reserve zero for no match
102: EB 0A                      | jmp stub+0x10E

104: 83 C6 34                   | add esi, 52
107: FF 4D F4                   | dec dword [ebp-0x0C]
10A: EB B4                      | jmp stub+0x0C0

10C: 31 C0                      | xor eax, eax                  ; no extension match
10E: 5F                         | pop edi
10F: 5E                         | pop esi
110: 5B                         | pop ebx
111: 89 EC                      | mov esp, ebp
113: 5D                         | pop ebp
114: C3                         | ret

115: 55                         | push ebp                        ; ASCII-case comparison
116: 89 E5                      | mov ebp, esp
118: 56                         | push esi
119: 57                         | push edi
11A: 8B 75 08                   | mov esi, [ebp+8]
11D: 8B 7D 0C                   | mov edi, [ebp+0x0C]
120: 8B 4D 10                   | mov ecx, [ebp+0x10]
123: 85 C9                      | test ecx, ecx
125: 74 26                      | jz stub+0x14D

127: 0F B6 06                   | movzx eax, byte [esi]
12A: 0F B6 17                   | movzx edx, byte [edi]
12D: 3C 41                      | cmp al, 'A'
12F: 72 06                      | jb stub+0x137
131: 3C 5A                      | cmp al, 'Z'
133: 77 02                      | ja stub+0x137
135: 04 20                      | add al, 0x20
137: 80 FA 41                   | cmp dl, 'A'
13A: 72 08                      | jb stub+0x144
13C: 80 FA 5A                   | cmp dl, 'Z'
13F: 77 03                      | ja stub+0x144
141: 80 C2 20                   | add dl, 0x20
144: 38 D0                      | cmp al, dl
146: 75 0C                      | jne stub+0x154
148: 46                         | inc esi
149: 47                         | inc edi
14A: 49                         | dec ecx
14B: 75 DA                      | jne stub+0x127

14D: B8 01 00 00 00             | mov eax, 1
152: EB 02                      | jmp stub+0x156
154: 31 C0                      | xor eax, eax
156: 5F                         | pop edi
157: 5E                         | pop esi
158: 89 EC                      | mov esp, ebp
15A: 5D                         | pop ebp
15B: C3                         | ret
```

Relocate the four absolute operands before writing the code page:

| Operand offset | Encoding | Value |
| ---: | --- | --- |
| `0x009` | `abs32` | `module_base + 0x0033D910`, active character name |
| `0x00E` | `abs32` | `table_base` |
| `0x024` | `abs32` | `module_base + 0x0015C5D2`, custom-match continuation |
| `0x032` | `abs32` | `module_base + 0x0015C507`, stock fallback |

The hook itself has one `rel32` operand at `module_base + 0x0015C501`:

```text
signed-rel32 = stub_base - (module_base + 0x0015C505)
```

As a relocation test vector only, a preferred-base process with `stub_base = 0x00670000` and `table_base = 0x02000000` produces:

```text
009: 10 D9 73 00 | active character address
00E: 00 00 00 02 | extension table address
024: D2 C5 55 00 | custom-match continuation
032: 07 C5 55 00 | stock fallback
hook bytes: E9 FB 3A 11 00 90 90
```

## Verification

The hook bytes were read back from the matching local executable independently of the decompiler. The documented 348-byte template was assembled as 32-bit x86, and every listed byte matched the assembler output after the four relocation operands were zeroed.

An x86 emulator exercised the complete relocated blob with its real stack-frame contract. The checks covered ASCII case folding, exact non-ASCII byte matching, a 24-byte name, palette values `0x00` through `0xFF`, custom-color priority, valid-table misses, invalid magic, invalid byte size, the 1,024-entry bound, register preservation, stack preservation, and the stock fallback continuation. All checks passed.

This verifies the injected code in isolation. It has not yet been observed inside a running client, so the launcher should initially expose the feature behind an opt-in setting and retain the original-byte fail-closed checks.

## Installation without a DLL

No DLL or remote thread is required. A launcher can install the table and hook before the first game instruction runs:

```text
verify the executable size and SHA-256
launch the client suspended
find the loaded main-module base
parse and validate every extension entry outside the client
allocate and write the extension table, then protect it read-only
allocate and relocate the lookup stub, then protect it execute-read
verify the seven original hook bytes
temporarily make the hook page writable
write the complete jump and padding
flush the instruction cache
restore the original page protection
resume the main thread
```

If the fingerprint, hook bytes, table validation, allocation, relocation, or page-protection step fails, terminate the suspended child without applying a partial patch. Runtime addresses must always use the loaded module base plus the recorded RVA.

## Behavior contract

- The stock dialog continues to own exactly twenty `Friendlist.cfg` entries.
- The stock family list and its second-pass precedence remain unchanged when no extension entry matches.
- An extension entry with the same name intentionally supplies the final custom color.
- Removing a stock entry does not remove a duplicate extension entry. The extension file must be edited separately.
- Opening or saving the stock dialog cannot overwrite `Friendlist.ini`.
- The extension affects only local Show Users row coloring. It does not create a server-side friendship or change another packet.
- Extension changes take effect after relaunch until a separate immutable-table reload path is implemented.
