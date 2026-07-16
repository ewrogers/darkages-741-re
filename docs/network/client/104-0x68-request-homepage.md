# Request Homepage (`CRequestHomepage`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x68` (104) |
| Transform | `static` |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

The client asks the server for the homepage URL used by the main menu.

## Sent by

Both `SStipulation` handlers check the cached-homepage flag before processing the server greeting. If no URL has arrived yet, they call `net_send_request_homepage`. The paired reply is [`SBrowser`](../server/102-0x66-browser.md) subtype `3`.

## Body

```c
packet CRequestHomepage {
    u8 opcode;                 // 0x68
    u8 request_type;           // 1
}
```

The confirmed plaintext body is `68 01`.
