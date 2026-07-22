# Message (`SMessage`)

`SMessage` is the game's general text and prompt-delivery packet. Its type byte decides whether the same body becomes a short floating notice, a persistent history entry, a popup window, score text, or a two-button confirmation prompt.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x0A` (10) |
| Transform | static |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SMessage {
    u8      opcode                    // 0x0A
    u8      message_type

    if message_type == 0x11 {
        u8      dialog_value_0
        u8      dialog_value_1
        string8 value
    }

    string16 message
}
```

The main message is counted with a two-byte big-endian length, not a `string8`. It does not carry a wire terminator. Display paths copy the bytes and add their own null terminator when they need one.

Text remains an ANSI or DBCS byte string. It is not Unicode. The normal formatted-text paths recognize the client's inline `{=<letter>` color codes.

## Type routing

`PacketPreprocessor` receives the first chance to consume this packet. Messages that remain continue to the ordinary pane-tree consumers:

```text
SMessage
  |-- PacketPreprocessor
  |     `-- type 0x11: UserConfirmPane --> CConfirm
  |
  |-- net_handle_message_server_packet
  |     |-- GameMessagePane floating overlay
  |     |-- WindowMessageDialogPane popup
  |     `-- ScorePane
  |
  |-- NewSystemMessagePane
  |     `-- persistent message history
  |
  |-- NewChattingPane / NewChatting2Pane
  |     `-- embedded ChattingPane styled text buffer
  |
  `-- GameSettingDialog
        `-- type 0x07 setting-row updates
```

| Type | Floating overlay | Persistent history | Other result |
| ---: | --- | --- | --- |
| `0x00` | Palette `0x58` | Yes | Appends a newline to the overlay |
| `0x01`, `0x02` | No | Yes | History only |
| `0x03` | White | Yes | Used for equipment and load notices in the supplied login capture |
| `0x04` through `0x06` | No | Yes | History only |
| `0x07` | No | No | Update `GameSettingDialog` while it is open |
| `0x08`, `0x09` | No | No | Open the same standard scrollable message popup |
| `0x0A` | No | No | Open the alternate `woodbk.epf` popup layout |
| `0x0B` | Palette `0x77` | Yes | Appends a newline to the overlay |
| `0x0C` | Palette `0x54` | Yes | Appends a newline to the overlay |
| `0x0D` through `0x10` | No | No | Ignored by the recovered consumers |
| `0x11` | No | No | Open `UserConfirmPane`; reply through `CConfirm` |
| `0x12` | No | No | Append white text to `ScorePane` |
| Above `0x12` | No | No | Ignored |

Types `0x08`, `0x09`, and `0x0A` change tab bytes to carriage returns before opening the popup. Types `0x08` and `0x09` are behaviorally identical in this client. Their separate values may still matter to the server.

The exact channel names for `0x00`, `0x01`, `0x02`, `0x04` through `0x06`, `0x0B`, and `0x0C` are not present as client strings. Runtime captures are needed before calling any one of them whisper, guild, group, or world chat.

## User confirmation prompt

Type `0x11` is intercepted by `PacketPreprocessor` before normal pane-tree delivery. It opens the exact RTTI class `UserConfirmPane`, an `AlertPane` with two buttons. The packet's main `message` becomes the visible prompt.

The three prefix values are retained as opaque reply context. Project-owner runtime testing confirms that OK sends [`CConfirm`](../client/049-0x31-confirm.md) with choice `1`, while Cancel sends choice `0`. Both replies echo `dialog_value_0`, `dialog_value_1`, and `value`, but do not echo the visible prompt.

This path has no client-side feature gate. Its absence from ordinary captures means the server did not send type `0x11` during those sessions, not that the client implementation is unreachable.

## Tell or whisper responses

[`CTell`](../client/025-0x19-tell.md) has no local echo or direct response handler. The sender only submits the packet. This supports `SMessage` as the matching generic route for an incoming whisper, sent-message confirmation, or delivery error, and no RTTI-backed `STell` class was recovered.

Static client code cannot identify which `message_type` the server chooses or prove that success and failure use the same value. A paired capture is still required before assigning the Whisper channel name to one type.

## Game settings response

Type `0x07` uses the normal counted `message` bytes as a small text protocol for `GameSettingDialog`:

```text
full list:    "0" + row_1 + TAB + row_2 + TAB + ...
single row:   ASCII setting digit + replacement row text
```

The supplied full-list capture declares `message_length = 0x00B0` and begins with ASCII `0`. After removing that byte, the client splits eight row strings at tab bytes and assigns them to setting IDs 1 through 8. It consumes the row 7 token but deliberately leaves the client-managed row 7 text unchanged.

The single-row captures declare `message_length = 0x0016`. ASCII `1` selects row 1, and the remaining 21 bytes are displayed as either `Listen to whisper:OFF` or `Listen to whisper:ON `.

A supplied group-toggle capture confirms the same form for setting 2. The message begins with ASCII `2`, followed by either `Join a group     :OFF` or `Join a group     :ON `. This refreshes the row text when `GameSettingDialog` is open. The group button uses `SSelfLook.is_group_open` instead.

The parser treats ASCII `1` through `9` as single-row selectors. Any other first byte enters full-list mode; the observed list marker is ASCII `0`. The returned `ON` and `OFF` suffixes are not parsed as state. See [Game settings](../../systems/game-settings.md) for row ownership and persistence.

## Length limits

The wire field can describe up to 65,535 bytes, but each display target imposes a smaller practical limit.

| Destination | Accepted or safe message length | Behavior beyond it |
| --- | ---: | --- |
| Persistent history | 70 bytes | Entry is rejected |
| `ScorePane` | 70 bytes | Entry is rejected |
| Floating `GameMessagePane` | 130 bytes | No client clamp exists; a longer copy exceeds its local text buffer |
| Standard or alternate popup | 32,767 bytes | Length is treated as signed; larger values are not safely handled |
| Game Settings row | 63 bytes per copied row | The dialog uses a 64-byte temporary buffer without a local clamp |
| Ignored types | No display limit | Message is parsed but not copied into these UI targets |

For types `0x00`, `0x03`, `0x0B`, and `0x0C`, a message from 71 through 130 bytes can appear in the floating overlay but will not be saved in persistent history. A server that wants both results should keep these messages at 70 bytes or fewer.

## Message history and NPC speech

`SMessage` has no separate save-to-history flag. The type itself determines whether `NewSystemMessagePane` accepts the text. The embedded `ChattingPane` is a separate consumer: it accepts types `0x00`, `0x0B`, and `0x0C` and assigns palette indexes `0x58`, `0x77`, and `0x54` respectively.

[`SSay`](013-0x0d-say.md) is a different packet. Its world handler displays speech over a world object for three seconds. A separate `ChattingPane` consumer also retains Say and Shout text, while Chant remains world-only. None of these chat copies enters `NewSystemMessagePane` persistent history. The client therefore supports these server choices:

| Server traffic | Client result |
| --- | --- |
| Say or Shout `SSay` only | Temporary balloon plus chat-window text, not persistent history |
| Chant `SSay` only | Temporary world text, not saved |
| History-eligible `SMessage` only | Saved message; some types also enter the floating overlay |
| Both packets | World display, chat-window text when accepted, and a saved copy |

This split explains how NPC speech can sometimes be logged without an `SSay` flag changing. A capture of the same NPC interaction in both modes would confirm whether the live server sends both packets or substitutes one for the other.

The persistent and floating buffers are described in [Messages and history](../../systems/messages-and-history.md).
