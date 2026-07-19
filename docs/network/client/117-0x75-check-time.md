# Check Time (`CCheckTime`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x75` (117) |
| Transform | derived |
| Name provenance | Project-owner protocol vocabulary, confirmed by direct pairing with RTTI-backed `SCheckTime` |
| Builder | `net_send_check_time` |

## Purpose

The client sends `CCheckTime` only as the immediate response to [`SCheckTime`](../server/104-0x68-check-time.md). It returns the server's four-byte value unchanged and reports the current `timeGetTime()` tick count.

The client does not decide whether time is advancing correctly. It supplies the measurement; any comparison, tolerance, retry, or speed-hack response belongs to the server.

## Body

```text
packet CCheckTime {
    u8  opcode                    // 0x75
    u32 server_value             // copied unchanged from SCheckTime
    u32 client_tick_count        // timeGetTime()
}
```

All multibyte values use the normal packet big-endian encoding. The builder submits exactly nine meaningful plaintext bytes before the common encrypted-packet framing and trailer are applied.

## Timing behavior

`net_send_check_time` samples `timeGetTime()` once before writing the response. That API returns a 32-bit millisecond count that advances with Windows system uptime and wraps modulo `2^32`.

The response is built in the same main-thread network-event dispatch that handles `SCheckTime`. There is no client timer between request handling and sampling. Normal socket, event-queue, and frame-processing latency still contributes to when the server receives the response.

The responding dispatcher belongs to the gameplay `WorldPane`, so the confirmed pairing applies after the character has entered the world. No login-screen responder was found.

For two replies, a server can calculate:

```c
client_elapsed = second.client_tick_count - first.client_tick_count; // u32 wrap
server_elapsed = second_receive_time - first_receive_time;
```

A sustained disagreement could indicate a modified client clock or accelerated game processing, but that interpretation is an inference. The version 741 client contains only the reactive measurement path and reveals nothing about why the server sends a particular request.
