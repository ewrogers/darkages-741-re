# Packet transforms

Packets use one of three modes. The command code selects the mode, and the client and server directions have different command lists.

| Book name | Internal name | Meaning |
| --- | --- | --- |
| None | Raw | Body is sent as written |
| Startup key | Static | Uses the current shared key |
| Session key | Derived | Builds a 9-byte key for this packet |

The startup key, session key, MD5 source, seed table, and sequence are separate pieces. They should not be treated as one generic encryption key.

## Client submission terminator

Most client packet builders pass only their meaningful opcode-first fields to `net_submit_client_packet`. For an ordinary body, this function copies those bytes, appends `0x00`, and increases the queued length by one. The zero is not merely spare C-string storage. It reaches `net_send_client_packet`, appears in raw frames, and is encrypted as the final payload byte for static or derived packets.

For example, the `CHello` builder supplies five bytes, but the transform receives six:

```text
builder body:    62 61 72 61 6D
queued plaintext: 62 61 72 61 6D 00
```

The special CRC wrappers for opcodes `0x39` and `0x3A` follow their own construction path.

The client does not explain why this byte was included in the protocol. It is compatible with code that treats the end of a packet as a C string, and it may be a historical convenience, but the 7.41 receive code does not use it as a successful-decryption marker.

## Dialog-response inner wrapper

Only client opcodes `0x39` [`CMerchant`](client/057-0x39-merchant.md) and `0x3A` [`CPursuit`](client/058-0x3a-pursuit.md) enter this branch in `net_submit_client_packet`. It is an inner protection layer built before the ordinary command-selected transform.

Let `N` be the length of the original opcode-first builder body. Let `payload` be its `N - 1` bytes after the opcode. The inner wrapper has length `N + 7`:

```text
record DialogResponseInnerBody {
    u8 opcode
    u8 random_1
    u8 encoded_random_2
    u8 encoded_inner_length_high
    u8 encoded_inner_length_low
    bytes encrypted_inner[inner_length]
    u8 zero                              // literal 0
}
```

Construction is:

```text
random_1 = rand() & 0xFF
random_2 = rand() & 0xFF
inner_length = N + 1

encoded_random_2 = ((random_1 + 0xD3) & 0xFF) XOR random_2
encoded_inner_length_high = high(inner_length) XOR ((random_2 + 0x72) & 0xFF)
encoded_inner_length_low  = low(inner_length)  XOR ((random_2 + 0x73) & 0xFF)

plain_inner = big_endian_crc16(payload) + payload
key = (random_2 + 0x28) & 0xFF
for each byte in plain_inner
    encrypted_inner[i] = plain_inner[i] XOR key
    key = (key + 1) & 0xFF
```

The CRC is the client's [custom CRC16](checksums.md), initialized to zero and calculated over the original payload only. It does not include the opcode, random header, encoded length, or final zero.

A receiver can recover `random_2` directly:

```text
random_2 = encoded_random_2 XOR ((random_1 + 0xD3) & 0xFF)
```

It can then decode the two length bytes, reverse the incrementing XOR, split the first two plaintext bytes as the big-endian CRC, and verify the remaining payload.

The final zero is part of the inner body length. It is left clear by this construction step, then included when the complete wrapper passes through the outer static or derived transform. The copy routine writes scratch bytes beyond the meaningful inner segment, but they are not part of the transmitted body and must not be treated as fields.

The complete outgoing order is:

```text
CMerchant 0x39: builder body -> inner wrapper -> derived transform -> frame
CPursuit  0x3A: builder body -> inner wrapper -> static transform  -> frame
```

Sharing this inner wrapper does not make the outer transforms equal. The opcode still selects its ordinary transport mode after wrapping.

## Receive-side zero bytes

The server direction is not symmetric. Server bodies do not consistently carry a transmitted trailing zero. Captured packets such as `STransferServer`, `SStipulation`, and `SBrowser` end on meaningful nonzero field data.

`net_decrypt_server_packet` decrypts the complete transformed payload and returns the logical opcode-first body length. It then writes `0x00` immediately after that length in its local output buffer. `net_post_decoded_server_packet_event` does the same after copying the body into the queued event. These bytes make the in-memory buffers safe to inspect as terminated byte strings, but they are outside the packet length and are not protocol fields.

There is no check that the final decrypted payload byte equals zero. If the server does include a trailing zero inside its encrypted payload, that byte remains part of the returned body. `net_deserialize_server_packet` lets the concrete packet parser read its known fields and does not reject unread bytes at the end, so such a byte can simply remain unused.

Length-prefixed strings do not depend on either kind of trailing byte. The packet reader copies the declared string length and adds a zero to the destination buffer itself.

## Mode by direction

### Client to server

| Mode | Command codes |
| --- | --- |
| None | `0x00`, `0x10`, `0x48` |
| Startup key | `0x02`, `0x03`, `0x04`, `0x0B`, `0x26`, `0x2D`, `0x3A`, `0x42`, `0x43`, `0x4B`, `0x57`, `0x62`, `0x68`, `0x71`, `0x73`, `0x7B` |
| Session key | Every other command reaching `net_send_client_packet` |

### Server to client

