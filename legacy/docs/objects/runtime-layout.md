# Runtime layout

These are object-relative offsets in heap allocations. They are not static process addresses.

## World controller

| Offset | Type | Meaning | Confidence |
|---:|---|---|---|
| `+0x194` | pointer | `WorldObjectList` | Confirmed by lookup, insert, and erase wrappers |
| `+0x1D4` | pointer | Item resource context used during `WorldObject_Item` creation | Strong |
| `+0x1E0` | pointer | Spatial or world-state callback interface | Strong |
| `+0x20C` | pointer | Render or spatial observer used during insertion and removal | Strong |
| `+0x210` | `u32` | Local user ID | Confirmed |
| `+0x214` | `u32` | Self object ID used for list lookup | Confirmed |
| `+0x218` | `s32` | Dynamic-object retention range, initialized to `0x12` tiles | Confirmed |

## Common `WorldObject`

`object_ctor` at `0x5DB3F0` initializes the common base fields.

| Offset | Type | Meaning | Confidence |
|---:|---|---|---|
| `+0x24` | `u32` | Server object ID | Confirmed |
| `+0x28` | `u8` | Concrete render or subtype discriminator | Strong. Human `7`, monster `0x0A`, item `4` |
| `+0x2C` | `u32` | Broad category | Strong. Human/user `1`, monster `2`, item `8` |
| `+0x30` | `u8` | Enables a class-specific removal replacement or visual | Provisional |
| `+0x31` | `u8` | Collision level | Confirmed by map collision lookup |
| `+0x34` | `u32` | State initialized to `1` | Unknown semantics |
| `+0x38` | `u32` | Previous, cached, or auxiliary coordinate/state | Unknown semantics |
| `+0x3C` | `u32` | Previous, cached, or auxiliary coordinate/state | Unknown semantics |
| `+0x40` | `s32` | Map `y` | Confirmed |
| `+0x44` | `s32` | Map `x` | Confirmed |
| `+0x48` | `u8` or `u32` state | Object has been inserted into the world list | Strong |
| `+0x4C` | `s32` | Cache or sort state initialized to `-1` | Unknown semantics |
| `+0x70` | `u32` | State initialized to `2` | Unknown semantics |

Do not treat class-specific offset `+0x7C` as the object ID. The common identity used by packet handlers and `WorldObjectList` is `+0x24`.

## `WorldObject_Living`

| Offset | Type | Meaning | Confidence |
|---:|---|---|---|
| `+0x112` | character storage | Visible name copied by `object_living_set_name` at `0x5DF590` | Strong |
| `+0x192` | `u8` | Facing direction | Confirmed |

Observed allocation sizes are `0x1F0` for `WorldObject_Human`, `0x1F0` for `WorldObject_Monster`, `0x200` for `WorldObject_User`, and `0xB8` for `WorldObject_Item`.

## Object lookup and indexing

| Function | Address | Role |
|---|---:|---|
| `object_find` | `0x5C9810` | Controller wrapper around ID lookup |
| `object_list_find` | `0x5E73B0` | Finds the shared object by `object + 0x24` |
| `object_insert` | `0x5C8EA0` | Adds object to controller-owned indexes and observers |
| `object_reindex` | `0x5C92C0` | Repairs indexes after a direct coordinate change |
| `object_detach` | `0x5C9450` | Removes from controller-owned indexes and observers |
| `object_list_erase` | `0x5E6020` | Erases from cell and ID indexes |

All addresses use the executable's preferred image base of `0x400000`. With ASLR, calculate the runtime address from the loaded module base as described in the [documentation index](../README.md#address-convention).
