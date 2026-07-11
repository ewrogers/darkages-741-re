# Object subsystem

The client represents dynamic map contents with an RTTI-backed `WorldObject` class family. Server object IDs are the stable link between packets and local instances.

Confirmed RTTI classes include:

```text
WorldObject
  WorldObject_Living
    WorldObject_Human
    WorldObject_Monster
    WorldObject_User
  WorldObject_Item
```

`WorldObject_User` is the local player. `WorldObject_Human` represents other human actors. `WorldObject_Monster` represents the creature and NPC-style records sent by `SDrawObjects`. There is no separate `WorldObject_NPC` RTTI class in this client. A human-looking server actor may still arrive through `SDrawHumanObjects` and use `WorldObject_Human`.

The client also contains `WorldObject_Static`, `WorldObject_Damage`, `WorldObject_Dying`, `WorldObject_Effect`, `WorldObject_ObjectEffect`, `WorldObject_StaticEffect`, `WorldObject_GroupAd`, `WorldObject_MovingEffect`, `WorldObject_Name`, and `WorldObject_Name_Pane`. These support map fixtures, temporary visuals, labels, and overlays. Their complete lifecycles are not yet documented.

Read next:

- [Object lifecycle and packets](lifecycle.md)
- [View range and refresh](view-range-and-refresh.md)
- [Self-player initialization](self-player.md)
- [Runtime layout](runtime-layout.md)

Related packet pages:

- [`SDrawObjects` (`0x07`)](../network/server/007-0x07-draw-objects.md)
- [`SDrawHumanObjects` (`0x33`)](../network/server/051-0x33-draw-human-objects.md)
- [`SMoveObject` (`0x0C`)](../network/server/012-0x0c-move-object.md)
- [`SRemoveObjects` (`0x0E`)](../network/server/014-0x0e-remove-objects.md)
- [`CRefresh` (`0x38`)](../network/client/056-0x38-refresh.md)
