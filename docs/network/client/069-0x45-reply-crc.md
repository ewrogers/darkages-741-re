# Reply CRC (`CReplyCRC`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x45` (69) |
| Encoding | derived |
| Name provenance | Related class vocabulary matched to the locally confirmed reply builder |

## Purpose

The client sends this packet immediately after [`SRequestCRC`](../server/059-0x3b-request-crc.md). Its body is the server's two-byte challenge in reverse byte order.

The handler technically calls the shared custom CRC16 update twice. For a two-byte challenge and initial state zero, those calls reduce exactly to a byte swap. No client-owned data enters the calculation.

## Body

```text
packet CReplyCRC {
    u8      opcode                    // 0x45
    u16     response                  // byte-swapped SRequestCRC.challenge
}
```

For example:

```text
server body: 3B 12 34
client body: 45 34 12
```

`net_handle_request_crc_server_body` writes the three-byte plaintext body and submits it through the normal derived transform. That transport step is separate from the challenge calculation.

## What the client checks

Nothing. This path does not read the executable, map data, files, packet history, or a stored checksum. It does not compare the result with another value. The only input is the two-byte server challenge.
