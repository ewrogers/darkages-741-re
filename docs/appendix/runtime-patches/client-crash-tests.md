# Testing client crash fixes

The VM and Arbiter can verify these fixes without a private server or a twelve-hour wait. Use two layers: deterministic instruction/buffer tests first, then real client dispatch and UI tests. A session that merely stays alive supplies weaker evidence than observing the repaired ownership or bounds condition.

The [exact patch definitions](client-crash-fixes.md) have passed emulation with original-failure controls. The [Windows launcher](../../../tools/crash-launcher/README.md) passed 19 installer integration scenarios on Windows 11 build 26200 in Parallels, including all repairs, individual groups, routing controls, eight installation-failure checkpoints, and invalid-file rejection. All test children terminated and the client disk hash stayed unchanged. A patched client then logged in through Arbiter and passed five status-element cases and ten ground-item cases. Patches were applied only to process memory.

## Completed live checks and remaining limits

These results came from one Windows client launched with all six crash repairs and `--arbiter`. Arbiter sent decoded messages only toward that client, with looping disabled. A separate read-only observer checked native state while briefly suspending the verified main thread, resuming it in a `finally` block. The observer did not install hooks or call client functions.

| Repair | Completed Windows observation | Remaining check |
| --- | --- | --- |
| Status elements | All five pairs below retained their injected raw values and produced the expected formatted labels | Original-client unsafe lookup was reproduced in emulation, not in this logged-in Windows session |
| Rejected ground item | All ten cases below passed ID-index, insertion, and image checks, including continuation to a valid second record | Original-client null dereference was reproduced in emulation, not in this logged-in Windows session |
| Field-map palette | Installer verification and instruction emulation passed | Live alternating-map pool measurements |
| Balloon palette | Installer verification and instruction emulation passed | Live first-initialization handle release and marker output |
| Empty pixmap | Installer verification and instruction emulation passed | Native Windows empty-rectangle invocation |
| Alpha tail | Installer verification and 116 guarded instruction-emulation cases passed | Native Windows guarded buffers and normal dialog output |

For status testing, the observer reconstructed a modifiers-only message from the client's latest cached, parsed `SStatus`. It read the object twice for stability and checked its privilege and modifier fields against the owning panes. Core, HP/MP, and experience/currency blocks were omitted; unrelated modifier bytes, privilege, and standalone flags were preserved. Only attack and defense element bytes changed. This was not a replay of an exported raw capture. Both valid endpoint pairs, the first invalid value in each field, and the maximum wire-byte pair passed. The raw words at extra-status offsets `+0x4FC` and `+0x4FE` retained the injected values; the formatted buffers at `+0x198` and `+0x218` contained the expected labels. The original baseline was restored and verified afterward.

For ground items, the observer supplied a valid installed sprite/dye from an existing ground item and confirmed each synthetic ID was absent before use. On a map narrower and shorter than 255, the ten cases were: an ordinary valid tile; X equal to width; Y equal to height; X equal to 255 and 256; Y equal to 255 and 256; invalid first/valid second records; X equal to width minus one; and Y equal to height minus one. Rejected IDs remained absent from the index. Accepted IDs were indexed with their requested coordinates, an inserted flag of one, and a nonnull image. The second record in the mixed message met those same checks. No item actions were sent to the server.

The client remained responsive through the final checks. Normal window closure then ended the test process and discarded the four synthetic local items and all memory patches. No matching Windows Application Error or Windows Error Reporting events were found in the preceding three hours. The disk SHA-256 still matched the target. Private baseline data, character identifiers, captures, and screenshots are intentionally absent from this record. These checks establish the listed outcomes, not all gameplay paths or endurance behavior. The remaining sections describe reproducible procedures, including checks still pending.

## Establish the two runs

