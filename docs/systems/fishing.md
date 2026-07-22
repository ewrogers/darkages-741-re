# Fishing minigame

Fishing is a self-contained client UI game. The main dialog moves a boat and hook, creates falling or rising objects, detects hook collisions, and opens a timing gauge when the hook reaches an active object. Three RTTI-backed panes share the work.

```text
FishingDialogPane
  -> boat, line, hook, and moving objects
  -> collision with an active object
  -> FishingImpactPane timing gauge
  -> FishingGetPane catch-result animation
```

The code in this subsystem does not submit a network packet directly. The dialog reports completion through the timer owner supplied by its creator. A surrounding owner may continue the game or network flow after that callback.

## Main dialog

`ui_fishing_dialog_ctor` loads `fsh_dlg.txt`, the boat view, and four loose `fsh_1.spf` through `fsh_4.spf` object sprites. It seeds the C runtime random generator and starts the main update timer at 50 ms.

The dialog handles three client key codes:

| Code | Fishing action |
| ---: | --- |
| `0x80` | Move in one horizontal direction |
| `0x82` | Move in the other horizontal direction |
| `0x20` | Lower or raise the fishing line, depending on the current phase |

The client tracks key-down and key-up separately. Direction keys change the boat offset by three units per update while it remains inside its configured bounds. The space action advances the line through its lowering, collision, impact, and return phases.

`ui_fishing_dialog_handle_timer` owns the game state machine. Each update can:

- move the boat or change line length;
- advance every moving-object record by its signed speed;
- remove an object after it leaves the canvas;
- test the hook rectangle against an object's rectangle;
- create an impact gauge after a collision;
- create new objects from one of four sprite families.

Moving objects live in a private sentinel-based list. Each record contains a sprite selector, signed speed, position, direction flag, and active state. The dialog invalidates old and new rectangles instead of redrawing the entire window for every movement.

## Boat view

The boat is a small composed view rather than another pane. `ui_fishing_boat_view_load_assets` reads `fsh_ship.txt` and loads the ship, two ordinary character frames, two fishing character frames, and the needle or hook art.

`ui_fishing_boat_view_draw` draws the selected character frame on the ship, then draws the line and hook. Its rectangle helpers combine these pieces into one dirty region. Changing the boat offset or line length invalidates the old region, recalculates the bounds, and invalidates the new region.

## Impact gauge

`FishingImpactPane` loads `fsh_bar.txt`. It draws a bar, pin, highlighted target band, and a cached moving pointer. Timer event 0 moves the pointer every 25 ms and reverses it at the bar limits.

Pressing space while the gauge is active stops accepting another press and schedules completion timer `0x1A` after 500 ms. That callback notifies the parent fishing dialog, unregisters the gauge, and queues it for deletion. The target band width and initial pointer movement are randomized when the pane is created.

## Catch result

`FishingGetPane` loads two frames from `fsh_mget.txt`. Its 50 ms timer alternates the active frame and redraws the pane. The main dialog creates this pane only when no catch-result pane is already open, centers it over the fishing canvas, and owns its later unregister and deletion path.

## Lifetime

Each pane has a `TimerHandler` secondary base at `this + 0x11C`. Its deleting-destructor thunk adjusts that pointer back to the complete pane. Closing the main dialog also closes any catch-result pane, clears the moving-object list, reports to the configured timer owner, and destroys the `DialogPane` base.
