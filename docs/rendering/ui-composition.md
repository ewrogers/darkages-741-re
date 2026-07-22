# UI composition and compact layout

The UI and world are composed during one pane-tree walk. The map is not presented first and followed by a separate hardware UI pass. When the walker reaches `WorldPane`, that pane renders its world canvas and copies it toward the root. Later pane entries can then paint UI pixels over it before the completed root canvas is presented.

## Frame and tree order

`render_screen_tree_frame` performs the visual frame in this order:

```text
apply queued screen-hierarchy changes
        |
begin the root canvas
        |
render_screen_subtree(root)
        |
end the root canvas
        |
present the completed canvas
```

`render_screen_subtree` walks each hierarchy node's ordered child entries from index zero upward. For each visible entry it:

1. Computes the pane's absolute origin.
2. Intersects its bounds with the inherited clip and root screen.
3. Calls primary-vtable slot `0x5C`, the draw-to-target hook.
4. Recurses into that entry's child subtree.

The pane is therefore drawn before its descendants. Siblings encountered later can cover pixels from earlier siblings. A pane draw can mark the root dirty, and the presenter only copies the completed root when a redraw is needed.

The event tree is separate. Input uses child-first event propagation, while visual composition uses this parent-before-children spatial walk.

## Solid-color overlays

`AlphaScreenPane` is a small overlay pane. Its constructor resolves one palette color, and `ui_alpha_screen_pane_draw_content` fills the pane's content rectangle with that color before the normal pane-to-target copy.

`AlphaScreenPaneSegmented` builds a graduated version from 33 ordinary child panes. When the parent joins the screen tree, `ui_segmented_alpha_screen_pane_register_screen` divides its rectangle into 33 vertical strips, registers each child, and clears each child canvas with the shared overlay color. The constructor gives those children linearly stepped pane values, so the finished parent can present a segmented transition instead of one uniform overlay.

## Where the world fits

`WorldPane` overrides the content path. Its work is:

```text
ground and map backgrounds
        |
ordinary world-object layers
        |
world light mask
        |
late layer-zero objects and local player replay
        |
copy and light-blend WorldPane into its target
        |
later UI panes and descendants
```

This means the GUI can occlude world pixels, but those pixels only exist if the current `WorldPane` viewport asked the world renderer to produce them.

## Compact and large layouts

`GUIBackPane` loads two layout records:

| Layout index | File | Client initialization |
| ---: | --- | --- |
| 0 | `_nbk_s.txt` | initial compact layout |
| 1 | `_nbk_l.txt` | large layout |

`BTN_CHANGELAYOUT` calls `ui_gui_back_toggle_layout`, which flips the index and enters `ui_gui_back_apply_layout`. That function reapplies the GUI background, buttons, inventory, chat, system-message, and other child-pane geometry.

The same function also calls the live `MapInterface` at virtual slot `0x4C`. In `WorldPane_Impl` that slot reaches `render_world_apply_view_layout`. Its input is the selected layout's six-value `MAP` record:

```c
struct WorldViewLayout {
    s32 top;
    s32 left;
    s32 bottom;
    s32 right;
    s32 view_center_y;
    s32 view_center_x;
};
```

`render_world_apply_view_layout` changes the actual `WorldPane` rectangle, stores a local content rectangle with 14-pixel vertical and 28-pixel horizontal margins, updates the renderer's view center, resets view-dependent state, invalidates the light mask, and invalidates the pane. The margins match half of the 27-pixel-high by 56-pixel-wide isometric ground tile footprint.

## Does compact mode change visible tiles?

Yes. The layout switch is more than UI occlusion.

`render_ground_layer` derives the visible isometric cells from the current world-view bounds. `render_collect_world_objects` performs matching viewport and screen-bound clipping before placing objects into the 32 render queues. Since the layout toggle changes those bounds and invalidates the world caches, the next draw can visit a different number of ground cells, statics, players, items, and effects.

Visual occlusion still matters. A large GUI region can cover some world pixels after they are composed. But the client also changes the source viewport, so the extra tiles seen in the compact arrangement are not necessarily pixels that were already rendered behind the old UI.

The exact `_nbk_s.txt` and `_nbk_l.txt` `MAP` rectangles are asset data, not constants in `ui_gui_back_apply_layout`. Those private archive entries are absent from this checkout, so their pixel dimensions remain unrecorded. The executable's constructor fallback uses `top = 30`, `left = 30`, `bottom = 300`, `right = 500`, `center_y = 150`, and `center_x = 250`, but that does not prove the installed layout values.
