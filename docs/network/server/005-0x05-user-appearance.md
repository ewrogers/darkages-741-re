# User Appearance (`SUserAppearance`)

`SUserAppearance` establishes the local player's object ID and carries a compact action-state byte. The server can also send a state-only form that changes those action flags without replacing the rest of the saved self appearance.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x05` (5) |
| Transform | derived |
| Session owner | RTTI class `WorldUserFunc` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```c
struct SUserAppearanceBody {
    u8 opcode;                         // 0x05
    u32be object_id;
    u8 unknown_full_update_0;
    u8 unknown_full_update_1;
    u8 unknown_full_update_2;
    u8 appearance_state;
    u8 unknown_full_update_3;
};
```

The packet has one fixed `u32be` followed by five bytes. The four bytes surrounding `appearance_state` are stored on a full update, but their meanings are not yet established.

A receive-side zero may follow this structure. It is not consumed by `net_deserialize_user_appearance_server_packet`. See [Receive-side zero bytes](../packet-transforms.md#receive-side-zero-bytes).

## Full and state-only updates

Bit `0x80` of `appearance_state` changes how the packet is applied:

| Condition | Client behavior |
| --- | --- |
| `(appearance_state & 0x80) == 0` | Stores `object_id` as both self-object IDs and copies the four unknown appearance bytes |
| `(appearance_state & 0x80) != 0` | Leaves those fields unchanged |

Both forms store `appearance_state & 0x7F` at `WorldUserFunc + 0x15C88`. This makes `0x80` an update marker, not one of the persistent state bits.

The state-only body is still the same fixed size. Its object ID and four other bytes are parsed but ignored by the handler.

## Persistent state bit 0

Bit `0x01` of the saved low-seven-bit state is an action lock. When set, the client rejects a proposed local move before checking characters or map collision. The same bit also restricts several other actions, including an inventory-move request path, so it is broader than a simple movement permission.

The local movement order is:

```c
if (appearance_action_state & 0x01)
    return false;

if (!map_can_move_direction(position, direction))
    return false;

move_local_object(direction);
send_CMove(direction);
```

`map_can_move_direction` checks bounds, dynamic occupants, and direction-specific `SOTP.DAT` static collision. It does not inspect ground tile IDs and does not search the skillbook for a skill named Swimming.

This action lock is a plausible way for the server to leave a character without Swimming stuck in water. A capture made while entering water is still needed to prove that the server specifically sends state-only `0x81` to set the lock and `0x80` to clear it.

## Visible appearance is separate

This packet does not rebuild the local player's sprite. The swimming body is selected by the packed appearance variant in [`SDrawHumanObjects`](051-0x33-draw-human-objects.md), which creates or refreshes `WorldObject_User`.

This separation lets the server update movement restrictions and visible appearance independently:

- `SUserAppearance` stores the local action state;
- `SDrawHumanObjects` selects the visible human body-resource family.

The combined flow is described in [Movement and swimming](../../systems/movement-and-swimming.md).

## Supplied login trace

The supplied login trace contains one full `SUserAppearance`. Its five bytes after the object ID are `02 00 03 00 00`, so the persistent state is clear. One additional zero follows the parsed body.

## Known limits

Only persistent state bit `0x01` has identified client consumers. The meanings of bits `0x02` through `0x40` and the four full-update bytes remain unknown.
