# Endpoint resolution and fallback order

Endpoint selection is split between configuration construction and the later socket connection routine. The normal US path is based on `usa.nfo`, `da0.kru.com`, and a hardcoded fallback. Other regional modes can use command-line arguments, `iplookup.tbl`, `taiwan.nfo`, or `mServer.tbl`.

## Configuration fields

The active configuration object is stored through global pointer `dword_73D950`. The relevant object-relative fields are:

| Offset | Meaning |
|---:|---|
| `+0x295` | Four raw IPv4 address bytes copied into `sockaddr_in` |
| `+0x29D` | Hostname text used by the bare command-line parser |
| `+0x434` | Base port in host byte order |
| `+0x436` | Signed port offset added before `htons` |
| `+0x438` | Command-line endpoint override was accepted |
| `+0x439` | Missing/zero override port was replaced with port 23 |
| `+0x55C` | Successful fallback endpoint has already been cached |
| `+0x561` | Multi-server record count |
| `+0x562` | Current multi-server record index |
| `+0x564` | Pointer to `0x281C`-byte multi-server records |
| `+0x668` | Persistent `SBadGuy` installation marker |

These are offsets inside a heap object, not static process addresses.

## Bare command-line override

`config_apply_command_line_endpoint_override` (`0x433010`) accepts a dotted IPv4 address or a hostname and an optional port.

Priority inside this function is:

1. Dotted IPv4 argument, copied as four decimal octets.
2. Hostname argument, resolved with Winsock 1.1 `gethostbyname` and the first returned IPv4 address.
3. If that hostname lookup fails, set `210.101.85.25:2610` and return 0.
4. With no usable argument, set `52.88.55.94:2610` and return 0.

An omitted or zero port becomes 23 and sets the flag at `+0x439`. A valid override sets `+0x438`, stores mode byte 5 at `+0x8E`, and returns 1.

The return value matters. A regional initializer may continue to another source after a zero result.

## US `usa.nfo` path

`config_init_dark_ages_endpoint_and_install_ids` (`0x433380`) resolves `da0.kru.com` and uses the first returned address. DNS failure uses `52.88.55.94`.

The selected port is:

```c
port = config->bad_guy_marker ? 2601 : 2610;
```

The same function also initializes the installation identifiers documented under [Client installation identifier](../security/client-installation-id.md).

## Taiwan path

`config_init_taiwan_endpoint` (`0x4338A0`) uses this strict priority:

1. A successful bare command-line override.
2. Numeric IPv4 and port from disk `iplookup.tbl`.
3. Hostname and port text from archived `taiwan.nfo`, resolved with `gethostbyname`.

The archived `taiwan.nfo` payload is tokenized on spaces. The first token is the hostname and the second is the decimal port.

## Connection-time retry

`net_connect_and_initialize_transport` (`0x565210`) builds the first `sockaddr_in` from `+0x295` and the sum of base port `+0x434` and signed offset `+0x436`.

For the US-style regional path, a failed first `connect` triggers:

1. Resolve `da0.kru.com` again.
2. Select port 2610, or 2601 when `+0x668` is set.
3. Replace the configured address and port.
4. Create a new TCP socket and retry.
5. On success, write `iplookup.tbl` once unless `+0x55C` was already set.

```c
if (connect(socket, &address) == SOCKET_ERROR) {
    host = gethostbyname("da0.kru.com");
    if (host == NULL) {
        exit(0);
    }

    config->ipv4 = first_ipv4(host);
    config->port = config->bad_guy_marker ? 2601 : 2610;

    socket = create_tcp_socket();
    if (connect(socket, &address) == SOCKET_ERROR) {
        disconnect_or_exit();
    }

    cache_iplookup_once(config->ipv4, config->port);
}
```

Region 0 without the auxiliary mode and region 2 branch to the direct/multi-server path instead of this `da0.kru.com` retry.

## Multi-server cycling

The direct path can cycle the `mServer.tbl` records at `+0x564`. It increments `+0x562` modulo the record count at `+0x561`, copies the next record's IPv4 from offset `+0x04`, copies its port from offset `+0x08`, and attempts another connection.

This makes `mServer.tbl` a later retry source, not the highest-priority source for the normal US startup endpoint.
