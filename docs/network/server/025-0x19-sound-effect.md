# Sound Effect (`SSoundEffect`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x19` (25) |
| Encoding | derived |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server uses this packet either to play one sound effect or to select background music. The first body byte chooses the form.

The constructor passes opcode `0x19` to the server packet base and installs the exact `SSoundEffect` vtable.

## Body

```text
packet SSoundEffect {
    u8      opcode                    // 0x19
    u8      sound

    if sound == 0xFF {
        u8      track
    }
}
```

`net_deserialize_sound_effect_server_packet` consumes only one byte for a sound effect and two bytes for the `0xFF` music form. Some server implementations may append another `u16`, but version 741 does not read it. It is not part of the client-confirmed body.

## Handling

`audio_handle_sound_effect_packet` follows these rules:

- Values `0x00` through `0xFE` play the matching one-shot sound ID. The sound loader tries `<id>.mp3` in `Legend.dat`, then `<id>.wav` when the MP3 entry is absent.
- `sound == 0xFF` and `track != 100` selects `.\music\<track>.mp3`.
- `sound == 0xFF` and `track == 100` leaves the current music unchanged.

The music file callback changes the logical `.mp3` extension to `.mus` when it opens the loose file. A new track uses the normal fade-out and fade-in path.

Track `100` is a no-op, not a stop command. The client has separate functions for stopping music and sound effects, but this packet handler does not call them. No other stop sentinel appears in this path.

See [Audio system](../../audio/README.md) for asset lookup, mixing, and fades. No paired client packet is required.
