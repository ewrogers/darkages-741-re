# Stuck modifiers

This patch releases the client's held keys when the game loses focus. It prevents Alt, Ctrl, Shift, and other keys from remaining logically pressed when their physical key-up messages go to another window.

## Hook and dependencies

| Role | Static address | RVA |
| --- | --- | --- |
| Inactive `WM_ACTIVATE` call | `0x004A9D81` | `0x000A9D81` |
| Original activation-state function | `0x004AC950` | `0x000AC950` |
| `input_get_event_manager` | `0x00427380` | `0x00027380` |
| `input_post_key_up` | `0x00466E60` | `0x00066E60` |
| `GetMessageTime` import thunk | `0x0062006E` | `0x0022006E` |

The hook site must contain exactly:

```text
000: E8 CA 2B 00 00 | call original_activation_state ; original inactive-focus behavior
```

This is the original `CALL` to the activation-state function. Replace it with:

```text
000: E8 <stub rel32> | call modifier_cleanup_stub ; release keys before original behavior
```

where:

```text
signed-rel32 = stub_base - (module_base + 0x000A9D86)
```

The nearby active and click-active branch uses a different call site and remains unchanged. The cleanup therefore runs only when the low word of `WM_ACTIVATE.wParam` is `WA_INACTIVE`.

## Cleanup flow

The client stores pressed-key state in a 256-byte array at `EventMan + 0x334`. The high bit marks a pressed scan code. Its current modifier mask is at `EventMan + 0x434`.

The injected stub follows the client's normal input path:

```c
event_man = input_get_event_manager();
if (event_man != NULL) {
    message_time = GetMessageTime();

    for (scan_code = 0; scan_code < 256; scan_code++) {
        if (event_man->pressed_keys[scan_code] & 0x80) {
            input_post_key_up(event_man, scan_code, 0, message_time, 0);
        }
    }

    event_man->modifier_mask = 0;
}

original_activation_state(false);
```

Calling `input_post_key_up` clears the native pressed-key entry and emits the normal internal key-up event. The final modifier write is an explicit safety cleanup after the scan.

The stub preserves the caller's flags and general-purpose registers. Its final `JMP` enters the original activation-state function, which returns through the return address created by the replacement `CALL`.

## Injected stub template

Allocate at least 68 executable bytes in the target process. Build this template at `stub_base`. The four zeroed `rel32` operands are filled from the relocation table below.

```text
000: 9C                         | pushfd                              ; preserve caller flags
001: 60                         | pushad                              ; preserve general-purpose registers
002: E8 00 00 00 00             | call input_get_event_manager        ; rel32, obtain EventMan
007: 85 C0                      | test eax, eax                       ; a missing manager is safe
009: 74 32                      | je cleanup_done                     ; skip the scan when EventMan is null
00B: 89 C3                      | mov ebx, eax                        ; EBX = EventMan
00D: E8 00 00 00 00             | call GetMessageTime                ; rel32 through the import thunk
012: 89 C7                      | mov edi, eax                        ; timestamp for synthetic key-up events
014: 31 F6                      | xor esi, esi                        ; scan_code = 0
scan_loop:
016: F6 84 33 34 03 00 00 80    | test byte ptr [ebx+esi+0x334],0x80 ; is this scan code pressed?
01E: 74 0D                      | je next_scan                       ; no event is needed when clear
020: 6A 00                      | push 0                              ; final key-up argument
022: 57                         | push edi                            ; message timestamp
023: 6A 00                      | push 0                              ; repeat state
025: 56                         | push esi                            ; scan code
026: 89 D9                      | mov ecx, ebx                        ; this = EventMan
028: E8 00 00 00 00             | call input_post_key_up              ; rel32, use the native event path
next_scan:
02D: 46                         | inc esi                             ; advance to the next scan code
02E: 81 FE 00 01 00 00          | cmp esi, 256                        ; cover the complete key-state array
034: 7C E0                      | jl scan_loop                        ; continue until all 256 entries were checked
036: C6 83 34 04 00 00 00       | mov byte ptr [ebx+0x434],0         ; clear the cached modifier mask
cleanup_done:
03D: 61                         | popad                               ; restore registers
03E: 9D                         | popfd                               ; restore flags
03F: E9 00 00 00 00             | jmp original_activation_state      ; rel32, resume the displaced call target
```

Write each displacement as a signed little-endian 32-bit integer:

| Stub operand offset | Instruction | Value |
| --- | --- | --- |
| `0x03` | `CALL input_get_event_manager` | `(module_base + 0x00027380) - (stub_base + 0x07)` |
| `0x0E` | `CALL GetMessageTime` thunk | `(module_base + 0x0022006E) - (stub_base + 0x12)` |
| `0x29` | `CALL input_post_key_up` | `(module_base + 0x00066E60) - (stub_base + 0x2D)` |
| `0x40` | `JMP` original activation-state function | `(module_base + 0x000AC950) - (stub_base + 0x44)` |

Reject the installation if any displacement does not fit a signed 32-bit integer.

The target at RVA `0x0022006E` is executable import-thunk code:

```text
000: FF 25 64 93 66 00 | jmp dword ptr [GetMessageTime_IAT] ; executable import thunk
```

Use a direct relative `CALL` to that thunk. Do not interpret the thunk bytes as an indirect function pointer.

## Installation and removal

Install while the process is suspended:

1. Verify the executable fingerprint and the five original call bytes.
2. Allocate the stub, fill all four relocations, and write all 68 bytes.
3. Change the stub to executable protection and verify its complete contents.
4. Make the call-site page writable and write the complete five-byte replacement call.
5. Verify the call and its surrounding bytes, then restore the old page protection.
6. Flush the instruction cache for both the stub and the call site.
7. Resume only after every check succeeds.

To remove the patch, suspend execution, restore the original five-byte call first, flush the instruction cache, and only then release the stub allocation.

The hook site, original bytes, helper targets, object fields, and import thunk above were rechecked against the local version-741 executable.

The general checks in the [safe launcher workflow](safe-launcher-workflow.md) also apply.
