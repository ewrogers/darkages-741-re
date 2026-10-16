# In-memory crash-fix launcher

`CrashFixLauncher.exe` starts the fingerprinted 7.41 client suspended, installs the book's six repairs at seven hook sites, verifies the writes, and resumes it. It never opens `Darkages.exe` for writing. Closing the game discards all patches.

The [book](../../docs/appendix/runtime-patches/client-crash-fixes.md) owns the original bytes, RVAs, stub code, and relocations. `PatchData.g.cs` is generated from its [executable verifier](../../binaryninja/scripts/verify_client_crash_patches.py). No client executable, assets, or captures belong in this directory or a launcher distribution.

## Run in Windows

Put the launcher beside `Darkages.exe` and double-click it. It uses that directory as the client's working directory and enables all repairs. From PowerShell:

```powershell
& 'C:\Dark Ages\CrashFixLauncher.exe'
& 'C:\Dark Ages\CrashFixLauncher.exe' --verify-only
& 'C:\Dark Ages\CrashFixLauncher.exe' --only status-elements
& 'C:\Dark Ages\CrashFixLauncher.exe' --vanilla
& 'C:\Dark Ages\CrashFixLauncher.exe' --pause
& 'C:\Dark Ages\CrashFixLauncher.exe' --arbiter
& 'C:\Dark Ages\CrashFixLauncher.exe' --arbiter --vanilla
```

`--verify-only` creates a suspended child, installs and verifies the selected patches, then terminates that child without running game code. `--vanilla` starts a fingerprint-checked unpatched control. `--pause` waits for Enter after installation so an x86 debugger can attach to the printed PID before the game runs; EOF cancels and terminates the suspended child. An argument error or installation failure returns nonzero and is recorded in `%LOCALAPPDATA%\DarkAgesCrashLauncher\logs` when that directory is writable. Run from a terminal to read an error that would disappear when a double-clicked console closes.

`--only` accepts a comma-separated list: `field-map-palette`, `ground-item-null`, `status-elements`, `balloon-palette`, `empty-pixmap`, `alpha-tail`. The status group selects both lookups. Use `--client PATH` for a client elsewhere. Arguments after `--` are quoted and passed to the game.

`--arbiter` adds two memory-only routing patches: preserve stock endpoint/installation-ID initialization, then replace the resulting endpoint with `127.0.0.1:2610`, and disable the official-server retry after a failed connection. Arbiter must already be listening. This flag does not launch or configure Arbiter. With `--arbiter --vanilla`, only the routing patches apply, providing a proxy-connected control with all crash repairs disabled. See the [exact wrapper and routing bytes](../../docs/appendix/runtime-patches/command-line-endpoint.md#arbiter-loopback-wrapper).

## Installation guarantees and limits

The launcher requires SHA-256 `054a5d6adc56099c6bfd9d2a58675aff62dc788b63209a3d906492f5b89e96c6`, length `3,112,960`, and the expected x86 PE headers (`SizeOfImage = 0x506000`). It holds a read-only file handle that denies writes/deletion during installation, validates the loaded headers and all seven original hook sites before writing, and checks each selected original again immediately before its replacement.

The shared stub starts as writable memory and becomes execute/read before hook installation. Each hook's original protection is restored. Remote bytes and protections are read back, instruction caches are flushed, and the disk fingerprint is checked again before resume. Any handled failure before resume terminates only the launcher's own child and confirms termination; a cleanup failure explicitly reports the PID. The launcher never attaches to an existing game process. A resumed process owns its stub until exit. Killing the launcher externally during installation can leave a suspended child; its PID is printed and logged.

This is an x86 .NET Framework 4 console program. Module discovery dynamically resolves `NtQueryInformationProcess`, reads the x86 PEB image base, and checks it against the fingerprinted PE headers. That internal PEB layout is a compatibility constraint; unexpected results abort. It was tested on Windows 11 build 26200 in Parallels. See Microsoft's contracts for [process creation](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw), [memory protection and cache flushing](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotectex), and [process information](https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntqueryinformationprocess).

## Build and verify

From the repository root, regenerate/check constants with Python:

```text
python3 tools/crash-launcher/generate_patch_data.py --check
```

In Windows PowerShell, using the x86 .NET Framework compiler supplied with the tested VM:

```powershell
& .\tools\crash-launcher\Build.ps1 -OutputDirectory .\artifacts\crash-launcher -IntegrationTests
& .\artifacts\crash-launcher\LauncherIntegrationTests.exe 'C:\Dark Ages\Darkages.exe'
```

Omit `--check` to regenerate `PatchData.g.cs` after changing the canonical verifier. `Build.ps1` builds the launcher and runs its non-process self-test. `-IntegrationTests` also builds a separate test runner with fault checkpoints; those checkpoints are compiled out of the production launcher. Keep compiled `.exe` files in ignored artifact/build directories.

VM validation passed 19 integration scenarios: all repairs together, six individual groups, an unpatched verification control, eight deliberate failures with Arbiter routing selected from child creation through the step immediately before resume, two Arbiter verification controls with crash repairs on/off, and invalid-file rejection before process creation. Every verification/fault child terminated and the client hash remained unchanged. The production build passed `--verify-only`, resumed the client, and logged in through the local Arbiter listener with `--arbiter`. Five status-element and ten ground-item cases then passed native state checks. The other four repairs have instruction-emulation evidence but still need their Windows gameplay checks. See the book's [completed results and remaining procedures](../../docs/appendix/runtime-patches/client-crash-tests.md).

The optional `verify_arbiter_endpoint.py` check requires Unicorn (tested with 2.1.4). It executes the wrapper at two address pairs against a mocked stock initializer, checking the call/return, stack, registers, flags, preserved installation fields and final IPv4/port. It does not emulate the real initializer's registry or DNS calls.
