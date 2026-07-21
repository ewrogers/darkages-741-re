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

## Start here

- [Initial connection](connection.md) explains how the host, port, and socket are chosen.
- [Transport](transport.md) follows packets between game code and TCP.
- [Packet body notation](packet-body-notation.md) defines the field lists used on packet pages.
- [Shared protocol types](protocol-types.md) centralizes enums and bit flags used by several packets.
- [Packet transforms](packet-transforms.md) explains the startup key, session key, seed table, and the `CMerchant`/`CPursuit` inner wrapper.
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
