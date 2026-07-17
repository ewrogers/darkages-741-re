# Message (`SMessage`)

`SMessage` is the game's general text-delivery packet. Its type byte decides whether the same body becomes a short floating notice, a persistent history entry, a popup window, or score text.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x0A` (10) |
| Encoding | startup key |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SMessage {
    u8      opcode                    // 0x0A
    u8      message_type

    if message_type == 0x11 {
        u8      unknown_0
        u8      unknown_1
        string8 unknown_text
    }

    u16     message_length
    bytes   message[message_length]
}
```

The main message is counted with a two-byte big-endian length, not a `string8`. It does not carry a wire terminator. Display paths copy the bytes and add their own null terminator when they need one.

Text remains an ANSI or DBCS byte string. It is not Unicode. The normal formatted-text paths recognize the client's inline `{=<letter>` color codes.

## Type routing

Two client objects inspect this packet independently:

```text
SMessage
  |-- net_handle_message_server_packet
  |     |-- GameMessagePane floating overlay
  |     |-- WindowMessageDialogPane popup
  |     `-- ScorePane
  |
  `-- NewSystemMessagePane
        `-- persistent message history
```

| Type | Floating overlay | Persistent history | Other result |
| ---: | --- | --- | --- |
| `0x00` | Palette `0x58` | Yes | Appends a newline to the overlay |
| `0x01`, `0x02` | No | Yes | History only |
| `0x03` | White | Yes | Used for equipment and load notices in the supplied login capture |
| `0x04` through `0x06` | No | Yes | History only |
| `0x07` | No | No | Ignored by the recovered consumers |
| `0x08`, `0x09` | No | No | Open the same standard scrollable message popup |
| `0x0A` | No | No | Open the alternate `woodbk.epf` popup layout |
| `0x0B` | Palette `0x77` | Yes | Appends a newline to the overlay |
| `0x0C` | Palette `0x54` | Yes | Appends a newline to the overlay |
| `0x0D` through `0x10` | No | No | Ignored by the recovered consumers |
| `0x11` | No | No | Extra prefix is parsed, but no recovered consumer displays it |
| `0x12` | No | No | Append white text to `ScorePane` |
| Above `0x12` | No | No | Ignored |

Types `0x08`, `0x09`, and `0x0A` change tab bytes to carriage returns before opening the popup. Types `0x08` and `0x09` are behaviorally identical in this client. Their separate values may still matter to the server.

The exact channel names for `0x00`, `0x01`, `0x02`, `0x04` through `0x06`, `0x0B`, and `0x0C` are not present as client strings. Runtime captures are needed before calling any one of them whisper, guild, group, or world chat.

## Length limits

The wire field can describe up to 65,535 bytes, but each display target imposes a smaller practical limit.

| Destination | Accepted or safe message length | Behavior beyond it |
| --- | ---: | --- |
| Persistent history | 70 bytes | Entry is rejected |
| `ScorePane` | 70 bytes | Entry is rejected |
| Floating `GameMessagePane` | 130 bytes | No client clamp exists; a longer copy exceeds its local text buffer |
| Standard or alternate popup | 32,767 bytes | Length is treated as signed; larger values are not safely handled |
| Ignored types | No display limit | Message is parsed but not copied into these UI targets |

For types `0x00`, `0x03`, `0x0B`, and `0x0C`, a message from 71 through 130 bytes can appear in the floating overlay but will not be saved in persistent history. A server that wants both results should keep these messages at 70 bytes or fewer.

## Message history and NPC speech

`SMessage` has no separate save-to-history flag. The type itself determines whether `NewSystemMessagePane` accepts the text.

[`SSay`](013-0x0d-say.md) is a different packet. It attaches a speech balloon to a world object for three seconds and does not append that text to persistent history. The client therefore supports these server choices:

| Server traffic | Client result |
| --- | --- |
| `SSay` only | Temporary balloon, not saved |
| History-eligible `SMessage` only | Saved message; some types also enter the floating overlay |
| Both packets | World balloon and a saved copy |

This split explains how NPC speech can sometimes be logged without an `SSay` flag changing. A capture of the same NPC interaction in both modes would confirm whether the live server sends both packets or substitutes one for the other.

The persistent and floating buffers are described in [Messages and history](../../systems/messages-and-history.md).
