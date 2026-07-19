# Safe launcher

These changes are intended for a launcher that writes to the suspended process. They do not modify `Darkages.exe` on disk.

The target uses preferred image base `0x00400000`, but Windows may relocate it. Always calculate a runtime address as:

```text
runtime address = loaded module base + RVA
```

## Launcher flow

```text
confirm the executable size and SHA-256
launch the process suspended
find the loaded main-module base

for each selected patch
    read and compare the original bytes
    make the target page writable
    write the complete replacement instructions
    flush the instruction cache
    restore the old page protection

resume the main thread
```

If the fingerprint or any original byte differs, stop and terminate the suspended child. Never guess against a different executable.

## Safety checklist

- Patch only the matching target fingerprint.
- Use the loaded module base, not the preferred image base.
- Verify every original byte before writing.
- Change complete x86 instructions.
- Keep the process suspended until all patches succeed.
- Flush the instruction cache after writes.
- Restore memory protection before resuming.
- Fail closed and leave the executable file untouched.
