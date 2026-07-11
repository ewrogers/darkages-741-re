# Self-player initialization

The local player is initialized in stages. No single packet both establishes identity and fully constructs the object.

## Stage 1: establish the self ID

`SUserAppearance` (`0x05`) reaches `net_handle_s_user_appearance` at `0x5F2E90`. Its first field is a `u32be object_id`.

When bit `0x80` of the byte stored at packet-object offset `+0x17` is clear, the handler stores the same ID in two controller fields:

| Controller offset | Accessors | Observed use |
|---|---|---|
| `+0x210` | `object_set_local_user_id` `0x5C70F0`, `object_get_local_user_id` `0x5C7110` | Local user identity |
| `+0x214` | `object_set_self_object_id` `0x5C7130`, `object_get_self_object_id` `0x5C7150` | Object-list lookup and self-record comparison |

The handler then forwards the full packet to another client component at controller offset `+0x2CC`. It does not allocate `WorldObject_User` itself.

## Stage 2: allocate the self object

`SDrawHumanObjects` (`0x33`) reaches `net_handle_s_draw_human_objects` at `0x5F3340`. The handler compares the record's object ID with controller offset `+0x214`.

```c
if (record.object_id == object_get_self_object_id(world)) {
    user = object_get_self_user(world);

    if (user == NULL) {
        user = object_create_self_user(world,
                                      record.object_id,
                                      record.y,
                                      record.x);
    }

    apply_human_or_disguise_appearance(user, &record);
} else {
    human = object_create_human(world,
                               record.object_id,
                               record.y,
                               record.x);
    apply_human_or_disguise_appearance(human, &record);
}
```

`object_get_self_user` at `0x5EEDB0` looks up the stored ID and uses MSVC RTTI to cast the result to `WorldObject_User`. `object_create_self_user` at `0x5CA830` allocates the confirmed RTTI class and inserts it into the common world-object containers.

Normal appearance records are applied by `object_human_apply_appearance` at `0x5E0070`. A special appearance value of `0xFFFF` selects the disguised or monster-form path through `object_living_apply_monster_appearance` at `0x5E0370`.

## Stage 3: position and view synchronization

`SUserPosition` (`0x04`) reaches `net_handle_s_user_position` at `0x5F2F00`. It finds the `WorldObject_User`, writes the two coordinates, and calls `object_reindex` at `0x5C92C0`. It then calls `object_set_view_position` at `0x5EEC70` so the camera and visible map state follow the server position.

Later `SMove` (`0x0B`) messages maintain the local position and view. Their final byte also participates in round-trip timing when it matches the client's pending movement token.

## Ordering consequence

The client tolerates identity and object construction arriving separately:

```text
SUserAppearance 0x05
  store self ID
        |
        v
SDrawHumanObjects 0x33 record with matching ID
  allocate WorldObject_User and apply appearance
        |
        v
SUserPosition 0x04 and SMove 0x0B
  synchronize object coordinates and view
```

`SUserPosition` checks whether the self object already exists. This avoids dereferencing a missing user if packet arrival or scene setup has not yet completed.
