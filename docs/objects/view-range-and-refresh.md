# View range and refresh

## Dynamic-object retention range

The world pane constructor `map_world_pane_ctor` at `0x5C64F0` initializes offset `+0x218` to `0x12`, or 18 tiles. The cleanup test uses Manhattan distance:

```c
distance = abs(object_x - center_x) + abs(object_y - center_y);

if (distance > 18 && object->category != 0) {
    object_detach(object);
}
```

`object_collect_out_of_range` at `0x5C7AF0` performs the distance test. `object_prune_out_of_range` at `0x5C7CD0` detaches the collected objects. Category `0` objects are skipped by the normal call, which preserves static map objects for their separate rebuild path.

This 18-tile diamond is a dynamic-object retention boundary. It should not be treated as the exact rectangular screen-culling area. The renderer can stop drawing an indexed object before the retention cleanup removes it.

## When the range is rebuilt

`object_set_view_position` at `0x5EEC70` always updates the current view coordinates. Its third argument decides whether to perform a full visible-area rebuild.

| Source | Full rebuild | Behavior |
|---|---|---|
| `SUserPosition` `0x04` | Yes | Synchronizes self position, prunes distant dynamic objects, and rebuilds visible static state |
| `SMove` `0x0B`, normal step | No | Shifts the view for the adjacent step without running the full prune |
| `SMove` `0x0B`, authoritative result `4` | Yes | Re-centers from server coordinates and performs the full rebuild |
| Self record in `SDrawHumanObjects` `0x33` | Usually yes | Re-centers and rebuilds unless the handler decides the current self appearance/state can be preserved |

The full path calls `object_rebuild_visible_area` at `0x5C7DF0`. It updates the render center, prunes dynamic objects beyond 18 tiles, calls `map_build_static_world_objects` at `0x5CD730`, and refreshes dependent map and effect layers.

## Objects entering and leaving range

The client does not invent dynamic objects when the view center moves. Objects enter local state when the server sends `SDrawObjects` (`0x07`) or `SDrawHumanObjects` (`0x33`). Duplicate object IDs are replaced by the creation helpers, which makes server resends safe.

A remote `SMoveObject` (`0x0C`) does not remove an actor merely because its destination is off screen or beyond the retention boundary. The object is reindexed and can be culled by rendering. Authoritative lifetime cleanup comes from either:

- `SRemoveObjects` (`0x0E`) from the server
- the next full visible-area rebuild, which prunes dynamic objects beyond the 18-tile Manhattan range

This means an object moving out of view can remain indexed briefly until a server removal or a full local rebuild.

## F5 and `CRefresh`

`object_handle_world_input_event` at `0x5F1480` recognizes the internal F5 event code `0x89`. Ctrl+R is an alternate shortcut when the event modifier byte is `2`.

Both shortcuts perform the same two calls:

```c
object_reset_movement_sync_state(world, 0);
net_send_c_refresh(world);
```

`object_reset_movement_sync_state` at `0x5F4900` advances a reset generation, clears a vector of pending 12-byte movement records, resets related pending state, and clears the active movement flag at controller offset `+0x294`.

`net_send_c_refresh` at `0x5F4640` sends a body containing only opcode `0x38`. There is no request payload:

```text
plaintext body: 38
```

The packet uses the normal common client transform mode before framing and transmission.

F5 does not directly clear the object list or invoke `object_rebuild_visible_area`. The intended resynchronization depends on the server answering with the normal state packets. Resent draw records replace matching IDs, and `SRemoveObjects` can delete stale IDs. The exact set and order of the server's refresh response requires a packet capture or server implementation to confirm.

The local registry contains payload-free `SSelfSaveOK` (`0x21`), but `net_dispatch_game_server_message` at `0x5ED990` has no `0x21` handler. It also has no `0x22` refresh-complete branch. There is therefore no client evidence that either opcode completes the F5 refresh in this build.
