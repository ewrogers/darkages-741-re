# Network system

The network system moves messages between the game and the server. It has four clear layers:

```text
game code
   |
packet body and command code
   |
packet transform and frame
   |
TCP socket
```

Keeping these layers separate makes packet work much easier. A gameplay packet page can describe fields without repeating socket or encryption details.

## Choose a starting point

| Question | Start with | Then follow |
| --- | --- | --- |
| How does the client establish a connection? | [Initial connection](connection.md) | [Transport](transport.md) for queued work and TCP framing |
| What does a known opcode mean? | The [client](client/README.md#packet-index) or [server](server/README.md#packet-index) index | The packet's body, owner, and paired messages; choose the direction first |
| How do I read a body schema? | [Packet body notation](packet-body-notation.md) | [Shared protocol types](protocol-types.md) for reused enums and flags |
| How is a body transformed for transmission? | [Packet transforms](packet-transforms.md) | [Checksums](checksums.md) and [transport framing](transport.md) |
| How do messages form an interaction? | [Packet interaction flows](interaction-flows.md) | The referenced system and direction-specific packet pages |

## NPC conversations

Begin with [NPC dialogs](../systems/npc-dialogs.md) for session ownership, then follow its [round trips](../systems/npc-dialogs.md#server-and-client-round-trips) and the matching packet pair:

| Conversation | Server to client | Client to server |
| --- | --- | --- |
| Screen menu | [SScreenMenu](server/047-0x2f-screen-menu.md) supplies the menu | [CMerchant](client/057-0x39-merchant.md) returns the selected value |
| Pursuit | [SPursuitMessage](server/048-0x30-pursuit-message.md) supplies a conversation step | [CPursuit](client/058-0x3a-pursuit.md) returns navigation, an answer, or close |

Each packet page owns its exact body variants. Keep these NPC conversations separate from [player exchange](../systems/player-exchange.md), which uses a different protocol for trading between players.

<a id="start-here"></a>

## Read next

- [Initial connection](connection.md) explains how the host, port, and socket are chosen.
- [Transport](transport.md) follows packets between game code and TCP.
- [Packet body notation](packet-body-notation.md) defines the field lists used on packet pages.
- [Shared protocol types](protocol-types.md) centralizes enums and bit flags used by several packets.
- [Packet transforms](packet-transforms.md) explains `raw`, `static`, and `derived` modes, their key and sequence state, and the `CMerchant`/`CPursuit` inner wrapper.
- [Checksums](checksums.md) documents the custom CRC16 and standard CRC32.
- [Server list and greeting](server-tables.md) covers `mServer.tbl` and stipulation updates.
- [Packet interaction flows](interaction-flows.md) follows bulletin, exchange, group, and NPC screen-menu conversations in both directions.
- [Client packet index](client/README.md) lists messages sent by the client.
- [Server packet index](server/README.md) lists messages sent by the server.

## Direction names

- A `CPacket` travels from client to server.
- An `SPacket` travels from server to client.

The same command code can mean different things in each direction. The two indexes are therefore kept separate.

## Wire byte order

All multibyte integers in packet bodies and the common frame header are big-endian. Packet field lists write `u16`, `u24`, and `u32` without an endian suffix because that rule is universal here. File formats and runtime memory structures state their byte order separately.

## What a packet page contains

Each page aims to answer:

1. What does this packet do?
2. When is it sent or handled?
3. Which transform does it use?
4. What fields are known?
5. What remains uncertain?

Addresses and low-level evidence belong in the [function reference](../appendix/functions.md) and YAML exports. Packet pages stay focused on the protocol a game or server programmer needs.
