# Configuration

The client chooses most startup settings internally. The command line is much smaller than it first appears.

## Active command line

The active parser in `app_parse_command_line` recognizes uppercase `-D`, but its handler does nothing in this build. No confirmed active flag changes the server address or port.

There is also a positional endpoint parser:

```text
Darkages.exe <host-or-ip> [port]
```

`net_parse_endpoint_override` can read this form, resolve a hostname, and store the address and port. The normal configuration path does not call it. The parser is dormant because `app_select_distribution_mode` always chooses distribution mode 1.

Changing the whole distribution mode would affect more than networking. A launcher should instead redirect only the endpoint setup call. See [Runtime patches](../appendix/runtime-patches.md).

The parser follows old, loose rules:

- An argument beginning with a digit is read as dotted IPv4.
- Other text is resolved as a hostname, using the first returned IPv4 address.
- A missing or zero port becomes port 23.
- Failed hostname lookup installs `210.101.85.25:2610` and reports failure.
- Missing positional input installs `52.88.55.94:2610` and reports failure.

These fallback values do not become active unless the dormant parser is enabled.

## Default endpoint

`net_configure_default_endpoint` prepares these values:

```text
host name:  da0.kru.com
backup IP:  52.88.55.94
port:       2610
```

If `%SystemRoot%\System32\Mscfg.dll` exists, the port becomes `2601`. This file is not a library used by the client. The server creates it after an `SBadGuy` client-ban response so later connections use the wrong port.

The `Port: 5` setting in `Darkages.cfg` selects TCP. It does not mean TCP port 5. The final network port is the base port plus a normally zero signed offset from the configuration object.

## Choosing an endpoint

The normal path is:

1. Start with `da0.kru.com` and port 2610, or 2601 when the marker file exists.
2. Resolve the host name.
3. Try the resolved address.
4. If that attempt fails, try the built-in backup IP.
5. If both attempts fail, report the socket error and stop the connection.

The hostname and backup IP are two steps in one connection attempt. This is not a general retry loop.

## Launcher override

For a custom server, the clean route is to enable the existing positional parser at launch. The launcher can resolve the requested host itself and pass a dotted IPv4 address plus port. This keeps address parsing inside a narrow startup change.

Two policies are useful:

- **Custom first:** use the supplied endpoint, but keep the official backup if it fails.
- **Connect or fail:** use only the supplied endpoint and show the normal connection error if it fails.

The second policy also disables the `da0.kru.com` fallback. Exact bytes and safety checks are kept in [Runtime patches](../appendix/runtime-patches.md).

## Connection results

On success, `net_connect_and_initialize_transport` stores the connected socket, initializes the packet state, and registers it with the client.

On failure, the socket is closed and reset to `INVALID_SOCKET`. Name lookup failure, connection failure, and socket setup failure take different branches, but none silently changes to an arbitrary endpoint.

See [Initial connection](../network/connection.md) for the network side of this flow.
