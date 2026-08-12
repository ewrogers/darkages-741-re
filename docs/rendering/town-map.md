# Town map overlay

The town map opened from the map action, normally the `T` key, is a prepainted image with a live player marker. The client does not redraw streets from the loaded `.map` file. It loads town-specific SPF art from `national.dat`, projects the character's current tile coordinate onto that art, and draws one animated EPF marker.

This is separate from the [Tab wireframe map](tab-map.md), which builds its picture from live map cells.

## Frame composition

`TownMapPane` rebuilds its canvas in this order:

1. `_t_back.spf` supplies the 568 by 406 background.
2. `_t_icon.spf` supplies shared legend art in the local current-map mode. The server-keyed mode disables it.
3. `_tN.spf` supplies the main town image, where `N` is the selected asset number.
4. `_tNn.spf` supplies a town-name overlay at a fixed pane position.
5. `tmuser.epf` supplies the local player's marker when `N` is also the active map number.

The installed `tmuser.epf` has seven frames. The first timer delay is 100 ms, then the pane advances the frame every 50 ms. A pointer press and matching release closes the pane. The normal keyboard handler also accepts its close commands.

## Selecting the image

The pane caches two decimal text tables from `national.dat` the first time it is constructed:

```text
_tcoord.txt:  map_number  pane_x  pane_y  map_width  map_height
_tncoord.txt: key         asset   pane_x  pane_y     map_width  map_height
```

The local map action looks up the active map number in `_tcoord.txt`. Server packet [`SScreenShot`](../network/server/107-0x6b-town-map.md) instead supplies the one-byte key used with `_tncoord.txt`. Both paths then load `_t<asset>.spf` and `_t<asset>n.spf`.

The final two values are the logical map dimensions, not a fixed pixel scale. For example, the installed map 505 record is:

```text
505 165 123 50 50
```

Its `_t505.spf` frame is 216 by 109 pixels. The client therefore fits a 50 by 50 tile diamond into that 216 by 109 image and places it at pane position `(165, 123)`.

## Projecting the player position

`ui_town_map_project_position` uses the loaded SPF dimensions and the table's map dimensions. Let `(x, y)` be the live character tile coordinate, `(px, py)` the pane position, `(iw, ih)` the image size, and `(mw, mh)` the logical map size.

Ignoring integer rounding, the projection is:

```text
screen_x = px + iw * (mh + y - x) / (mw + mh)
screen_y = py + ih * (x + y) / (mw + mh)
```

Increasing map `x` moves down and left. Increasing map `y` moves down and right. The four map corners therefore land on the top, left, right, and bottom points of the image diamond.

The real function performs several signed integer divisions instead of one final division, so each term truncates toward zero. This can change the result by a pixel near some tile boundaries. It then draws the marker with its top-left corner at `(screen_x - 6, screen_y - 19)`, placing the marker's lower center near the projected point.

The coordinates are read again whenever the pane redraws. The native marker is suppressed when a server-selected asset does not match the active map number.

## Replacing the images

The images can be replaced by rebuilding `national.dat` with entries under the same names. The archive uses its ordinary fixed-name DAT format and stores these image payloads without archive-level compression.

Replacing only `_tN.spf` keeps the existing pane offset and logical dimensions. The projection automatically uses the replacement frame's pixel width and height, but the art will align only if it represents the same isometric diamond. A different-size frame may also extend beyond the 568 by 406 pane.

Changing `pane_x` and `pane_y` in `_tcoord.txt` moves both the main image and its projection. Changing `map_width` or `map_height` changes the projection scale and should match the actual map dimensions. Because the two coordinate tables are cached once per process, an archive or table replacement needs to be present before the first town map opens, or the client must be restarted.

The current SPF writer documentation is a generated inverse of the reader and is not yet production-qualified. A replacement tool should preserve unknown prefix and frame fields from a compatible source, rebuild the DAT offsets, and verify a decode, encode, decode round trip before distribution.

## Additional markers

Baking symbols into `_tN.spf` is enough for fixed landmarks. Replacing `_tNn.spf` can also change the fixed label overlay. Neither method can follow runtime objects.

The native pane has no collection of town-map markers. It draws only the local character. Dynamic markers therefore require a code hook or client change. The narrow hook point is the composition path after `_tN.spf` is drawn. For each bounded marker record, the hook can:

1. Require the marker's map number to match the displayed asset or active map, according to the desired policy.
2. Call the same projection helper with the marker's tile coordinate.
3. Load a compatible marker frame or use a retained pixmap.
4. Blit it onto the pane canvas with an explicit anchor offset.

Hooks should only read a local immutable marker snapshot and draw from the main UI thread. Marker updates, image loading, configuration parsing, and IPC must not block inside the draw hook. Moving or animated markers also need their old and new bounds invalidated; relying only on the native player's small invalidation rectangle can leave stale pixels elsewhere on the map.

Function addresses and evidence belong in the [function reference](../appendix/functions.md) and deterministic analysis exports.
