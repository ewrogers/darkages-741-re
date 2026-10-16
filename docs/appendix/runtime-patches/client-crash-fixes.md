# Client crash fixes

These six repairs address the verified client faults in [Client crash faults](../client-crash-faults.md): a field-map handle leak, a rejected-item null dereference, invalid status-element lookups, a balloon palette leak, a gradient tail over-read, and division by an empty pixmap. Seven hook sites implement them because attack and defense elements have separate lookups.

The original bytes were checked against the matching 7.41 executable and Binary Ninja disassembly. The replacement machine code has passed isolated x86 emulation, including original-failure controls. The [Windows launcher](../../../tools/crash-launcher/README.md) installed and read back all seven hooks, passed failure-cleanup tests, and resumed a client in a Windows 11 Parallels VM. That client logged in through Arbiter and passed five status-element and ten ground-item packet cases, with native state checked after dispatch. The other four repairs still need their live Windows checks; the [VM results and procedure](client-crash-tests.md) distinguish completed observations from remaining tests. No executable file was modified.

## Hook sites

Require the [exact target fingerprint](../../../contributing/research-policy.md#project-goal). The preferred image base is `0x00400000`. Let `B` be the actual loaded main-module base and `S` the address of a new `0x184`-byte shared executable-code allocation. Runtime addresses are `B + RVA`; file offsets below are reference information only. The allocation contains code and NOP alignment padding, with no mutable state.

| Patch | Static VA | RVA | File offset | Original bytes | Replacement bytes/template | Stub entry |
| --- | ---: | ---: | ---: | --- | --- | ---: |
| `field-map-palette` | `0x00476FCF` | `0x00076FCF` | `0x000763CF` | `E8 9C B4 FF FF` | `E8 4C B7 FF FF` | none |
| `ground-item-null` | `0x005F32EB` | `0x001F32EB` | `0x001F26EB` | `8B 85 BC FE FF FF` | `E9 <rel32> 90` | `S + 0x000` |
| `status-attack` | `0x00575AF2` | `0x00175AF2` | `0x00174EF2` | `0F BF 88 FC 04 00 00` | `E9 <rel32> 90 90` | `S + 0x020` |
| `status-defense` | `0x00575B1C` | `0x00175B1C` | `0x00174F1C` | `0F BF 91 FE 04 00 00` | `E9 <rel32> 90 90` | `S + 0x040` |
| `balloon-palette` | `0x00474434` | `0x00074434` | `0x00073834` | `E8 17 42 0D 00` | `E9 <rel32>` | `S + 0x060` |
| `empty-pixmap` | `0x004538AD` | `0x000538AD` | `0x00052CAD` | `8D 4D 84 E8 0B D4 02 00` | `E9 <rel32> 90 90 90` | `S + 0x080` |
| `alpha-tail` | `0x00411C67` | `0x00011C67` | `0x00011067` | `F6 C6 FC 74 1F` | `E9 <rel32>` | `S + 0x0C0` |

Each replacement covers complete original instructions and preserves the overwritten byte count. For every `E9 <rel32>`, write the four-byte signed little-endian value:

```text
(S + entry_offset) - (B + hook_RVA + 5)
```

The field-map replacement is a direct relative call within the same module, so its five bytes remain the same after module relocation. `file_archive_contains` is at RVA `0x00072720`.

As a concrete displacement check, if `B = 0x00400000` and `S = 0x01000000`, the hook replacements are:

| Patch | Complete replacement bytes for this example only |
| --- | --- |
| `field-map-palette` | `E8 4C B7 FF FF` |
| `ground-item-null` | `E9 10 CD A0 00 90` |
| `status-attack` | `E9 29 A5 A8 00 90 90` |
| `status-defense` | `E9 1F A5 A8 00 90 90` |
| `balloon-palette` | `E9 27 BC B8 00` |
| `empty-pixmap` | `E9 CE C7 BA 00 90 90 90` |
| `alpha-tail` | `E9 54 E4 BE 00` |

These example displacements are not reusable at a different `S` or `B`. Relocate the stub operands below as well.

## Behavior and preserved contracts

### Field-map palette probe

The original call borrows a palette entry merely to test existence. Its result is stored at `[ebp-0x10]` and compared only with zero. Redirecting it to `file_archive_contains` retains the same `this`, one stack argument, and `ret 4` convention. The helper performs lookup and release internally and returns 1 or 0. Subsequent palette loading still performs its own normal lookup. Do not enlarge the pool as a substitute for returning the handle.

### Rejected ground item

The stub reproduces the overwritten load of the item pointer into `eax`. A nonnull pointer continues at RVA `0x001F32F1`, the original vtable fetch. A null pointer continues at RVA `0x001F32FE`, which resets the exception-cleanup state, performs the normal reference cleanup, and advances to the next record. It does not exit the whole packet handler or bypass the creator's existing map-bounds checks. Flags and stack depth are preserved at both continuations.

The creator already removes an old object with the same ID before it attempts insertion. This patch does not undo that existing identity behavior. It also does not turn malformed/truncated record data into a valid packet.

### Status elements

Each stub reproduces its signed 16-bit pane-field load, then checks the resulting register against 9 with an unsigned comparison. Values `0..9` retain their original index; all others, including negative s16 values from memory corruption, become index zero. Execution resumes at the original table lookup, which selects the existing narrow string `"None"` for zero.

The attack stub changes only the loaded `ecx` index; defense changes only `edx`. Both preserve flags and stack depth. The raw packet and pane fields are not rewritten, so invalid input remains available for diagnostics. Install both element hooks to cover both lookups.

### Balloon palette ownership

The native palette-loading call is replaced with a jump. Its already-pushed palette ID and data pointer remain on the stack. The stub calls `file_palette_load_rgb` with the original `ecx`; that callee returns with `ret 8`. It then saves flags and all general registers, passes the entry handle from `[ebp-0x130]` to `file_archive_release_entry`, restores the saved state, and returns to the original post-call branch.

The release helper consumes its one stack argument with `ret 4` and does not need an archive `this` pointer. The handle remains active while palette loading consumes the mapped bytes, then becomes free. The shared palette ID and palette-loader return registers remain unchanged. This repairs normal completion; it does not add new C++ exception-unwind cleanup if palette loading throws.

### Empty pixmap

This hook is after the canvas readiness checks and the function's exception-frame setup, but before constructing the temporary clip-region object or changing clipping state. The stub rejects a null pixmap or either nonpositive rectangle extent: bottom minus top at pixmap `+0x10`/`+0x08`, and right minus left at `+0x14`/`+0x0C`.

For valid extents it restores registers/flags and executes the displaced `lea ecx,[ebp-0x7C]` and region-constructor call exactly once, then resumes at RVA `0x000538B5`. Invalid input jumps to the existing common epilogue at RVA `0x00053A5E`, with the temporary-region cleanup state still `-1`. No region destructor or clipping restoration is needed because neither resource was acquired. This guards the source extents used by both divisions; it is not a general validator for arbitrary pixmap pointers or inconsistent storage.

### Alpha tail

At the hook, `eax` points to the next source pixel, `ebx` to the destination pixel, `esi` to the next alpha token, and `dx` retains the current count in `dh` and alpha in `dl`. Native `[ebp-0x30]` is `draw_width % 4`. The shared stub keeps the existing complete-group loop and replaces the entire old tail.

- A zero remainder jumps directly to native row advance at RVA `0x00011DA4`, reading no additional alpha or pixel data.
- For a remainder of 1 through 3, each iteration consumes one alpha value, reads one 16-bit source and destination pixel, applies the native MMX component arithmetic to the low lane, and writes one 16-bit destination pixel.
- All three masks are read from the client's current MMX-mask globals, so RGB555 and RGB565 retain their original arithmetic. The constant four-lane value 32 comes from the same native table.
- After the last remaining pixel, the stub advances through the native row bookkeeping. It leaves `esp` and `ebp` intact. The original saved-register epilogue and final `emms` still run; the stub makes no native calls while MMX is active.

The loop no longer requests four alpha values for a partial tail or performs an eight-byte pixel load/store at a row boundary. No producer padding or larger row allocation is needed. As in the native complete-group loop, a valid run stream must cover the requested source rectangle. A malformed stream containing only zero-count tokens can still scan indefinitely; this patch repairs the known producer/consumer length mismatch rather than adding a new stream-length field.

## Shared stub template

Offsets in this listing are relative to `S`. Zero operands marked by relocation comments are placeholders, not runnable addresses. Local conditional branches and alignment NOPs are final bytes. The verifier checks this complete listing against its own byte template.

```text
; ground item
000: 8B 85 BC FE FF FF                   | mov eax, dword ptr [ebp - 0x144]
006: 9C                                  | pushfd
007: 85 C0                               | test eax, eax
009: 74 06                               | je 0x11
00B: 9D                                  | popfd
00C: E9 00 00 00 00                      | jmp <B + 0x001F32F1>
011: 9D                                  | popfd
012: E9 00 00 00 00                      | jmp <B + 0x001F32FE>
017: 90 90 90 90 90 90 90 90 90          | alignment NOPs
; attack element
020: 0F BF 88 FC 04 00 00                | movsx ecx, word ptr [eax + 0x4fc]
027: 9C                                  | pushfd
028: 83 F9 09                            | cmp ecx, 9
02B: 76 02                               | jbe 0x2f
02D: 31 C9                               | xor ecx, ecx
02F: 9D                                  | popfd
030: E9 00 00 00 00                      | jmp <B + 0x00175AF9>
035: 90 90 90 90 90 90 90 90 90 90 90    | alignment NOPs
; defense element
040: 0F BF 91 FE 04 00 00                | movsx edx, word ptr [ecx + 0x4fe]
047: 9C                                  | pushfd
048: 83 FA 09                            | cmp edx, 9
04B: 76 02                               | jbe 0x4f
04D: 31 D2                               | xor edx, edx
04F: 9D                                  | popfd
050: E9 00 00 00 00                      | jmp <B + 0x00175B23>
055: 90 90 90 90 90 90 90 90 90 90 90    | alignment NOPs
; balloon palette
060: E8 00 00 00 00                      | call <B + 0x00148650>
065: 9C                                  | pushfd
066: 60                                  | pushal
067: FF B5 D0 FE FF FF                   | push dword ptr [ebp - 0x130]
06D: E8 00 00 00 00                      | call <B + 0x00072760>
072: 61                                  | popal
073: 9D                                  | popfd
074: E9 00 00 00 00                      | jmp <B + 0x00074439>
079: 90 90 90 90 90 90 90                | alignment NOPs
; empty pixmap
080: 9C                                  | pushfd
081: 60                                  | pushal
082: 8B 45 0C                            | mov eax, dword ptr [ebp + 0xc]
085: 85 C0                               | test eax, eax
087: 74 1F                               | je 0xa8
089: 8B 48 10                            | mov ecx, dword ptr [eax + 0x10]
08C: 2B 48 08                            | sub ecx, dword ptr [eax + 8]
08F: 7E 17                               | jle 0xa8
091: 8B 48 14                            | mov ecx, dword ptr [eax + 0x14]
094: 2B 48 0C                            | sub ecx, dword ptr [eax + 0xc]
097: 7E 0F                               | jle 0xa8
099: 61                                  | popal
09A: 9D                                  | popfd
09B: 8D 4D 84                            | lea ecx, [ebp - 0x7c]
09E: E8 00 00 00 00                      | call <B + 0x00080CC0>
0A3: E9 00 00 00 00                      | jmp <B + 0x000538B5>
0A8: 61                                  | popal
0A9: 9D                                  | popfd
0AA: 31 C0                               | xor eax, eax
0AC: E9 00 00 00 00                      | jmp <B + 0x00053A5E>
0B1: 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 | alignment NOPs
; alpha tail
0C0: 8B 4D D0                            | mov ecx, dword ptr [ebp - 0x30]
0C3: 85 C9                               | test ecx, ecx
0C5: 0F 84 B4 00 00 00                   | je 0x17f
0CB: 84 F6                               | test dh, dh
0CD: 75 08                               | jne 0xd7
0CF: 66 8B 16                            | mov dx, word ptr [esi]
0D2: 83 C6 02                            | add esi, 2
0D5: EB F4                               | jmp 0xcb
0D7: 80 EE 01                            | sub dh, 1
0DA: 0F B6 FA                            | movzx edi, dl
0DD: 0F 6E D7                            | movd mm2, edi
0E0: 0F B7 38                            | movzx edi, word ptr [eax]
0E3: 0F 6E C7                            | movd mm0, edi
0E6: 0F B7 3B                            | movzx edi, word ptr [ebx]
0E9: 0F 6E CF                            | movd mm1, edi
0EC: 0F 6F 1D 00 00 00 00                | movq mm3, qword ptr [B + 0x002C4264]
0F3: 0F F9 DA                            | psubw mm3, mm2
0F6: 0F 6F 25 00 00 00 00                | movq mm4, qword ptr [B + 0x002D90D8]
0FD: 0F 6F EC                            | movq mm5, mm4
100: 0F 6F F4                            | movq mm6, mm4
103: 0F DB E0                            | pand mm4, mm0
106: 0F 71 D4 05                         | psrlw mm4, 5
10A: 0F DB E9                            | pand mm5, mm1
10D: 0F 71 D5 05                         | psrlw mm5, 5
111: 0F D5 E2                            | pmullw mm4, mm2
114: 0F D5 EB                            | pmullw mm5, mm3
117: 0F FD E5                            | paddw mm4, mm5
11A: 0F DB E6                            | pand mm4, mm6
11D: 0F 6F FC                            | movq mm7, mm4
120: 0F 6F 25 00 00 00 00                | movq mm4, qword ptr [B + 0x002D90D0]
127: 0F 6F EC                            | movq mm5, mm4
12A: 0F 6F F4                            | movq mm6, mm4
12D: 0F DB E0                            | pand mm4, mm0
130: 0F DB E9                            | pand mm5, mm1
133: 0F D5 E2                            | pmullw mm4, mm2
136: 0F D5 EB                            | pmullw mm5, mm3
139: 0F FD E5                            | paddw mm4, mm5
13C: 0F 71 D4 05                         | psrlw mm4, 5
140: 0F DB E6                            | pand mm4, mm6
143: 0F EB FC                            | por mm7, mm4
146: 0F 6F 25 00 00 00 00                | movq mm4, qword ptr [B + 0x002D90C8]
14D: 0F 6F EC                            | movq mm5, mm4
150: 0F 6F F4                            | movq mm6, mm4
153: 0F DB E0                            | pand mm4, mm0
156: 0F DB E9                            | pand mm5, mm1
159: 0F D5 E2                            | pmullw mm4, mm2
15C: 0F D5 EB                            | pmullw mm5, mm3
15F: 0F FD E5                            | paddw mm4, mm5
162: 0F 71 D4 05                         | psrlw mm4, 5
166: 0F DB E6                            | pand mm4, mm6
169: 0F EB FC                            | por mm7, mm4
16C: 0F 7E FF                            | movd edi, mm7
16F: 66 89 3B                            | mov word ptr [ebx], di
172: 83 C0 02                            | add eax, 2
175: 83 C3 02                            | add ebx, 2
178: 49                                  | dec ecx
179: 0F 85 4C FF FF FF                   | jne 0xcb
17F: E9 00 00 00 00                      | jmp <B + 0x00011DA4>
```

## Stub relocations

For each `rel32` operand at offset `O`, write `B + target_RVA - (S + O + 4)` as a signed little-endian 32-bit value. For `abs32`, write `B + target_RVA` as an unsigned little-endian address. The block is exactly `0x184` bytes, including alignment padding.

| Operand offset | Kind | Target RVA | Purpose |
| ---: | --- | ---: | --- |
| `0x00D` | `rel32` | `0x001F32F1` | Item nonnull continuation |
| `0x013` | `rel32` | `0x001F32FE` | Item normal cleanup |
| `0x031` | `rel32` | `0x00175AF9` | Attack table lookup |
| `0x051` | `rel32` | `0x00175B23` | Defense table lookup |
| `0x061` | `rel32` | `0x00148650` | Native palette loader |
| `0x06E` | `rel32` | `0x00072760` | Entry release helper |
| `0x075` | `rel32` | `0x00074439` | Balloon post-load branch |
| `0x09F` | `rel32` | `0x00080CC0` | Temporary region constructor |
| `0x0A4` | `rel32` | `0x000538B5` | Tiler after displaced call |
| `0x0AD` | `rel32` | `0x00053A5E` | Tiler common epilogue |
| `0x0EF` | `abs32` | `0x002C4264` | Four MMX lanes containing 32 |
| `0x0F9` | `abs32` | `0x002D90D8` | Current high-component mask |
| `0x123` | `abs32` | `0x002D90D0` | Current middle-component mask |
| `0x149` | `abs32` | `0x002D90C8` | Current low-component mask |
| `0x180` | `rel32` | `0x00011DA4` | Native alpha row advance |

## Installation, removal, and scope

Use the [safe launcher](safe-launcher.md), with these additional allocation details:

1. Verify the original executable size and SHA-256 and start a fresh client suspended. Find `B` from the loaded module, not from the preferred image base.
2. Compare every selected hook's original bytes. Check compatibility with any other patch that touches those instructions; a differing byte is a failure, not permission to chain unknown code.
3. Allocate at least `0x184` bytes writable. Require signed `rel32` reachability between each selected hook, its stub entry, and every relative native target used by that stub. No original-image code cave is assumed.
4. Copy the full shared template and apply all 15 relocations using `B` and the actual `S`. Change the completed allocation to executable/read-only. Read back the relocated bytes.
5. Temporarily change protection for each hook range, write the complete replacement, and read it back. Restore the original protection and flush the instruction cache for the allocation and all hooks before resuming.
6. On a mismatch or failed operation, leave the child suspended and terminate it, or fully restore every already-written hook before any resume. Do not leave a hook pointing at a missing or partially initialized allocation.

The six repairs can be selected independently, except that both status hooks are needed for complete element protection. Allocating the full block simplifies the documented layout even when only one stub is selected. Never write the original file or save a patched copy of it.

Removal requires a paused process with no thread executing the shared allocation or returning into it. Restore the verified original hook bytes, restore protections, flush the instruction cache, and only then release the allocation. A fresh process is preferable for A/B tests; removing patches in a running session does not undo already-leaked handles or restore removed objects.

## Reproduce the checks

[`verify_client_crash_patches.py`](../../../binaryninja/scripts/verify_client_crash_patches.py) contains the same template, hook definitions, and relocation list. It returns byte plans for verification and emulation only; it has no process-attachment or installation path.

```sh
python binaryninja/scripts/verify_client_crash_patches.py --binary client/Darkages.exe
python -m pip install unicorn==2.1.4
python binaryninja/scripts/verify_client_crash_patches.py --binary client/Darkages.exe --emulate
```

The first command uses only Python's standard library. The emulator is an optional dependency for the second check. Both commands verify the private executable's fingerprint; the emulated original/patched images live only in Unicorn memory. The script also checks the book's original-byte table, complete stub listing, and relocation table for drift, then rechecks the executable hash before exiting.

| Check performed here | Result and boundary |
| --- | --- |
| Seven original hook sequences | Match private executable and Binary Ninja disassembly |
| Hook/stub relocations at two different module/allocation bases | Resolve to the documented targets; native emulation runs at the preferred image base |
| Archive handle contract | Native contains/release helpers with a controlled lookup: original fills 20 slots, patched 40 probes leave zero busy |
| Item result contract | Original null dereference reproduced; patched null takes native cleanup, nonnull preserves native continuation |
| Both element indexes | All 256 byte values plus two negative s16 values each; valid names unchanged, invalid selects None without rewriting fields |
| Balloon ownership | Mocked palette consumption plus native release; one release, preserved return registers/flags and stack depth |
| Pixmap guard | Null, zero/reversed extents and valid extents; invalid path avoids region construction |
| Full MMX function | 116 two-row guarded cases, RGB555/565, clipping, vertical flip, and widths 1..8, 31..33, 255, 256, 639..641 as listed in the verifier; pixels match a scalar oracle |
| Original MMX controls | Widths 1, 4, and 640 fault against exact-end guard pages |
| Windows client installation | 19 installer scenarios passed, including routing controls and failure cleanup; disk hash unchanged |
| Arbiter login and local packet dispatch | Five status-element and ten ground-item cases passed native state checks; see [completed live checks](client-crash-tests.md#completed-live-checks-and-remaining-limits) |
| Other Windows gameplay cases and endurance | Not performed; use the [VM procedure](client-crash-tests.md) |

These results establish instruction-level behavior, selected calling contracts, and the recorded live packet outcomes. They do not establish every Windows exception-unwinding path, DirectDraw surface lifetime, interaction with other patches, server transfers, or endurance behavior.
