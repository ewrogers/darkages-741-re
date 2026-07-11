# Client startup

The client enters its own code at `startup_win_main` (`0x57A710`). The normal path creates one Win32 window, opens the required resource archives, initializes Miles audio, reads client configuration, initializes DirectDraw, then constructs the remaining UI and game systems.

## WinMain sequence

`startup_win_main` performs these steps in order:

1. If `check.nfo` exists, write a binary `lod.bin` table through `sub_42F0A0` (`0x42F0A0`) and exit. The table contains repeated `u32` addresses and `u16` values. Its exact purpose is still provisional.
2. Scan the `lpCmdLine` text with `startup_parse_dash_options` (`0x57A550`).
3. Check for a pending patch with `startup_run_pending_patcher` (`0x57A330`).
4. Create the named mutex `Nexon.SingleInstance`. A second instance exits immediately.
5. Read `HKCU\Software\KRU\Dark Ages\DisplayMode`. If it is absent, probe DirectDraw and write the selected mode back to the registry.
6. Call `startup_initialize_client` (`0x4A9F80`).
7. On success, enter the application loop at `sub_4AC750` and later shut down through `sub_4AC060`.
8. If the post-game advertisement fields are set, launch `ad.exe` with the recorded arguments.

The base logical resolution is 640 by 480. `render_detect_display_mode` (`0x57A640`) accepts 16-bit or 32-bit desktop modes. It returns mode 2 at 1280 by 960 or larger, mode 1 below that threshold, and mode 0 for an unsupported depth.

## Command-line forms

There are two independent parsers.

### Dash options

`startup_parse_dash_options` scans space-delimited tokens beginning with `-`. Only uppercase `-D` is recognized. Its handler, `startup_handle_debug_option_stub` (`0x57A460`), is empty in this build. No other dash switch is supported by this parser.

### Bare endpoint arguments

`config_apply_command_line_endpoint_override` (`0x433010`) calls `GetCommandLineA` itself, skips the quoted or unquoted executable name, and treats the first bare argument as a hostname or dotted IPv4 address. A second argument is an optional port.

```text
Darkages.exe host.example.test 2610
Darkages.exe 192.0.2.10 2610
```

This parser is used by the default regional configuration and as the first choice in the Taiwan configuration. The `usa.nfo` path has its own `da0.kru.com` initializer, so a bare override is not proven to replace the normal US endpoint.

## Main initializer

The important order inside `startup_initialize_client` is:

| Address | Action |
|---:|---|
| `0x4A9FCF` | Start Winsock 1.1 and require an exact 1.1 result |
| `0x4AA001` | Capture timer baselines and a legacy Windows version label |
| `0x4AA010` | Register the window class with procedure `sub_4A9C30` |
| `0x4AA18B` / `0x4AA1CC` | Create the windowed or fullscreen-style window |
| `0x4AA229` | Adjust the process working set from physical memory size |
| `0x4AA22F` | Change the working directory to the executable directory |
| `0x4AA2F4` | Open the main and required secondary `.dat` archives |
| `0x4AAFB8` | Construct the Miles audio system |
| `0x4AB013` | Construct configuration from `Darkages.cfg` and region markers |
| `0x4AB05E` | Show the window |
| `0x4AB0F2` | Initialize DirectDraw and render surfaces |
| `0x4AB241` | Load `msg.tbl` from the national archive or disk |
| `0x4AB891` | Choose and load the regional profile |
| `0x4ABA61` | Load `Legend.pal` and finish the primary render setup |
| `0x4ABC3B` | Resolve the local hostname and mark a local `10.x.x.x` address |

`startup_set_working_directory_to_executable` (`0x4AD3A0`) parses the executable path from `GetCommandLineA`, removes the filename, and calls `SetCurrentDirectoryA`. Relative data, music, patch, and configuration paths therefore resolve beside the executable.

## Required archives

The main archive is `Legend.dat`, with `DarkAges.dat` as its only startup fallback. The remaining startup archives are required individually:

```text
misc.dat
seo.dat
khanpal.dat
khanmad.dat
khanmeh.dat
khanmim.dat
khanmns.dat
khanmtz.dat
khanwad.dat
khanweh.dat
khanwim.dat
khanwns.dat
khanwtz.dat
setoa.dat
national.dat
ia.dat
hades.dat
roh.dat
```

A missing required archive raises the client LOD exception and aborts startup. See [Fastfile archives](../file-formats/fastfile-archives.md) for the archive layout and transforms.

## Audio initialization

`audio_system_ctor` (`0x568F20`) allocates the Miles driver wrapper. `audio_initialize_miles_driver` (`0x5693F0`) then:

1. Sets the Miles redistribution directory to `.\music`.
2. Starts Miles Sound System.
3. Opens a digital driver at 22050 Hz, 16-bit, stereo.
4. Retries with its final driver flag changed from 1 to 0.
5. Calls `AIL_shutdown` if both attempts fail.

The client later uses Miles streams for MP3 playback and sample handles for effects such as WAV data.

## Video initialization

`render_initialize_video_system` (`0x593F30`) wraps `render_initialize_directdraw` (`0x4495D0`). The DirectDraw routine creates the interface, chooses cooperative and display modes, inspects the pixel masks, creates the primary surface, and records the supported 16-bit pixel format. Unsupported render modes cause startup to fail with a fatal display-mode message.

## Patch handoff

`startup_run_pending_patcher` checks both `Patch\Info` and `Patch\Script`. If both exist, it starts `Patcher2.exe` and exits the client. If the pair is incomplete, it deletes both marker files and continues normal startup.
