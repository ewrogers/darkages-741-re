# Bad Guy (`SBadGuy`)

`SBadGuy` activates the client's persistent soft-ban path for an installation identity. The client creates a marker under the Windows system directory and immediately terminates. On later launches, marker existence changes the endpoint and prevents `CLogin` from being submitted.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x4A` (74) |
| Encoding | session key |
| Packet class | RTTI class `SBadGuy` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SBadGuy {
    u8      opcode                    // 0x4A
    u8      mode
    u8      marker_byte
    u32     guard
}
```

`net_deserialize_bad_guy_server_packet` reads both byte fields and the big-endian guard. The soft-ban action runs only when:

```c
mode == 0 && guard == 0x7D3AFF99
```

Other values are consumed without creating the marker.

## Client flow

```text
CLogin sends the installation values
        |
        v
server selects SBadGuy
        |
        v
client creates Mscfg.dll and terminates
        |
        v
next launch detects the marker
        |
        +--> default port changes from 2610 to 2601
        |
        +--> CLogin terminates before submission
```

The project owner identifies this as the server's way to invalidate or soft-ban a client installation ID. The executable confirms the complete client-side mechanism. Server-side selection policy is outside this binary.

## Creating the marker

`net_handle_bad_guy_server_packet` asks Windows for the system directory, then constructs this path from four split string fragments:

```text
%SystemRoot%\System32\Mscfg.dll
```

The nearby wide strings `yummy` and `rocks` are assigned to locals but are not used in the path.

The handler opens the file with read/write access, no sharing, and `CREATE_NEW`. It does not replace an existing marker.

When creation succeeds, the client:

1. Writes `marker_byte` at file offset zero.
2. Seeks to absolute offset `0xDB72`.
3. Sets end-of-file, making the file `0xDB72` bytes long.
4. Closes the file.
5. Calls an invalid-memory clearing path that normally terminates the process.

If creation fails, including when the file already exists or the process lacks permission, the handler writes through a null pointer and normally terminates anyway. A valid `SBadGuy` therefore ends the running client whether or not persistence succeeds.

The marker byte and file contents have no confirmed later meaning. Startup checks only whether the path exists.

## Effect on later launches

`app_config_ctor` calls `app_detect_bad_guy_marker` before selecting the distribution endpoint. The function reconstructs the same path and tests file existence:

```c
app_config->bad_guy_marker_present = file_exists(path); // +0x668
```

For the active default endpoint, a set flag changes the TCP port from `2610` to `2601`.

The same flag is checked by [`CLogin`](../client/003-0x03-login.md). When it is set, `net_send_login_request` reaches another invalid-memory clearing call before constructing opcode `0x03`. Even if a marked client reaches a server on port `2601`, normal login submission cannot continue.

The packet does not overwrite or delete the registry-backed installation IDs. Those values remain available to identify the installation. The persistent client-side state is the marker file and its transient `app_config + 0x668` flag.

## Local Good Guy patch

The [Good Guy runtime patch](../../appendix/runtime-patches/ignore-local-bad-guy-marker.md) changes the marker-present branch to write `0` to the flag. A client left unusable by the marker can then use the normal port and submit `CLogin` again without deleting the file.

This patch affects startup detection only. A newly received `SBadGuy` still creates the marker when possible and terminates the current process. It also does not change the installation IDs or any server-side decision about them.

## Packet construction and dispatch

`net_bad_guy_server_packet_ctor` passes opcode `0x4A` to the common server packet base and installs the exact `SBadGuy` vtable. `net_register_bad_guy_server_packet_factory` registers its constructor with `server_packet_factory`.

After deserialization, `net_dispatch_server_packet` sends the object directly to `net_handle_bad_guy_server_packet`. There is no client response packet. The valid action terminates the client instead.

## Known limits

The actual system path and write permission depend on the Windows environment, redirection, and process privileges. Creation failure still terminates the current client but does not prove that the marker persisted.

Removing the local marker would clear the client-side flag on the next launch. That does not prove the server-side installation ban is cleared, because the unchanged installation IDs can be sent again in `CLogin`.
