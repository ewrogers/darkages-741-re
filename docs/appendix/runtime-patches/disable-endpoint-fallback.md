# Disable endpoint fallback

This patch makes a failed connection use the client's normal disconnected cleanup instead of retrying the official endpoint.

## Target

At static address `0x005655F4` (RVA `0x001655F4`), replace:

```diff
- 000: C7 85 94 FB FF FF 00 00 00 00 | mov dword ptr [ebp-0x46C], 0 ; prepare the fallback attempt
+ 000: E9 06 13 00 00                | jmp disconnected_cleanup     ; keep the failed connection closed
+ 005: 90 90 90 90 90                | nop x5                       ; fill the displaced ten-byte instruction
```

After a failed first connection, the original code resolves `da0.kru.com` and tries again. This patch jumps to the existing disconnected cleanup path at static address `0x005668FF` instead.

Use it with the [positional endpoint patch](command-line-endpoint.md) for a strict "connect to this endpoint or fail" policy. The normal socket close and `INVALID_SOCKET` state are preserved.

Apply it with the [safe launcher workflow](safe-launcher.md).
