# Command-line endpoint

This patch redirects endpoint setup to the client's existing positional command-line parser.

## Target

At static address `0x00432253` (RVA `0x00032253`), replace:

```diff
- 000: E8 28 11 00 00 | call net_configure_default_endpoint ; always use the compiled default
+ 000: E8 B8 0D 00 00 | call net_parse_endpoint_override    ; accept the positional override first
```

`app_config_ctor` normally calls `net_configure_default_endpoint`. The replacement `CALL` targets the existing `net_parse_endpoint_override` instead.

The parser accepts:

```text
Darkages.exe <host-or-ip> [port]
```

The parser reads the raw `GetCommandLineA` text. It handles quotes around the executable path, but it does not remove quotes around the host or port. Only quote the executable when its path contains spaces:

```text
"C:\Dark Ages\Darkages.exe" 127.0.0.1 2610
```

Do not pass `"127.0.0.1"` or `"2610"`. A quoted address begins with a quote instead of a digit, so the parser treats the complete quoted text as a hostname. When that lookup fails, it installs `210.101.85.25:2610`, clears the accepted-override flags, and returns false. The patched mode-1 call site does not inspect that return value. Missing positional input similarly installs `52.88.55.94:2610` and returns false.

For predictable behavior, the launcher should resolve a host to dotted IPv4 before launch, pass an explicit unquoted port, and validate the exact command line before resuming the process.

## Initialization limitation

This five-byte replacement does not switch the distribution-mode field, but it skips more than the compiled endpoint. `net_configure_default_endpoint` also loads or creates the registry-backed installation ID and its derived value. The configuration object is initially zeroed, so the direct redirection leaves `app_config + 0x424` and `app_config + 0x428` at zero.

Those values do not participate in [`CVersion`](../../network/client/000-0x00-version.md), the stipulation exchange, or the body of [`CTransferServer`](../../network/client/016-0x10-transfer-server.md). They are masked and sent later by [`CLogin`](../../network/client/003-0x03-login.md). The client produces a structurally consistent login block from zero values, but server acceptance of that identity is not known.

Treat this direct-call patch as an endpoint experiment, not a stock-compatible startup patch. A complete implementation should preserve the original initializer and apply the validated endpoint afterward. A launcher-owned wrapper can call `net_configure_default_endpoint` first and then `net_parse_endpoint_override`; it should treat parser failure as launch failure instead of connecting to a compiled fallback.

Without the [official fallback patch](disable-endpoint-fallback.md), a later connection failure can still retry `da0.kru.com` even after a valid positional override.

Apply it with the [safe launcher workflow](safe-launcher.md).

## Arbiter loopback wrapper

The [crash-fix launcher](../../../tools/crash-launcher/README.md) supports `--arbiter` without using the direct parser-call replacement above. It calls the original initializer first, preserving installation-ID setup, then changes only the resulting IPv4 and port to `127.0.0.1:2610`. `--arbiter --vanilla` retains that routing while disabling all crash repairs, so both test runs can connect through the same proxy.

At RVA `0x00032253`, original `E8 28 11 00 00` becomes `E8 <rel32>` targeting the wrapper. The original call and wrapper are both argumentless calls using `ecx` for the configuration pointer. With `S` equal to the crash stub allocation, the wrapper starts at `S + 0x190`, after NOP padding following the original `0x184` bytes. The combined allocation is `0x1AD` bytes. Its 29-byte template is:

```text
56 8B F1 E8 ?? ?? ?? ??
C7 86 95 02 00 00 7F 00 00 01
66 C7 86 34 04 00 00 32 0A 5E C3
```

The hook operand is `(S + 0x190) - (B + 0x00032258)`. The wrapper call operand at `S + 0x194` is `(B + 0x00033380) - (S + 0x198)`. Both are signed little-endian `rel32` values. The resulting instructions are:

```asm
push esi
mov esi, ecx
call net_configure_default_endpoint
mov dword ptr [esi+0x295], 0x0100007f
mov word ptr [esi+0x434], 0x0a32
pop esi
ret
```

The initializer at RVA `0x00033380` preserves `esi` and returns with plain `ret`; its normal initialization includes configuration fields `+0x424` and `+0x428`. The wrapper's added instructions preserve its return value, outgoing volatile registers and flags, restore the caller's `esi`, and balance the stack. The four endpoint bytes become `7F 00 00 01`; the port remains in the configuration's host-order 16-bit field. No positional endpoint arguments or parser fallback are involved.

The launcher also requires and installs the exact ten-byte [disable-fallback patch](disable-endpoint-fallback.md) at RVA `0x001655F4`. It verifies both original sites along with the crash hooks before writing, and applies the same protection, readback, cache-flush and suspended-child failure handling. Both routing changes affect process memory only.

The wrapper passed isolated x86 execution at two address pairs against a mocked initializer, preserving sentinel installation fields and the call's register/flag/stack results. Windows 11 Parallels testing verified the installed bytes, an established client connection to `127.0.0.1:2610`, successful account login, and the [local packet tests](client-crash-tests.md#completed-live-checks-and-remaining-limits). Later server transfers remain untested.
