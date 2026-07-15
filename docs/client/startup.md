# Startup controls

The reference launcher supports four focused runtime changes: the single-client guard, the two intro videos, an optional command-line server endpoint, and an optional connect-or-fail policy. The patches reuse existing control-flow paths and leave `Darkages.exe` unchanged on disk.

These addresses apply only to the target executable documented by this book:

```text
Size: 3,112,960 bytes
SHA-256: 054a5d6adc56099c6bfd9d2a58675aff62dc788b63209a3d906492f5b89e96c6
Preferred image base: 0x00400000
```

## Runtime patch summary

Create the process suspended, locate the actual `Darkages.exe` module base, verify the original bytes, apply the selected writes, flush the instruction cache, restore page protection, and resume the main thread.

| Behavior | Runtime address | Verify | Write |
| --- | --- | --- | --- |
| Skip intro videos | `module_base + 0x000ACA85` | `6A 01` | `6A 02` |
| Allow multiple clients | `module_base + 0x0017A7D9` | `75 07` | `EB 07` |
| Enable positional endpoint parser | `module_base + 0x00032253` | `E8 28 11 00 00` | `E8 B8 0D 00 00` |
| Disable official endpoint fallback | `module_base + 0x001655F4` | `C7 85 94 FB FF FF 00 00 00 00` | `E9 06 13 00 00 90 90 90 90 90` |

Do not calculate a runtime address from the preferred image base. ASLR may relocate the module. The launcher must use the base of the loaded main module in the new process.

Fail closed if the file fingerprint or any original byte sequence differs. Patch complete x86 instructions.

## Single-client instance guard

`app_winmain` at static address `0x0057A710` creates the named mutex `Nexon.SingleInstance`:

```asm
0057A7C3  call CreateMutexA
0057A7C9  mov  [app_single_instance_mutex], eax
0057A7CE  call GetLastError
0057A7D4  cmp  eax, 0xB7
0057A7D9  jne  0x0057A7E2
0057A7DB  push 0
0057A7DD  call process_terminate
0057A7E2  ; normal startup continues
```

Windows error `0xB7` is `ERROR_ALREADY_EXISTS`. The original conditional jump reaches normal startup only when the mutex did not already exist.

Change `JNE +7` (`75 07`) to `JMP +7` (`EB 07`). This is preferable to removing the termination call because it preserves instruction length, stack balance, mutex creation, and the normal `CloseHandle` cleanup near `0x0057AA65`.

The guard is only a local process policy. Running multiple clients can still expose shared-file, account, or server-side restrictions that are outside this check.

## Intro video sequence

`event_handle_intro_state` at `0x004ACA50` controls the opening sequence:

- State `0` posts state `1`.
- State `1` constructs the video pane and starts `CIf.bik`, followed by `CIb.bik`.
- State `2` is the normal post-video continuation.

`event_intro_video_frame_timer` at `0x0042E600` advances from the first clip to the second. After the second clip, it closes Bink playback and posts state `2`. This confirms that state `2` is the correct continuation point.

The initial transition is:

```asm
004ACA81  push 0
004ACA83  push 0
004ACA85  push 1
004ACA87  mov  ecx, [event_manager]
004ACA8D  call post_intro_state
```

Change `PUSH 1` (`6A 01`) to `PUSH 2` (`6A 02`). This bypasses the entire allocation, open, decode, render, and cleanup sequence. Patching a shared Bink function or removing only the playback call could affect other videos or leave the state machine waiting in state `1`.

## Enable positional endpoint parser

`app_config_ctor` at static address `0x00431FF0` normally initializes the mode-1 server endpoint by calling `net_configure_default_endpoint`:

```asm
00432253  call net_configure_default_endpoint
```

The executable also contains `net_parse_endpoint_override` at `0x00433010`. That function reads the positional host and port arguments already supplied to the client. The call sites are compatible: both functions receive the configuration object in `ECX`, the constructor ignores the return value, and the downstream distribution mode remains `1`.

Change the complete five-byte `CALL` from `E8 28 11 00 00` to `E8 B8 0D 00 00`. This redirects only the endpoint initializer and preserves the surrounding constructor control flow. The replacement target is calculated relative to the end of the instruction, so copying the complete verified bytes is safer than rebuilding the displacement in the launcher.

