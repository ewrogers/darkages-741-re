# Sound effects

Sound effects are short numbered MP3 files stored inside `Legend.dat`. The game keeps one Miles sample handle for each effect it has loaded.

## Lookup and cache

`audio_sfx_get_or_load` turns a numeric effect ID into a file name:

```text
<id>.mp3
```

It looks for that entry in `Legend.dat`. If no MP3 entry exists, it tries `<id>.wav`. The matching archive contains no WAV effects, but the fallback is still active code.

The cache is roughly:

```c
struct SoundEffectEntry {
    bool active;
    u16 id;
    MilesSample *sample;
    SoundEffectEntry *next;
};
```

Different IDs can play at the same time because they own different sample handles. Replaying the same ID reuses its existing handle instead of allocating another voice for that ID.

## Matching asset set

| Property | Result |
| --- | --- |
| Entries | 165 numeric MP3 files |
| ID range | 0 through 167, without 3, 118, or 119 |
| Sample rates | 11,025 through 44,100 Hz |
| Channels | 26 mono and 139 stereo |
| Bitrates | 16 through 320 kbit/s |
| Common bitrate | 64 kbit/s on 125 effects |
| Duration | About 0.12 through 14.37 seconds |

The archive stores the complete MP3 bytes. Miles receives the entry name, a pointer to those bytes, and the byte count.

## Playing and stopping

`audio_play_sound_effect` reaches `audio_sfx_play`, which loads or finds the handle, applies the shared sound-effect volume, and starts it. The manager can stop one ID or stop every cached handle.

The options pane exposes levels `0` through `10`. `audio_set_sound_volume_level` multiplies the level by `20` and immediately applies that value to every cached handle. New handles receive the same value when they are loaded. The default level is `3`, which becomes `60`.

Setting sound to zero also stops all current handles and clears a manager flag. That flag records the setting, but `audio_play_sound_effect` does not use it as a separate playback gate. The zero sample volume is what keeps later effects silent.

## Server trigger

The server can play an effect with [`SSoundEffect`](../network/server/025-0x19-sound-effect.md). A command byte below `0xFF` is passed directly to `audio_play_sound_effect` as the numeric ID.

Other local UI and gameplay paths also call the same manager function. This keeps packet-driven and local feedback sounds on the same cache and volume setting.
