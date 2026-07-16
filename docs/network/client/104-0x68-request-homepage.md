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
    u8 terminator;             // 0, appended by net_submit_client_packet
}
```

The builder supplies `68 01`. The common submission layer appends the transmitted zero, so the plaintext entering the static transform is `68 01 00`. The supplied decoded trace omits this common terminator.
