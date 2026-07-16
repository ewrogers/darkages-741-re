# Runtime patches

These changes are intended for a launcher that writes to the suspended process. They do not modify `Darkages.exe` on disk.

The target uses preferred image base `0x00400000`, but Windows may relocate it. Always calculate a runtime address as:

```text
runtime address = loaded module base + RVA
```

## Patch list

| Purpose | Static address | RVA | Verify | Write |
| --- | --- | --- | --- | --- |
| Skip intro videos | `0x004ACA85` | `0x000ACA85` | `6A 01` | `6A 02` |
| Allow multiple clients | `0x0057A7D9` | `0x0017A7D9` | `75 07` | `EB 07` |
| Enable positional endpoint parser | `0x00432253` | `0x00032253` | `E8 28 11 00 00` | `E8 B8 0D 00 00` |
| Disable official endpoint fallback | `0x005655F4` | `0x001655F4` | `C7 85 94 FB FF FF 00 00 00 00` | `E9 06 13 00 00 90 90 90 90 90` |
| Hide all static map art | `0x005E47FF` | `0x001E47FF` | `74 05` | `EB 00` |

## Allow multiple clients

`app_winmain` creates the named mutex `Nexon.SingleInstance`, then checks for Windows error `ERROR_ALREADY_EXISTS`.

The patch changes the existing conditional jump into an unconditional jump to normal startup. It keeps the instruction size, mutex creation, stack balance, and normal handle cleanup.

This only bypasses the local process check. It does not bypass account, server, or shared-file restrictions.

## Skip the intro

`event_handle_intro_state` normally posts intro state 1. The patch posts state 2 instead.

State 2 is the normal continuation after both video clips finish. This is narrower than changing Bink playback because it follows the client's own state machine and avoids creating the video pane.

## Enable the positional endpoint parser

`app_config_ctor` normally calls `net_configure_default_endpoint`. The replacement `CALL` targets the existing `net_parse_endpoint_override` instead.

The parser accepts:

```text
Darkages.exe <host-or-ip> [port]
```

For predictable behavior, the launcher should resolve a host to dotted IPv4 before launch and pass an explicit port.

This patch changes only endpoint setup. It does not switch the whole distribution mode. Without the next patch, a failed connection can still retry `da0.kru.com`.

## Disable the official fallback

After a failed first connection, the original code resolves `da0.kru.com` and tries again. This patch jumps to the existing disconnected cleanup path at static address `0x005668FF` instead.

Use it with the positional endpoint patch for a strict "connect to this endpoint or fail" policy. The normal socket close and `INVALID_SOCKET` state are preserved.

## Hide all static map art

`render_static_object` normally skips drawing only when the object's hidden byte is set. The patch forces the same existing jump to the normal function epilogue for every static object.

This hides walls, trees, and fixed map decorations. It does not hide ground, characters, items, or effects, and it does not change collision.

For a live `?` button toggle, use a DLL hook instead of rewriting these bytes while the process is running. The hook design is described in [Walls and occlusion](../rendering/walls-and-occlusion.md).

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
