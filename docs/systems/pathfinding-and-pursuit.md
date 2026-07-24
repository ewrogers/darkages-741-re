# Pathfinding and entity pursuit

Right-clicking a living world object starts a client-side pursuit and auto-attack loop. The client finds a shortest walk to a tile beside the target, follows that route with ordinary movement packets, and attempts another attack every 100 ms while it remains beside and facing the target. There is no special follow packet and no server-side path request.

This behavior is better described as pursuit than passive following. Its terminal action is an attack, and the native entity helper does not offer a walk-only option.

## From right-click to attack

The input manager emits pointer event type `6` for a right-button release. A hit-tested `WorldObject_Living` forwards that action to `ui_world_pane_handle_living_object_message`, which rejects the local character and passes the other object's `u32` ID to `ui_world_pane_pursue_and_auto_attack_target`.

```text
right-button release
  -> hit-tested WorldObject_Living
  -> living-object action 6
  -> resolve target by object ID
  -> already adjacent?
       yes: face the target or send CAttack
       no:  find a shortest route to an adjacent tile
            send ordinary CMove steps
  -> check the target again after 100 ms
```

The helper resolves the object ID again on every check. It does not retain a world-object pointer across timer callbacks. This lets it notice the target's new tile or stop safely after the object leaves the local object list.

The adjacent path is also a loop. A facing mismatch sends `CChangeDirection`, then the next timer check can attack. An already-facing character sends `CAttack` immediately and still schedules the next check. This produces repeated attack requests at the 100 ms pursuit cadence without using the Space key's separate throttle.

The client reuses [`CMove`](../network/client/006-0x06-move.md), [`CChangeDirection`](../network/client/017-0x11-change-direction.md), and [`CAttack`](../network/client/019-0x13-attack.md). The server therefore sees the same commands that keyboard movement and the Space attack key produce.

## The path search

`ui_world_pane_build_breadth_first_path` is a breadth-first search, not A*. Every edge is one cardinal tile and has the same cost, so the first reached goal has the fewest steps under the current collision state.

```c
fill(predecessor_direction, 5);       // 5 means unseen
queue.push(start);

while (!queue.empty()) {
    Tile here = queue.pop_front();

    if (here is any requested goal)
        return rebuild_path(here, start);

    for (direction = Up; direction <= Left; direction++) {
        Tile next = step(here, direction);

        if (can_move(here, direction) &&
            predecessor_direction[next] == 5) {
            predecessor_direction[next] = direction;
            queue.push_back(next);
        }
    }
}
```

The search expands directions in `Up`, `Right`, `Down`, `Left` order. `map_can_move_direction` supplies the same bounds, dynamic-object, special-state, and SOTP static-collision checks used by normal local movement.

Ground click-to-move supplies one exact goal tile. Entity pursuit supplies the target's four adjacent tiles, so the occupied target tile does not need to be passable. The route stores a direction and its source coordinates for each step. `ui_world_pane_advance_queued_path` replays the records in forward movement order and verifies that the local character is still at the expected source tile before sending the next step.

The predecessor array is a fixed 400 by 400 byte grid. The search queue reserves the current map's tile count plus 128 entries. The start tile is enqueued before it is marked, so one neighbor can enqueue it once more. Already-marked neighbors prevent that quirk from becoming a loop.

## Moving objects and doors

The search reads the live world state. `map_can_move_direction` queries the destination cell's current object list and applies the class-specific passability state for humans and monsters. When an object moves, `world_reindex_object` removes it from its old spatial cell and inserts it at its new coordinates. The next search therefore sees the new occupied and vacated tiles.

The client also validates every queued step again through `map_try_move_local_player`. A human or creature that enters a previously planned route can block the next step even before the following 100 ms search. The pursuit timer then discards that route and tries another.

Static collision is live as well. `world_static_set_tile_id` changes a static object's current tile ID. `map_can_move_direction` reads the current and destination cells' live static IDs and looks up their current [SOTP collision flags](../file-formats/sotp.md). A door transition that replaces a closed tile ID with an open one therefore changes the next movement check and path search without rebuilding the map.

These world updates do not call the pathfinder directly. The only callers of the shared search are ground click-to-move and entity pursuit. The only callers of entity pursuit are the living-object action and timer ID `10`.

This creates two different behaviors:

- Entity pursuit rebuilds from current object and door state on its next nominal 100 ms timer check.
- Ground click-to-move builds once. Every step is still revalidated, but a newly blocked step has no pursuit timer to rebuild or resume the route after the obstacle moves away. New input must start another ground path.

The search itself is synchronous on the main thread, so it sees one consistent snapshot. It does not predict where another player, creature, or door will be when a later step runs.

## Cost compared with A*

