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
