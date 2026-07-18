# Configuration

The client chooses most startup settings internally. The command line is much smaller than it first appears.

## Active command line

The active parser in `app_parse_command_line` recognizes uppercase `-D`, but its handler does nothing in this build. No confirmed active flag changes the server address or port.

There is also a positional endpoint parser:

```text
Darkages.exe <host-or-ip> [port]
```

`net_parse_endpoint_override` can read this form, resolve a hostname, and store the address and port. The normal configuration path does not call it. The parser is dormant because `app_select_distribution_mode` always chooses distribution mode 1.

Changing the whole distribution mode would affect more than networking. A launcher should instead redirect only the endpoint setup call. See [Enable the positional endpoint parser](../appendix/runtime-patches/enable-positional-endpoint-parser.md).

The executable also contains an older `.nfo` marker scanner and country- and ISP-specific endpoint integrations. They are not reached by this build's hardcoded selector. See [Distribution markers](distribution-markers.md).

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

If `%SystemRoot%\System32\Mscfg.dll` exists, the port becomes `2601`. This file is not a library used by the client. The [`SBadGuy`](../network/server/074-0x4a-bad-guy.md) handler creates it as a persistent client-installation soft-ban marker.

The [Good Guy runtime patch](../appendix/runtime-patches/ignore-local-bad-guy-marker.md) keeps the marker-present flag clear. It restores the normal endpoint and login path for later launches while leaving the file and installation IDs unchanged.

The `Port: 5` setting in `Darkages.cfg` selects the transport labeled `PPP or LAN`. It does not mean TCP port 5. Selectors 1 through 4 are the compiled `MODEM COM1` through `MODEM COM4` paths described in [Network transport](../network/transport.md). The final TCP port is the base port plus a normally zero signed offset from the configuration object.

## Installation identity

The default endpoint initializer also loads or creates a persistent 32-bit installation ID under `HKCR\NXKRI.Ctrl.1`, value `CLSID`. It derives a related 16-bit value and keeps a disguised registry copy under `HKCR\KRIHC.Ctrl.1`.

These values are separate from the `Mscfg.dll` marker. [`CLogin`](../network/client/003-0x03-login.md) masks both values with fresh random bytes and sends them in its installation block.

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

The second policy also disables the `da0.kru.com` fallback. Exact bytes and safety checks are kept in [Disable the official endpoint fallback](../appendix/runtime-patches/disable-official-endpoint-fallback.md).

## Connection results

On success, `net_connect_and_initialize_transport` stores the connected socket, initializes the packet state, and registers it with the client.

On failure, the socket is closed and reset to `INVALID_SOCKET`. Name lookup failure, connection failure, and socket setup failure take different branches, but none silently changes to an arbitrary endpoint.

See [Initial connection](../network/connection.md) for the network side of this flow.

## Saved audio levels

`Darkages.cfg` stores `Sound Volume` and `Music Volume` as user levels. A new configuration starts both at `3`. The options pane limits them to `0` through `10`, while the audio manager multiplies each value by `20` before passing it to Miles.

See [Audio system](../audio/README.md) for playback and fade behavior.

## Saved game settings

Six rows in the Game Settings dialog belong to the client. They live in the global `AppConfig` object and are written to `Darkages.cfg` when the dialog closes normally. The current configuration format, version `0x2600`, saves all six keys.

The other seven rows are server-managed. Their `ON` or `OFF` text is returned through `SMessage` and is not copied into `AppConfig` or written to the local file.

See [Game settings](../systems/game-settings.md) for the memory fields, file keys, packet flow, and later consumers.
