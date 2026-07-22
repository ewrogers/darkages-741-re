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
    u8  drag_bounds_enabled         // +0x5CA
    s32 minimum_drag_x              // +0x5CC
    s32 minimum_drag_y              // +0x5D0
    s32 maximum_drag_x              // +0x5D4
    s32 maximum_drag_y              // +0x5D8
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

Dialogs can optionally clamp movement to a caller-supplied rectangle. `ui_dialog_set_drag_bounds` enables the four limits, and `ui_dialog_clear_drag_bounds` disables them. The base pointer handler applies the limits after updating the pane position during a drag.

The base class also owns a title-text buffer and a background pixmap. One background helper loads a named image from the main archive or accepts an already decoded pixmap. A second helper loads a loose or archive-backed image through the general image-file path. Registering a dialog attaches every local control after the outer screen; unregistering reverses that relationship before removing the outer screen.

Many callbacks use the control's attachment-order index as its action ID. For example, the login dialog's layout lists its edit areas before its buttons, but the constructor attaches `OK`, `Cancel`, `Name`, then `Password`. The action IDs follow the constructor order.

The layout files supply names, rectangles, art, and palette values. They do not create control classes on their own. See [UI layout files](ui-layouts.md) and the [UI layout registry](../appendix/ui-layout-registry.md).

The shared `ControlPane` hierarchy supplies the native button, progress, radio, scroll, and text-edit behavior. Its exact classes and state transitions are described in [Native UI controls](ui-controls.md).

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

## Dialog drawing and alerts

`DialogPane` separates its frame from its controls. `ui_dialog_draw` calls the background and content hooks over the dialog rectangle. A named background uses the configured pixmap. Without one, the client lazily loads `DlgBack2.spf` and can tile the built-in frame pieces.

The dialog keeps the focused attachment index separately from the control objects. `ui_dialog_focused_control_uses_text_input` first checks that the focused control still exists and is enabled, then asks its virtual hook whether text input is active. The default action has its own attachment index. Refreshing it can change the control's enabled state and invalidate the expanded control rectangle.

`AlertPane` maps attachment action `0` to its first choice and action `2` to its optional second choice. `YesNoAlertPane` retains callback state and converts those choices to `true` or `false`. After dispatch, the alert unregisters, hides, and enters the normal deferred-deletion path. The exact RTTI destructor thunks adjust the `TimerHandler` secondary base by `0x11C` before destroying the complete pane.

## Dragged panes

Exact RTTI `DraggedPane` is a temporary captured pane used as the common base for dragged inventory items, map items, pictures, skills, spells, and world items. Construction captures the mouse and replaces any older active dragged pane through deferred deletion.

Pointer movement updates the pane position from a retained pointer origin. On release, the pane walks the screen hierarchy under that origin and calls its virtual drop-target hook with target-local coordinates. The walk continues until a target consumes the drop. The pane then releases capture, unregisters, hides, and enters deferred deletion.

The drag pane's visibility, capture, and lifetime remain separate states. Its owner can receive a callback during registration or removal, and the exact `TimerHandler` destructor thunk adjusts `this` by `0x11C`.

## Emoticon selector

Exact RTTI `EmoticonSelectPane_A` owns eight option rectangles and a description buffer. Pointer movement hit-tests those rectangles, invalidates the old and new option, copies the selected option description, and redraws the description area.

A pointer selection or numeric key commits an option through the retained chat owner and shared emoticon state, then closes the pane. Other mapped keys close or refresh it without choosing. The selector clamps programmatic selection to the eight valid indexes and falls back to option zero.

The shared label loader treats each configured option as two DBCS-aware text parts separated by a semicolon. `EquipPane` and `UserLookPane` draw the right-hand part beside the selected `HumanState` image.

## Equipment and character views

Exact RTTI `EquipPane` owns 18 worn-equipment entries. Each entry keeps its sprite, dye byte, name, current durability, and maximum durability. The pane draws those entries with the local character profile and can send [`CRemoveEquipment`](../network/client/068-0x44-remove-equipment.md) for a selected one-byte slot.

An attached exact RTTI `GroupViewPane` is a small owner-relative panel. It draws `equip02.epf` or `equip03.epf` and advances its expand or collapse transition through a requeued timer callback. Group state and visibility remain separate from the transition state.

Exact RTTI `UserLookPane` is the corresponding view for another character. Its decoded body carries the viewed character ID, 18 equipment records, display strings, legend data, portrait, and profile. The pane can send an ordinary group request for the displayed name or begin an exchange with the retained character ID.

## Full-screen story panes

Two early full-screen panes combine archive text, art, input, and timers without using a dialog layout.

Exact RTTI `BkStoryPane` reads `story1.tbl` through `story7.tbl`, pairs each stage with `bkstory1.epf` through `bkstory7.epf` and `backpal1.pal` through `backpal7.pal`, and reveals the buffered lines on a 150 ms timer. Enter, Space, or a pointer release advances the page. Escape closes it.

Exact RTTI `StaffPane` loads `staff.tbl` and `staff.epf`, scrolls the visible lines and art on a 20 ms timer, and closes when the loaded frame count is reached. A pointer release or Escape also closes it.

Both panes register against the root screen and event trees, hide the Windows cursor while active, and restore the cursor and `legend01.pal` when closing. `StaffPane` uses the exact RTTI `BlackHole` owner for deferred deletion after it has detached from events and timers. This keeps stale queued callbacks from targeting an already freed pane.

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
