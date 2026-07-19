# Multiple clients

This patch bypasses the local single-instance check while preserving the rest of normal startup.

## Target

At static address `0x0057A7D9` (RVA `0x0017A7D9`), replace:

```diff
- 000: 75 07 | jne normal_startup ; continue only when no older instance exists
+ 000: EB 07 | jmp normal_startup ; always continue through normal startup
```

`app_winmain` creates the named mutex `Nexon.SingleInstance`, then checks for Windows error `ERROR_ALREADY_EXISTS`.

The patch changes the existing conditional jump into an unconditional jump to normal startup. It keeps the instruction size, mutex creation, stack balance, and normal handle cleanup.

This only bypasses the local process check. It does not bypass account, server, or shared-file restrictions.

Apply it with the [safe launcher workflow](safe-launcher.md).
