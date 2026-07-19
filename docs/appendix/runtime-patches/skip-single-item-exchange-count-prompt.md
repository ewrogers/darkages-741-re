# One-item exchange

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
000: 55       | push ebp     ; displaced prologue
001: 8B EC    | mov ebp, esp ; establish the original frame
003: 6A FF    | push -1      ; displaced exception-state value
```

Its replacement is:

```text
000: E9 <stub rel32> | jmp one_item_exchange_stub ; inspect the live stack before opening a prompt
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
000: 53                         | push ebx                         ; preserve working registers
001: 56                         | push esi                         ; preserve working registers
002: 57                         | push edi                         ; preserve working registers
003: 89 CE                      | mov esi, ecx                     ; ESI = ExchangeDialog
005: 8B 7C 24 10                | mov edi, [esp+0x10]              ; EDI = decoded SExchange body
009: 0F B6 5F 02                | movzx ebx, byte ptr [edi+2]      ; BL = one-based inventory slot
00D: 84 DB                      | test bl, bl                      ; slot zero is invalid
00F: 74 5F                      | je original_prompt               ; fail open
011: 80 FB 3C                   | cmp bl, 60                       ; inventory has 60 slots
014: 77 5A                      | ja original_prompt               ; fail open when out of range
016: E8 00 00 00 00             | call ui_get_gui_back_pane        ; rel32, obtain the live UI root
01B: 85 C0                      | test eax, eax                    ; root may be absent
01D: 74 51                      | je original_prompt               ; fail open
01F: 8B 80 88 4F 00 00          | mov eax, [eax+0x4F88]           ; current inventory pane
025: 85 C0                      | test eax, eax                    ; pane may be absent
027: 74 47                      | je original_prompt               ; fail open
029: 0F B6 CB                   | movzx ecx, bl                    ; convert slot to an index
02C: 49                         | dec ecx                           ; one-based to zero-based
02D: 8B 84 88 A0 01 00 00       | mov eax, [eax+ecx*4+0x1A0]      ; inventory item pane
034: 85 C0                      | test eax, eax                    ; slot may be empty
036: 74 38                      | je original_prompt               ; fail open
038: 80 B8 44 02 00 00 00       | cmp byte ptr [eax+0x244], 0     ; can this item stack?
03F: 74 2F                      | je original_prompt               ; non-stackable items keep the prompt
041: 83 B8 40 02 00 00 01       | cmp dword ptr [eax+0x240], 1    ; is the live quantity exactly one?
048: 75 26                      | jne original_prompt              ; other quantities keep the prompt
04A: 0F B6 86 34 06 00 00       | movzx eax, byte ptr [esi+0x634] ; save the dialog's local state byte
051: 50                         | push eax                          ; preserve it across the builder call
052: 88 9E 34 06 00 00          | mov byte ptr [esi+0x634], bl    ; temporarily supply the inventory slot
058: 6A 01                      | push 1                            ; count = 1
05A: 89 F1                      | mov ecx, esi                     ; this = ExchangeDialog
05C: E8 00 00 00 00             | call exchange_count_builder     ; rel32, send the native subtype 2 response
061: 5A                         | pop edx                           ; recover the saved state byte
062: 88 96 34 06 00 00          | mov byte ptr [esi+0x634], dl    ; restore dialog state
068: 5F                         | pop edi                           ; restore registers
069: 5E                         | pop esi                           ; restore registers
06A: 5B                         | pop ebx                           ; restore registers
06B: 31 C0                      | xor eax, eax                     ; handled, no prompt
06D: C2 04 00                   | ret 4                            ; consume the packet-body argument
original_prompt:
070: 5F                         | pop edi                           ; restore registers
071: 5E                         | pop esi                           ; restore registers
072: 5B                         | pop ebx                           ; restore registers
073: 55                         | push ebp                          ; replay displaced prologue
074: 89 E5                      | mov ebp, esp                     ; replay displaced prologue
076: 6A FF                      | push -1                           ; replay displaced exception-state value
078: E9 00 00 00 00             | jmp original_continuation        ; rel32 to RVA 0x0006A695
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
000: E9 <signed-rel32> | jmp one_item_exchange_stub ; replace the five-byte prologue
```

where:

```text
signed-rel32 = stub_base - (module_base + 0x0006A695)
```

The complete rollback bytes are:

```text
000: 55       | push ebp     ; restore original prologue
001: 8B EC    | mov ebp, esp ; restore original frame setup
003: 6A FF    | push -1      ; restore original exception-state value
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
