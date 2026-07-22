# Configuration

The client chooses most startup settings internally. The command line is much smaller than it first appears.

## Installation configuration

The configuration constructor calls `app_load_config_file`. A successful read keeps the parsed values. A missing or rejected file calls `app_set_default_config`. The constructor then saves the active configuration in either case, so an old file is normalized to the current layout.

`Darkages.cfg` is a versioned text file. Its fixed labels cover the transport selector, keyboard mode, telephone text, Korean and English font choices, four quoted endpoint pairs, chat mode, ground animation, and audio levels. Later game options are present only when the stored version is new enough. This is installation-wide state, not the per-character files described below.

The default builder selects the same distribution-specific endpoint tables used by startup and initializes the three saved audio levels to `3`.

## Active command line

The active parser in `app_parse_command_line` recognizes uppercase `-D`, but its handler does nothing in this build. No confirmed active flag changes the server address or port.

There is also a positional endpoint parser:

```text
Darkages.exe <host-or-ip> [port]
```

`net_parse_endpoint_override` can read this form, resolve a hostname, and store the address and port. The normal configuration path does not call it. The parser is dormant because `app_select_distribution_mode` always chooses distribution mode 1.

Changing the whole distribution mode would affect more than networking. A launcher should instead redirect only the endpoint setup call. See [Enable the positional endpoint parser](../appendix/runtime-patches/command-line-endpoint.md).

The executable also contains an older `.nfo` marker scanner and country- and ISP-specific endpoint integrations. They are not reached by this build's hardcoded selector. See [Distribution markers](distribution-markers.md).

`maybe_net_load_endpoint_from_command_file` is another unreferenced legacy path. It treats the text after the executable name as a filename, reads a host or dotted IPv4 address and port from that file, and updates `Config`. No caller reaches it in this executable, so it is not an alternate syntax supported by normal version-741 startup.

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

The [Good Guy runtime patch](../appendix/runtime-patches/ignore-bad-guy-marker.md) keeps the marker-present flag clear. It restores the normal endpoint and login path for later launches while leaving the file and installation IDs unchanged.

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

The second policy also disables the `da0.kru.com` fallback. Exact bytes and safety checks are kept in [Disable the official endpoint fallback](../appendix/runtime-patches/disable-endpoint-fallback.md).

## Connection results

On success, `net_connect_and_initialize_transport` stores the connected socket, initializes the packet state, and registers it with the client.

On failure, the socket is closed and reset to `INVALID_SOCKET`. Name lookup failure, connection failure, and socket setup failure take different branches, but none silently changes to an arbitrary endpoint.

See [Initial connection](../network/connection.md) for the network side of this flow.

## Per-character configuration

The client keeps several local conveniences separate for each character. When an in-game character becomes active, it creates a directory from that character's name and reads the character's spell lines, skill line, user lists, and text macros from that directory.

The path builder produces this form:

```text
.\<character-name>.\<filename>
```

The dot before the second backslash is part of the client path. Normal Win32 path handling removes the trailing dot from that directory component, so the directory normally appears on disk as `<character-name>`. These files belong to the local client. They are not server-synchronized character state.

| File | Contents |
| --- | --- |
| `SpellBook.cfg` | Up to ten timed chant lines for each named spell |
| `SkillBook.cfg` | One optional line for each named skill |
| `Familylist.cfg` | Twenty locally classified family or guild names |
| `Friendlist.cfg` | Twenty locally classified friend names |
| `Macro.cfg` | Ten numbered quick-text macros |

`Darkages.cfg` and `Legend.cfg` do not use this path. They remain installation-level configuration files beside the executable.

### Spell lines

`SpellBook.cfg` begins with a marker and then repeats one section per spell:

```text
SpellbookUsed
<spell name>
Spell0:<first line>
Spell1:<second line>
...
Spell9:<tenth line>
<next spell name>
...
```

The names between record groups are spell names, not character names. The character has already been selected by the directory.

`SpellDelayControlPane` finds the current spell's section and loads ten 256-byte runtime slots. It sends the configured lines through [`CSpellDelaySay`](../network/client/078-0x4e-spell-delay-say.md) at one-second intervals during the timed cast. A missing file or section leaves the slots empty.

