# Menu item quantities

This patch changes stackable item labels in `ClientItemMenuDialog` from `Potion` to `Potion (5)`. It covers the own-inventory lists used by `SScreenMenu` subtypes 5 and 11, including merchant and storage flows that use this dialog class.

## Target and dependencies

| Role | Static address | RVA |
| --- | --- | --- |
| `ClientItemMenuDialog` row-builder call | `0x004D4F82` | `0x000D4F82` |
| Existing `ItemListPane` row builder | `0x004D3700` | `0x000D3700` |
| `ui_get_gui_back_pane` | `0x005A9C40` | `0x001A9C40` |
| `ui_text_truncate_dbcs_safe` | `0x0047D670` | `0x0007D670` |
| `wsprintfA` import address-table entry | `0x00669380` | `0x00269380` |

The row-builder hook is:

```diff
- 000: E8 79 E7 FF FF    | call item_list_row_builder   ; build the original menu row
+ 000: E8 <stub rel32>   | call menu_item_quantity_stub ; rewrite only the temporary label
```

The original code builds each row from a one-based inventory slot. The name is passed separately from that slot and is copied immediately into a 256-byte local buffer by the row builder. The hook changes only the temporary name pointer. The slot, icon, dye, selection value, and every other argument remain unchanged.

The injected code relies on these fingerprint-specific object fields:

```c
struct GUIBackPaneFields {
    u8 unrelated_0000[0x4F88];
    InventoryPane_A *item_inventory;       // +0x4F88
};

struct InventoryPaneFields {
    u8 unrelated_0000[0x1A0];
    InvItemPane *items[60];                // +0x1A0, slots 1 through 60
};

struct InvItemPaneFields {
    u8 unrelated_0000[0x240];
    u32 quantity;                          // +0x240
    u8 can_stack;                          // +0x244
};
```

An invalid slot, missing pane pointer, non-stackable item, or zero quantity uses the original label. This fail-open behavior keeps stale UI state from blocking construction of the server-requested dialog.

## Confirmed call path

For `SScreenMenu` subtype 5, the client reaches this row builder through three direct calls:

| Stage | Static address | RVA | Original call bytes |
| --- | --- | --- | --- |
| Subtype 5 dispatch | `0x004CDAA1` | `0x000CDAA1` | `E8 7A 15 00 00` |
| `ClientItemMenuDialog` construction | `0x004CF083` | `0x000CF083` | `E8 98 5C 00 00` |
| Inventory row construction | `0x004D4F82` | `0x000D4F82` | `E8 79 E7 FF FF` |

These calls construct the list. They are not called again merely because an already-open dialog is drawn. A counter probe installed after the list appears can therefore report zero at all three sites without disproving this path.

For a useful reachability test, install all probes first, close the current menu, and trigger a fresh subtype 5 response. The first two counters should advance once and the row counter should advance once per active slot accepted by the dialog. A row probe temporarily replaces the quantity hook, so it tests reachability only. Restore the quantity hook and reopen the menu to test the label change.

Interpret the counters together:

| Dispatch | Constructor | Row | Meaning |
| --- | --- | --- | --- |
| `0` | `0` | `0` | No fresh subtype 5 construction was observed, or the wrong process or module base was probed. |
| nonzero | `0` | `0` | The subtype handler ran, but it did not construct this dialog. |
| nonzero | nonzero | `0` | The dialog was constructed, but no active inventory row reached the builder. |
| nonzero | nonzero | nonzero | The target is live. If labels remain unchanged after restoring the patch, inspect stub relocation, feature configuration, and the live inventory-pane lookup. |

## Label bounds

The replacement label is at most 255 bytes plus its terminating zero. The quantity is formatted as unsigned decimal in ` (quantity)`. Space for the complete suffix is reserved before copying the name.

If the name and suffix fit, the name is preserved. If they do not fit, the patch reserves another three bytes for `...`, copies the bounded prefix, and calls the client's existing `ui_text_truncate_dbcs_safe` helper before adding the ellipsis. This prevents truncation from leaving a Windows DBCS lead byte at the end.

