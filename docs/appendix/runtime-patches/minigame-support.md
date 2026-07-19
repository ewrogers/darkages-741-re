# Minigame assets

This patch makes the installed `cious.dat` mini-game assets available to the version 741 client. It keeps every original DAT unchanged, preserves the existing `misc.dat` overlay, and does not require a DLL.

The launcher opens `cious.dat` in a dormant archive object during startup. Archive lookup then follows this order:

```text
misc.dat -> cious.dat -> archive requested by the caller
```

The local `cious.dat` has 167 real entries. None of their case-insensitive names collide with entries in any of the other 20 legacy DAT archives in the installation.

This specification applies only to the 3,112,960-byte executable with SHA-256 `054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6`. Its preferred image base is `0x00400000`. Resolve every runtime address as the loaded module base plus the RVA; do not assume the preferred base after launch.

## Hooks and dependencies

| Role | Static address | RVA | File offset, reference only |
| --- | --- | --- | --- |
| `setoa.dat` `file_archive_open` call | `0x004AABEF` | `0x000AABEF` | `0x000A9FEF` |
| `file_archive_open` | `0x00471E00` | `0x00071E00` | `0x00071200` |
| Dormant archive accessor | `0x00473450` | `0x00073450` | `0x00072850` |
| `file_archive_find_entry` entry | `0x00472470` | `0x00072470` | `0x00071870` |
| `file_archive_find_entry` continuation | `0x00472476` | `0x00072476` | `0x00071876` |
| Dormant archive pointer global | `0x006FD084` | `0x002FD084` | Not file-backed |
| `misc.dat` archive pointer global | `0x006FD088` | `0x002FD088` | Not file-backed |

The startup call site must contain exactly:

```text
000: E8 0C 72 FC FF | call file_archive_open ; original setoa.dat open
```

Replace it with:

```text
000: E8 <open wrapper rel32> | call open_wrapper ; open setoa.dat, then cious.dat
```

where:

```text
signed-rel32 = stub_base - (module_base + 0x000AABF4)
```

The `file_archive_find_entry` entry must contain exactly:

```text
000: 55          | push ebp      ; displaced function prologue
001: 8B EC       | mov ebp, esp  ; establish the original frame
003: 83 EC 34    | sub esp, 0x34 ; reserve the original locals
```

Replace it with:

```text
000: E9 <lookup wrapper rel32> | jmp lookup_wrapper ; apply the cious.dat overlay
005: 90                         | nop                ; cover the sixth displaced byte
```

where:

```text
signed-rel32 = (stub_base + 0x40) - (module_base + 0x00072475)
```

The trailing `NOP` covers the sixth displaced prologue byte. The gateway in the stub reproduces all six bytes before continuing at RVA `0x00072476`.

## Behavior

The open wrapper first performs the original `setoa.dat` open. If that succeeds, it obtains the dormant archive object and opens `cious.dat` with the same 20-handle capacity used by the normal startup archives. Its return value replaces the original call's result, so a missing or invalid `cious.dat` follows the caller's existing startup-failure path.

The lookup wrapper behaves like this:

```c
if (archive == cious_archive || archive == misc_archive) {
    return original_find_entry(archive, name);
}

entry = original_find_entry(cious_archive, name);
if (entry != NULL) {
    return entry;
}

return original_find_entry(archive, name);
```

The original lookup checks `misc.dat` before its argument, so the effective precedence remains `misc.dat`, then `cious.dat`, then the requested archive. The two direct-archive checks prevent recursive overlay lookup. On a complete miss, `misc.dat` is checked twice; this adds only two small index searches and does not borrow an entry handle.

The dormant singleton is already closed and destroyed by the client's normal shutdown and startup-failure cleanup paths. The patch therefore adds no separate lifetime hook.

## Injected stub template

Allocate at least 160 bytes in the target process. Build this template at `stub_base`. Offsets `0x00`, `0x40`, `0x80`, and `0x90` contain the open wrapper, lookup wrapper, original-function gateway, and `cious.dat` filename.