### Skill lines

`SkillBook.cfg` uses the same section idea with one value per skill:

```text
SkillbookUsed
<skill name>
Skill:<configured line>
<next skill name>
Skill:<configured line>
```

When a skill passes its local activation checks, `SkillInvItemPane` loads the matching line. A nonempty value is sent once through `CSpellDelaySay` immediately before [`CUseSkill`](../network/client/062-0x3e-use-skill.md). This is separate from the server-controlled slot lock described in [Skill and spell action delays](../systems/action-delays.md).

### Family and friend lists

`Familylist.cfg` and `Friendlist.cfg` each contain exactly twenty lines. Each line is one character name, and unused entries are blank. The client keeps each entry in a 40-byte runtime slot, so a compatible file should keep a name within 39 bytes plus its terminating zero.

The stock reader does not split a line on commas and does not recognize a color suffix. A line such as `CharacterA,CharacterB` or `CharacterA#4` is one literal name and therefore will not match either character. The stock friend dialog also exposes exactly twenty text fields. Its commit path requests as many as 64 bytes from each field while writing into one of the 40-byte slots, so manually edited or pasted values must still remain within the 39-byte payload limit.

The project owner reports that playable character names are effectively limited to 13 characters. Separately, the Show Users packet path accepts a name of at most 24 bytes before discarding the row. These are different limits, and configuration storage is byte-oriented rather than Unicode-character-oriented.

These lists change how matching names appear in the online-user pane. A friend match uses palette index `0x80`; a family or guild match uses `0x24`. See [Show Users (`SShowUsers`)](../network/server/054-0x36-show-users.md) for the row-building behavior.

The fixed arrays cannot be enlarged by changing the loop bound. The family array begins immediately after the friend array, and the family array ends at the end of the containing `UserInfo` storage. The safe extension design keeps the stock files and dialog intact and adds a separate launcher-owned table. See [Extended friend highlights](../appendix/runtime-patches/extended-friend-highlights.md).

That runtime extension uses `Friendlist.ini` beside the stock per-character `Friendlist.cfg`. The client never reads or writes the INI file. A launcher parses its group, color, and member records and supplies the resulting lookup table.

### Text macros

`Macro.cfg` contains ten quoted records. Their file order follows the keyboard digits `1` through `9`, then `0`:

```text
Macro1: "<text>"
Macro2: "<text>"
...
Macro9: "<text>"
Macro0: "<text>"
```

Each macro has a 128-byte runtime slot. The reader looks for the next opening quote and copies until the next closing quote. It does not provide an escape form for a quote inside the value. If the file is absent, the client supplies ten built-in quick-text defaults.

### Text and save behavior

All five files contain ordinary byte strings. There is no binary header, encryption, or checksum. The Korean client expects ANSI text and treats Korean text as DBCS data, which normally means Windows code page 949 in its original environment.

The family, friend, and macro files use C text mode. Their writers therefore produce CRLF line endings on Windows. They are loaded when their shared manager is created and all records are written again when that manager is destroyed.

The spell and skill editors use binary mode and write LF line endings. They preserve other ability sections by copying the file through a working-directory `tmp.cfg`, deleting the old file, and renaming the temporary file. Their editor-side `%s` parsing also makes whitespace inside spell names, skill names, or configured lines unreliable. Manual changes are safest while the client is closed.

## Saved audio levels

`Darkages.cfg` stores `Sound Volume` and `Music Volume` as user levels. A new configuration starts both at `3`. The options pane limits them to `0` through `10`, while the audio manager multiplies each value by `20` before passing it to Miles.

See [Audio system](../audio/README.md) for playback and fade behavior.

## Saved game settings

Six rows in the Game Settings dialog belong to the client. They live in the global `AppConfig` object and are written to `Darkages.cfg` when the dialog closes normally. The current configuration format, version `0x2600`, saves all six keys.

The other seven rows are server-managed. Their `ON` or `OFF` text is returned through `SMessage` and is not copied into `AppConfig` or written to the local file.

See [Game settings](../systems/game-settings.md) for the memory fields, file keys, packet flow, and later consumers.