```text
Potion + 5        -> Potion (5)
very long name    -> bounded name... (100)
```

This is a byte-capacity guarantee, not a font-width calculation. The suffix survives the row builder's fixed buffer. A custom skin with a narrower visible row may still clip text according to its normal drawing behavior.

## Injected stub template

Allocate at least 360 executable bytes in the target process. Build this template at `stub_base`. The four zeroed operands are filled using the relocation table below.

```text
000: 55                         | push ebp                          ; standard frame
001: 89 E5                      | mov ebp, esp                      ; access the original row arguments
003: 53                         | push ebx                          ; preserve working registers
004: 56                         | push esi                          ; preserve working registers
005: 57                         | push edi                          ; preserve working registers
006: 81 EC 20 01 00 00          | sub esp, 0x120                   ; local name and suffix buffers
00C: 89 CB                      | mov ebx, ecx                      ; EBX = original row-builder owner
00E: 8B 75 18                   | mov esi, [ebp+0x18]               ; ESI = original label
011: 89 B5 D8 FE FF FF          | mov [ebp-0x128], esi             ; default to the original label
017: 85 F6                      | test esi, esi                     ; label may be null
019: 0F 84 1A 01 00 00          | je build_row                      ; fail open
01F: 0F B6 7D 1C                | movzx edi, byte ptr [ebp+0x1C]   ; one-based inventory slot
023: 83 FF 01                   | cmp edi, 1                        ; reject slot zero
026: 0F 82 0D 01 00 00          | jb build_row                      ; fail open
02C: 83 FF 3C                   | cmp edi, 60                       ; inventory has 60 slots
02F: 0F 87 04 01 00 00          | ja build_row                      ; fail open
035: E8 00 00 00 00             | call ui_get_gui_back_pane         ; rel32, obtain the live UI root
03A: 85 C0                      | test eax, eax                     ; root may be absent
03C: 0F 84 F7 00 00 00          | je build_row                      ; fail open
042: 8B 80 88 4F 00 00          | mov eax, [eax+0x4F88]            ; current inventory pane
048: 85 C0                      | test eax, eax                     ; pane may be absent
04A: 0F 84 E9 00 00 00          | je build_row                      ; fail open
050: 8B 84 B8 9C 01 00 00       | mov eax, [eax+edi*4+0x19C]       ; item pane for the one-based slot
057: 85 C0                      | test eax, eax                     ; slot may be empty
059: 0F 84 DA 00 00 00          | je build_row                      ; fail open
05F: 80 B8 44 02 00 00 00       | cmp byte ptr [eax+0x244], 0      ; can this item stack?
066: 0F 84 CD 00 00 00          | je build_row                      ; keep non-stackable labels unchanged
06C: 8B 88 40 02 00 00          | mov ecx, [eax+0x240]             ; live quantity
072: 85 C9                      | test ecx, ecx                     ; ignore a stale zero quantity
074: 0F 84 BF 00 00 00          | je build_row                      ; fail open
07A: 89 8D D4 FE FF FF          | mov [ebp-0x12C], ecx             ; save quantity for formatting
080: E8 06 00 00 00             | call suffix_data_ready           ; push the inline format-string address
085: 20 28 25 75 29 00          | db " (%u)", 0                    ; quantity suffix format
suffix_data_ready:
08B: 58                         | pop eax                           ; EAX = address of " (%u)"
08C: FF B5 D4 FE FF FF          | push dword ptr [ebp-0x12C]       ; quantity
092: 50                         | push eax                           ; format string
093: 8D 45 E4                   | lea eax, [ebp-0x1C]               ; suffix buffer
096: 50                         | push eax                           ; destination buffer
097: FF 15 00 00 00 00          | call dword ptr [wsprintfA_IAT]    ; abs32, format the suffix
09D: 83 C4 0C                   | add esp, 12                       ; caller removes wsprintfA arguments
0A0: 83 F8 01                   | cmp eax, 1                        ; require a useful suffix
0A3: 0F 8E 90 00 00 00          | jle build_row                     ; fail open on formatting failure
0A9: 83 F8 0F                   | cmp eax, 15                       ; bound suffix length
0AC: 0F 83 87 00 00 00          | jae build_row                     ; fail open if unexpectedly large
0B2: 89 85 E0 FE FF FF          | mov [ebp-0x120], eax             ; save suffix byte length
0B8: 31 C9                      | xor ecx, ecx                     ; name_length = 0
name_length_loop:
0BA: 81 F9 00 01 00 00          | cmp ecx, 256                      ; never read beyond the row-builder limit
0C0: 73 09                      | jae name_length_done              ; cap unterminated input at 256 bytes
0C2: 80 3C 0E 00                | cmp byte ptr [esi+ecx], 0        ; end of the original label?
0C6: 74 03                      | je name_length_done               ; length is complete
0C8: 41                         | inc ecx                           ; count another byte
0C9: EB EF                      | jmp name_length_loop              ; continue bounded scan
name_length_done:
0CB: BA FF 00 00 00             | mov edx, 255                      ; maximum label bytes before null
0D0: 2B 95 E0 FE FF FF          | sub edx, [ebp-0x120]             ; reserve the complete suffix
0D6: 39 D1                      | cmp ecx, edx                     ; does the name fit?
0D8: 76 3D                      | jbe copy_full_name                ; keep the full name when possible
0DA: 83 EA 03                   | sub edx, 3                        ; reserve three bytes for an ellipsis
0DD: 8D BD E4 FE FF FF          | lea edi, [ebp-0x11C]             ; bounded combined-label buffer
0E3: 89 D1                      | mov ecx, edx                     ; bytes to copy before truncation
0E5: FC                         | cld                                ; copy forward
0E6: F3 A4                      | rep movsb                          ; copy the bounded name prefix
0E8: C6 07 00                   | mov byte ptr [edi], 0             ; terminate before DBCS cleanup
0EB: 52                         | push edx                          ; maximum prefix length
0EC: 8D 85 E4 FE FF FF          | lea eax, [ebp-0x11C]             ; combined-label buffer
0F2: 50                         | push eax                          ; text to truncate safely
0F3: E8 00 00 00 00             | call ui_text_truncate_dbcs_safe  ; rel32, avoid a dangling lead byte
0F8: 83 C4 08                   | add esp, 8                       ; caller removes helper arguments
0FB: 8D BD E4 FE FF FF          | lea edi, [ebp-0x11C]             ; find the cleaned string end
ellipsis_end_loop:
101: 80 3F 00                   | cmp byte ptr [edi], 0            ; current terminator?
104: 74 03                      | je append_ellipsis                ; append at the terminator
106: 47                         | inc edi                           ; advance one byte
107: EB F8                      | jmp ellipsis_end_loop             ; continue bounded local scan
append_ellipsis:
109: 66 C7 07 2E 2E             | mov word ptr [edi], 0x2E2E       ; write ".."
10E: C6 47 02 2E                | mov byte ptr [edi+2], 0x2E       ; write the third dot
112: 83 C7 03                   | add edi, 3                        ; destination now follows the ellipsis
115: EB 09                      | jmp append_suffix                  ; name portion is complete
copy_full_name:
117: 8D BD E4 FE FF FF          | lea edi, [ebp-0x11C]             ; combined-label buffer
11D: FC                         | cld                                ; copy forward
11E: F3 A4                      | rep movsb                          ; copy the complete original name
append_suffix:
120: 8D 75 E4                   | lea esi, [ebp-0x1C]              ; formatted suffix buffer
123: 8B 8D E0 FE FF FF          | mov ecx, [ebp-0x120]             ; suffix byte length
129: 41                         | inc ecx                           ; include the null terminator
12A: FC                         | cld                                ; copy forward
12B: F3 A4                      | rep movsb                          ; append suffix and terminator
12D: 8D 85 E4 FE FF FF          | lea eax, [ebp-0x11C]             ; completed temporary label
133: 89 85 D8 FE FF FF          | mov [ebp-0x128], eax             ; replace only the label argument
build_row:
139: FF 75 28                   | push dword ptr [ebp+0x28]         ; replay original argument 9
13C: FF 75 24                   | push dword ptr [ebp+0x24]         ; replay original argument 8
13F: FF 75 20                   | push dword ptr [ebp+0x20]         ; replay original argument 7
142: FF 75 1C                   | push dword ptr [ebp+0x1C]         ; replay inventory slot
145: FF B5 D8 FE FF FF          | push dword ptr [ebp-0x128]       ; original or rewritten label
14B: FF 75 14                   | push dword ptr [ebp+0x14]         ; replay original argument 4
14E: FF 75 10                   | push dword ptr [ebp+0x10]         ; replay original argument 3
151: FF 75 0C                   | push dword ptr [ebp+0x0C]         ; replay original argument 2
154: FF 75 08                   | push dword ptr [ebp+0x08]         ; replay original argument 1
157: 89 D9                      | mov ecx, ebx                     ; restore original this pointer
159: E8 00 00 00 00             | call item_list_row_builder       ; rel32, perform normal row construction
15E: 8D 65 F4                   | lea esp, [ebp-0x0C]              ; release locals
161: 5F                         | pop edi                           ; restore registers
162: 5E                         | pop esi                           ; restore registers
163: 5B                         | pop ebx                           ; restore registers
164: 5D                         | pop ebp                           ; restore caller frame
165: C2 24 00                   | ret 0x24                          ; remove nine row arguments
```

