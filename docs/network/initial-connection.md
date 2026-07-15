# Command line and initial connection

The version-741 target does not expose a working command-line IP or port override. The executable contains a positional endpoint parser, but the active build selector returns distribution mode `1` unconditionally. Mode `1` initializes its endpoint from `da0.kru.com` instead of calling that parser.

All addresses below are static virtual addresses for image base `0x00400000`.

## Effective command-line behavior

| Input | Result in this target | Evidence |
| --- | --- | --- |
| `-D<text>` | Recognized, then ignored because its handler is an empty function | `app_parse_command_line` at `0x0057A550`; `app_handle_d_option_stub` at `0x0057A460` |
| `<hostname-or-ip> [port]` | No effect in the active mode | `net_parse_endpoint_override` at `0x00433010` is called only by inactive distribution modes |
| Other flags or values | No active option handling found | The WinMain parser recognizes only uppercase `D` |

`app_set_working_directory_from_executable` at `0x004AD3A0` also reads the full command line. It only extracts the executable directory and calls `SetCurrentDirectoryA`; it does not parse options.

Every direct `GetCommandLineA` call was enumerated. The remaining uses belong to inactive distribution-mode parsers, copy the command line into patch UI state, or initialize the C runtime. None supplies another active flag or value.

### Dormant endpoint syntax

The unreachable parser accepts this form:

```text
Darkages.exe <IPv4-or-hostname> [port]
```

It treats a first argument beginning with a digit as four dotted decimal octets. Otherwise it copies a hostname, calls `gethostbyname`, and uses the first returned IPv4 address. The optional second argument is converted with `atoi`. A missing or zero port becomes `23`.

This is weak legacy parsing, not a supported interface. A hostname lookup failure installs `210.101.85.25:2610` and returns false. No usable positional argument installs `52.88.55.94:2610` and returns false. More importantly, `app_select_distribution_mode` at `0x00434EF0` always returns `1`, so none of these values replace the active endpoint.

Changing the distribution selector just to activate this parser is not considered a safe endpoint patch. Other behavior is also selected by the same mode.

## Runtime endpoint override

