# Client packet send pipeline

Outgoing packets are assembled as an unframed body whose first byte is the CPacket opcode. Unlike SPackets, the client does not register outgoing RTTI-backed packet classes; most bodies are built inline at the action or UI call site.

## Pipeline

1. A builder writes the opcode and payload using helpers such as `net_write_u8`, `net_write_u16_be`, and `net_write_u32_be`.
2. `net_submit_client_packet` at `0x563E00` copies/owns the body and queues communications event 6.
3. The communications worker reaches `net_dispatch_communications_event` and calls `net_send_client_packet` at `0x5648A0`.
4. `net_send_client_packet` selects an opcode-dependent transform policy.
5. Binary mode writes `0xAA`, the transformed body size as `u16be`, and the transformed body, then calls Winsock `send`.

The size field counts the transformed body, including its opcode and any sequence/integrity trailer. It does not include the three framing bytes.

The logical length passed to `net_submit_client_packet` includes the opcode and excludes its local trailing zero. The function adds that sentinel itself. It is the preferred logical egress hook because monitoring, blocking, and replacement occur before wrapper, transform, and framing state. See [Hooks and injection](../event-proxy/hooks-and-injection.md#logical-cpacket-egress).

## Common transformation policy

- No common transform: `0x00`, `0x10`, `0x48`.
- Transform mode 0: `0x02`, `0x03`, `0x04`, `0x0B`, `0x26`, `0x2D`, `0x3A`, `0x42`, `0x43`, `0x4B`, `0x57`, `0x62`, `0x68`, `0x71`, `0x73`, `0x7B`.
- Default transform mode 1: all other opcodes reaching the sender.

`net_encrypt_client_packet_body` at `0x567FB0` preserves the opcode, inserts a rolling sequence byte, transforms the remaining payload, and appends integrity/key material.

## Outgoing sequence reset and the pre-version handshake

`net_reset_client_packet_sequence` at `0x563DE0` writes `0` to `net_client_packet_sequence`. The encryptor uses the current byte in the packet and then increments the shared byte, so the first encrypted packet after a reset carries sequence `0`, the next carries `1`, and so on with byte-sized wraparound.

The recovered startup path has this producer-side order:

1. Queue opcode `0x62`, whose complete pre-transform bytes spell the client codename `"baram"` (`0x62` + `"aram"`).
2. Call `net_reset_client_packet_sequence` at `0x57993A`.
3. Queue raw `0x00 CVersion`.

The `0x62` sender branch does not itself reset the counter. The surrounding handshake routine performs the reset after enqueueing it. `CVersion` is raw and therefore neither contains nor consumes a sequence byte.

Submission is asynchronous: `net_submit_client_packet` copies the body into communications event 6, `net_enqueue_communications_event` at `0x586210` releases the worker semaphore, and the producer continues without waiting. Consequently, the worker can encrypt queued `"baram"` after the producer has reset the shared counter. In that execution, `"baram"` carries sequence `0`, increments the counter to `1`, CVersion leaves it unchanged, and the next encrypted packet carries `1`. If `"baram"` is processed before the explicit reset, the next encrypted packet after CVersion instead carries `0`. A capture can distinguish the two by checking the sequence byte immediately following opcode `0x62`.

The exact XOR schedule, per-direction seed masks, MD5 integrity bytes, dialog wrapper, and CRC recurrence are documented in [Packet encryption, decryption, and CRC reconstruction](./packet-crypto-and-crc.md).

## Special 0x39 and 0x3A wrapper

Before the common worker-thread transformation, `net_submit_client_packet` wraps opcodes `0x39` and `0x3A` with random bytes, an encoded size, and a table-driven 16-bit checksum calculated by `net_calculate_dialog_crc16` at `0x568870`.

## Legacy text mode

The same sender contains an older text transport. It encodes body bytes into printable characters in chunks and emits lines beginning with `*` or `+`. This appears to coexist with the later binary `0xAA` framing for compatibility.

## Key IDA names

| Address | Name | Role |
|---:|---|---|
| `0x563E00` | `net_submit_client_packet` | Own/copy and queue a CPacket body |
| `0x563DE0` | `net_reset_client_packet_sequence` | Reset outgoing encrypted-packet sequence to zero |
| `0x5643D0` | `net_dispatch_communications_event` | Worker-thread event dispatcher |
| `0x5648A0` | `net_send_client_packet` | Transform, frame, and call `send` |
| `0x564140` | `net_write_u8` | Write one byte |
| `0x564160` | `net_write_u16_be` | Write a big-endian 16-bit integer |
| `0x5641F0` | `net_write_u32_be` | Write a big-endian 32-bit integer |
| `0x567FB0` | `net_encrypt_client_packet_body` | Common packet transform and trailer |
| `0x568870` | `net_calculate_dialog_crc16` | Special-wrapper checksum |
| `0x586210` | `net_enqueue_communications_event` | Add an asynchronous worker event and release its semaphore |
