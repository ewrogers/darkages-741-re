# Web Board (`CWebBoard`)

`CWebBoard` asks the server for URL and session data used by an embedded browser pane. The response is [`SWebBoard`](../server/098-0x62-web-board.md).

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x73` (115) |
| Encoding | startup key |
| Name provenance | Related class vocabulary matched to locally confirmed builder behavior |

## Body

```text
packet CWebBoard {
    u8 opcode                              // 0x73
    u8 action

    if action == 3 {
        u8 selector_1
        u8 selector_2
    }
}
```

Only actions `0` and `3` are constructed by this client.

## Action 0

`BrowserDialogPane` sends the exact body `73 00` when constructed without already supplied web-board data or a starting URL. It then schedules timer `0x572` for 20,000 ms. Receipt of any `SWebBoard` cancels that timer; otherwise the timer opens a `Web Board Request Timeout` alert and closes the waiting dialog.

The matching executable contains this dialog and request path, but no normal constructor caller has been identified. Treat its stock-UI availability as unresolved.

## Action 3

`net_send_web_board_game_request` sends:

```text
73 03 <selector_1> <selector_2>
```

Confirmed callers are web-backed in-game views associated with `Puzzle::RankingState`, `RopeSkipping::RankingState`, and `FindFarmpetPane`. Their selector sources differ, so the shared meanings of the two bytes remain unresolved. This request does not start a timeout timer.

The server responds with `SWebBoard` action `3`, which supplies a start URL and query data for the already active `BrowserGameControlPane`.
