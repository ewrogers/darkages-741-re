# Walk-route collision

Long right-click routes can cross an off-screen wall in the plan and stop when the character reaches it. The native BFS has enough storage for every normal map tile. The defect is that it asks the viewport's live static-object list for collision instead of using the complete map.

See [Pathfinding and following](../../systems/pathfinding-and-pursuit.md#why-a-distant-route-can-cross-a-wall) for the game behavior and the `lod600.map` example.

## Diagnostic first trial

Apply only the ground click-to-move change at `RVA 0x001EFDCE` to confirm the off-screen-static diagnosis. Leave the optional pursuit change and both injected-hook designs disabled. This trial is not the final `live OR raw` planner.

```text
required SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
target:            module_base + 0x001EFDCE
verify:            6A 01
write:             6A 00
rollback:          6A 01
```

Launch suspended, verify the fingerprint and original bytes, make the two-byte write with temporary page protection, flush the instruction cache, restore protection, then resume.

Expected `lod600.map` test:

```text
start: (11,8)
goal:  (24,8)
wall:  (19,8)

unpatched route: 13 steps directly right, then blocked at the wall
patched route:   15 steps through row 7 and around the wall
```

If the route still enters `(19,8)`, restore `6A 01` and confirm the loaded executable fingerprint and module-relative target. If ordinary ground click-to-move fails elsewhere, restore the same original bytes before testing anything else.

## Collision modes

`map_can_move_direction` has two static-collision modes. Bounds, movement state, privileges, and known dynamic occupants are checked before this choice.

| Mode | Static source | Behavior |
|---:|---|---|
| `1` | Live `WorldObject_Static` objects | Tests both sides of the edge with the direction mask. Missing off-screen objects look empty. |
| `0` | Complete raw map storage | Reads the destination cell and rejects it when its two `SOTP.DAT` low nibbles combine to `0x0F`. |

Ground click-to-move, entity pursuit, and the actual local step all pass mode `1`. No current caller selects the raw-map mode.

The mode choice affects only static collision. The shared bounds, state, privilege, and live dynamic-object scan runs first. Changing BFS to mode `0` therefore continues to avoid every currently known player, monster, or NPC that the native client considers blocking. It cannot avoid an entity that the server has not sent and the live world list does not contain.

The matching `SOTP.DAT` contains only collision values `0x00` and `0x0F`, with either value optionally combined with render bit `0x80`. Mode `0` therefore loses no directional distinction for the supplied static flags.

## Minimal map-wide workaround

Changing the ground-route call from mode `1` to mode `0` is a same-size runtime patch. The optional second change applies the same workaround to entity pursuit.

The preferred image base is `0x00400000`. File offsets are reference information only. A launcher uses the loaded module base plus the RVA.

| Use | Static address | RVA | File offset | Original | Replacement |
|---|---:|---:|---:|---|---|
| Ground click-to-move | `0x005EFDCE` | `0x001EFDCE` | `0x001EF1CE` | `6A 01` | `6A 00` |
| Entity pursuit, optional | `0x005F4D15` | `0x001F4D15` | `0x001F4115` | `6A 01` | `6A 00` |

```diff
- push 1
+ push 0
```

This corrects the base wall at `(19,8)` in `lod600.map` and lets native BFS choose the route around it.

This is a workaround, not the best general fix. Raw map cells do not contain a packet-driven door's current live tile ID. The project owner observed that the Tab map shows doors in their default open state and does not change when a door opens or closes. The patched planner would share that base-map behavior. A currently closed door can still be planned through, although the live safety check before the actual step will stop it.

## Solution levels

| Level | Planning collision | When a new blocker appears | Tradeoff |
|---|---|---|---|
| Okay | Raw mode `0` only | Native step check stops, ground route strands | Two-byte diagnostic workaround; known dynamic occupants remain checked, but live static states are replaced rather than combined. |
| Better | Live mode `1` **and** raw mode `0` must both allow the edge | Native step check stops, ground route strands | Correct `live solid OR raw-map solid` planning with a small injected call wrapper. |
| Best practical | Same live-or-raw planner | Retain the goal and replan on the next main-thread tick | Preserves native BFS and movement while adapting to newly visible occupants and static changes. |
| Full replacement | Custom BFS or A* over the same combined collision model | Extension owns retry and cancellation | Most flexible and most code to maintain; A* is not itself a correctness fix. |

The best practical option is the preferred design for version 741. It changes the collision source and stale-route behavior without replacing the proven native route format, movement sender, acknowledgement pacing, or pursuit timer.

## Per-map tile exclusions

The collision wrapper at `RVA 0x001F5068` is also the narrowest place to stop native BFS from crossing a known warp or another policy-blocked tile. It sees the source Y, source X, and direction for every candidate edge. After both native collision modes accept the edge, derive the destination and consult a bounded immutable rule snapshot:

```c
destination = step(source_x, source_y, direction);

if (!map_can_move_direction(world, source_y, source_x, direction, 1))
    return false;
if (!map_can_move_direction(world, source_y, source_x, direction, 0))
    return false;

rules = current_tile_rules;
if (rules.map_id == world->map_id && rules.blocked[destination.y][destination.x])
    return false;

return true;
```

A dense bit set needs at most 65,025 bits, about 8 KiB, for a normal version-741 map. Publish it as an immutable, versioned snapshot from the main-thread dispatcher. The hook may read the last complete snapshot but must not allocate, parse configuration, wait for IPC, or edit it.

This hook changes both ground click-to-move and entity-pursuit planning because both use the shared BFS. It does not change manual steps or the final live safety check. If an intentional route must enter a warp, either publish a request-scoped terminal exception or submit that exact segment through the route-vector path below.

No client algorithm can avoid a truly unknown entity. If the server has not sent a player, monster, or NPC, the live world list has no record to plan around. The best practical option handles that limit by keeping the native safety check on every step and replanning after the entity becomes known.

## Best-practical implementation

This is an injected runtime patch. It can live in a launcher-allocated code block or in an injected DLL. It does not rewrite the executable on disk.

Three call sites are required. All are ordinary five-byte relative calls, so each site can redirect to a helper without splitting an instruction.

| Purpose | Static address | RVA | File offset | Verified original bytes |
|---|---:|---:|---:|---|
| Capture a ground-click goal | `0x005EFDE3` | `0x001EFDE3` | `0x001EF1E3` | `E8 F8 4F 00 00` |
| Combine live and raw planning collision | `0x005F5068` | `0x001F5068` | `0x001F4468` | `E8 73 AF FF FF` |
| Detect a failed queued step | `0x005F4A46` | `0x001F4A46` | `0x001F3E46` | `E8 95 BF FF FF` |

The extension owns small bounded state outside client objects:

```c
struct GroundRouteState {
    WorldPane *world;
    u32 map_id;
    s32 goal_x;
    s32 goal_y;
    u32 generation;
    bool active;
    bool replan_pending;
};
```

Do not store this pointer across a world restart without validation. `WorldPane +0x26C` supplies the map ID. The current map dimensions, transfer state, map storage, and self object must pass the normal world-ready checks before planning.

### Goal-capture helper

The call at `0x005EFDE3` originally invokes `ui_world_pane_build_path_to_tile` after a plain ground right-click. Its replacement helper:

1. Advances the extension generation.
2. Saves the complete `WorldPane`, current map ID, and requested goal.
3. Clears `replan_pending` and marks the goal active.
4. Tail-calls or forwards to the native builder with the original arguments.
5. Returns the native success value and preserves the original `__thiscall` cleanup.

Only this native ground-click call site captures a goal. Entity pursuit calls the shared BFS directly and keeps its own target ID and timer.

### Collision helper

Redirect the BFS call at `0x005F5068` to the live-or-raw helper below. It receives the same `WorldPane` in `ECX` and the same four stack arguments as `map_can_move_direction`. It ignores the caller's original mode and performs both native checks.

```c
live_allowed = map_can_move_direction(world, y, x, direction, 1);
if (!live_allowed)
    return false;

return map_can_move_direction(world, y, x, direction, 0);
```

The helper returns through `AL` and performs the same 16-byte stack cleanup as the replaced `__thiscall` target. Preserve all x86 callee-saved registers.

### Failed-step helper

Redirect the call at `0x005F4A46` to a wrapper around `map_try_move_local_player`.

On success, return normally. On failure during the active saved ground generation:

1. Set `replan_pending` before clearing native movement state.
2. Call `ui_world_pane_reset_movement_state(world, 0)`.
3. Return without running BFS recursively.

For entity pursuit, clear only the failed route with reset argument `1` and let its native 100 ms timer replan. Do not turn a pursuit failure into a saved ground goal.

### Main-thread replan

The existing main-thread dispatcher consumes `replan_pending` on its next tick. It must verify the saved generation, complete `WorldPane`, map ID, map readiness, bounds, and self object before use.

```text
failed saved step
  -> mark replan pending
  -> clear stale native route
  -> return from old advance call
  -> next main-thread dispatcher tick
       -> validate generation, world, map, self, and goal
       -> build native path from current tile to saved goal
       -> collision call hook applies live AND raw checks
       -> start the first native step
```

If no route exists, clear the saved goal and perform the ordinary full reset. Do not retry an unreachable full-map search every frame. A bounded timer or relevant world-object movement event can request a later retry if that behavior is wanted.

When the native route reaches the saved goal, clear the extension state. Also clear it when the world or map changes, a full native movement reset occurs without `replan_pending`, or the user replaces movement through another ground click, keyboard direction, attack, or other native cancellation action.

## Live-or-raw collision detail

A robust injected helper can replace the call to `map_can_move_direction` inside `ui_world_pane_build_breadth_first_path`.

| Hook | Static address | RVA | File offset | Verified original bytes |
|---|---:|---:|---:|---|
| BFS neighbor collision call | `0x005F5068` | `0x001F5068` | `0x001F4468` | `E8 73 AF FF FF` |

The desired planning rule can reuse both native modes:

```c
bool route_can_move(WorldPane *world, s32 y, s32 x, u8 direction)
{
    bool live_allowed = map_can_move_direction(
        world, y, x, direction, 1);

    if (!live_allowed)
        return false;

    return map_can_move_direction(
        world, y, x, direction, 0);
}
```

This treats a move as blocked when either collision view reports a solid obstacle:

```text
blocked = live_view_blocked || raw_tab_map_tile_blocked
```

The first call preserves current live statics, door states, and known dynamic occupants. The second adds complete raw-map walls outside the viewport. Both calls scan known dynamic occupants, which is redundant but preserves the native rules without reconstructing them.

The helper must preserve the original `__thiscall` arguments and stack cleanup. It changes planning only. `map_try_move_local_player` remains native, so every submitted step still receives the live safety check.

This changes planning only. The ordinary local-step safety check remains native.

## Cancel a stranded ground route

Collision can still change after any route is built. `ui_world_pane_advance_queued_path` currently ignores a failed `map_try_move_local_player` call.

| Hook | Static address | RVA | File offset | Verified original bytes |
|---|---:|---:|---:|---|
| Queued-step attempt | `0x005F4A46` | `0x001F4A46` | `0x001F3E46` | `E8 95 BF FF FF` |

A call wrapper can cancel cleanly:

```c
bool try_queued_step(WorldPane *world, u8 direction)
{
    bool moved = map_try_move_local_player(world, direction);

    if (!moved) {
        bool keep_pursuit_timer = world->pursuit_target_id != 0;
        ui_world_pane_reset_movement_state(world,
            keep_pursuit_timer ? 1 : 0);
    }

    return moved;
}
```

The wrapper must preserve the original `__thiscall` stack cleanup. Ground routes use a full reset. Pursuit routes clear only the failed route so the existing 100 ms timer can replan.

Cancellation is the smallest safe behavior, but it does not walk around a newly visible monster. Automatic ground-route adaptation needs one more piece of injected state: retain the requested goal when click-to-move begins. When a saved step fails, queue a replan from the current tile to that retained goal on the next main-thread dispatcher tick. Do not re-enter BFS recursively from the failed-step call. If the new search has no route, perform the ordinary full reset.

Entity pursuit does not need this addition. Its native 100 ms target timer already clears and replans around newly known occupants.

The retained ground goal needs its own generation, similar to native pursuit. A new ground click replaces the goal and advances the generation. Keyboard movement, attack, authoritative position reset, map change, and world restart cancel it. A queued replan must compare its saved generation before changing the route, so stale work cannot restart cancelled movement.

Run the replan from the main-thread dispatcher. A failed step hook should only clear the stale route and queue work. It should not run BFS recursively while `ui_world_pane_advance_queued_path` is still consuming the old route.

If the replan finds no route, cancel cleanly. An optional bounded timer can retry a temporarily occupied goal, but it should not run an unbounded full-map search every frame.

## Injecting an externally planned route

The client route vector can accept a path produced by an external A*, waypoint system, or other policy engine. Directly replacing its three pointers is unnecessary and unsafe. Use the client's own vector helpers on the main thread so allocation and capacity remain owned by the same runtime.

| Purpose | Static address | RVA |
|---|---:|---:|
| Full movement reset | `0x005F4900` | `0x001F4900` |
| Start the next queued step | `0x005F4990` | `0x001F4990` |
| Append one 12-byte route record | `0x005F59A0` | `0x001F59A0` |
| Clear route records while retaining capacity | `0x005F5A80` | `0x001F5A80` |

The vector begins at `WorldPane +0x2A8`. Its `start`, `end`, and capacity-end pointers occupy `+0x2A8`, `+0x2AC`, and `+0x2B0`. `+0x2B8` is the remaining-record count, and byte `+0x294` is the active-route flag.

```c
struct path_route_step {
    u8 direction;       // +0x00
    u8 reserved[3];
    s32 source_y;       // +0x04
    s32 source_x;       // +0x08
};
```

The native builder reconstructs from goal to start and appends each edge in that order. The replay function consumes `records[--remaining]`. Given forward absolute tiles `p[0]` through `p[n]`, append records for edges `n - 1` through `0`. Each record contains the direction from `p[i]` to `p[i + 1]` and the source coordinates from `p[i]`.

```c
bool install_exact_route(WorldPane *world, u32 map_id, Tile *p, u32 tile_count)
{
    validate_world_map_and_tiles(world, map_id, p, tile_count);
    require(p[0] == current_player_tile(world));
    require_each_edge_is_cardinal_and_allowed(p);

    if (tile_count == 1)
        return true;

    ui_world_pane_reset_movement_state(world, 0);

    for (i = tile_count - 1; i > 0; --i) {
        path_route_step step;
        step.direction = direction_from_to(p[i - 1], p[i]);
        step.source_y = p[i - 1].y;
        step.source_x = p[i - 1].x;
        path_route_step_vector_push_back(&world->route, &step);
    }

    world->remaining_route_steps = tile_count - 1;
    world->route_active = 1;
    return ui_world_pane_advance_queued_path(world) != 0;
}
```

Bound the request to a simple current-map path, at most `width * height` tiles. A one-tile path is an immediate no-op. Validate the exact executable, live complete `WorldPane`, current map ID, map-ready state, coordinates, and every edge before the reset. The full reset already clears the vector through the native erase helper. Recheck the first native step result. If it fails, perform another full reset and report the blocked edge.

Do not run this from an IPC worker. Queue a pointer-free route command and perform validation and mutation in the normal main-thread dispatcher tick. Keep an extension generation and expected map ID so user input, a map change, a server correction, or a newer route makes queued work stale.

An exact route should not silently replan with native BFS after a blocked step because that can violate its requested tile sequence. The failed-step hook can cancel and publish the failed source, destination, and reason. A controller may submit a new externally planned route, use bounded exact-route retries for a temporary occupant, or explicitly request native fallback.

This sequence is confirmed by static Binary Ninja analysis of vector construction and replay. It has not yet been live-tested as an injector. Start with a two- or three-edge route on an open map. Verify the captured absolute route, one-step-per-position-update pacing, ordinary input cancellation, blocked-first-step reset, and clean unload before trying a warp segment.

## Crossing maps

Never place tiles from two maps in one native vector. A warp is a server-owned transition, and the old route becomes invalid when the new map and position arrive.

Represent a trip as map-tagged segments:

```text
segment 1: map A, current tile ... warp tile
wait:      confirmed map B and entry position
segment 2: map B, entry tile ... next warp or goal
```

For daRPC, publish the new vector through its existing route observer after installation, then wait for its atomic `location.changed` publication at a warp. That event pairs the staged map identity with the following position. Validate the expected map and optional entry region, then submit the next segment with a new revision. A timeout, unexpected map, manual movement, disconnect, or authoritative correction cancels or returns control to the external planner.

## Replacing BFS with A*

A DLL can replace the planner without replacing movement transport. The clean boundary is `ui_world_pane_build_breadth_first_path` or its two native callers.

The replacement can read the complete map dimensions and cells, overlay live static replacements and known dynamic occupants, and run BFS or A*. It should then write the same reversed 12-byte route records the native advance function expects:

```c
struct RouteStep {
    u8 direction;
    u8 padding[3];
    s32 source_y;
    s32 source_x;
};
```

Keep native movement pacing. Submit one step through `map_try_move_local_player`, then wait for the local position update before advancing. Run planning and route mutation on the main game thread.

A* is feasible, but it is not needed to fix this bug. A* using only the live viewport would have the same incorrect collision model as native BFS. Native BFS finds a shortest route once it receives the combined collision view. The live-or-raw collision hook plus reactive replan is smaller and preserves more client behavior.

## Installation rules

Use the [safe launcher](safe-launcher.md). Require the exact version-741 fingerprint, verify every original byte before writing, resolve static targets as module-base-relative RVAs, and never rewrite `Darkages.exe`.