| Mode | Command codes |
| --- | --- |
| None | `0x00`, `0x03`, `0x40` |
| Startup key | `0x01`, `0x02`, `0x0A`, `0x56`, `0x60`, `0x62`, `0x66`, `0x6F` |
| Session key | Every other command reaching `net_receive_frames` |

These are transport rules. They do not prove that every command has a packet class.

## Startup key

The built-in 9-byte key is:

```text
55 72 6B E5 6E 49 74 A3 49
 U  r  k  .  n  I  t  .  I
```

The constructor briefly builds this from the readable text `UrkcnItnI`. It replaces bytes 3 and 7 before expanding the key for the XOR loop. Later inspection of the source text can therefore be misleading.

The difference between the readable and working keys is itself a useful diagnostic:

```text
readable: 55 72 6B 63 6E 49 74 6E 49    "UrkcnItnI"
working:  55 72 6B E5 6E 49 74 A3 49
XOR:      00 00 00 86 00 00 00 CD 00
```

A supplied pre-login timeout capture had readable ASCII except for bytes altered by the repeating `0x86` and `0xCD` difference. Decoding it with the working key recovers `You have been idle for too long. Your connection has been closed.` exactly. This is a wrong-startup-key artifact, not a regional text encoding.

The server can replace both the startup key and seed-table selector in an `SVersionCheck` subtype 0 message:

```text
packet SVersionCheckKeyUpdate {
    u8 opcode                    // 0x00
    u8 subtype                   // 0
    u32be configuration_crc
    u8 seed_table_selector       // 0 through 9
    u8 key_length
    u8 key[key_length]
}
```

## Session key

The session-key path starts with the active character name. The client repeatedly expands lowercase MD5 text into a 1024-byte source. A packet then selects nine bytes from that source:

```text
for i from 0 through 8
    index = (seed16 + (seed8 * seed8 + i * 9) * i) mod 1024
    key[i] = md5_source[index]
```

`net_send_login_request` stores the submitted character name. The later key setup passes that same value to `net_build_md5_salt_source`, confirming the name is the seed input.

The client copies the nine selected bytes four times into an expanded buffer. This lets the 32-bit XOR loop cycle through the short key without reading past it.

## Seed XOR table

The client builds 256 byte values from a selector between 0 and 9. Some mappings repeat values and are not permutations. Each byte is repeated into a 32-bit word, such as `0x5A5A5A5A`, for the block XOR loop.

In the formulas below, `u8` wraps to 0 through 255. Signed division truncates toward zero.

| Selector | Result byte for index `i` |
| ---: | --- |
| 0 | `i` |
| 1 | `0x80 + (odd(i) ? -((i + 1) / 2) : ((i + 1) / 2))` |
| 2 | `0xFF - i` |
| 3 | `0x80 + (odd(i) ? -((0xFF - i) / 2) : ((0xFF - i) / 2))` |
| 4 | `(i / 16) * (i / 16)` |
| 5 | `u8(i * 2)` |
| 6 | `0xFF - u8(i * 2)` |
| 7 | `i <= 0x7F ? 0xFF - 2 * i : 2 * i - 0x100` |
| 8 | `i <= 0x7F ? 2 * i : 0x1FF - 2 * i` |
| 9 | `0xFF - u8(((i - 0x80) / 8) * ((i - 0x80) / 8))` |

Selector 0 is the built-in default. The live server may negotiate another selector. Values outside 0 through 9 are invalid for the locally mapped code.

## Sequence counters

Every encrypted packet carries a one-byte sequence. The sender uses its current value for the packet, then increments its counter for the next encrypted packet. The byte naturally wraps from 255 to 0.

Client-to-server and server-to-client traffic use separate sequence streams. `net_client_packet_sequence` owns the client's outgoing stream. `net_decrypt_server_packet` reads the incoming server sequence from the packet and does not change the client counter.

Each endpoint still owns its own local state for a stream. For client-to-server traffic, the client's send counter and the server's receive counter are separate values that should advance in step. Server-to-client traffic has another send and receive pair. An implementation should not use one counter for both directions or share one variable between send and receive handling.

Raw packets do not pass through the encryption function, so they do not advance this sequence. The sequence is also separate from the seed-table selector described above.

## Outgoing transformed body

```text
struct ClientTransformedBody {
    u8 opcode
    u8 sequence
    u8 encrypted_payload[...]
    u8 md5_bytes[4]             // digest bytes 13, 3, 11, 7
    u8 encoded_seed[3]
}
```

The MD5 covers the opcode, sequence, and transformed payload. `net_encrypt_client_packet` produces a body eight bytes longer than the queued plaintext it receives. For an ordinary builder body, the earlier submission terminator makes the complete transformed body nine bytes longer than the builder's declared length.

`CHello` demonstrates both rules: five builder bytes become six queued plaintext bytes, then fourteen transformed bytes. The client increments its outgoing sequence for every body handled by `net_encrypt_client_packet`, including a body whose builder supplied only an opcode.

## Incoming transformed body

`net_decrypt_server_packet` keeps the opcode, reads the independent server sequence, recovers two seed values from the final three bytes, and reverses the seed-table and key XOR passes.

The decoded server body is four bytes shorter than the transformed body. The server direction does not append the same four selected MD5 bytes used by the client direction.

Function addresses and detailed evidence are in the [function reference](../appendix/functions.md) and the YAML exports.