```text
open_wrapper:
000: 55                         | push ebp                       ; standard frame
001: 8B EC                      | mov ebp, esp                   ; preserve caller arguments
003: FF 75 10                   | push dword ptr [ebp+0x10]      ; original third argument
006: FF 75 0C                   | push dword ptr [ebp+0x0C]      ; original second argument
009: FF 75 08                   | push dword ptr [ebp+0x08]      ; original archive filename
00C: E8 00 00 00 00             | call file_archive_open         ; rel32, keep the setoa.dat open
011: 85 C0                      | test eax, eax                  ; did the original open succeed?
013: 74 19                      | je open_done                   ; preserve its failure result
015: E8 00 00 00 00             | call dormant_archive_accessor  ; rel32, obtain spare archive object
01A: 85 C0                      | test eax, eax                  ; accessor may fail
01C: 74 10                      | je open_done                   ; preserve original result if unavailable
01E: 6A 00                      | push 0                         ; normal open flags
020: 6A 14                      | push 20                        ; match the normal handle capacity
022: 68 00 00 00 00             | push cious_filename            ; abs32 at stub_base+0x90
027: 8B C8                      | mov ecx, eax                   ; this = dormant archive object
029: E8 00 00 00 00             | call file_archive_open         ; rel32, return cious.dat open result
open_done:
02E: 8B E5                      | mov esp, ebp                   ; release wrapper frame
030: 5D                         | pop ebp                        ; restore caller frame
031: C2 0C 00                   | ret 0x0C                       ; callee removes three arguments
034: CC CC CC CC CC CC CC CC CC CC CC CC | int3 padding ; trap accidental execution

lookup_wrapper:
040: 55                         | push ebp                       ; standard frame
041: 8B EC                      | mov ebp, esp                   ; expose the name argument
043: 56                         | push esi                       ; preserve ESI
044: 8B F1                      | mov esi, ecx                   ; ESI = requested archive
046: 3B 35 00 00 00 00          | cmp esi, [cious_archive_ptr]   ; abs32, avoid recursive overlay lookup
04C: 74 1E                      | je requested_lookup           ; search cious.dat directly
04E: 3B 35 00 00 00 00          | cmp esi, [misc_archive_ptr]    ; abs32, preserve misc.dat behavior
054: 74 16                      | je requested_lookup           ; search misc.dat directly
056: 8B 0D 00 00 00 00          | mov ecx, [cious_archive_ptr]   ; abs32, use cious.dat as the overlay
05C: 85 C9                      | test ecx, ecx                  ; archive may not have opened
05E: 74 0C                      | je requested_lookup           ; fail open to the requested archive
060: FF 75 08                   | push dword ptr [ebp+0x08]      ; requested entry name
063: E8 18 00 00 00             | call original_lookup_gateway   ; fixed local call into the gateway
068: 85 C0                      | test eax, eax                  ; was the entry found in cious.dat?
06A: 75 0A                      | jne lookup_done               ; return the overlay entry
requested_lookup:
06C: 8B CE                      | mov ecx, esi                   ; restore the requested archive
06E: FF 75 08                   | push dword ptr [ebp+0x08]      ; same entry name
071: E8 0A 00 00 00             | call original_lookup_gateway   ; run the normal archive lookup
lookup_done:
076: 5E                         | pop esi                        ; restore ESI
077: 5D                         | pop ebp                        ; restore caller frame
078: C2 04 00                   | ret 4                          ; callee removes the name argument
07B: CC CC CC CC CC          | int3 padding                   ; trap accidental execution

original_lookup_gateway:
080: 55                         | push ebp                       ; reproduce displaced prologue
081: 8B EC                      | mov ebp, esp                   ; reproduce displaced prologue
083: 83 EC 34                   | sub esp, 0x34                  ; reproduce displaced local allocation
086: E9 00 00 00 00             | jmp original_lookup_continue   ; rel32 to RVA 0x00072476
08B: CC CC CC CC CC          | int3 padding                   ; separate code from filename data

cious_filename:
090: 63 69 6F 75 73 2E 64 61 74 00 | db "cious.dat", 0 ; archive filename
09A: CC CC CC CC CC CC       | int3 padding                   ; fill the 160-byte allocation
```

Fill each zeroed operand before writing the stub:

| Stub operand offset | Instruction | Value |
| --- | --- | --- |
| `0x0D` | `CALL file_archive_open` | `(module_base + 0x00071E00) - (stub_base + 0x11)` |
| `0x16` | `CALL` dormant archive accessor | `(module_base + 0x00073450) - (stub_base + 0x1A)` |
| `0x23` | `PUSH cious.dat` | `stub_base + 0x90` as an unsigned little-endian address |
| `0x2A` | `CALL file_archive_open` | `(module_base + 0x00071E00) - (stub_base + 0x2E)` |
| `0x48` | `CMP` dormant archive pointer | `module_base + 0x002FD084` as an unsigned little-endian address |
| `0x50` | `CMP misc.dat` archive pointer | `module_base + 0x002FD088` as an unsigned little-endian address |
| `0x58` | `MOV` dormant archive pointer | `module_base + 0x002FD084` as an unsigned little-endian address |
| `0x87` | `JMP` original lookup continuation | `(module_base + 0x00072476) - (stub_base + 0x8B)` |

The calls at offsets `0x63` and `0x71` already target the gateway at `stub_base + 0x80` and need no relocation. Reject the installation if any relative displacement does not fit a signed 32-bit integer.

## Installation and removal

Install while the process is suspended:

1. Verify the executable fingerprint, both hook sites, and the presence of `cious.dat` beside the executable.
2. Allocate 160 writable bytes, fill every relocation, write the complete stub, and verify it.
3. Change the stub to executable, non-writable protection.
4. Make both hook pages writable and write the complete replacements.
5. Verify the hooks and their surrounding bytes, then restore the old page protections.
6. Flush the instruction cache for the stub and both hook sites.
7. Resume only after every check succeeds.

To remove the patch, suspend execution, restore both original hook sequences, flush the instruction cache, and only then release the stub allocation. Do not remove it from a process that has already opened `cious.dat`; use it as a launch-time patch for the complete process lifetime.

The general checks in the [safe launcher workflow](safe-launcher-workflow.md) also apply.