Let `V` be the number of map cells. [`SMapSize`](../network/server/021-0x15-map-size.md) supplies one-byte width and height values, so a 255 by 255 map has at most 65,025 cells. With four cardinal directions, one full breadth-first search dequeues at most 65,025 cells and tests at most 260,100 directed neighbors.

Breadth-first search runs in `O(V + E)`, which is `O(V)` on this four-neighbor grid. Its queue operations and predecessor lookup are constant time. The client also avoids the priority queue, distance scores, and heuristic calculations required by a usual A* implementation.

A* with a binary heap is `O(E log V)` in the worst case, but a Manhattan-distance heuristic usually visits far fewer cells before reaching a distant target. For pursuit, the admissible heuristic is the smallest distance to any adjacent goal:

```c
h = minimum(
    abs(tile.x - goal[i].x) +
    abs(tile.y - goal[i].y)
);
```

Both algorithms return a shortest cardinal route when A* uses that admissible heuristic. Both can still explore nearly every reachable cell when the target is enclosed or unreachable. A* also does not predict moving obstacles. It needs the same per-step validation and replanning policy.

At the pursuit cadence, an unreachable target could cause up to about 650,250 cell dequeues and 2,601,000 directional checks per second before timer delays and other main-loop work are considered. This is a bound, not a measured frame cost. `map_can_move_direction` is more expensive than an array lookup because it inspects dynamic objects and live static collision.

The client choice is reasonable for one bounded local search. BFS is simple, allocation-friendly, and guarantees the fewest tile steps. A custom system should prefer A* when searches are commonly long, several agents plan at once, or profiling shows the repeated collision checks matter.

## A bounded C-like implementation

A cleaner implementation can keep the same behavior while marking the start tile immediately. Store this workspace on the world system rather than placing the large arrays on the stack.

```c
enum {
    MAP_LIMIT = 255,
    MAX_TILES = MAP_LIMIT * MAP_LIMIT,
    DIR_START = 4,
    DIR_UNSEEN = 5
};

struct Tile {
    s32 y;
    s32 x;
};

struct PathStep {
    u8 direction;
    s32 source_y;
    s32 source_x;
};

struct PathWorkspace {
    u8 came_from[MAX_TILES];
    Tile queue[MAX_TILES];
    PathStep reverse_steps[MAX_TILES];
};
```

The FIFO search uses the live movement check. `world_can_move` must test the move from `here`, not only whether `next` looks empty, because SOTP collision is direction-specific.

```c
bool build_shortest_path(
    World *world,
    Tile start,
    Tile goals[],
    u32 goal_count,
    Path *out,
    PathWorkspace *work)
{
    u32 head = 0;
    u32 tail = 0;
    u32 direction;

    fill(work->came_from, world->width * world->height, DIR_UNSEEN);
    work->came_from[tile_index(world, start)] = DIR_START;
    work->queue[tail++] = start;

    while (head < tail) {
        Tile here = work->queue[head++];

        if (tile_is_any_goal(here, goals, goal_count))
            return rebuild_path(world, start, here, out, work);

        for (direction = 0; direction < 4; direction++) {
            Tile next;
            u32 index;

            if (!world_can_move(world, here, direction))
                continue;

            next = step_tile(here, direction);
            index = tile_index(world, next);

            if (work->came_from[index] != DIR_UNSEEN)
                continue;

            work->came_from[index] = (u8)direction;
            work->queue[tail++] = next;
        }
    }

    return false;
}
```

Reconstruction walks backward, then reverses the temporary records so the first stored step leaves `start`:

```c
bool rebuild_path(
    World *world,
    Tile start,
    Tile reached,
    Path *out,
    PathWorkspace *work)
{
    u32 count = 0;

    while (!same_tile(reached, start)) {
        u8 direction = work->came_from[tile_index(world, reached)];
        Tile source = step_tile_reverse(reached, direction);

        work->reverse_steps[count].direction = direction;
        work->reverse_steps[count].source_y = source.y;
        work->reverse_steps[count].source_x = source.x;
        count++;
        reached = source;
    }

    path_clear(out);

    while (count != 0)
        path_push(out, work->reverse_steps[--count]);

    return true;
}
```

## How following stays current

Pursuit uses timer ID `10` with a 100 ms delay. Timer entries are one-shot. Each successful pursuit check schedules the next entry with two callback values:

- the target object ID;
- the current pursuit generation.

The timer callback runs through `WorldPane`'s `TimerHandler` secondary base at `WorldPane + 0x11C`. It subtracts that adjustment, compares the callback generation with the live generation, and calls `ui_world_pane_pursue_and_auto_attack_target` again only when they match.

Each new check discards the old route, resolves the current target coordinates, and searches again. A temporarily blocked target or a failed path search is not terminal. As long as the target still resolves, the client retries at 100 ms intervals.

Successful movement is still acknowledgement-driven. A local position-change message advances the next queued step. Exhausting the current route clears its steps without changing the pursuit generation, which deliberately leaves the pending target check valid.

