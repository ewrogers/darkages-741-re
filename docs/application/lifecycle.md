# Application lifecycle

The client follows a small Windows game lifecycle. It prepares its settings, opens the first screen, runs the game loop, and then cleans up.

```text
launch
  |
  +-- prepare working directory and settings
  +-- check for another client
  +-- create the game window and core systems
  +-- play the intro sequence
  +-- enter the game loop
  +-- close handles and exit
```

The names below can be searched in Binary Ninja. Addresses and confidence notes live in the [function reference](../appendix/functions.md).

## Startup

`app_winmain` is the main entry point. Its early work includes:

1. `app_set_working_directory_from_executable` makes relative file paths start beside the executable.
2. `app_parse_command_line` handles the active command-line options.
3. `app_config_ctor` builds the client configuration, including the first server endpoint.
4. `startup_run_pending_patcher` checks for a completed patch handoff.
5. A named Windows mutex checks whether another client is already running.
6. The window, renderer, audio, input, pane, and network objects are prepared.
7. `event_handle_intro_state` starts the opening sequence.

The large `app_initialize` routine owns step 6. It starts Winsock, registers and creates the main window, opens the required archives, then constructs the core managers and panes in dependency order. If any required stage fails, `app_initialize_failure_cleanup` walks the completed stages in reverse, deletes each registered singleton, closes the archives, destroys the partial window, and unregisters its window class.

Win32 activation remains separate from construction. `app_set_active` applies the configured process-priority override while inactive, restores the saved priority when active, forwards the state to the video system, and invalidates the root pane after reactivation. Window move and size messages update the DirectDraw presentation origin only in windowed mode.

The mutex is named `Nexon.SingleInstance`. If Windows reports that it already exists, the original client exits. This is only a local guard. It does not change any account or server rules.

## Patch handoff

The lobby can notify this client about an update through [`SVersionCheck`](../network/server/000-0x00-version-check.md) subtype `2`. The client writes the supplied version and file-list data to `Patch/Info`, launches `Patcher2.exe`, and exits. This happens directly from the version response and does not require the separate `CRequestPatch` and `SSendPatch` opcodes.

Startup provides a recovery path for a handoff that has progressed far enough to contain both `Patch/Info` and `Patch/Script`. When both files exist, `startup_run_pending_patcher` launches `Patcher2.exe` and exits before the normal client starts. If only one marker exists, the client deletes both and continues. The patcher's own download and update behavior is outside this analysis.

## Intro sequence

The intro is a three-state sequence:

```text
state 0 -> request the intro
state 1 -> play CIf.bik, then CIb.bik
state 2 -> continue into the normal client
```

`event_handle_intro_state` owns the state change. `ui_intro_video_begin_sequence` opens the clips, while `event_intro_video_frame_timer` advances and closes them.

Keyboard or pointer input moves the next-frame deadline to the current time, so the sequence advances immediately on the next timer pass. Destroying the RTTI-backed `CIPane` unregisters it from the pane tree, clears its singleton slot, and releases both archive resources.

This is useful because a launcher can skip the video cleanly by starting at state 2. It avoids changing the shared video player or leaving the intro pane half-open. The exact runtime patch is in [Skip the intro](../appendix/runtime-patches/skip-intro.md).

## Shutdown

When the game loop returns, the client tears down panes and event objects first. The same small `has`, `get`, and `destroy` helpers make each singleton cleanup conditional and preserve reverse construction order. Audio stops its samples, cancels its music timer, closes its stream, and shuts down Miles. The client also releases the tile-remapping tables, image and map-tile libraries, shuts down the video system, deletes it, and releases DirectDraw. The single-instance mutex is closed before the process exits.

The login server can also save a deferred [`SAdvertisement`](../network/server/091-0x5b-advertisement.md) command. When its saved string is nonempty, `app_winmain` performs the full shutdown first and then tries to launch `ad.exe` with that string and three numeric arguments. The separate program is not present in the matching local installation, and the client ignores launch failure.

The renderer-specific order is covered in [Renderer lifecycle](../rendering/lifecycle.md).
The audio-specific order is covered in [Audio lifecycle](../audio/lifecycle.md).

## Related pages

- [Configuration](configuration.md)
- [Game loop](game-loop.md)
- [Event system](../systems/events.md)
- [Audio system](../audio/README.md)
- [Runtime patches](../appendix/runtime-patches.md)
