# Pathfinding and following

Double-right-clicking a player or monster tells the client to walk beside that target and attack it. The client finds the route itself. It does not ask the server for a path.

This page calls that action **pursuit** because the built-in version always ends in an attack. The client has no normal follow-only button.

## What double-right-click does

The input manager turns the second nearby right-button press into pointer event type `5`. When that event lands on a living object, meaning a player or monster, `world_living_dispatch_right_click_action` builds living-object action `6`. `ui_world_pane_handle_living_object_message` then passes the object's ID to `ui_world_pane_pursue_and_auto_attack_target`.

```text
second right-button press
  -> find the clicked living object
  -> remember its object ID
  -> target is beside the local character?
       yes: turn toward it or attack
       no:  find a route to a tile beside it
            send normal movement steps
  -> check the same target again after 100 ms
```

The target ID matters more than the saved coordinates. On each new check, the client looks up that ID again and reads the target's current tile.

Movement, turning, and attacking use the ordinary [`CMove`](../network/client/006-0x06-move.md), [`CChangeDirection`](../network/client/017-0x11-change-direction.md), and [`CAttack`](../network/client/019-0x13-attack.md) senders.

## The route search

The client uses **breadth-first search**, usually shortened to **BFS**. It does not use A*.

BFS keeps a line of tiles to check. It checks the oldest tile first, then adds each new tile that can be reached from it. This spreads across the map one step at a time.

```c
bool find_path(Tile start, Tile goals[4], Path *path)
{
    clear_seen_tiles();
    queue.push(start);
    seen[start] = START;

    while (!queue.empty()) {
        Tile here = queue.pop_front();

        if (is_one_of_goals(here, goals))
            return build_path_back_to_start(here, start, path);

        for (u8 direction = UP; direction <= LEFT; direction++) {
            if (!map_can_move_direction(here, direction))
                continue;

            Tile next = step_tile(here, direction);

            if (seen[next] != UNSEEN)
                continue;

            seen[next] = direction;
            queue.push(next);
        }
    }

    return false;
}
```

Directions are checked in this order:

1. Up
2. Right
3. Down
4. Left

The first goal found has the fewest movement steps. When several shortest routes exist, that direction order helps decide which one wins.

Ground click-to-move uses one goal tile. Target pursuit uses the four tiles beside the target. The target's own occupied tile does not need to be walkable.

The client remembers which direction first reached each tile. When it finds a goal, it walks those records backward to the start, then stores the movement steps in the order they must run.

The seen-tile storage is a fixed 400 by 400 byte array. Version 741 map width and height are one byte each, so a normal map is at most 255 by 255 tiles.

## Moving players and monsters

The route search reads the current map state.

When another player or monster moves, `world_reindex_object` moves it between the world's tile lists. The next route search sees its new location.

The client also checks each saved movement step again before using it. If somebody walks into the route, that step can be blocked even though it was open when the route was built.

Entity pursuit checks the target again every 100 ms. A blocked pursuit can therefore build a different route on a later check.

## Opening and closing doors

A door change replaces the live static tile ID. Movement then reads the collision flags for that new tile ID from [`SOTP.DAT`](../file-formats/sotp.md).

Opening or closing a door does not directly call the pathfinder. Instead, the change is noticed by:

- the safety check before the next movement step; or
- the next 100 ms pursuit check.

Ground click-to-move is different. It builds one route and has no 100 ms target timer. If a door blocks that route, opening it later does not make the old ground path restart. Another click is needed.

## BFS compared with A*

[`SMapSize`](../network/server/021-0x15-map-size.md) stores one-byte width and height values. The largest normal map therefore contains:

```text
255 * 255 = 65,025 tiles
```

On a four-direction map, one full BFS can check at most 65,025 tiles and about 260,100 possible moves.

BFS is simple:

- each tile enters the queue at most once;
- queue work is cheap;
- it always finds a route with the fewest tile steps.

A* adds an estimate of how far each tile is from the goal. A common estimate is:

```c
estimate = abs(tile.x - goal.x) + abs(tile.y - goal.y);
```

That estimate often lets A* ignore much of the map. A* will usually do less work on a long route, but its priority queue costs more per checked tile.

