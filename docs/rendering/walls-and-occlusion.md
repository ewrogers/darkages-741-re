# Walls and occlusion

Walls, trees, and other fixed map art become `WorldObject_Static` objects. They use the same sorted world-object draw path as characters and items.

## Why the player shows through some art

`SOTP.DAT` supplies a render flag for each static tile. Flag `0x80` makes `render_static_object` use blend mode `0x6D` instead of normal opaque drawing.

The client draws the player first, then blends the wall or tree over the finished pixels. It does not make the player sprite transparent.

Mode `0x6D` uses a screen-style operation on each 16-bit color component:

```text
output = source + destination * (max - source) / max
```

The result can look dithered because of the source art and 16-bit color steps, but this path is a software blend rather than a checkerboard dither.

Later jungle trees use the same mechanism when their SOTP entry contains `0x80`. It is a tile flag, not a special tree renderer.

## Hide static art with a launcher patch

The simplest runtime patch hides every `WorldObject_Static` draw:

| Item | Value |
| --- | --- |
| Static address | `0x005E47FF` |
| RVA | `0x001E47FF` |
| Verify | `74 05` |
| Write | `EB 00` |

The replacement takes an existing jump to the function's normal epilogue. Stack cleanup and the security-cookie check still run.

This hides walls, trees, and all other static map art. Characters, items, effects, ground tiles, and collision remain active. Use the normal [safe launcher workflow](../appendix/runtime-patches/safe-launcher-workflow.md).

## Toggle with the `?` control

A DLL hook is a better fit for a live toggle. Two hooks are enough:

```text
GUIBackPane pointer handler
          |
          +-- left-click inside BTN_HELP
                  |
                  +-- toggle walls_visible

static-object draw hook
          |
          +-- visible: call original draw
          +-- hidden:  return without drawing
```

`ui_gui_back_handle_pointer` already reads the `BTN_HELP` rectangle for its hover tooltip. It has no help click action in this client. The old `HelpDialog` constructor also has no callers, so claiming the left-click does not replace an active dialog path.

The pointer hook can follow the same layout lookup used by the client:

```text
layout = gui_back + 0x198
       + gui_back.active_layout * 0x262C

help_rect = layout + 0xCD8
```

When a left-button event lands inside that rectangle, toggle a DLL-owned boolean, invalidate the pane, consume the event, and return. All other events call the original handler through the trampoline. Hover still reaches the original tooltip path.

The static draw hook should default to visible and never wait on IPC. A safe first version hides all static art. Later versions can offer narrower rules:

- Hide only SOTP `0x80` occluders by reading `WorldObject_Static + 0xB9`.
- Hide collision-bearing statics by reading the tile ID at `+0x7C` and checking its SOTP low nibble.
- Hide all statics for the clearest map view.

The first option removes the art that blends over the player, but it does not remove every wall. The second is closer to a wall toggle, but it also hides collidable trees and props. The renderer has no separate wall class.

For a normal x86 detour, copy complete instructions into each trampoline:

| Hook | RVA | Whole bytes available at entry |
| --- | --- | --- |
| `ui_gui_back_handle_pointer` | `0x001A0CF0` | `55 8B EC 81 EC DC 00 00 00` |
| `render_static_object` | `0x001E47E0` | `55 8B EC 83 EC 30` |

Resolve both from the loaded module base and verify the target fingerprint and bytes before installing either hook.
