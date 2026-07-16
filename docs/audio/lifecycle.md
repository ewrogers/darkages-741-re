# Audio lifecycle

Audio starts with the other core game systems and shuts down in the reverse order. A failed audio driver does not stop the client from running. Playback calls simply have no driver to use.

## Startup

`audio_sound_manager_ctor` creates the `SoundManager` singleton and its Miles driver wrapper. `audio_miles_driver_ctor` then:

1. Sets the Miles redistributable directory to `.\music`.
2. Starts Miles.
3. Requests a 22,050 Hz, 16-bit, stereo digital driver.
4. Retries with default driver flags if the first open fails.
5. Shuts Miles down if both attempts fail.

`audio_sound_manager_initialize` creates the two active players after that:

- `SndEffectPlayer` receives the shared digital driver and starts an empty effect cache.
- `BGMPlayer` receives the same driver, installs its file callbacks, and starts with no open stream.

The Bink video player also passes this digital driver to `BinkOpenMiles`. Intro video sound therefore joins the same Miles output instead of opening a second game mixer.

## Normal shutdown

`audio_sound_manager_dtor` calls `audio_destroy_players` before releasing Miles:

```text
stop and release every sound-effect handle
cancel the music fade timer
pause and close the music stream
delete both players
close the Miles digital driver
call Miles shutdown
clear the audio singletons
```

Canceling the music timer before closing its stream matters. It prevents a later timer event from touching a deleted player.

The application-level order is covered in [Application lifecycle](../application/lifecycle.md).
