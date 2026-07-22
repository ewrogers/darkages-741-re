# Movement and swimming

Swimming appearance is server-directed, while the client's local swimming-like state comes from the current ground tile. `gndattr.tbl` marks selected ground tile IDs with a special height-1 attribute. A human standing on one of those tiles caches that marker and may move only when the user is privileged or the 89-entry skill array contains the name from localized message slot `0x77`.

The trigger is confirmed, but its original gameplay name is not. The supplied client files do not contain the localized label from slot `0x77`, and `gndattr.tbl` calls the shared property `ATTR_gnd_paint` rather than Swimming. The height-1 tiles, swimming body resources, item tint, and skill gate make deep water or swimming the strongest interpretation.

## Mental model

```text
gndattr.tbl height-1 tile
    |
    +-- Human/User state -------> privilege or localized skill-name check
    |                                  |
    |                            local move input
    |
    +-- ground item ------------> fixed translucent ground-paint hint

SUserAppearance action state --> action lock
SDrawHumanObjects ------------> normal or swimming body resources
```

Skill names arrive through [`SAddSkill`](../network/server/044-0x2c-add-skill.md). `map_has_special_movement_permission` scans those retained names when the local `WorldObject_Human` ground-tile state is nonzero. No fixed slot is reserved for this skill.

## Ground-tile state

`WorldControllerPane` loads `gndattr.tbl` when it is constructed. The table assigns one `ATTR_gnd_paint` record to individual ground tile IDs or inclusive ID ranges. Ordinary heights greater than `2` describe how much of an object receives the record's color. The parser reserves heights `1` and `2` as flags instead.

The first flag, height `1`, drives this movement state:

1. A Human or User position-change message reaches `ui_world_controller_handle_object_message` after the coordinates have changed.
2. The controller calls the object's primary-vtable slot `0x28`.
3. `world_human_refresh_ground_tile_state` queries the map cell at the object's current X and Y, obtains its ground tile ID, and looks up that ID in `gndattr.tbl`.
4. `world_human_set_ground_tile_state` stores the height-1 marker at `WorldObject_Human + 0x1ED`.

The constructor clears this byte. Moving onto a marked tile sets it; moving onto an unmarked tile clears it. A state change also selects or clears a cloned human image-session snapshot, refreshes direction and motion state, and changes the Human motion-start override. While the byte is set, an ordinary Human motion request returns without starting the common living-object motion timer.

Ground items use the same query differently. On a height-1 tile, `WorldObject_Item` substitutes a fixed translucent paint record with bytes `39 AE EF 80` and depth `100`. This provides a separate visual clue that the tile is a special painted or water-like surface. The height-2 flag is parsed but does not feed the Human movement gate.

## Turn or move

Directional input has a simple two-stage rule. If the requested direction differs from the local player's facing, the client turns immediately and sends [`CChangeDirection`](../network/client/017-0x11-change-direction.md). If it already matches, the client attempts one tile of movement instead.

The server answers or overrides facing with [`SChangeDirection`](../network/server/017-0x11-change-direction.md). Its object ID can select any `WorldObject_Living`, including other players, creatures, and Mundanes. This is a general world update rather than a reply limited to the local player.

## Local movement checks

`map_try_move_local_player` obtains the local `WorldObject_User`, computes the destination tile, and calls `map_can_move_direction`. A successful check moves the local object and sends [`CMove`](../network/client/006-0x06-move.md).

[`SUserPosition`](../network/server/004-0x04-user-position.md) is the authoritative reset path. It replaces the local object's tile coordinates, reindexes that object, and recenters the world view rather than applying one directional step.

The local move path checks these states in order:

1. If the local human's `gndattr.tbl` height-1 state is nonzero, any privilege or the localized skill-name match must grant permission.
2. Destination bounds.
3. Bit `0x01` of the saved `SUserAppearance` action state.
4. Privilege levels `1` and `2`, plus other broad collision-bypass conditions.
5. Dynamic occupants such as monsters and humans.
6. Direction-specific static collision from `SOTP.DAT`.

