# Audio system

The client sends music, sound effects, and video sound through one Miles digital driver. Miles decodes the files, mixes the active voices, and sends a 22,050 Hz, 16-bit, stereo stream to Windows.

```text
game and packet events
  |
  +-- SoundManager
        +-- SndEffectPlayer -> cached Miles sample handles
        +-- BGMPlayer       -> one Miles stream
        +-- Bink video      -> the same Miles driver
                              |
                              +-- Windows audio output
```

There is no separate PCM mixer in the client. The game chooses files, owns the volume rules, and schedules music fades. Miles performs the decode, resampling, and final mix.

## Choose a playback path

| Question | Start with | Then inspect |
| --- | --- | --- |
| How is audio initialized or stopped? | [Audio lifecycle](lifecycle.md) | Its driver setup, failure handling, and shutdown paths |
| How does a music change fade? | [Music](music.md) | The [fade timer](music.md#fade-timer) for cadence, step rule, and stream lifetime |
| How does a server message select a sound? | [Sound effects](sound-effects.md#server-trigger) | [SSoundEffect](../network/server/025-0x19-sound-effect.md) for effect and music selection, or [SDamageEffect](../network/server/019-0x13-damage-effect.md) for its sound field |

[MIDI support](midi.md) documents a separate compiled path. It should not be used as the starting point for playback from the matching assets.

## Main parts

| Part | Job |
| --- | --- |
| `SoundManager` | Gives the rest of the game one place to play and stop audio |
| `SndEffectPlayer` | Loads numbered effects from `Legend.dat` and caches them |
| `BGMPlayer` | Owns one looping music stream and its fade timer |
| `MidiPlayer` | Compiled standard MIDI path that is not used by the matching assets |

The active formats are MP3. Music uses loose numbered `.mus` files, while sound effects use numbered `.mp3` entries inside `Legend.dat`. The `.mus` extension is only a naming convention. It does not identify a different codec.

## Read next

- [Audio lifecycle](lifecycle.md) follows driver setup, failure handling, and shutdown.
- [Music](music.md) explains track selection, volume, and fades.
- [Sound effects](sound-effects.md) covers numbered assets and cached sample handles.
- [MIDI support](midi.md) separates compiled support from the active playback path.

Exact function addresses and confidence notes are in the [function reference](../appendix/functions.md) and [`audio.yaml`](../../analysis/exports/audio.yaml).