The reference launcher resolves `HOST` to dotted IPv4 before launch and supplies that address with the explicit port. This avoids relying on the parser's hostname-resolution behavior while retaining its existing address and port validation.

This patch is custom-first rather than custom-only. If the primary connection fails, the unchanged mode-1 unhappy path can still resolve `da0.kru.com` and try the official endpoint.

## Disable official endpoint fallback

`net_connect_and_initialize_transport` at `0x00565210` makes the primary blocking `connect()` call at `0x005655E6`. A successful connection branches to the normal continuation. A `SOCKET_ERROR` result falls through at `0x005655F4` into the hardcoded `da0.kru.com` lookup and retry block.

The first fallback instruction is a complete 10-byte initialization:

```asm
005655F4  mov  dword [ebp-0x46C], 0
```

Replace its bytes `C7 85 94 FB FF FF 00 00 00 00` with `E9 06 13 00 00 90 90 90 90 90`. The near jump targets the existing shared failure cleanup at `0x005668FF`; the five trailing `NOP` bytes pad the replacement to the full original instruction length.

The cleanup closes the current socket, stores `INVALID_SOCKET`, calls `WSACleanup`, and returns. The successful primary path never reaches this patch site. This makes the selected custom endpoint connect-or-fail without changing connection setup or success handling.

Use this patch only with the positional endpoint patch. The reference launcher enforces that relationship by accepting `--no-fallback` only alongside `--server HOST --port PORT`.

## Launcher safety checklist

1. Verify the on-disk size and SHA-256 before launching.
2. Start the process suspended.
3. Find the loaded main-module base in that process.
4. Read and compare the full original instruction bytes at each selected RVA.
5. Temporarily grant write access with `VirtualProtectEx`.
6. Write the full replacement instruction with `WriteProcessMemory`.
7. Call `FlushInstructionCache` and restore the original page protection.
8. Resume the main thread only after all selected patches succeed.
9. Terminate the suspended process if any verification or write fails.

The deterministic record used for these findings is [`analysis/exports/startup.yaml`](../../analysis/exports/startup.yaml).

## Reference C99 launcher

[`examples/windows/startup_launcher.c`](../../examples/windows/startup_launcher.c) is a minimal Windows launcher that implements this workflow without writing `Darkages.exe`. It verifies the file fingerprint, optionally resolves a custom hostname to IPv4, launches suspended, reads the 32-bit image base from the new process, applies selected patches, and resumes only after verification succeeds.

Build with MSVC:

```text
cl /nologo /W4 /O2 examples\windows\startup_launcher.c bcrypt.lib ws2_32.lib
```

Or build with MinGW-w64:

```text
gcc -std=c99 -Wall -Wextra -O2 -municode examples/windows/startup_launcher.c -lbcrypt -lws2_32 -o startup_launcher.exe
```

With no startup patch flags, the launcher applies both the multi-client and intro-skip patches. Use `--multi` or `--skip-intro` to apply only one. Add `--server HOST --port PORT` to enable the existing positional endpoint parser. Add `--no-fallback` when the custom endpoint must connect or fail:

```text
startup_launcher.exe C:\path\to\client\Darkages.exe
startup_launcher.exe --multi C:\path\to\client\Darkages.exe
startup_launcher.exe --skip-intro C:\path\to\client\Darkages.exe
startup_launcher.exe --server 127.0.0.1 --port 2610 C:\path\to\client\Darkages.exe
startup_launcher.exe --multi --server game.example.test --port 2610 C:\path\to\client\Darkages.exe
startup_launcher.exe --server game.example.test --port 2610 --no-fallback C:\path\to\client\Darkages.exe
```

The launcher validates the port, resolves the host itself, and passes a dotted IPv4 address plus the explicit port to the client. The endpoint patch redirects only the mode-1 initialization call. It does not change the distribution selector.

Without `--no-fallback`, a rejected or incomplete primary connection still resolves `da0.kru.com` and tries the official endpoint. With `--no-fallback`, the failure path closes the socket and returns without another lookup or connection attempt.