The action-state bit rejects the move before ordinary collision checks and before the privilege-level `1` or `2` collision bypass. Any nonzero privilege bypasses the separate special-state skill check, but privilege does not bypass the action lock. The lock's other exact effects are documented with [`SUserAppearance`](../network/server/005-0x05-user-appearance.md#action-state-and-partial-updates).

The static collision step examines the two live `WorldObject_Static` tile IDs on the source and destination edges. Ground tile IDs are not part of that collision test. They are consulted earlier through the cached height-1 state. A packet-driven door change therefore takes effect immediately because [`SStaticObjectState`](../network/server/050-0x32-static-object-state.md) replaces the live static tile ID that this check sends to `SOTP.DAT`. See [SOTP static tile flags](../file-formats/sotp.md).

## Server acknowledgement and correction

Each accepted local step sends [`CMove`](../network/client/006-0x06-move.md) with a rolling byte counter. [`SMove`](../network/server/011-0x0b-move.md) echoes that counter and the server's previous position.

Directions `0` through `3` advance the world view from the server-supplied position. Direction `4` is a no-step correction path. It resets local movement state, returns the view to the supplied position, and sends [`CRefreshUser`](../network/client/056-0x38-refresh-user.md) when the local player's coordinates disagree. The later [`SUserPosition`](../network/server/004-0x04-user-position.md) path can replace the object's coordinates authoritatively.

The matching step echo also updates the UI network indicator. It uses the latest raw movement round-trip time and four threshold bands, not a moving average.

## Local walk interpolation

The local `ScrollLevel` preference changes only how the accepted tile step is animated. Disabled movement uses four interpolation ticks at 114 ms each. Enabled movement uses eight ticks at 57 ms each. Both sequences last 456 ms and cover the same projected tile distance.

`CMove` is sent immediately after the animation sequence is selected. The preference does not change its body, step counter, send path, or the server's movement validation. See [Game settings](game-settings.md#scroll-level-and-movement-timing) for the frame and pixel-step tables.

## Visible swimming form

[`SDrawHumanObjects`](../network/server/051-0x33-draw-human-objects.md) carries a packed appearance byte. The project protocol calls high-nibble forms `0x80` and `0x90` `MaleHead` and `FemaleHead`. They select body resource `5` with M and W resource prefixes.

Those variants resolve through the `MM005` and `WM005` EPF motion families. Their body frames are only head-sized, matching the observed swimming form where most of the character is below the water surface.

The normal human renderer still draws this form. Swimming changes the selected body resources rather than switching to a dedicated water renderer.

## Server and client responsibilities

The client derives the local state from the current ground tile's `gndattr.tbl` height-1 marker. The visible swimming appearance variants and the `SStatus` standalone `0x02` bit remain separate paths.

The server still selects the visible Head body form and can send the local action lock. The client does not infer that form from the skill-name match.

[`SUserAppearance`](../network/server/005-0x05-user-appearance.md) supports a state-only update. Bit `0x80` marks that form, while persistent bit `0x01` locks movement and several actions. The likely water transition is `0x81` for a locked character and `0x80` for an unlocked one, but that exact pairing still needs a water-entry capture.

The sprite half is firmer: `MaleHead` and `FemaleHead`, body resource `5`, and the head-sized EPF families are confirmed locally and match the observed male and female swimming forms.

## Why `SStatus 0x02` is not enough

The `SStatus` parser preserves flag `0x02` in the temporary packet object, but none of the registered `SStatus` consumers reads it. It is not copied into `WorldUserFunc`, consulted by movement, or passed to the renderer.

The project protocol may still call that server-side state Swimming. In the 7.41 client, the confirmed pieces are the unused `SStatus` bit, the `SUserAppearance` action lock, the ground-derived skill-name check, and the `SDrawHumanObjects` body variant. Their exact server-side coordination still needs a water-entry capture.
