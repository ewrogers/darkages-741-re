# Initial connection

The client uses a blocking TCP connection during startup. After it connects, Windows notifies the game window when data arrives or the socket closes.

Endpoint selection begins in [Configuration](../application/configuration.md). This page starts with the chosen IPv4 address and port.

## Happy path

`net_open_transport` selects the normal TCP transport. `net_connect_and_initialize_transport` then:

1. Starts Winsock 1.1.
2. Creates an IPv4 stream socket.
3. Sets the send buffer to 16,384 bytes.
4. Calls `connect` with the selected address and port.
5. Registers `FD_READ` and `FD_CLOSE` notifications with the game window.

The connection function does not send a distribution-specific handshake in the active mode. Login and version messages are handled later by the packet system.

## Bootstrap and lobby connections

The live 7.41 exchange reaches the main create-or-login screen in two connections. The bootstrap endpoint confirms the client and selects a server record. It then transfers the client to the lobby connection, where the main-menu data is prepared.

| Order | Direction | Plain body | Result |
| --- | --- | --- | --- |
| 1 | Server | [`SHello`](server/126-0x7e-hello.md) `7E 1B "CONNECTED SERVER\n"` | `ESC C` enables binary framing |
| 2 | Client | [`CHello`](client/098-0x62-hello.md) `62 61 72 61 6D 00` | Replies to the terminal-style welcome using the static transform |
| 3 | Client | [`CVersion`](client/000-0x00-version.md) `00 02 E5 4C 4B 00` | Reports version 741 and fixed `L`, `K` bytes |
| 4 | Server | [`SVersionCheck`](server/000-0x00-version-check.md) subtype `0` | Supplies configuration CRC, seed-table selector `2`, and a nine-byte static key |
| 5 | Client | [`CMulti`](client/087-0x57-multi-server.md) `57 00 00 00 00` | Selects the only local server record, ID `0` |
| 6 | Server | [`STransferServer`](server/003-0x03-transfer-server.md) | Supplies `127.0.0.1:2610` and a 27-byte handoff token |
| 7 | Client | [`CTransferServer`](client/016-0x10-transfer-server.md) | Reconnects, echoes the token, and appends `00` |
| 8 | Server | [`SStipulation`](server/096-0x60-stipulation.md) mode `0` | Checks the local greeting with CRC32 `0xE5DC1439` |
| 9 | Client | [`CRequestHomepage`](client/104-0x68-request-homepage.md) `68 01 00` | Requests the homepage because it is not cached yet |
| 10 | Server | [`SBrowser`](server/102-0x66-browser.md) subtype `3` | Caches `http://www.darkages.com` as the homepage URL |

This table shows the complete plaintext bodies queued by the 7.41 client. It omits the `AA + u16be size` frame and transform sequence or trailer bytes. Most builders do not count the final zero themselves; `net_submit_client_packet` appends it and includes it in the sent length. The supplied decoded trace strips this common terminator from some transformed packets, while the raw `CHello` frame preserves enough length information to prove it is present.

## Lobby role

The destination of the bootstrap transfer is the lobby or login server. It owns the main menu and account work rather than the live game world. Confirmed client paths on this connection include character creation, login, password changes, the stipulation check, and homepage discovery. A successful login can use another `STransferServer` and `CTransferServer` exchange to move the authenticated character to a game server.

Character creation is a two-request exchange on this connection. See [Character creation](../systems/character-creation.md) for the `CNewUser`, `SNewUserCheck`, and `CNewUserAppearance` flow.

## Retry path

If the first `connect` fails, the client resolves `da0.kru.com` again, creates a fresh socket, and tries once more. A new lookup can pick up a changed DNS address.

This means the built-in behavior is not strictly "connect to the configured address or fail." A runtime launcher that supplies a custom endpoint may also disable this fallback. See [Runtime patches](../appendix/runtime-patches.md).

## Failure behavior

| Failure | Result |
| --- | --- |
| Winsock 1.1 is unavailable | Exit the process |
| First socket creation fails | Build a network error and enter the fatal error path |
| First connection fails | Resolve the official host and try once more |
| Fresh name lookup fails | Exit the process |
| Second socket creation fails | Clean up and return disconnected |
| Second connection fails | Close the socket and return disconnected |
| Window notification setup fails | Exit the process |

If the second connection succeeds, a one-time path may save the selected address and port in `iplookup.tbl`. Failure to open that file shows a damaged-file message and exits.

The `mServer.tbl` rotation code belongs to other distribution modes. The active mode does not use it.

## Connected state

On success, the socket is stored in the network object and packet state is initialized. Later reads arrive through the window message path and enter `net_receive_pending_data`.

On normal failure, `net_close_socket` closes the handle and stores `INVALID_SOCKET`. Packet code should treat that value as disconnected.

Addresses and confidence notes are in the [function reference](../appendix/functions.md).