1. Take a clean VM snapshot. Verify that the installed `Darkages.exe` has the book's [size and SHA-256](../../../contributing/research-policy.md#project-goal). Record Windows version, debugger version, client fingerprint, active patches, and Arbiter's decoded-packet mode.
2. Use an x86 debugger, such as x32dbg or WinDbg configured for the 32-bit client. Resolve each breakpoint from the actual module base `B` plus the documented RVA. The hexadecimal constants below are RVAs unless identified as an object-relative field.
3. Run an original-client control and a freshly launched patched-client run from the same snapshot. The supplied launcher implements the [suspended-launch procedure](safe-launcher.md): use `CrashFixLauncher.exe --vanilla` for the control and `CrashFixLauncher.exe --pause` for all repairs with a debugger attach point before resume. `--only status-elements --pause` selects one repair group, and `--verify-only` checks installation without running game code. The launcher prints the child PID, module/stub bases, and verified hook RVAs. Verify the live hook and relocated stub bytes before resuming. The supplied Python verifier checks/emulates bytes without installing them.
4. Run the [offline verifier](client-crash-fixes.md#reproduce-the-checks) against the VM's executable as well. `--emulate` runs the machine code in isolated emulator memory, not in the game. It needs no server, Arbiter, Binary Ninja, or account.
5. For Arbiter cases, use its supported **decoded server-to-client injection** path. Let it construct encryption, framing, sequence state, and checksums. If its packet editor separates the opcode from the body, account for that when using the byte offsets below. Do not manually splice plaintext into an encrypted stream.

Only inject the artificial test messages toward the local client. Keep the normal server-bound route free of test messages. Use packet builders or edit a privately captured valid message; preserve every unrelated field. Do not commit captures, character data, game files, dumps, or database files. A useful shareable result is a sanitized table of case name, original/patched, relevant field values, breakpoint/counter result, and pass/fail.

Restart or restore the snapshot between crash controls. A debugger can stop on the first exception or unsafe lookup; letting the client terminate is not necessary to prove each original failure.

For the local Arbiter listener at `127.0.0.1:2610`, launch `CrashFixLauncher.exe --arbiter` for the patched run and `CrashFixLauncher.exe --arbiter --vanilla` for the control. Add `--pause` for debugger attachment before resume, or `--only status-elements` to select a single repair group. The routing wrapper preserves the normal installation-ID initializer; the [direct parser-call experiment](command-line-endpoint.md) has a different initialization limitation. Routing support passed the installer checks, account login, and the local packet cases recorded above. Later server transfers remain untested.

## Status elements through Arbiter

Open the extra-status pane. Obtain a genuine [`SStatus`](../../network/server/008-0x08-status.md) containing the combat-modifier block (`fields & 0x04`). Clone it, preserving flags, privilege bits, all other blocks, and every non-element modifier. Inject the clone client-bound with these pairs:

| Attack | Defense | Patched result |
| ---: | ---: | --- |
| 0 | 9 | None and Undead, unchanged from the original |
| 9 | 0 | Undead and None, unchanged from the original |
| 10 | 0 | None and None |
| 0 | 10 | None and None |
| 255 | 255 | None and None |

For a complete plaintext body including opcode at position zero, the modifiers start at:

```text
m = 2 + (fields&0x20 ? 28 : 0)
      + (fields&0x10 ?  8 : 0)
      + (fields&0x08 ? 24 : 0)
attack position  = m + 6
defense position = m + 7
```

Subtract one if Arbiter exposes a payload that excludes the opcode. Do not assume a fixed offset when the selected blocks differ.

Set breakpoints at the original table lookups, RVAs `0x00175AF9` and `0x00175B23`. In the patched run, `ecx` or `edx`, respectively, must be zero for an invalid field and unchanged for `0..9`. The pane's raw fields at `this + 0x4FC` and `+0x4FE` still contain the injected values. Confirm the selected pointer is the None table entry and the pane redraws without an exception. Reinject the untouched clone afterward.

In the original run, an invalid index computes an address outside the ten-pointer stack array beginning at `ebp-0x28`. That observed out-of-range lookup is a deterministic failure criterion even if that particular stack value happens to point to readable memory and does not immediately crash. Do not require every invalid value to cause the same exception address.

## Ground-item rejection through Arbiter

Read the current map dimensions from a genuine [`SMapSize`](../../network/server/021-0x15-map-size.md), or from the current object list. Start with an authentic ground-item [`SDrawObjects`](../../network/server/007-0x07-draw-objects.md) record so the sprite tag and dye are valid. Assign an entity ID confirmed absent from the client's current ID index; never reuse the local player or another existing entity's ID.

A single ground-item body is 16 bytes including opcode: one opcode byte, a big-endian count of one, and a 13-byte item record. In this form X starts at position 3, Y at 5, entity ID at 7, tagged sprite at 11, dye at 13, and the two retained-on-wire unused bytes at 14 and 15. Creature and named-NPC records have different lengths. Keep the record count and length correct for each constructed message.

| Position | Patched result |
| --- | --- |
| A verified ordinary in-map tile | Item creates and refreshes normally |
| `x = width`, Y otherwise valid | Insertion rejects; handler continues without dereferencing null |
| `y = height`, X otherwise valid | Same rejection and continuation |
| X or Y = 255, then 256 | Both rejected for one-byte map dimensions |
| Two records: invalid item first, valid item with a second unused ID next | First is skipped; second is still processed |

For a maximum coordinate of `width-1` or `height-1`, select an otherwise usable test tile and distinguish unrelated image/placement failures from the boundary comparison. On a map narrower than 255, the `x = width` case also demonstrates why rejecting only coordinates above 255 is incomplete.

In the patched run, stop at stub entry `S + 0x000`. A rejected item has `eax == 0` after the reproduced load. It must continue at RVA `0x001F32FE`, reset `[ebp-4]` to `-1`, and reach the next-record path at `0x001F3319`. The valid case reaches the original vtable fetch at `0x001F32F1` with a nonnull pointer. In the original control, the invalid case dereferences null at that fetch.

Do not interact with synthetic items. Restart the client or use its normal map teardown to remove the local fixtures. No item was created on the server, and the test does not require sending an item action back to it.

## Measure the field-map pool directly

The archive singleton pointer is stored at `B + 0x002FD07C` for `setoa.dat`. Read that pointer as `A`; the pool pointer is the 32-bit value at `A + 0x3C`, and the count at `A + 0x40` should be 20. Each slot is `0x14` bytes. Count slots whose first 32-bit field equals one. Read these values while the main thread is paused at a stable post-load point, not halfway through an ordinary borrow.

1. Open a real travel map once and allow its balloon initialization to complete. Record the idle occupancy and loaded map name as the baseline.
2. Through Arbiter, replay authentic [`SFieldMap`](../../network/server/046-0x2e-field-map.md) messages for two installed field-map names with existing palettes, alternating names. Close each view normally. Do not select travel destinations; that would send `CFieldMap`. If needed, Arbiter can locally block only that selection message during this UI test while continuing normal connection traffic.
3. Repeat the same name as a control: the loader's unchanged-name early return must leave occupancy unchanged.
4. In the original run, measure a few alternating successful loads and confirm one additional retained slot per palette probe. Stop before pool exhaustion rather than waiting for a later dialog to fail.
5. In the patched run, perform at least 40 alternating loads. Idle occupancy must remain at the established baseline, and palette/art output must remain correct. Observe `file_archive_contains` returning 1 or 0 rather than retaining an entry pointer.

If `misc.dat` supplies either palette, inspect the pool that actually owns the returned handle. A handle lies within `pool .. pool + count*0x14` for its owner. Track both archives when overrides are present. Existing legitimate borrowers and the separate balloon leak affect the starting occupancy, so a blanket expectation of zero busy slots is incorrect for an arbitrary live session. Windows handle, GDI, and total-memory counters do not measure these slots.

## Check balloon release on first initialization

Use a fresh process, because the shared palette ID guard normally prevents later balloon constructions from repeating the palette load. Break after the lookup at RVA `0x000743E7`, record the nonnull handle stored in `[ebp-0x130]`, and verify its first 32-bit field is one. Continue to RVA `0x00074439`, after the palette call or its replacement stub.

The original control leaves that slot busy. With the balloon patch, the same slot is zero immediately at the continuation. The shared palette ID at `B + 0x002C6928` must retain the successfully allocated ID, and the marker must render with the same palette. This one observed release is stronger evidence than constructing many balloons after initialization and seeing no growth.

## Test an empty pixmap without changing assets

At a real call to `render_canvas_tile_pixmap`, pause at RVA `0x000538AD`, after its canvas readiness checks. Read the pixmap pointer from `[ebp+0x0C]` and save its four rectangle fields at offsets `+0x08`, `+0x0C`, `+0x10`, and `+0x14`.

For one draw, set bottom equal to top, or right equal to left. Step the patched guard and confirm it goes to RVA `0x00053A5E` before the region constructor or any clipping change. Restore the rectangle while paused before allowing another draw. Confirm a normal rectangle still follows the constructor at RVA `0x00080CC0` and the continuation at `0x000538B5`.

For the original control, the corresponding zero extent reaches an integer division at RVA `0x0005392E` or `0x0005393F`. Stop at that instruction or its first-chance exception, then restore the snapshot. Do not remove or corrupt an archive just to create this condition. The offline verifier covers null and reversed rectangles as well.

## Prove the alpha boundary in the VM

First open a real NPC dialog and verify that execution reaches `render_blit_pointer_rle_alpha_mmx`, RVA `0x000119C0`. A run using a different rendering dispatch path does not test this patch. At the tail, a drawn width divisible by four must go from `S + 0x0C0` to native row advance `B + 0x00011DA4` without entering the old token fetch at `B + 0x00011C94`.

For a deterministic native boundary test, use debugger-created scratch buffers at a genuine invocation of that function. This is an advanced test in the disposable VM; the emulated guarded cases are the easier first step. Let the normal caller supply the return address, saved registers, pixel-mask initialization, and MMX lifecycle.

1. Pause at the function entry before its prologue. Save its eleven argument words and the flip byte at `B + 0x002D8FD8`. Set the flip byte to zero for this one-row case.
2. Allocate three separate two-page regions with a 4096-byte readable/writable first page and a `PAGE_NOACCESS` second page: source `P`, destination `D`, and alpha `A`. Allocate a four-byte row-pointer table `R` and a 16-byte rectangle `Q`. Use a debugger allocation/`VirtualAlloc` facility; do not carve these buffers from client objects.
3. For width `W = 640`, put exactly `W` source and destination 16-bit pixels at the ends of their first pages. Fill the source with `0xFFFF` and destination with zero. Put exactly three little-endian alpha words, `0xFF10`, `0xFF10`, `0x8210`, in the final six bytes of A's first page. These encode `255+255+130` pixels at alpha 16. Store that stream pointer in R and `{0,0,1,W}` as four little-endian 32-bit rectangle coordinates in Q.
4. Replace only the arguments below. Keep the original return address at `[esp]` and put a breakpoint there before continuing.

| Stack position at function entry | Test argument |
| ---: | --- |
| `[esp+0x04]` | `P + 4096 - 2*W`, source |
| `[esp+0x08]` | Q, rectangle |
| `[esp+0x0C]` | `2*W`, source pitch in bytes |
| `[esp+0x10]` | `D + 4096 - 2*W`, destination |
| `[esp+0x14]` | 0, destination X |
| `[esp+0x18]` | 0, destination Y |
| `[esp+0x1C]` | `2*W`, destination pitch in bytes |
| `[esp+0x20]` | R, absolute alpha-row pointer table |
| `[esp+0x24]` | 0, initial run count |
| `[esp+0x28]` | 0, initial alpha |
| `[esp+0x2C]` | 0, additional alpha X offset |

5. The patched call must return normally, blend exactly W pixels, and never touch the inaccessible pages. For these white/black inputs, every output word must be `0x7BEF` with RGB565 masks or `0x3DEF` with RGB555 masks. Read the low word at `B + 0x002D90D8`: high-component mask `0xF800` selects the first expectation, `0x7C00` the second. The original control reads beyond the last alpha token at its unnecessary tail and raises a first-chance access violation. Stop there; do not resume into general exception handling.
6. Repeat fresh cases at widths 1, 2, 3, 4, 5, 639, and 641, with exactly W encoded alpha values and exactly W pixels before each guard. Build alpha words as `(min(255, remaining) << 8) | 16` until W values are covered. This tests partial tails as well as zero remainders. Check output against the verifier's scalar formula or known input/output pixels, not just the absence of a fault.
7. At the saved caller return breakpoint, restore the argument slots at their original saved addresses and the flip byte before the caller resumes. The native callee has already restored its nonvolatile registers and executed `emms`; do not replace the live return address or synthesize a new game-thread stack. Free scratch allocations only after the function has returned, or restore the VM snapshot.

Successful guard-page cases establish that the tested tail does not consume unencoded alpha or touch extra pixels. Normal dialog tests then check visual output and lifecycle integration. They do not establish that every possible corrupt run stream is bounded; the complete-group decoder still assumes a valid stream.

## Record the result

For each repair, retain the original control observation and patched invariant: pool occupancy, returned handle flag, table index, continuation address, or guard-page outcome. Record normal-path visual results too. Only after both pass should an ordinary play/endurance run be used to look for interactions with other patches, transfers, dialogs, and resource teardown. An overnight session is useful integration evidence, but it cannot replace these short deterministic checks.
