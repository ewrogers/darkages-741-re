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
4. A named Windows mutex checks whether another client is already running.
5. The window, renderer, audio, input, pane, and network objects are prepared.
6. `event_handle_intro_state` starts the opening sequence.

The mutex is named `Nexon.SingleInstance`. If Windows reports that it already exists, the original client exits. This is only a local guard. It does not change any account or server rules.

## Intro sequence

The intro is a three-state sequence:

```text
state 0 -> request the intro
state 1 -> play CIf.bik, then CIb.bik
state 2 -> continue into the normal client
```

`event_handle_intro_state` owns the state change. `ui_intro_video_begin_sequence` opens the clips, while `event_intro_video_frame_timer` advances and closes them.

This is useful because a launcher can skip the video cleanly by starting at state 2. It avoids changing the shared video player or leaving the intro pane half-open. The exact runtime patch is in [Runtime patches](../appendix/runtime-patches.md).

## Shutdown

When the game loop returns, the client tears down panes and event objects first. Audio stops its samples, cancels its music timer, closes its stream, and shuts down Miles. The client also releases the main image and map-tile libraries, shuts down the video system, deletes it, and releases DirectDraw. The single-instance mutex is closed before the process exits.

The renderer-specific order is covered in [Renderer lifecycle](../rendering/lifecycle.md).
The audio-specific order is covered in [Audio lifecycle](../audio/lifecycle.md).

## Related pages

- [Configuration](configuration.md)
- [Game loop](game-loop.md)
- [Event system](../systems/events.md)
- [Audio system](../audio/README.md)
- [Runtime patches](../appendix/runtime-patches.md)
