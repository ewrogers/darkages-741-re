# Ignore Bad Guy marker

This patch keeps the marker-present flag clear so a later launch uses the normal endpoint and login path.

## Target

| Static address | RVA | Verify bytes and instruction | Write bytes and instruction |
| --- | --- | --- | --- |
| `0x00431F85` | `0x00031F85` | `C6 82 68 06 00 00 01` `mov byte ptr [edx+0x668], 1` | `C6 82 68 06 00 00 00` `mov byte ptr [edx+0x668], 0` |

`app_detect_bad_guy_marker` normally writes `1` to `app_config + 0x668` when `%SystemRoot%\System32\Mscfg.dll` exists. That flag changes the default port from `2610` to `2601` and stops [`CLogin`](../../network/client/003-0x03-login.md) before its packet is built.

The patch replaces that complete seven-byte `mov` instruction with the same write of `0`. The normal file check and field initialization still run, but the marker no longer changes the endpoint or blocks login. This is narrower than skipping the detector call, which could leave the field uninitialized.

The marker file remains on disk. This patch does not change the registry-backed installation IDs, clear any server-side decision, or suppress the immediate termination caused by a newly received [`SBadGuy`](../../network/server/074-0x4a-bad-guy.md). It only makes a later launch ignore the persistent local marker.

Apply it with the [safe launcher workflow](safe-launcher-workflow.md).
