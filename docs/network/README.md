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
- [Packet transforms](packet-transforms.md) explains the startup key, session key, and seed table.
- [Client packet index](client/README.md) lists messages sent by the client.
- [Server packet index](server/README.md) lists messages sent by the server.

## Direction names

- A `CPacket` travels from client to server.
- An `SPacket` travels from server to client.

The same command code can mean different things in each direction. The two indexes are therefore kept separate.

## What a packet page contains

Each page aims to answer:

1. What does this packet do?
2. When is it sent or handled?
3. Which transform does it use?
4. What fields are known?
5. What remains uncertain?

Addresses and low-level evidence belong in the [function reference](../appendix/functions.md) and YAML exports. Packet pages stay focused on the protocol a game or server programmer needs.
