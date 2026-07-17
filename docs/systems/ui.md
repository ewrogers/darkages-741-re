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
    ControlList *controls       // +0x594
    s32 setup_index_a           // +0x598, purpose not fully known
    s32 setup_index_b           // +0x59C, purpose not fully known
    s32 focused_control         // +0x5AC
    s32 hovered_control         // +0x5BC
    s32 hover_zone              // +0x5C0
}
```

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

This makes a pane similar to a small game-engine node with its own surface. Layout decides where it goes, visibility decides whether it participates, and the render hook decides what pixels it contributes. See [Rendering system](../rendering/README.md) for the full frame path.

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
