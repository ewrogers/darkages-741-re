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
