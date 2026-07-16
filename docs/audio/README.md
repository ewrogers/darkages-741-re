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

## Main parts

| Part | Job |
| --- | --- |
| `SoundManager` | Gives the rest of the game one place to play and stop audio |
| `SndEffectPlayer` | Loads numbered effects from `Legend.dat` and caches them |
| `BGMPlayer` | Owns one looping music stream and its fade timer |
| `MidiPlayer` | Compiled standard MIDI path that is not used by the matching assets |

The active formats are MP3. Music uses loose numbered `.mus` files, while sound effects use numbered `.mp3` entries inside `Legend.dat`. The `.mus` extension is only a naming convention. It does not identify a different codec.

## Pages

- [Audio lifecycle](lifecycle.md)
- [Music](music.md)
- [Sound effects](sound-effects.md)
- [MIDI support](midi.md)

Exact function addresses and confidence notes are in the [function reference](../appendix/functions.md) and [`audio.yaml`](../../analysis/exports/audio.yaml).
