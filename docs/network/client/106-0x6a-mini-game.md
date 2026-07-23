# Mini Game (`CMiniGame`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x6A` (106) |
| Encoding | derived |
| Name provenance | Related class vocabulary matched to locally confirmed builders and mini-game RTTI |

## Purpose

The client sends this packet for mini-game lifecycle and interaction traffic. The locally confirmed builders emit actions `5`, `6`, `7`, and `8`.

## Actions

| Value | Client behavior |
| ---: | --- |
| `5` | Sent when `MiniGame::AbstractGame` or `FindFarmpet::FindFarmpetPane` closes. |
| `6` | Sends one game value and a counted text value from mini-game controls. |
| `7` | Sends a client-generated nonzero `u32` counter used by mini-game play paths. |
| `8` | Reports the locally calculated fishing result as subtype `2`, a success flag, and a reserved zero byte. |

No local builder for actions `0` through `4` was found.

## Body

```text
packet CMiniGame {
    u8      opcode                    // 0x6A
    u8      action

    if action == 6 {
        u8      game_value
        string8 text
    }

    if action == 7 {
        u32     request_id
    }

    if action == 8 {
        u8      subtype               // locally built as 2
        u8      flag
        u8      reserved_zero
    }
}
```

Action `5` has no payload after the action byte. The common submission path adds its normal transmitted terminator outside the builder's logical body length.

The action `7` builder changes a zero counter to one before sending and increments it again afterward. The exact server-side meaning of that counter remains unresolved.

For action `8`, `flag` is `1` after a successful local fishing catch and `0` after a miss, cancellation, or invalid starting position. The observed plaintext bodies are:

| Plaintext body | Client result |
| --- | --- |
| `6A 08 02 01 00` | Fishing success |
| `6A 08 02 00 00` | Fishing failure |

`FishingDialogPane` does not submit the packet directly. Its destructor notifies the world pane through timer selector `0x0B`, and the world pane builds this response from the dialog's completion state.

## Paired server packet

[`SMiniGame`](../server/100-0x64-mini-game.md) action `4` opens Rope Skipping, Puzzle, or Find Farmpet. Its action `7` carries the two-value update consumed by active Find Farmpet and Puzzle play panes. Action `8`, subtype `1`, requests the local fishing dialog.

## Known limits

The field layouts above come from all five local opcode `0x6A` write sites. Names such as `game_value`, `request_id`, and `flag` describe their client use; server behavior is not yet available to show whether it independently validates the fishing result.