A small main-thread controller can reproduce that policy without holding object pointers. Starting pursuit should increment the generation before the first call. Cancellation should increment it again so an older timer cannot resume the controller.

```c
void pursuit_tick(WorldPane *world, u32 target_id, u32 generation)
{
    WorldObject_Living *target;
    WorldObject_User *self;
    Tile goals[4];

    if (generation != world->pursuit.generation)
        return;

    path_clear(&world->pursuit.route);
    target = world_find_living_by_id(world, target_id);
    self = world_get_self_user_object(world);

    if (target == 0 || self == 0) {
        cancel_pursuit(world);
        return;
    }

    if (tiles_are_adjacent(self->tile, target->tile)) {
        u8 direction = direction_to(self->tile, target->tile);

        if (self->direction != direction)
            request_change_direction(world, direction);
        else
            net_send_attack();
    } else {
        make_adjacent_goals(target->tile, goals);

        if (build_shortest_path(
                world, self->tile, goals, 4,
                &world->pursuit.route, &world->path_work)) {
            advance_queued_path(world);
        }
    }

    schedule_pursuit_timer(world, 100, target_id, generation);
}
```

## Pursuit state

The useful fields form one compact state group inside `WorldPane`:

```c
struct WorldPanePursuitState {
    bool path_active;             // WorldPane +0x294
    PathStepVector route;         // WorldPane +0x2A8
    s32 remaining_steps;          // WorldPane +0x2B8
    u32 target_id;                // WorldPane +0x2BC
    s32 target_tile_y;            // WorldPane +0x2C0
    s32 target_tile_x;            // WorldPane +0x2C4
    u32 generation;               // WorldPane +0x2C8
};
```

The stored target coordinates describe the last resolved position. The object ID is the durable lookup key. A live `WorldObject` stores that ID at `+0x24`, `tile_y` at `+0x40`, and `tile_x` at `+0x44`.

## Stop and cancellation rules

`ui_world_pane_reset_movement_state(world, 0)` is the full cancellation primitive. It increments the generation, clears the target ID, clears the queued route, and clears the active-path flag. Old timer entries are not removed immediately, but their generation check makes them inert.

Passing `1` is different. It clears the route while preserving the generation. The client uses that form when a route has run out but the scheduled entity check should continue. It is not a reliable way to cancel pursuit.

| Condition | Result |
| --- | --- |
| Target is adjacent and the character already faces it | Send `CAttack` and schedule the next 100 ms pursuit check. |
| Target is adjacent but facing differs | Send `CChangeDirection` and schedule the next check, which can then attack. |
| Target ID no longer resolves | Stop after the initial reset; no timer is requeued. |
| No route exists or a step is temporarily blocked | Keep the target and retry after 100 ms. |
| Target moves | Re-resolve its ID and rebuild the path on the next timer check. |
| Current route reaches its end | Clear the route but preserve the generation so pursuit can continue. |
| New ground click or new entity pursuit | Fully reset and replace the older path and target. |
| Keyboard direction, Shift+right movement, Space attack, or an emotion shortcut | Fully reset the current pursuit. |
| `SUserPosition`, rejected `SMove` direction `4`, map-size change, or world reinitialization | Fully reset the current pursuit. |
| Special movement state rejects a queued step | Show the normal movement error and fully reset. |

## Invoking it manually

The direct native entry point is `ui_world_pane_pursue_and_auto_attack_target`:

```c
void start_pursuit(WorldPane *world, u32 target_id)
{
    ui_world_pane_pursue_and_auto_attack_target(world, target_id);
}
```

Call it on the main game thread with the live `WorldPane` as the x86 `__thiscall` receiver. A hook already running in a `WorldPane` event, timer, or packet callback can retain that call's complete-object `this` for the duration of the dispatch. Do not hardcode a heap pointer or call through the adjusted `TimerHandler` pointer.

The ordinary UI path supplies only another live `WorldObject_Living`. The helper itself performs an ID lookup but does not repeat that RTTI check before reading the object's coordinates. A manual caller should resolve and validate the ID first. External commands should be queued and applied from the main-thread dispatcher rather than calling pane, movement, timer, or packet code from an IPC thread.

For a fixed tile without an attack, use the ground path:

```c
ui_world_pane_reset_movement_state(world, 0);

if (ui_world_pane_build_path_to_tile(
        world, self_y, self_x, goal_y, goal_x, true)) {
    ui_world_pane_advance_queued_path(world);
}
```

That path does not track an entity. A walk-only follower needs a small controller that re-resolves the target ID, chooses an adjacent goal, and invokes the lower path helpers without entering the terminal attack branch. The native entity entry point intentionally couples following and attacking.

Static addresses, the module-relative entry point, function roles, state-write comments, and the global predecessor grid are recorded in [`pathfinding.yaml`](../../analysis/exports/pathfinding.yaml).
