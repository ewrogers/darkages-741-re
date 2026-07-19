# Minigame support patch

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
E8 0C 72 FC FF
```

Replace it with `E8 <open wrapper rel32>`, where:

```text
signed-rel32 = stub_base - (module_base + 0x000AABF4)
```

The `file_archive_find_entry` entry must contain exactly:

```text
55 8B EC 83 EC 34
```

Replace it with `E9 <lookup wrapper rel32> 90`, where:

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
00: 55 8B EC FF 75 10 FF 75 0C FF 75 08 E8 00 00 00
10: 00 85 C0 74 19 E8 00 00 00 00 85 C0 74 10 6A 00
20: 6A 14 68 00 00 00 00 8B C8 E8 00 00 00 00 8B E5
30: 5D C2 0C 00 CC CC CC CC CC CC CC CC CC CC CC CC
40: 55 8B EC 56 8B F1 3B 35 00 00 00 00 74 1E 3B 35
50: 00 00 00 00 74 16 8B 0D 00 00 00 00 85 C9 74 0C
60: FF 75 08 E8 18 00 00 00 85 C0 75 0A 8B CE FF 75
70: 08 E8 0A 00 00 00 5E 5D C2 04 00 CC CC CC CC CC
80: 55 8B EC 83 EC 34 E9 00 00 00 00 CC CC CC CC CC
90: 63 69 6F 75 73 2E 64 61 74 00 CC CC CC CC CC CC
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
