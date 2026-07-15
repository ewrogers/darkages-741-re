# SBadGuy installation marker and login kill switch

`SBadGuy` is a persistent client-side kill switch. When its guard fields are valid, the handler attempts to create `%SystemRoot%\System32\Mscfg.dll` and deliberately crashes. If marker creation succeeds, later launches detect that file, select TCP port `2601` instead of `2610`, and deliberately crash again before submitting `CLogin`.

This strongly supports the installation soft-ban interpretation. The client cannot show whether a GM command, an automated server rule, or another server-side action sends the packet.

## Control flow

```text
receive SBadGuy 0x4A
    |
    | mode == 0 and guard == 0x7D3AFF99
    v
create or replace %SystemRoot%\System32\Mscfg.dll
    |
    | write marker byte and set file length to 0xDB72
    v
deliberate null write and immediate crash
    |
    | next client launch
    v
marker existence sets config +0x668
    |
    +-> connect to da0.kru.com port 2601 instead of 2610
    |
    +-> CLogin builder performs another deliberate null write
```

## Packet handler

`net_handle_s_bad_guy` at `0x5F7900` receives the RTTI-deserialized packet object. The packet body is:

```text
u8     opcode          0x4A
u8     mode            activation requires 0
u8     marker_byte     written to byte 0 of the marker file
u32be  guard           activation requires 0x7D3AFF99
```

The deserializer at `0x597AC0` stores these payload fields at packet offsets `+0x10`, `+0x11`, and `+0x14`.

If `mode` is not zero or `guard` does not match, the handler returns success without changing local state.

## Persistent marker

The handler reconstructs the wide path `%SystemRoot%\System32\Mscfg.dll` from split strings. The nearby `yummy` and `rocks` strings are assigned to locals but are not used in the path. They appear to be decoys.

The handler opens the marker with `CREATE_ALWAYS`, read/write access, no sharing, and normal attributes. If creation succeeds, it:

1. Writes `marker_byte` as the first byte.
2. Seeks from the beginning to `0xDB72`.
3. Calls `SetEndOfFile`, producing a file length of `0xDB72` bytes.
4. Calls `memset(NULL, 0, 100)`, causing an access violation.

If file creation fails, the alternate branch writes zero to address `0`. The packet therefore crashes the process whether or not the marker can be persisted.

The logical location comes from `GetSystemDirectoryW`. Permissions, WOW64 redirection, and legacy file virtualization can affect the physical location on newer Windows versions. Both the writer and startup check reconstruct the same logical path.

`config_detect_bad_guy_marker` at `0x431ED0` reconstructs the same path during client configuration construction. It uses `_waccess(path, 0)` as an existence check and sets configuration byte `+0x668` to `1` when the file exists. The marker contents are not read by this check.

## Endpoint change

`config_init_dark_ages_endpoint_and_install_ids` at `0x433380` resolves `da0.kru.com` and selects a base TCP port:

| Marker state | Base port |
|---|---:|
| Absent | `2610` (`0x0A32`) |
| Present | `2601` (`0x0A29`) |

`net_connect_and_initialize_transport` at `0x565210` reads the same marker flag when creating the socket address. Its fallback connection path repeats the `2601` versus `2610` selection. The effective port also includes the signed configuration offset at `config + 0x436`, which is normally zero in this path.

This makes the marker visible to the service through endpoint selection even before the normal login packet could be submitted.

## Login kill switch

`net_send_c_login` at `0x4BAA80` checks `config + 0x668` before building opcode `0x03`. When the marker is present, it calls `memset(NULL, 0, 100)`. The call to `net_submit_client_packet` at `0x4BB00B` is therefore unreachable in a normal marked process.

The marker bit is not serialized as a field in `CLogin`. The client crashes before sending that packet.

## Registry installation identifiers

The client also maintains two installation identifiers. These are separate from the marker-file flag:

| Registry location | Value | Local use |
|---|---|---|
| `HKCR\NXKRI.Ctrl.1` | `CLSID`, `REG_DWORD` | Primary random 32-bit installation identifier at `config + 0x424` |
| `HKCR\KRIHC.Ctrl.1` | `CLSID`, `REG_DWORD` | Obfuscated derivative decoded to 16 bits at `config + 0x428` |

If the primary value is absent or invalid, the client generates four bytes with `rand()` and stores them. `config_derive_install_id_checksum16` at `0x436E10` derives the 16-bit value with a custom recurrence and a `0x1021` lookup table. The second registry value stores that result with random padding and a byte-wise XOR using `0xAC`, `0xAD`, `0xAE`, and `0xAF`.

`net_send_c_login` loads the primary 32-bit identifier and the derived 16-bit identifier, applies additional per-login obfuscation, and writes them into `CLogin` as `u32be` and `u16be` fields. These values behave like an installation fingerprint, not the persistent ban flag itself.

See [Client installation identifier](client-installation-id.md) for the exact registry validation, secondary-value packing, per-login XOR masks, and integrity recurrence.

## Conclusions

| Claim | Client evidence |
|---|---|
| `SBadGuy` deliberately crashes the client | Confirmed on both marker creation success and failure paths |
| The effect persists across launches | Confirmed when marker creation succeeds, through the `Mscfg.dll` existence check |
| A marked installation uses another endpoint | Confirmed, port `2601` replaces `2610` |
| A marked installation crashes during login | Confirmed before `CLogin` submission |
| Registry identifiers are sent during login | Confirmed after local obfuscation |
| The registry identifiers are the ban flag | Not supported; the file-existence byte at `config + 0x668` is the kill-switch flag |
| GMs are the source of the packet | Not provable from the client binary |
