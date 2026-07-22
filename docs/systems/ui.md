# UI and panes

The UI works like a small game scene system, but it does not use one universal tree. It has three connected layers.

```text
Screen hierarchy             Event pane tree
(position and drawing)       (input and packet routing)
        |                              |
        +---------- Pane --------------+
                      |
                 DialogPane
                      |
          local controls in attach order
```

## Screen hierarchy

The spatial `HierList<Screen>` tracks screen relationships and positions. It helps answer questions such as "where is this pane on screen?" and "what is its parent position?"

`ui_screen_hierarchy_get_absolute_origin` walks this hierarchy to turn a local point into a screen point.

## Event pane tree

`EventHandlerList` is a separate parent-and-child tree used for events. `ui_pane_register_event_handler` adds a pane. `event_dispatch_pane_subtree` visits children first, then the parent.

The two trees often describe the same visible objects, but they serve different jobs. Do not assume a drawing parent is automatically the event parent.

## Dialog controls

A `DialogPane` owns a local collection of controls. Controls are added with `ui_dialog_add_control` in the order chosen by the pane constructor. That order can differ from the order of definitions in the text layout file.

```text
struct DialogPaneFields {
    ControlList *controls           // +0x594
    s32 default_action_control_index // +0x598, -1 disables
    s32 cancel_action_control_index  // +0x59C, -1 disables
    u8  dialog_drag_active          // +0x5A0
    s32 drag_anchor_x               // +0x5A4
    s32 drag_anchor_y               // +0x5A8
    s32 focused_control_index       // +0x5AC, -1 means none
    u8  control_press_active        // +0x5B0
    s32 pressed_control_index       // +0x5B4
    u8  pressed_zone                // +0x5B8
    s32 hovered_control_index       // +0x5BC, -1 means none
    u8  hover_zone                  // +0x5C0, 7 means no hit
    s32 pointer_target_control_index // +0x5C4, -1 means none
    u8  pointer_target_zone         // +0x5C8, 7 means no hit
}
```

The two former setup indexes are keyboard shortcuts. `ui_dialog_set_default_action` stores the control invoked by Enter or Space. `ui_dialog_set_cancel_action` stores the control invoked by Escape. The setters accept `-1` to disable the shortcut. Otherwise they resolve the index through the current control list, so these are attachment-order indexes rather than layout definition numbers.

Shortcut dispatch checks that the selected control is still enabled, then calls the dialog action handler with the control index and action code `8`. A focused control can retain Enter or Space for its own editing behavior instead of allowing the default action. Escape takes the cancel path directly.

| Dialog | Default | Cancel | Initial focus |
| --- | ---: | ---: | ---: |
| Login | `0` (OK) | `1` (Cancel) | `2` (Name) |
| Create user | `7` | `8` | `9` (Name) |
| Exchange | `0` (Accept) | `1` (Cancel) | None |
| Drop gold | `0` (OK) | `1` (Cancel) | `3` (Amount) |
| Message popup | `0` | `0` | None |

The pointer fields preserve three related states. A press remembers the control and hit zone where the button went down, so release activates only the same pair. The hover pair updates the control's visual zone. The pointer-target pair drives secondary enter/leave-style transition hooks. `DialogPane` uses control index `-1` and hit zone `7` as the two no-target sentinels.

Many callbacks use the control's attachment-order index as its action ID. For example, the login dialog's layout lists its edit areas before its buttons, but the constructor attaches `OK`, `Cancel`, `Name`, then `Password`. The action IDs follow the constructor order.

The layout files supply names, rectangles, art, and palette values. They do not create control classes on their own. See [UI layout files](ui-layouts.md) and the [UI layout registry](../appendix/ui-layout-registry.md).

## Pane state

Several states that look similar are independent:

- **Registered:** the pane is in the event tree.
- **Visible:** the pane can be drawn.
- **Input priority:** the pane is earlier or later in event traversal.
- **Focused control:** a dialog control receives keyboard or text input.
- **Mouse capture:** one pane receives pointer events directly.
- **Alive:** the object still exists and can safely receive calls.

When a screen behaves strangely, check each state instead of treating "shown" as one switch.

Hidden panes are skipped for pointer and keyboard input. If they remain registered, application and network events can still reach them. Hiding a pane also releases mouse capture when that pane owns it.

## Drawing hooks

The pane tree also controls drawing. `render_screen_subtree` clips a visible pane, calls its draw-to-target virtual method, and then walks its children.

Each pane can override a content hook. `ImagePane` draws an image there, while `WorldPane` draws the map and world objects. The common `ui_pane_draw_to_target` hook then copies the pane's canvas into its parent.

This makes a pane similar to a small game-engine node with its own surface. Layout decides where it goes, visibility decides whether it participates, and the render hook decides what pixels it contributes. See [Rendering system](../rendering/README.md) for the full frame path and [UI composition and compact layout](../rendering/ui-composition.md) for exact traversal order and the layout-dependent world viewport.

## Pane classes

RTTI exposes a large family of pane classes, including dialogs, controls, lists, world panes, overlays, and tabs. The inheritance data proves class relationships, but it does not prove which panes are alive at a given moment.

```text
LObject
  +-- Canvas
  |     +-- Pane
  |           +-- DialogPane
  |           +-- ControlPane
  |                 +-- ButtonControlPane
  +-- TimerHandler
        +-- also present inside Pane as a secondary base
```

The complete alphabetical list is in the [Pane type appendix](../appendix/pane-types.md). Shared object fields and handler slots are in [Pane and event layouts](../appendix/runtime/panes.md). The [function reference](../appendix/functions.md) contains registry and dialog helper addresses.
