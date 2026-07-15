# 098 / 0x62: Request Sequence (`CRequestSequence?`)

- Direction: client to server
- Internal name: `CRequestSequence?`
- Local behavioral alias: `Client codename ("baram") / RequestSequence?`
- Name provenance: Internal-style local name inferred from this client's behavior; no exact leaked class match is known yet.
- Evidence: concrete pre-version builder at `sub_579090` (`0x579821`)
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `sub_579090` at `0x579090`; submitted at `0x579821` immediately before `CVersion` is built.

## Current structural notes

- The builder copies the hardcoded ASCII client codename `"baram"` and submits five bytes.
- Interpreted as a packet body, this is opcode `0x62` followed by ASCII payload `"aram"`: `62 61 72 61 6D`.
- `net_submit_client_packet` appends its NUL sentinel before mode-0 transformation.
- The local `RequestSequence` name remains tentative. The concrete bytes and pre-version ordering are proven; user tribal knowledge identifies `"baram"` as the client codename.
- Opcode `0x62` uses common transform mode 0, so its transformed body includes and consumes the rolling sequence byte.
- The opcode's sender branch does not reset that counter. The surrounding startup routine calls `net_reset_client_packet_sequence` immediately after enqueueing `"baram"` and before enqueueing raw CVersion.
- Because the communications queue is asynchronous, `"baram"` can be transformed after the reset and therefore carry sequence `0`, leaving sequence `1` for the next encrypted packet. See [Client packet send pipeline](../../client/network-send.md#outgoing-sequence-reset-and-the-pre-version-handshake).