Write `rel32` displacements as signed little-endian 32-bit integers. Write `abs32` values as unsigned little-endian 32-bit addresses.

| Stub operand offset | Kind | Instruction | Value |
| --- | --- | --- | --- |
| `0x36` | `rel32` | `CALL ui_get_gui_back_pane` | `(module_base + 0x001A9C40) - (stub_base + 0x3A)` |
| `0x99` | `abs32` | `CALL [wsprintfA IAT]` | `module_base + 0x00269380` |
| `0xF4` | `rel32` | `CALL ui_text_truncate_dbcs_safe` | `(module_base + 0x0007D670) - (stub_base + 0xF8)` |
| `0x15A` | `rel32` | `CALL ItemListPane row builder` | `(module_base + 0x000D3700) - (stub_base + 0x15E)` |

Reject the installation if either `rel32` displacement does not fit a signed 32-bit integer.

## Hook relocation

After the relocated stub is written, calculate the hook operand at `module_base + 0x000D4F83` as:

```text
signed-rel32 = stub_base - (module_base + 0x000D4F87)
```

As a relocation test vector only, using preferred `module_base = 0x00400000` and `stub_base = 0x10000000` produces:

```text
036: 06 9C 5A F0 | call ui_get_gui_back_pane       ; example stub rel32 operand
099: 80 93 66 00 | call [wsprintfA IAT]            ; example stub abs32 operand
0F4: 78 D5 47 F0 | call ui_text_truncate_dbcs_safe ; example stub rel32 operand
15A: A2 35 4D F0 | call item_list_row_builder      ; example stub rel32 operand
hook bytes: E8 79 B0 B2 0F | call menu_item_quantity_stub  ; example installed hook
```

Do not use those test-vector values when ASLR or a different allocation address changes either base.

## Installation and removal

Install while the process is suspended:

1. Verify the executable fingerprint and the five original hook bytes.
2. Allocate the stub, fill all four relocations, and write all 360 bytes.
3. Change the stub to executable protection if it was allocated writable-only.
4. Flush the instruction cache for the stub.
5. Make the hook page writable, write the complete five-byte call, flush the instruction cache, and restore the old page protection.
6. Resume only after every check and write succeeds.

To remove the patch, suspend execution, restore the five original hook bytes first, flush the instruction cache, and only then release the stub allocation. If installation fails before the hook is written, release the unused stub and leave the hook untouched.

The general checks in the [safe launcher workflow](safe-launcher.md) also apply. The related packet path is described on [Screen Menu (`SScreenMenu`)](../../network/server/047-0x2f-screen-menu.md).
