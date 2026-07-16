# Sound Effect (`SSoundEffect`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x19` (25) |
| Encoding | derived key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server uses this packet for sound effects and music changes. The first payload byte selects the form.

The constructor calls `net_server_packet_base_ctor` with opcode `0x19` and installs the `SSoundEffect` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SSoundEffect {
    u8 opcode                 // 0x19
    u8 command

    if command == 0xFF {
        u8 music_id            // 0..99 selects a track, 100 means no change
    } else {
        // command is the numeric sound-effect ID
    }
}
```

## Handling

`net_server_sound_effect_deserialize` reads the command byte and reads `music_id` only for command `0xFF`.

`audio_handle_sound_effect_packet` then follows one of two paths:

- `command < 0xFF` calls `audio_play_sound_effect(command)`.
- `command == 0xFF` and `music_id != 100` builds `.\music\<music_id>.mp3` and calls `audio_play_music_path`.
- `command == 0xFF` and `music_id == 100` leaves the current music unchanged. It does not stop it.

The music file callback changes the logical `.mp3` extension to `.mus` when opening the loose file. See [Audio system](../../audio/README.md) for the mixer, asset, and fade paths.

No paired client packet is required for this command.
