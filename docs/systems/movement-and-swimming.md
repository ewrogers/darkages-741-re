# Movement and swimming

Swimming is server-directed in this client. The client can display a separate swimming body and obey a server-supplied action lock, but it does not search for a skill named Swimming or decide that a ground tile is water on its own.

## Mental model

```text
server knows map rules and character skills
    |
    +-- SUserAppearance state --> local action lock
    |
    +-- SDrawHumanObjects ------> normal or swimming body resources
                                      |
local move input --> action lock --> occupants and SOTP collision --> CMove
```

The skill's name arrives through [`SAddSkill`](../network/server/044-0x2c-add-skill.md) as display data. No client function compares that name, reserves a swimming slot, or asks the skillbook whether it is present.

## Turn or move

Directional input has a simple two-stage rule. If the requested direction differs from the local player's facing, the client turns immediately and sends [`CChangeDirection`](../network/client/017-0x11-change-direction.md). If it already matches, the client attempts one tile of movement instead.

The server answers or overrides facing with [`SChangeDirection`](../network/server/017-0x11-change-direction.md). Its object ID can select any `WorldObject_Living`, including other players, creatures, and Mundanes. This is a general world update rather than a reply limited to the local player.

## Local movement checks

`map_try_move_local_player` obtains the local `WorldObject_User`, computes the destination tile, and calls `map_can_move_direction`. A successful check moves the local object and sends [`CMove`](../network/client/006-0x06-move.md).

[`SUserPosition`](../network/server/004-0x04-user-position.md) is the authoritative reset path. It replaces the local object's tile coordinates, reindexes that object, and recenters the world view rather than applying one directional step.

`map_can_move_direction` checks these states in order:

1. Destination bounds.
2. Bit `0x01` of the saved `SUserAppearance` action state.
3. Privilege and other broad bypass conditions.
4. Dynamic occupants such as monsters and humans.
5. Direction-specific static collision from `SOTP.DAT`.

The action-state bit rejects the move before ordinary collision checks. It also restricts some non-movement actions, so it is best understood as an action lock rather than a simple movement permission.

The static collision step examines the two static tile IDs on the source and destination edges. It does not inspect the ground tile ID. See [SOTP static tile flags](../file-formats/sotp.md).

## Server acknowledgement and correction

Each accepted local step sends [`CMove`](../network/client/006-0x06-move.md) with a rolling byte counter. [`SMove`](../network/server/011-0x0b-move.md) echoes that counter and the server's previous position.

Directions `0` through `3` advance the world view from the server-supplied position. Direction `4` is a no-step correction path. It resets local movement state, returns the view to the supplied position, and sends [`CRefreshUser`](../network/client/056-0x38-refresh-user.md) when the local player's coordinates disagree. The later [`SUserPosition`](../network/server/004-0x04-user-position.md) path can replace the object's coordinates authoritatively.

The matching step echo also updates the UI network indicator. It uses the latest raw movement round-trip time and four threshold bands, not a moving average.

## Local walk interpolation

The local `ScrollLevel` preference changes only how the accepted tile step is animated. Disabled movement uses four interpolation ticks at 114 ms each. Enabled movement uses eight ticks at 57 ms each. Both sequences last 456 ms and cover the same projected tile distance.

`CMove` is sent immediately after the animation sequence is selected. The preference does not change its body, step counter, send path, or the server's movement validation. See [Game settings](game-settings.md#scroll-level-and-movement-timing) for the frame and pixel-step tables.

## Visible swimming form

[`SDrawHumanObjects`](../network/server/051-0x33-draw-human-objects.md) carries a packed appearance byte. High-nibble variants `8` and `9` select body resource `5` with M and W resource prefixes.

Those variants resolve through the `MM005` and `WM005` EPF motion families. Their body frames are only head-sized, matching the observed swimming form where most of the character is below the water surface.

The normal human renderer still draws this form. Swimming changes the selected body resources rather than switching to a dedicated water renderer.

## Server and client responsibilities

The client has no local relationship among:

- the text name `Swimming` in the skillbook;
- a ground-tile water classification;
- the swimming appearance variants;
- the `SStatus` standalone `0x02` bit.

The server must therefore decide whether the character has the skill and whether the current location counts as water. It can then send the visible appearance variant and any local action restriction needed by the client.

[`SUserAppearance`](../network/server/005-0x05-user-appearance.md) supports a state-only update. Bit `0x80` marks that form, while persistent bit `0x01` locks movement and several actions. The likely water transition is `0x81` for a locked character and `0x80` for an unlocked one, but that exact pairing still needs a water-entry capture.

The sprite half is firmer: variants `8` and `9`, body resource `5`, and the head-sized EPF families are confirmed locally and match the observed male and female swimming forms.

## Why `SStatus 0x02` is not enough

The `SStatus` parser preserves flag `0x02` in the temporary packet object, but none of the registered `SStatus` consumers reads it. It is not copied into `WorldUserFunc`, consulted by movement, or passed to the renderer.

The project protocol may still call that server-side state Swimming. In the 7.41 client, however, the working movement and appearance paths are the `SUserAppearance` action state and `SDrawHumanObjects` body variant described above.
