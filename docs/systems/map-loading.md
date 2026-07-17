# Map loading and cache

Moving to another map is both a cache lookup and a network transfer. The client first tries to reuse a complete local map. If that fails, it fills an in-memory grid from server rows, saves the whole grid once, and only then makes it active in the world.

The loading pane follows the network transfer. It is not shown while the client checks the local cache.

## Full flow

```text
SMapSize
   |
   +-- current in-memory map matches -------------------+
   |                                                    |
   +-- read maps\lod<map_id>.map and CRC matches ------+--> apply map
   |
   +-- cache miss --> CMapRequest --> SMapPart rows
                                      |
                                      +-- final-index row
                                          CRC, save, close pane, apply map
```

[`SMapSize`](../network/server/021-0x15-map-size.md) supplies the map number, one-byte dimensions, flags, and a three-byte cache value. The client resets its transfer state, prepares a grid with those dimensions, and compares the server value with its own CRC16. The CRC16 is zero-extended into the packet's three-byte slot.

The client can accept either the map already held in memory or a cache file read from `maps\lod<map_id>.map`. The disk read is synchronous. It copies cells into the grid only when the full expected `width * height * 6` bytes were read, then checks the CRC again.

If either cache source matches, `map_finish_transfer` applies it immediately. No `MapLoadingPane` is constructed for this path.

## Receiving rows

On a cache miss, the client marks the transfer active, sets progress to zero, and sends [`CMapRequest`](../network/client/005-0x05-map-request.md). Sending the request still does not show the loading pane.

The first [`SMapPart`](../network/server/060-0x3c-map-part.md) received while the transfer is active creates `MapLoadingPane`. Each packet supplies one `u16` row index followed by exactly one six-byte tile record for every X position in the prepared map width. `map_set_cell` converts the packet values into the native in-memory cell array and marks that array dirty.

The row is a network chunk within the full-map download. Runtime observations show the server sending all rows needed for the map; no standalone `SMapPart` row-patch behavior is confirmed.

The percentage is derived from the supplied row index:

```text
progress = (row_index + 1) * 100 / map_height
```

Rows therefore stream into memory, not into the cache file. [`SMap`](../network/server/006-0x06-map.md) may also update a rectangle in the same in-memory grid while a transfer is active, but it does not update progress or complete the transfer. Its surviving cells are included if a later final `SMapPart` writes the complete grid.

## Completing and saving

The client treats `row_index == map_height - 1` as completion. It then performs these steps in order:

1. Clear the active-transfer flag.
2. Recompute CRC16 across the complete in-memory grid.
3. Open the map cache with `wb` and write the complete contiguous `width * height * 6` bytes.
4. Destroy and unregister `MapLoadingPane`.
5. Install the prepared map storage into the world, rebuild the ready view at its current position, and invalidate world and lighting output.

The file write is one operation after the final-index row. There are no per-row disk writes. The packet handler ignores the writer's result, and the writer does not check the returned write count. A cache write failure therefore does not stop the client from activating the received map.

See [MAP files](../file-formats/map.md) for the persistent byte layout.

## Multiple client processes

Several clients using the same working directory also use the same relative `maps\lod<map_id>.map` path. Client 7.41 does not keep that file open after a read or write, but its embedded `fopen_s` path uses secure sharing rules while the operation is active:

| Open mode | Windows sharing | Effect on another client |
| --- | --- | --- |
| `rb` | `FILE_SHARE_READ` | Another reader may open the file, but a writer may not |
| `wb` | no sharing | Neither a reader nor another writer may open the file |

The writer opens with `CREATE_ALWAYS`, writes the complete map, then calls `fclose` before the received map is activated. A reader cannot open the truncated or partially written file during that interval. Once `fclose` flushes and releases the handle, a later client can read the completed cache and accept it when its dimensions and CRC match the new `SMapSize`.

The loading pane is destroyed after the writer returns. Its visible disappearance therefore means the cache handle has already been closed on the normal completion path.

There is one short race. If another client's cache check occurs while the exclusive writer is open, its `rb` open fails with a sharing violation. `SMapSize` treats that exactly like any other cache miss and sends `CMapRequest`; it does not retry the file during the same map entry. The reverse ordering can also matter: an existing reader blocks the first client's writer, and the ignored write failure leaves the old cache in place.

This sharing behavior is separate from the single-instance check. It also only helps clients that resolve the relative map path to the same directory. Separate installations or different process working directories have separate caches.

## Loading pane lifetime

`MapLoadingPane` loads `_nloadm.txt`, registers itself as a visible screen pane, and starts at zero percent. Its `Noname`, `Head`, `Body`, and `Tail` entries form the background and progress bar. Progress changes invalidate the pane so the bar is redrawn.

Normal completion destroys the pane. Its destructor unregisters it from the screen and clears the global singleton pointer before the new map is applied. If the transfer stalls before the first row, no pane appears. If it stalls after the first row, no timeout or separate close path was found in this map-transfer flow.

## Ordering limits

The client does not keep a received-row count or bitmap. Duplicate and out-of-order rows are accepted, and arrival of the final-index row completes the transfer even if an earlier row was never received. In that case, unchanged cells from the prepared grid can be saved and activated.

`map_set_cell` rejects coordinates outside the allocated grid, but the raw `SMapPart` handler does not visibly validate a body length before reading `map_width` records. These are client behavior limits, not recommended server behavior.
