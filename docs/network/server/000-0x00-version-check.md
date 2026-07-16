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
    u8 opcode                 // 0x00
    u8 subtype

    if subtype == 0:
        u32be configuration_crc
        u8 seed_table_selector
        u8 static_key_length
        bytes static_key[static_key_length]
}
```

The handler reads the selector from body offset 6, reads the key length from offset 7, and queues the key beginning at offset 8.

Selector values `0` through `9` choose the mappings documented in [Packet transforms](../packet-transforms.md). The executable starts with selector `0` and the embedded nine-byte static key, but this subtype can replace both values.

The observed subtype-0 body carries configuration CRC32 `0x4BDA8542`, seed-table selector `2`, and the nine-byte static key `5E 6B 62 70 56 5B 5F 7D 71`. Its local server-table CRC matches and the table contains one entry, so the handler selects that record automatically and sends [`CMulti`](../client/087-0x57-multi-server.md) with server ID `0`.

The supplied decoded capture includes one zero byte after the nine-byte key. The handler stops at the declared key length and assigns no meaning to that extra byte.

Subtype `1` displays a localized error.

Subtype `2` starts the patch handoff. `net_handle_version_check` constructs the RTTI-backed `NewPatchPane`, which parses the remaining body as:

```c
struct VersionPatchNotice {
    u16be required_version;
    u8 file_count;

    repeat file_count times:
        u8 name_length;
        u8 name[name_length];
}
```

The pane records the local version, the required version, the bounded file-name strings, the current command line, and the executable and data filenames in `Patch/Info`. It then launches `Patcher2.exe` with no command-line arguments and exits the client. The separate patcher is expected to consume the handoff file.

On a later startup, `startup_run_pending_patcher` checks for both `Patch/Info` and `Patch/Script`. If both exist it launches `Patcher2.exe` and exits again. If the pair is incomplete, it deletes both marker files and continues normal startup. The legacy client packet `CRequestPatch` and server packet `SSendPatch` are not on this verified launch path.

The paired request is [Version (`CVersion`)](../client/000-0x00-version.md).
