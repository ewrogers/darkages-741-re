# MIDI support

Standard MIDI support is still compiled into the client, but it is not part of the active audio path for the matching assets.

The evidence is clear:

- RTTI contains a `MidiPlayer` class derived from `Pane`.
- The client imports the Windows `midiStream*` and `midiOut*` APIs.
- `audio_midi_parse_smf` checks standard `MThd` and `MTrk` chunks.
- The stream callback fills two 1,024-byte buffers and sends MIDI events to Windows.
- MIDI channel volume uses controller 7. A separate master value scales each channel.

The missing live path is equally important:

- `audio_midi_play_file` has no static callers.
- `audio_midi_set_master_volume` has no static callers.
- The executable contains no `.mid` path string.
- No local archive entry or loose asset has a MIDI header.

This means the code could parse and stream a standard MIDI file, but the current game flow and asset set do not use it. Calling the dormant code from an injection would require more lifetime and error-path testing.

The numbered `.mus` files are unrelated to this MIDI engine. They are MP3 files played by `BGMPlayer` through Miles. See [Music](music.md).
