# Player popup menu

Ctrl+left-clicking another visible player opens a small local action menu. The click itself sends no packet. The client waits until an action is selected, then either requests the player's information, sends a group request, or prepares a whisper.

The exact RTTI class is `PopupMenuPane`. It is a `Pane` and a `Singleton<PopupMenuPane>`. It is not a `DialogPane`, a `TextMenuDialog`, or the server-driven screen menu used by `SScreenMenu`.

## Opening the menu

The world pane first offers the pointer event to its hit-tested world objects. A living-object message then reaches `ui_world_pane_handle_living_object_message`.

```text
left-button down
  -> world-object hit test
  -> another category-1 user
  -> Ctrl flag is set
  -> ui_popup_menu_open_for_user
  -> PopupMenuPane
```

The target must not be the local player's object ID. The test checks only the Ctrl bit, so Ctrl+Shift also opens the menu. Shift without Ctrl follows the ordinary click path. The `UserClickMode` setting only suppresses the ordinary information request and does not suppress this Ctrl branch.

The popup stores the target's `u32` object ID at `+0x364`, not a pointer to the world object. Drawing and actions resolve the current name from that ID. This avoids keeping a stale object pointer when a player leaves the map.

## Pane and layout

`PopupMenuPane` loads `lpopup.txt` from `setoa.dat`. The local layout is 82 by 68 pixels:

| Name | Rectangle | Purpose |
| --- | --- | --- |
| `Noname` | `0 0 82 68` | Whole popup |
| `Box0` | `4 4 78 18` | Target name |
| `Box1` | `4 22 78 36` | Action 0 |
| `Box2` | `4 36 78 50` | Action 1 |
| `Box3` | `4 50 78 64` | Action 2 |

The popup appears at the click position and shifts left or up when its right or bottom edge would leave the parent screen. The outer pane joins both the screen hierarchy and event pane tree. An embedded `Pane` at `+0x1D0` participates in screen composition. The popup does not take mouse capture.

The primary-vtable pointer handler at slot `+0x48` performs its own row hit testing. Pointer movement updates the hover row and cursor. A left press runs the current row and closes the popup. A left press outside an action row also closes it but returns false, so the event may continue to a pane behind it. Right press and keyboard or text input also close the popup and return false.

## Actions

The English labels come from `msg.tbl` in `national.dat`. Other language tables can provide different text.

| Row | Label | Result |
| ---: | --- | --- |
| `0` | `info` | Sends [`CRequestObjectInfo`](../network/client/067-0x43-request-object-info.md) subtype `1` with the target object ID. |
| `1` | Group label | Sends [`CGroup`](../network/client/046-0x2e-group.md) action `2` with the resolved target name. |
| `2` | `whisper` | Selects the target in the tell composer and recent-recipient list. No packet is sent until the player submits text. |

The group row chooses one of three labels without changing its packet body:

| Observed roster state | Label |
| --- | --- |
| Target is not marked as grouped | `group request` |
| Target is marked as grouped and the local name is in the roster | `group disband` |
| Target is marked as grouped and the local name is absent | `currently in group` |

The server decides what action `2` means for the current group state. The popup does not edit the roster locally.

## Extending it

Changing `lpopup.txt` can reskin, resize, or reposition the existing header and three rows. It cannot add behavior by itself. The constructor, draw loop, hit test, and action dispatcher all use a fixed count of three.

Changing those loop bounds to four is unsafe. The three action rectangles occupy `+0x1A0` through `+0x1CF`, and the embedded `Pane` begins immediately at `+0x1D0`. A fourth in-object rectangle would overwrite that pane.

There are three practical extension levels:

1. Replace or specialize one existing row. Hook `ui_popup_menu_dispatch_action` and change the matching label. This keeps the native layout and lifecycle.
2. Add rows with sidecar state. Use a taller custom layout, keep extra rectangles outside the original object, and extend the draw, pointer, and action handlers together. This requires careful cleanup when the popup unregisters.
3. Replace the popup with a custom pane. Reuse the verified Ctrl-click and target-ID gate, then register a new pane with its own row collection. This is the cleanest design for several new actions.

Keep the target as an object ID and resolve it again when an action runs. Any new server action also needs protocol and server support. A hook should do only bounded main-thread UI work and must not wait for IPC or another process.

Static addresses, function roles, and evidence are kept in the [function reference](../appendix/functions.md) and [`ui-player-popup-menu.yaml`](../../analysis/exports/ui-player-popup-menu.yaml).

## Known limits

This path is confirmed statically in the matching version 741 client and against its local layout and English message assets. Live parent, sibling, and z-order state have not yet been recorded from a running session.
