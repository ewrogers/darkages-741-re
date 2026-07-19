# Version Check (`SVersionCheck`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x00` (0) |
| Transform | `raw` |
| Packet class | None found |
| Internal name provenance | Project-owner protocol knowledge, supported by the local version/bootstrap handler |

## Purpose

The server sends this message for **version check**.

`net_dispatch_main_menu_events` routes decoded opcode `0x00` directly to `net_handle_version_check`. It does not construct an RTTI packet object. Subtype `0` checks configuration state and installs the session seed-table selector and static key.

## Body

```text
packet SVersionCheck {
    u8      opcode                    // 0x00
    u8      subtype

    if subtype == 0 {
        u32     server_list_crc
        u8      seed_table_selector
        u8      static_key_length
        bytes   static_key[static_key_length]
    }
}
```

The handler reads the selector from body offset 6, reads the key length from offset 7, and queues the key beginning at offset 8.

Selector values `0` through `9` choose the mappings documented in [Packet transforms](../packet-transforms.md). The executable starts with selector `0` and the embedded nine-byte static key, but this subtype can replace both values.

The CRC covers the same uncompressed server-list serialization carried inside [`SMulti`](086-0x56-multi.md): record count followed by each record's ID, IPv4 bytes, big-endian port, and NUL-terminated name. Greeting text is not included.

The observed subtype-0 body carries server-list CRC32 `0x4BDA8542`, seed-table selector `2`, and the nine-byte static key `5E 6B 62 70 56 5B 5F 7D 71`. Its local server-table CRC matches and the table contains one entry, so the handler selects that record automatically and sends [`CMulti`](../client/087-0x57-multi-server.md) operation `0` with server ID `0`.

When the local list is empty or the CRC differs, the client opens `ServerSelectDialogPane` in request mode. Its constructor sends `CMulti` operation `1`; `SMulti` then replaces the list, saves `mServer.tbl`, and refreshes the selection UI.

The supplied decoded capture includes one zero byte after the nine-byte key. The handler stops at the declared key length and assigns no meaning to that extra byte.

Subtype `1` displays a localized error.

Subtype `2` starts the patch handoff. `net_handle_version_check` constructs the RTTI-backed `NewPatchPane`, which parses the remaining body as:

```text
record VersionPatchNotice {
    u16     required_version
    u8      file_count

    repeat file_count {
        string8 name
    }
}
```

The pane records the local version, the required version, the bounded file-name strings, the current command line, and the executable and data filenames in `Patch/Info`. It then launches `Patcher2.exe` with no command-line arguments and exits the client. The separate patcher is expected to consume the handoff file.

On a later startup, `startup_run_pending_patcher` checks for both `Patch/Info` and `Patch/Script`. If both exist it launches `Patcher2.exe` and exits again. If the pair is incomplete, it deletes both marker files and continues normal startup. The legacy client packet `CRequestPatch` and server packet `SSendPatch` are not on this verified launch path.

The paired request is [Version (`CVersion`)](../client/000-0x00-version.md).
