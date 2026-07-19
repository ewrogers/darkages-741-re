# Walls and occlusion

Walls, trees, and other fixed map art become `WorldObject_Static` objects. They use the same sorted world-object draw path as characters and items.

## Why the player shows through foreground art

The client has two separate effects that can look similar.

`SOTP.DAT` flag `0x80` makes `render_static_object` draw that static tile with blend mode `0x6D`. Ground items are in layer 4, living objects are in layer 7, and static art is in layer 16, so the flagged wall or tree blends over pixels already drawn beneath it.

Mode `0x6D` uses a screen-style operation on each 16-bit color component:

```text
output = source + destination * (max - source) / max
```

The result can look dithered because of the source art and 16-bit color steps, but this path is a software blend rather than a checkerboard dither.

Later jungle trees use this mechanism when their SOTP entry contains `0x80`. It is a tile flag, not a special tree renderer.

The local player's ghostly foreground view is different. `render_collect_world_objects` saves the self draw entry at render-context offset `0x2B0`. After the normal world layers, `render_replay_layer_zero_and_self` draws that saved self entry a second time. In the normal, non-blinded state it supplies selector byte `1`, which `render_living_object` converts to blend mode 3. The wall remains unchanged while a translucent copy of the self appears over it.

## Hide static art with a launcher patch

The simplest runtime patch hides every `WorldObject_Static` draw:

| Item | Value |
| --- | --- |
| Static address | `0x005E47FF` |
| RVA | `0x001E47FF` |
| Verify | `74 05` |
| Write | `EB 00` |

The replacement takes an existing jump to the function's normal epilogue. Stack cleanup and the security-cookie check still run.

This hides walls, trees, and all other static map art. Characters, items, effects, ground tiles, and collision remain active. Use the normal [safe launcher workflow](../appendix/runtime-patches/safe-launcher.md).

## What the `?` button opens

The `?` control is `BTN_HELP`, and its normal left-click action opens the keyboard hot-key pane. The complete path is:

```text
BTN_HELP rectangle
    -> GUIBackPane action slot 0
    -> ui_gui_back_handle_pointer
    -> ui_gui_back_activate_action(action_id = 0)
    -> ui_create_hot_key_pane
    -> ui_hot_key_pane_ctor
    -> _nhotkem.txt and _nhotkey.txt
```

`ui_gui_back_layout_init_common` reads `BTN_HELP` from each GUI layout. `ui_gui_back_apply_layout` copies the active rectangle into action slot 0. On a left-button event, `ui_gui_back_handle_pointer` performs the hit test, applies the normal click debounce, and calls `ui_gui_back_activate_action`. Action 0 allocates the RTTI-backed `HotKeyPane`, whose constructor loads the two hot-key layouts and registers the pane with the screen and event trees.

The action dispatcher is the narrow hook if that button ever becomes a live toggle. A hook can consume action 0, toggle private state, and skip the original call. Every other action should pass through unchanged. The Alt-held launcher patch below does not need this hook or a DLL.

```c
if (action_id == 0) {
    item_overlay_enabled = !item_overlay_enabled;
    return;
}

original(gui_back, action_id);
```

| Hook | Static address | RVA | Whole bytes available at entry |
| --- | --- | --- | --- |
| `ui_gui_back_activate_action` | `0x005A0B70` | `0x001A0B70` | `55 8B EC 6A FF` |

## Make occluded items visible

The working no-DLL solution keeps static art unchanged and adds a separate translucent item pass while either Alt key is held.

### Capture during the world draw

A wrapper calls `render_collect_world_objects`, then copies up to 255 eligible layer-4 item entries into launcher-allocated state. It accepts only non-null objects with the exact `WorldObject_Item` vtable and ordinary blend mode 1.

### Replay after the completed pane

A second wrapper surrounds `render_world_pane_content`. It resets the capture state before the original draw. After that draw completes, it checks native EventMan Alt bit `0x01`, temporarily changes each captured item's `WorldObject_Item + 0xB0` blend mode from 1 to 3, calls `render_world_object`, and restores the mode.

This does not patch `render_item_object` or hook `render_replay_layer_zero_and_self`. It uses the item's existing mode-3 body blit directly.

The pass replays every eligible visible item, not only items proven to intersect static art. It runs after players, monsters, effects, lighting, and foreground statics. The translucent item hint is therefore technically topmost. There is no overlap filter or blinded-state check in the working implementation.

### Redraw on raw Alt events

Two more wrappers surround `input_emit_key_down` and `input_emit_key_up`. After the original input function, scan code `0x38` or `0xB8` invalidates the saved WorldPane. Pressing and releasing either Alt key therefore redraws immediately without mouse movement.

See [Hold Alt to show translucent ground-item hints](../appendix/runtime-patches/ground-item-hints.md) for the allocated state, bounded collector, replay flow, bytes, and rollback rules.

| Hook | Static address | RVA |
| --- | --- | --- |
| `input_emit_key_down` | `0x00467C10` | `0x00067C10` |
| `input_emit_key_up` | `0x00467E30` | `0x00067E30` |
| `render_world_pane_content` | `0x005CE280` | `0x001CE280` |
| `render_collect_world_objects` | `0x005D3740` | `0x001D3740` |

The frame hook replaces six whole prologue bytes. The other hooks replace five. The launcher also verifies the original static mode selector at `0x005E487D` without changing it, so normal SOTP and jungle-tree rendering remain intact.