The reference [C99 startup launcher](../client/startup.md#reference-c99-launcher) enables the dormant parser without changing the distribution mode. At `app_config_ctor + 0x263`, it redirects the active endpoint initializer call:

| Runtime address | Verify | Write |
| --- | --- | --- |
| `module_base + 0x00032253` | `E8 28 11 00 00` | `E8 B8 0D 00 00` |

The original call targets `net_configure_default_endpoint`. The replacement targets `net_parse_endpoint_override`. Both receive the same configuration pointer in `ECX`, and the caller ignores the parser's return value. Downstream code still sees distribution mode `1`.

Use the launcher form:

```text
startup_launcher.exe --server HOST --port PORT C:\path\to\client\Darkages.exe
```

The launcher requires an explicit port, resolves `HOST` to IPv4 itself, forwards the dotted address and port as positional client arguments, verifies the original five-byte `CALL`, and applies the redirect only in suspended process memory.

Without the companion connect-or-fail patch, this is a custom-first route. A failed primary connection still enters the original mode-1 retry path, which resolves `da0.kru.com`.

### Connect or fail

Add `--no-fallback` when the selected custom endpoint must be the only connection attempt:

```text
startup_launcher.exe --server HOST --port PORT --no-fallback C:\path\to\client\Darkages.exe
```

At `net_connect_and_initialize_transport + 0x3E4`, primary connection failure reaches the first instruction of the official retry block:

| Runtime address | Verify | Write |
| --- | --- | --- |
| `module_base + 0x001655F4` | `C7 85 94 FB FF FF 00 00 00 00` | `E9 06 13 00 00 90 90 90 90 90` |

The replacement jumps to shared cleanup at static address `0x005668FF`. That existing path closes the socket, stores `INVALID_SOCKET`, calls `WSACleanup`, and returns. Because the patch site is reached only after the primary `connect()` returns `SOCKET_ERROR`, successful custom connections are unchanged.

The launcher verifies and replaces the complete 10-byte instruction. It requires `--server` and `--port` with `--no-fallback`, and it modifies only the suspended process memory.

## Active endpoint selection

`app_config_ctor` at `0x00431FF0` loads `Darkages.cfg`, caches mode `1`, and calls `net_configure_default_endpoint` at `0x00433380`.

1. Resolve `da0.kru.com` with `gethostbyname` at `0x00433396`.
2. Copy the first returned IPv4 address to `app_config + 0x295`.
3. If that lookup fails, store the hardcoded IPv4 address `52.88.55.94` at `0x004333C2`.
4. Select base TCP port `2610`.
5. If `%SystemRoot%\System32\Mscfg.dll` exists, select port `2601` instead.

Project-owner context identifies `Mscfg.dll` as a dummy marker created after the server sends the banned-client packet known as `SBadGuy`. The marker is intended to persist a local client-ID ban by moving later connections to the non-working port `2601`. This packet-to-file relationship is a behavioral lead until the packet handler and file creation path are traced again in Binary Ninja.

The `Port: 5` line in `Darkages.cfg` is a transport selector. It means TCP in this path and is not TCP port 5. The eventual network port is:

```c
tcp_port = config_base_port + config_signed_port_offset;
```

The signed offset is at `app_config + 0x436` and is normally zero here. `htons` converts the result to network byte order.

## Happy path

`net_open_transport` at `0x005645C0` sends transport selector `5` to `net_connect_and_initialize_transport` at `0x00565210`.

1. Initialize Winsock 1.1.
2. Create an `AF_INET`, `SOCK_STREAM` socket.
3. Set `SO_SNDBUF` to 16,384 bytes.
4. Make a blocking `connect` call at `0x005655D0` using the selected IPv4 address and port.
5. On success, register window message `0x401` with `WSAAsyncSelect` at `0x005668ED` for `FD_READ | FD_CLOSE`.

Active mode `1` sends no distribution-specific handshake inside this connection routine. After registration, socket reads and closure are delivered through the window message path.

## Unhappy paths

| Failure | Client behavior |
| --- | --- |
| Initial `da0.kru.com` lookup fails during configuration | Continue with `52.88.55.94` and the selected port |
| Winsock startup fails or does not report version 1.1 | Terminate the process with exit code `0` |
| Initial `socket` creation fails | Convert `WSAGetLastError` to a `networkError` message and enter the fatal exception path |
| Primary `connect` fails | Resolve `da0.kru.com` again at `0x00565622`; this can recover from DNS rotation or a transient lookup failure |
| Fresh DNS lookup fails | Terminate the process with exit code `0` at `0x00565686` |
| Second socket creation fails | Leave through transport cleanup without another endpoint attempt |
| Second `connect` fails | Close the socket and return with `INVALID_SOCKET`; this routine shows no dialog and makes no third active-mode attempt |
| Second `connect` succeeds | A conditional one-time path records the chosen IPv4 address and port in `iplookup.tbl`; failure to open that file shows a damaged-file message and exits |
| `WSAAsyncSelect` registration fails | Terminate the process with exit code `0` |

The `mServer.tbl` rotation loop at `0x005658E1` belongs to other distribution modes. Hardcoded mode `1` never uses it, so it is not an active fallback for this client.

## Key symbols

| Symbol | Address | Role |
| --- | --- | --- |
| `app_config` | `0x0073D950` | Global configuration pointer |
| `app_select_distribution_mode` | `0x00434EF0` | Returns constant mode `1` |
| `net_configure_default_endpoint` | `0x00433380` | Selects hostname, fallback IPv4 address, and base port |
| `net_parse_endpoint_override` | `0x00433010` | Dormant positional host and port parser |
| `net_open_transport` | `0x005645C0` | Selects TCP for transport value `5` |
| `net_connect_and_initialize_transport` | `0x00565210` | Opens, connects, retries, and registers the socket |
| `net_close_socket` | `0x00566D90` | Closes the socket and stores `INVALID_SOCKET` |

The matching durable Binary Ninja names and comments are in [`analysis/exports/network.yaml`](../../analysis/exports/network.yaml).
