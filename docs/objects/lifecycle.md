# Object lifecycle and packets

## Creation

Two packet families create dynamic world objects.

| Packet | Handler | Local class | Selection rule |
|---|---:|---|---|
| `SDrawObjects` `0x07` | `net_handle_s_draw_objects` at `0x5F3150` | `WorldObject_Monster` | `sprite_id` from `0x4000` through `0x7FFF` |
| `SDrawObjects` `0x07` | `0x5F3150` | `WorldObject_Item` | `sprite_id` from `0x8000` through `0xBFFF` |
| `SDrawHumanObjects` `0x33` | `net_handle_s_draw_human_objects` at `0x5F3340` | `WorldObject_Human` | `object_id` differs from the stored self ID |
| `SDrawHumanObjects` `0x33` | `0x5F3340` | `WorldObject_User` | `object_id` equals the stored self ID |

The creation helpers first remove an existing object with the same ID, allocate the concrete RTTI class, set its coordinates, and insert it into the shared object indexes.

| Function | Address | Role |
|---|---:|---|
| `object_create_human` | `0x5CA140` | Creates another human actor |
| `object_create_monster` | `0x5CA4C0` | Creates a creature or NPC-style actor |
| `object_create_self_user` | `0x5CA830` | Creates the local player |
| `object_create_item` | `0x5CAC60` | Creates a ground item |
| `object_insert` | `0x5C8EA0` | Inserts into object, coordinate, render, and spatial state |
| `object_list_insert` | `0x5E5D40` | Adds to `WorldObjectList` and sets `object + 0x48` |

`SDrawObjects` contains a `u16be` record count. `net_s_draw_objects_read_record` at `0x598B30` consumes one variable-length record on each iteration. The client does not flatten the remaining packet into a fixed array.

```c
for (i = 0; i < record_count; ++i) {
    read_draw_object_record(&record);

    if (record.sprite_id >= 0x4000 && record.sprite_id <= 0x7fff) {
        object = object_create_monster(record.object_id,
                                      record.y,
                                      record.x,
                                      record.monster_class);
        object_living_apply_monster_appearance(
            object, record.sprite_id - 0x4000);
    } else if (record.sprite_id >= 0x8000 &&
               record.sprite_id <= 0xbfff) {
        object = object_create_item(record.object_id,
                                   record.y,
                                   record.x,
                                   record.sprite_id - 0x8000,
                                   record.flags);
    }
}
```

The exact meaning of several per-record bytes remains open. The class selection and sprite-ID ranges are confirmed by the handler.

## Movement and position correction

`SMoveObject` (`0x0C`) moves another living object. `net_handle_s_move_object` at `0x5F3930`:

1. Finds the object by its common ID at `object + 0x24`.
2. Accepts only broad categories `1` and `2`, used by human/user and monster actors.
3. RTTI-casts the instance to `WorldObject_Living`.
4. Corrects the stored source position when it differs from the packet.
5. Calls `object_reindex` at `0x5C92C0` after a direct coordinate correction.
6. Computes the adjacent destination from the direction and starts the living-object movement virtual method.

If the ID is missing or does not resolve to a living actor, the client sends `CPutRequest` (`0x0C`) through `net_send_c_put_request` at `0x5F4430`. This asks the server to resend the object description.

`SMove` (`0x0B`) is the local-player path. `net_handle_s_move` at `0x5F2FC0` applies the server result to the view position. An authoritative disagreement can trigger `CRefresh` (`0x38`) through `net_send_c_refresh` at `0x5F4640`.

## Direction and animation updates

`SChangeDirection` (`0x11`) finds the object, RTTI-casts it to `WorldObject_Living`, and calls `object_living_set_direction` at `0x5E0880`. The direction byte is stored at living-object offset `+0x192`. A changed value restarts or refreshes the displayed sprite. Missing objects cause a `CPutRequest`.

`SMotion` (`0x1A`) targets the same living categories. `net_handle_s_motion` at `0x5F3C80` combines the requested motion with the object's current direction and converts the wire duration to milliseconds:

```c
duration_ms = (u32)duration_10ms * 10;
living->start_motion(motion, living->direction, duration_ms);
```

`SDamageEffect` (`0x13`) is another object-ID update. `net_handle_s_damage_effect` at `0x5F40F0` can play a sound and forwards a `0..100` byte as a quarter-scale health or damage display value. The final meaning of all three bytes is not yet confirmed.

## Removal

`SRemoveObjects` (`0x0E`) has a plural RTTI name, but this build deserializes exactly one `u32be object_id`. `net_handle_s_remove_objects` at `0x5F3100` calls `object_remove_by_id` at `0x5C9FA0`.

The removal helper may ask the object for a temporary removal visual or replacement clone before detaching the original. That branch depends on `object + 0x30` and the caller's animation flag. The exact visual semantics vary by class and remain provisional.

`object_detach` at `0x5C9450` removes the original from:

- the spatial callback or index
- the renderer observer
- the coordinate cell collection
- the object-ID lookup

`object_list_erase` at `0x5E6020` performs the underlying list and index cleanup. Range-driven cleanup is described in [View range and refresh](view-range-and-refresh.md).
