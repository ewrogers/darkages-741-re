# Clear stuck modifier keys on focus loss

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
E8 CA 2B 00 00
```

This is the original `CALL` to the activation-state function. Replace it with:

```text
E8 <stub rel32>
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
00: 9C 60 E8 00 00 00 00 85 C0 74 32 89 C3 E8 00 00
10: 00 00 89 C7 31 F6 F6 84 33 34 03 00 00 80 74 0D
20: 6A 00 57 6A 00 56 89 D9 E8 00 00 00 00 46 81 FE
30: 00 01 00 00 7C E0 C6 83 34 04 00 00 00 61 9D E9
40: 00 00 00 00
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
FF 25 64 93 66 00
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
