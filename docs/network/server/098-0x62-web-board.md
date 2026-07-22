# Web Board (`SWebBoard`)

`SWebBoard` supplies URLs and board-session data to one of the client's embedded Internet Explorer controls. It does not create a pane by itself. The matching `BrowserDialogPane` or `BrowserGameControlPane` must already be active to consume it.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x62` (98) |
| Encoding | startup key |
| Name provenance | Exact Microsoft C++ RTTI class `SWebBoard` |
| Known owners | `BrowserDialogPane`, `MiniGame::BrowserGameControlPane` |
| Client response | None after the response is applied |

## Body

```text
packet SWebBoard {
    u8 opcode                              // 0x62
    u8 action

    if action == 3 {
        string8 start_url
    } else {
        string8 base_url
        string8 start_url
    }

    string8 board_data
}
```

Each string is stored in its own 256-byte packet-object buffer. For action `3`, the client derives `base_url` from `start_url` by retaining the scheme and authority and removing the path. For example, `http://host/path` produces `http://host`.

## When it is sent

The confirmed flow is request and response:

```text
embedded browser pane opens
  -> client sends CWebBoard 0x73
  -> server sends SWebBoard 0x62
  -> existing browser control navigates
```

The active action `3` requests come from in-game web-backed views. Confirmed owners include `Puzzle::RankingState`, `RopeSkipping::RankingState`, and `FindFarmpetPane`. They send [`CWebBoard`](../client/115-0x73-web-board.md) with two one-byte selectors and wait for a URL response. This is distinct from the front-end [`SBrowser`](102-0x66-browser.md) flow.

`BrowserDialogPane` contains a second request path for action `0`, with a 20-second timeout. No normal constructor caller for that dialog has been identified in the matching executable, so its availability through the stock UI remains unconfirmed.

## Actions and effects

| Action | Consumer | Effect |
| --- | --- | --- |
| `0` | `BrowserDialogPane` | Cancel request timer, install two cookies, save the base URL, and navigate to `start_url` |
| `1` | `BrowserDialogPane` | Same behavior as action `0`; no matching client request builder is known |
| `2` | None found | Parsed using the explicit-URL form, but neither known handler accepts it |
| `3` | `BrowserGameControlPane` | Derive the base URL and navigate to `start_url + "?" + board_data` |
| Other | None found | Parsed using the explicit-URL form, then ignored by the known handlers |

### Actions 0 and 1

`BrowserDialogPane` cancels timer `0x572` as soon as the packet arrives. It then accepts only actions `0` and `1`.

`board_data` must contain an equals sign followed later by an ampersand:

```text
anything=<domain-cookie-value>&<boardinfo-cookie-value>
```

The client ignores the text before `=`. It installs the bytes between `=` and `&` as the WinINet cookie named `domain`. It percent-encodes the remaining bytes and installs them as the cookie named `boardinfo`. Both cookies use `base_url`, after which the embedded browser navigates to `start_url`.

An unreferenced alternate helper performs the same action directly from a raw decoded buffer. It reads three one-byte-length strings, splits `board_data` the same way, installs the same cookies, and navigates the same embedded control. No caller reaches this older path in the analyzed client, so the RTTI-backed packet-object handler above remains the confirmed live implementation.

The delimiter searches use wrapping eight-bit indexes. If either `=` or `&` is absent, the client loops indefinitely. Manually injected action `0` or `1` packets must include both delimiters.

### Action 3

`BrowserGameControlPane` accepts only action `3`. If its embedded `BrowserWindow` exists, the handler:

1. stores the parser-derived base URL in the browser control;
2. builds `start_url + "?" + board_data`; and
3. asks the browser to navigate there with no additional header.

The client always appends `?`; it does not check whether `start_url` already has a query string. This path creates no timer, cookie, or persistent character state.

`BrowserWindow` is a small local ActiveX host around Internet Explorer's `IWebBrowser2`. It keeps the child window hidden until the matching document-complete event, intercepts `javascript:close();`, rejects `res://` navigation, and can reject HTTP navigation outside the saved base URL. Its document-host interfaces suppress the browser's default context menu and message UI, while a temporary message filter forwards keyboard input to the active browser object.

## Plaintext action 3 example

This example carries `http://127.0.0.1/` and `probe=1`:

```text
62 03 11 68 74 74 70 3A 2F 2F 31 32 37 2E 30 2E 30 2E 31 2F 07 70 72 6F 62 65 3D 31
```

With an active `BrowserGameControlPane`, the client derives base URL `http://127.0.0.1` and navigates to:

```text
http://127.0.0.1/?probe=1
```

The body still needs the normal static server-to-client transform, sequence, trailer, and outer frame. Sending it without the matching browser pane active produces no visible browser action.

## Known limits

- The two action `3` request selectors are confirmed fields, but their common meanings across all owners remain unresolved.
- No normal stock-UI opener for `BrowserDialogPane` has been identified.
- The client proves how it uses the supplied strings, not when the original server elected to return each URL.
