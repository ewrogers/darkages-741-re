# World objects

World objects keep the appearance and map-art state needed by the live scene. These fields belong to individual world objects, not the logged-in character's compact session record.

## World lighting state

`WorldPane` retains the last server time step and the resolved ambient state across map setup.

```c
struct WorldPaneLightingFields {
    u8 unknown_0000[0x1E8];
    bool hea_mask_active;            // +0x1E8
    u8 unknown_1E9[0x17];
    u8 ambient_intensity;            // +0x200
    u8 unknown_201;
    u16 ambient_color;               // +0x202, packed 16-bit RGB
    u8 unknown_204[0x58];
    u8 time_step;                    // +0x25C, from SChangeHour
    u8 unknown_25D[0x0F];
    u32 map_id;                      // +0x26C
};

struct LightProfileEntry {
    void *next;                      // +0x00, container link
    u32 unknown_04;
    s32 time_start;                  // +0x08, inclusive
    s32 time_end;                    // +0x0C, inclusive
    u8 intensity;                    // +0x10
    u8 red;                          // +0x11
    u8 green;                        // +0x12
    u8 blue;                         // +0x13
    u32 flags;                       // +0x14, bit 0 prevents HEA use
};
```

The update flow is explained in [Map lighting](../../rendering/lighting.md).

## Human appearance

```c
struct HumanAppearanceRecord {
    u8 gender_resource_prefix;       // +0x00, 0 = M and 1 = W
    u8 unknown_01[5];
    u16 body_resource;               // +0x06
    u8 unknown_08[0x27];
    u8 additional_appearance_flag;   // +0x2F
};                                  // size 0x30

struct WorldObjectHumanAppearanceFields {
    u8 world_object_base[0x90];
    HumanObjectImageSession *image_session; // +0x90
    u8 unknown_094[0x10];
    HumanAppearanceRecord appearance;       // +0xA4
    bool nonblocking_human;                 // +0xD4
    bool unknown_appearance_flag;           // +0xD5
};
```

`WorldObject_User` and `WorldObject_Human` both use this appearance record. Packed [`SDrawHumanObjects`](../../network/server/051-0x33-draw-human-objects.md) variants `8` and `9` decode to body resource `5` with M and W prefixes. `HumanObjectImageSession` then loads the small `MM005` or `WM005` motion family used for the swimming form.

Body resource `2` sets `nonblocking_human`; swimming body resource `5` does not. This dynamic-object collision flag is separate from the [local action lock](session.md#local-user-action-state) and from static `SOTP.DAT` collision.

## Static world object fields

These fields are useful for wall and occluder hooks.

```text
struct WorldObjectStaticFields {
    u32 tile_id                 // +0x7C
    u8 map_side                 // +0x80, one of the two static cell layers
    StaticTileCache *cache      // +0x84
    Canvas *image               // +0x88
    bool hidden                 // +0xAC, skips drawing when set
    u32 image_tile_id           // +0xB0, input to static animation mapping
    u8 sotp_render_flags        // +0xB9
}
```

The constructor initially copies the same static tile ID into `tile_id` and `image_tile_id`. The image path applies the current `stcani.tbl` mapping to `image_tile_id` before it opens an `stc` or `sts` resource.

Function addresses and evidence notes are in the [function reference](../functions.md) and YAML exports.
