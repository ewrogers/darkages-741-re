# Show inventory quantities in screen menus

This patch changes stackable item labels in `ClientItemMenuDialog` from `Potion` to `Potion (5)`. It covers the own-inventory lists used by `SScreenMenu` subtypes 5 and 11, including merchant and storage flows that use this dialog class.

## Target and dependencies

| Role | Static address | RVA |
| --- | --- | --- |
| `ClientItemMenuDialog` row-builder call | `0x004D4F82` | `0x000D4F82` |
| Existing `ItemListPane` row builder | `0x004D3700` | `0x000D3700` |
| `ui_get_gui_back_pane` | `0x005A9C40` | `0x001A9C40` |
| `ui_text_truncate_dbcs_safe` | `0x0047D670` | `0x0007D670` |
| `wsprintfA` import address-table entry | `0x00669380` | `0x00269380` |

The hook site must contain exactly:

```text
E8 79 E7 FF FF
```

Its replacement is:

```text
E8 <stub rel32>
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
000: 55 89 E5 53 56 57 81 EC 20 01 00 00 89 CB 8B 75
010: 18 89 B5 D8 FE FF FF 85 F6 0F 84 1A 01 00 00 0F
020: B6 7D 1C 83 FF 01 0F 82 0D 01 00 00 83 FF 3C 0F
030: 87 04 01 00 00 E8 00 00 00 00 85 C0 0F 84 F7 00
040: 00 00 8B 80 88 4F 00 00 85 C0 0F 84 E9 00 00 00
050: 8B 84 B8 9C 01 00 00 85 C0 0F 84 DA 00 00 00 80
060: B8 44 02 00 00 00 0F 84 CD 00 00 00 8B 88 40 02
070: 00 00 85 C9 0F 84 BF 00 00 00 89 8D D4 FE FF FF
080: E8 06 00 00 00 20 28 25 75 29 00 58 FF B5 D4 FE
090: FF FF 50 8D 45 E4 50 FF 15 00 00 00 00 83 C4 0C
0A0: 83 F8 01 0F 8E 90 00 00 00 83 F8 0F 0F 83 87 00
0B0: 00 00 89 85 E0 FE FF FF 31 C9 81 F9 00 01 00 00
0C0: 73 09 80 3C 0E 00 74 03 41 EB EF BA FF 00 00 00
0D0: 2B 95 E0 FE FF FF 39 D1 76 3D 83 EA 03 8D BD E4
0E0: FE FF FF 89 D1 FC F3 A4 C6 07 00 52 8D 85 E4 FE
0F0: FF FF 50 E8 00 00 00 00 83 C4 08 8D BD E4 FE FF
100: FF 80 3F 00 74 03 47 EB F8 66 C7 07 2E 2E C6 47
110: 02 2E 83 C7 03 EB 09 8D BD E4 FE FF FF FC F3 A4
120: 8D 75 E4 8B 8D E0 FE FF FF 41 FC F3 A4 8D 85 E4
130: FE FF FF 89 85 D8 FE FF FF FF 75 28 FF 75 24 FF
140: 75 20 FF 75 1C FF B5 D8 FE FF FF FF 75 14 FF 75
150: 10 FF 75 0C FF 75 08 89 D9 E8 00 00 00 00 8D 65
160: F4 5F 5E 5B 5D C2 24 00
```

Write `rel32` displacements as signed little-endian 32-bit integers. Write `abs32` values as unsigned little-endian 32-bit addresses.

| Stub operand offset | Kind | Instruction | Value |
| --- | --- | --- | --- |
| `0x36` | `rel32` | `CALL ui_get_gui_back_pane` | `(module_base + 0x001A9C40) - (stub_base + 0x3A)` |
| `0x99` | `abs32` | `CALL [wsprintfA IAT]` | `module_base + 0x00269380` |
| `0xF4` | `rel32` | `CALL ui_text_truncate_dbcs_safe` | `(module_base + 0x0007D670) - (stub_base + 0xF8)` |
| `0x15A` | `rel32` | `CALL ItemListPane row builder` | `(module_base + 0x000D3700) - (stub_base + 0x15E)` |

Reject the installation if either `rel32` displacement does not fit a signed 32-bit integer.

## Hook bytes

After the relocated stub is written, replace the verified five hook bytes at `module_base + 0x000D4F82` with:

```text
E8 <signed-rel32>
```

where:

```text
signed-rel32 = stub_base - (module_base + 0x000D4F87)
```

The complete rollback bytes are:

```text
E8 79 E7 FF FF
```

As a relocation test vector only, using preferred `module_base = 0x00400000` and `stub_base = 0x10000000` produces:

```text
stub +0x036: 06 9C 5A F0
stub +0x099: 80 93 66 00
stub +0x0F4: 78 D5 47 F0
stub +0x15A: A2 35 4D F0
hook bytes: E8 79 B0 B2 0F
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

The general checks in the [safe launcher workflow](safe-launcher-workflow.md) also apply. The related packet path is described on [Screen Menu (`SScreenMenu`)](../../network/server/047-0x2f-screen-menu.md).