Both algorithms can still check most of the map when a target cannot be reached. Neither predicts where a moving player will go. Both still need to check saved steps and build new routes when the world changes.

At the client's 100 ms pursuit rate, the worst theoretical case is about 650,250 checked tiles per second. This is a limit calculated from map size, not a measured frame cost.

For one character on these small maps, the client's BFS is a reasonable choice. A* becomes more useful when many characters plan routes or long searches happen often.

## How the client keeps following

Timer ID `10` runs 100 ms after each pursuit check. It carries:

- the target object ID; and
- a pursuit run number.

The run number prevents an old timer from restarting a pursuit that has already been replaced or cancelled.

Each valid timer check:

1. clears the old route;
2. finds the target by ID;
3. reads the target's new tile;
4. turns, attacks, or builds a new route;
5. schedules another check.

A failed route is not a cancellation. If the target still exists, the timer keeps trying.

Movement steps wait for local position updates. After the client learns that one step succeeded, it sends the next saved step. Reaching the end of a route clears those steps but keeps the pending target timer alive.

## Why it keeps attacking

When the target is beside the local character:

- a different facing direction sends `CChangeDirection`;
- the correct facing direction sends `CAttack`.

Both paths schedule another 100 ms check. That is why the client keeps trying to attack.

This path does not use the separate delay used by the Space-key attack handler. The server may still reject attacks according to its own combat rules.

## What stops it

`ui_world_pane_reset_movement_state(world, 0)` is the full stop operation. It:

- clears the target ID;
- clears the saved route;
- clears the active-route flag; and
- changes the pursuit run number so old timers are ignored.

Passing `1` clears the route but keeps the same run number. The client uses that form when the current route is finished but following should continue.

| Event | Result |
|---|---|
| Target disappears | Stop because its ID can no longer be found. |
| No route exists | Keep trying every 100 ms. |
| Target moves | Find its new tile and build another route. |
| Current route ends | Clear the route, but keep following. |
| New ground click or new target | Replace the old pursuit. |
| Arrow movement, Shift+right movement, Space, or an emotion shortcut | Fully stop the pursuit. |
| Position reset, rejected movement, map change, or world restart | Fully stop the pursuit. |

## Calling it manually

The built-in entry point is:

```c
void __thiscall ui_world_pane_pursue_and_auto_attack_target(
    WorldPane *world,
    u32 target_id);
```

Its RVA is `0x001F4A70`.

Call it only from the main game thread. `ECX` must contain the live, complete `WorldPane` pointer. The target ID must belong to a current living object.

This function has no options. It always means:

```text
follow until beside target
then turn and attack
repeat every 100 ms
```

There is no confirmed native entry for "follow but do not attack" or "stop three tiles away."

For one fixed tile without an attack, the ground route helpers can be used:

```c
ui_world_pane_reset_movement_state(world, 0);

if (ui_world_pane_build_path_to_tile(
        world, self_y, self_x, goal_y, goal_x, true)) {
    ui_world_pane_advance_queued_path(world);
}
```

That fixed-tile route does not keep following a moving object.

## Adding follow-only mode

A small launcher-installed runtime patch can reuse the native path search while adding:

- follow without attacking;
- a stop distance from 1 through 255 tiles;
- Shift+double-right-click as a follow-only gesture; and
- main-thread start and cancel entry points for another extension.

The unmodified client normally skips players and monsters while Shift is held, causing this gesture to fall through to its ground turn-or-step action. The patch adds a narrow exception for pointer type `5` and living-object categories `1` and `2`. Other Shift pointer actions keep their original behavior.

The default example makes Shift+double-right-click follow without attacking and stop at a shortest-path distance of three tiles. It keeps the normal 100 ms target checks, so walking starts again when the target moves away.

It does not need a DLL, but it still adds executable code to the running process. The exact hook bytes and stub are documented in [Auto-follow pathfinding](../appendix/runtime-patches/auto-follow-pathfinding.md).

The detailed Binary Ninja addresses and evidence are in [`analysis/exports/pathfinding.yaml`](../../analysis/exports/pathfinding.yaml).
