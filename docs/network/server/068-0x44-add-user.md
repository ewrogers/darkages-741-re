# Add User (`SAddUser`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x44` (68) |
| Transform | derived |
| Class name | `SAddUser` |
| Name provenance | Microsoft C++ RTTI in the target |
| Active consumer | None found |

## Result

`SAddUser` is an opcode-only message that has no gameplay effect in this client. The packet factory can construct it, but its deserializer reads no fields and no active pane, world, session, or UI handler checks opcode `0x44`.

The RTTI name is therefore stronger evidence for intended protocol vocabulary than for live behavior. In version 741, receiving it creates a temporary packet object, dispatches the network event through the pane system, and then leaves all observed game state unchanged.

## Body

```text
packet SAddUser {
    u8 opcode                     // 0x44
}
```

`net_create_add_user_server_packet` allocates exactly `0x10` bytes, which is the size of the common server packet base. There is no derived storage for payload fields. `net_deserialize_add_user_server_packet` is an empty function and does not advance the packet reader after the common dispatcher skips the opcode.

Extra decoded bytes would remain unread by this class. A sender should use the exact one-byte body rather than treating that behavior as an extension mechanism.

## What it modifies

The client changes none of the following:

- Local character or `WorldUserFunc` state
- The world object list
- Character position or appearance
- Any inventory, spell, skill, status, or GUI pane
- Any client timer

It also sends no client packet in response.

The local player is instead established and updated through packets such as [`SUserAppearance`](005-0x05-user-appearance.md), [`SUserPosition`](004-0x04-user-position.md), and the human-object drawing flow. Other visible users arrive through [`SDrawHumanObjects`](051-0x33-draw-human-objects.md). `SAddUser` does not duplicate those paths.

## Testing

The decoded plaintext body is simply:

```text
44
```

On a live encrypted connection it must still use the normal derived server-packet transform, sequence, and trailer. The expected result is no visible change and no client response. Logging the decoded event confirms that the packet was accepted even though no pane consumes it.

This makes `SAddUser` a useful no-op dispatch test, but not a way to spawn or refresh a player object.
