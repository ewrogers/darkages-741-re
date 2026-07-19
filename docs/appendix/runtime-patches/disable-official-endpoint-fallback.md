# Disable endpoint fallback

This patch makes a failed connection use the client's normal disconnected cleanup instead of retrying the official endpoint.

## Target

| Static address | RVA | Verify bytes and instruction | Write bytes and instruction |
| --- | --- | --- | --- |
| `0x005655F4` | `0x001655F4` | `C7 85 94 FB FF FF 00 00 00 00` `mov dword ptr [ebp-0x46C], 0` | `E9 06 13 00 00` `jmp disconnected_cleanup`, then five `nop` bytes |

After a failed first connection, the original code resolves `da0.kru.com` and tries again. This patch jumps to the existing disconnected cleanup path at static address `0x005668FF` instead.

Use it with the [positional endpoint patch](enable-positional-endpoint-parser.md) for a strict "connect to this endpoint or fail" policy. The normal socket close and `INVALID_SOCKET` state are preserved.

Apply it with the [safe launcher workflow](safe-launcher-workflow.md).
