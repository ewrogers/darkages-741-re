# User Appearance (`SUserAppearance`)

`SUserAppearance` establishes the local player's object ID and saves a few small identity values for the world UI. It also carries an action-state bitfield that can stop local movement without replacing the rest of the saved appearance state.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x05` (5) |
| Transform | derived |
| Session owner | RTTI class `WorldUserFunc` |
| UI owner | RTTI class `WorldPane::WorldPane_Impl` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SUserAppearance {
    u8      opcode                    // 0x05
    u32     user_id
    u8      facing                    // Direction
    u8      guild_value
    u8      character_class           // CharacterClass
    u8      action_state
    u8      unknown_final
}
```

The fixed body contains five bytes after `user_id`, not four. This matters because `action_state` and `unknown_final` are separate fields.

A receive-side zero may follow this structure. It is not consumed by `net_deserialize_user_appearance_server_packet`. See [Receive-side zero bytes](../packet-transforms.md#receive-side-zero-bytes).

## Fields retained by the client

On a full update, `session_update_from_user_appearance_packet` copies the fields into `WorldUserFunc`:

| Wire field | Session field | What is known |
| --- | --- | --- |
| `user_id` | `self_object_id` | Also becomes the world controller's two saved self IDs |
| `facing` | `appearance_facing` | Stored, but no later reader was found |
| `guild_value` | `appearance_guild_value` | Preserved as a raw byte |
| `character_class` | `character_class` | Preserved as a raw byte |
| `action_state` | `appearance_action_state` | Low seven bits are retained |
| `unknown_final` | `appearance_unknown_final` | Preserved as a raw byte |

`WorldPane_Impl` has virtual getters for the user ID, guild value, character class, action state, and final unknown byte. There is no equivalent getter or other identified reader for the cached `facing` byte.

The guild field is not converted to a boolean. The local code therefore does not distinguish a `has_guild` flag from a small guild-related value or ID. `guild_value` is intentionally neutral until a capture with values other than zero and one, or a clear consumer, settles it.

The final byte is also read, stored, and exposed by a getter, but no client decision based on it was found. It is not the movement flag.

## Action state and partial updates

Bit `0x80` of `action_state` changes how the packet is applied:

| Condition | Client behavior |
| --- | --- |
| `(action_state & 0x80) == 0` | Stores every field in the body |
| `(action_state & 0x80) != 0` | Stores only `action_state & 0x7F` |

This makes `0x80` an update marker rather than a persistent state bit. The packet remains fixed-size in both forms, so the other fields are still parsed and then ignored during a state-only update.

Persistent bit `0x01` is an action lock. When set, the client rejects a proposed local move before checking characters or map collision. The same bit restricts several other actions, so it is broader than a `can_move` boolean and its sense is inverted: one means locked.

```c
if (appearance_action_state & 0x01)
    return false;

if (!map_can_move_direction(position, direction))
    return false;

move_local_object(direction);
send_CMove(direction);
```

Bits `0x02` through `0x40` have no identified consumers.

## Runtime changes

`SStatus` does not update this action state. Its standalone fields bit `0x02`, called `Swimming` in project protocol vocabulary, stays in the temporary status packet and is not copied to `WorldUserFunc + 0x15C88`.

Only two direct writes to the saved action-state byte exist in this client:

1. `session_world_user_func_ctor` clears it when the session object is created.
2. `session_update_from_user_appearance_packet` replaces it from `SUserAppearance`.

A server that changes the lock during play must therefore resend opcode `0x05`. The state-only form appears designed for exactly this case. With no other persistent bits set, `action_state = 0x81` would set the lock and `0x80` would clear it while leaving user ID, facing, guild value, class, and the final byte untouched. A runtime capture is still needed to confirm that the live server uses those exact values.

## Direction and class

`facing` uses the shared [`Direction`](../protocol-types.md#direction) type. `character_class` uses [`CharacterClass`](../protocol-types.md#characterclass).

The helper only defines values `0` through `3`. A value of `4` does not enter an explicit `None` case and leaves its result undefined. Because the `SUserAppearance` facing copy is never read after storage, the local client does not confirm `4` as a bounce-back or no-direction value in this packet. A capture may still show the server using it as protocol vocabulary, but the 7.41 client does not interpret it that way here.

The client confirms that this is a raw one-byte discriminator. When virtual-key `0x09` (Tab) opens the map overlay, value `2` selects a different overlay configuration. Project-owner observation identifies this as the Rogue-only ability to zoom the map in and out; other classes receive the non-zoomable configuration. This directly supports `Rogue = 2`. The executable does not contain a complete local name table that independently proves all six labels.

## Visible appearance is separate

This packet does not rebuild the local player's sprite. [`SDrawHumanObjects`](051-0x33-draw-human-objects.md) creates or refreshes `WorldObject_User` and selects the visible body-resource family, including the swimming appearance.

This separation lets the server update movement restrictions and visible appearance independently:

- `SUserAppearance` stores the local identity and action state;
- `SDrawHumanObjects` selects the visible human body and facing used in the world.

The combined flow is described in [Movement and swimming](../../systems/movement-and-swimming.md).

## Supplied login trace

The supplied login trace contains one full `SUserAppearance`. Its five bytes after the object ID are `02 00 03 00 00`: down, zero guild value, class value 3, clear action state, and a zero final field. One additional receive-side zero follows the parsed body.

## Known limits

The meanings of action-state bits `0x02` through `0x40`, nonzero guild values, and `unknown_final` remain unresolved. The direction and class labels include project-owner protocol vocabulary, with the local limits stated above.
