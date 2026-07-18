# Skip the exchange count prompt for a one-item stack

This patch sends a count of one for a one-item stack while preserving the normal prompt for every other case.

## Target and dependencies

| Role | Static address | RVA |
| --- | --- | --- |
| `ui_exchange_handle_count_request` hook | `0x0046A690` | `0x0006A690` |
| Original continuation after the replaced prologue | `0x0046A695` | `0x0006A695` |
| `ui_get_gui_back_pane` | `0x005A9C40` | `0x001A9C40` |
| Existing `CExchange` subtype 2 count builder | `0x0046C2A0` | `0x0006C2A0` |

The hook site must contain exactly:

```text
55 8B EC 6A FF
```

Its replacement is:

```text
E9 <stub rel32>
```

Adding an item to a player exchange is a server-mediated two-step operation. The client first sends `CExchange` subtype 1 with the exchange ID and source inventory slot. When the server replies with `SExchange` subtype 1, `ui_exchange_handle_count_request` opens `AddItemWithCountDialog` without checking the live inventory quantity.

This runtime patch intercepts that server reply. A stackable item whose stored quantity is exactly one sends the client's existing `CExchange` subtype 2 count response with `count = 1`. Every other case resumes the original handler and opens the normal count dialog.

The detour is fail-open. An invalid slot, missing root pane, missing inventory pane, missing item pane, non-stackable item, or quantity other than one all use the original prompt path. The initial subtype 1 request and the server's decision to ask for a count remain unchanged.

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

struct ExchangeDialogFields {
    u8 unrelated_0000[0x630];
    u32 exchange_id;                       // +0x630
    u8 local_ack_state;                    // +0x634
};
```

At the hook entry, `ECX` is the `ExchangeDialog *` and `[ESP + 4]` points to the decoded `SExchange` body. The one-based inventory slot is body byte 2. The count builder uses the same `exchange_id` offset as `ExchangeDialog`, but expects the slot at `this + 0x634`. The stub therefore saves that byte, temporarily writes the slot, calls the existing builder with count one, and restores the byte.

## Injected stub template

Allocate at least 125 executable bytes in the target process. Build this template at the allocated `stub_base`. The three zeroed `rel32` operands are filled using the relocation table below.

```text
00: 53 56 57 89 CE 8B 7C 24 10 0F B6 5F 02 84 DB 74
10: 5F 80 FB 3C 77 5A E8 00 00 00 00 85 C0 74 51 8B
20: 80 88 4F 00 00 85 C0 74 47 0F B6 CB 49 8B 84 88
30: A0 01 00 00 85 C0 74 38 80 B8 44 02 00 00 00 74
40: 2F 83 B8 40 02 00 00 01 75 26 0F B6 86 34 06 00
50: 00 50 88 9E 34 06 00 00 6A 01 89 F1 E8 00 00 00
60: 00 5A 88 96 34 06 00 00 5F 5E 5B 31 C0 C2 04 00
70: 5F 5E 5B 55 89 E5 6A FF E9 00 00 00 00
```

Write each displacement as a signed little-endian 32-bit integer:

| Stub operand offset | Instruction | Value |
| --- | --- | --- |
| `0x17` | `CALL ui_get_gui_back_pane` | `(module_base + 0x001A9C40) - (stub_base + 0x1B)` |
| `0x5D` | `CALL CExchange subtype 2 builder` | `(module_base + 0x0006C2A0) - (stub_base + 0x61)` |
| `0x79` | `JMP original continuation` | `(module_base + 0x0006A695) - (stub_base + 0x7D)` |

Reject the installation if any displacement does not fit a signed 32-bit integer.

## Hook bytes

After the relocated stub is written, replace the verified five hook bytes at `module_base + 0x0006A690` with:

```text
E9 <signed-rel32>
```

where:

```text
signed-rel32 = stub_base - (module_base + 0x0006A695)
```

The complete rollback bytes are:

```text
55 8B EC 6A FF
```

As a relocation test vector only, placing the stub at preferred address `0x0066867A` produces:

```text
stub +0x17: AB 15 F4 FF
stub +0x5D: C5 3B E0 FF
stub +0x79: 9E 1F E0 FF
hook bytes: E9 E5 DF 1F 00
```

Do not use those test-vector displacements when ASLR or a different allocation address changes either base.

## Installation and removal

Install while the process is suspended:

1. Verify the executable fingerprint and the five original hook bytes.
2. Allocate the stub, fill all three relocations, and write all 125 bytes.
3. Change the stub to executable protection if it was allocated writable-only.
4. Flush the instruction cache for the stub.
5. Make the hook page writable, write the complete five-byte jump, flush the instruction cache, and restore the old page protection.
6. Resume only after every check and write succeeds.

To remove the patch, suspend execution, restore the five original hook bytes first, flush the instruction cache, and only then release the stub allocation. If installation fails before the hook is written, release the unused stub and leave the hook untouched.

The general checks in the [safe launcher workflow](safe-launcher-workflow.md) also apply.
