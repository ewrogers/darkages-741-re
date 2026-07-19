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

For predictable behavior, the launcher should resolve a host to dotted IPv4 before launch and pass an explicit port.

This patch changes only endpoint setup. It does not switch the whole distribution mode. Without the [official fallback patch](disable-endpoint-fallback.md), a failed connection can still retry `da0.kru.com`.

Apply it with the [safe launcher workflow](safe-launcher.md).
