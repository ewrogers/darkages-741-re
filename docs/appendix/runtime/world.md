# World objects

World objects keep the appearance and map-art state needed by the live scene. These fields belong to individual world objects, not the logged-in character's compact session record.

## World lighting state

`WorldPane` retains the last server time step and the resolved ambient state across map setup.

```c
struct WorldPaneLightingFields {
    u8 unknown_0000[0x1E8];
    bool light_mask_active;          // +0x1E8, HEA or forced Darkness base
    bool object_light_masks_active;  // +0x1E9, Darkness mode 3
    u8 unknown_1EA[0x16];
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

The base light mask is active for either an HEA-backed profile or forced Darkness. The adjacent object-mask flag is more specific: map mode `3` enables it so `SDrawHumanObjects` light images can be merged around visible humans. The update flow is explained in [Map lighting](../../rendering/lighting.md).

## World map state

`SMapSize` installs the active map into `WorldPane`. The dimensions are widened in memory, but client 7.41 supplies them from the packet's two low bytes.

```c
struct WorldPaneMapFields {
    u8 unknown_0000[0x1C4];
    s32 map_width;                   // +0x1C4, zero-extended packet u8
    s32 map_height;                  // +0x1C8, zero-extended packet u8
    u8 unknown_1CC[0x14];
    void *tab_map_controller;        // +0x1E0, NoMap and Rogue zoom paths
    u8 unknown_1E4[0x54];
    s32 view_y;                      // +0x238
    s32 view_x;                      // +0x23C
    u8 unknown_240[0x20];
    u32 map_flags;                   // +0x260, full SMapSize flags byte
    u8 weather_mode;                 // +0x264, map_flags & 0x0F
    u8 unknown_265[3];
    u32 previous_map_number;         // +0x268
    u32 current_map_number;          // +0x26C
    u8 unknown_270[0x0C];
    void *map_cell_storage;          // +0x27C
};
```

`map_cell_storage` keeps `u16` width and height fields internally and owns `width * height` six-byte map-cell records. The only live-network resize path receives its dimensions from `SMapSize`, so the wider internal types do not restore the discarded high dimension bytes.

The object at `tab_map_controller` serves the Tab-key map UI. Flag `0x40` prevents that path before the class check, while class value 2 enables Rogue zoom when the map is allowed. The packet's string8 map name is parsed but not copied into these `WorldPane` fields by the main handler.

## World position fields

World objects keep tile coordinates as signed 32-bit integers in Y, X memory order:

```c
struct WorldObjectPositionFields {
    u8 unknown_0000[0x40];
    s32 tile_y;                      // +0x40
    s32 tile_x;                      // +0x44
};
```

[`SUserPosition`](../../network/server/004-0x04-user-position.md) carries X, Y on the wire, sign-extends both words, writes these fields, and reindexes the local `WorldObject_User`. It then copies Y, X to `WorldPane.view_y` and `WorldPane.view_x` before rebuilding the visible map state.

## Human appearance

The normal form of `SDrawHumanObjects` is normalized into this 0x30-byte record before it reaches the renderer. The field order is not identical to the wire order.

```c
struct HumanAppearanceRecord741 {
    u8 resource_prefix;              // +0x00, 0 = male/M and 1 = female/W
    u8 pad_01;
    u16 head_sprite;                 // +0x02
    u8 hair_color;                   // +0x04
    u8 pad_05;
    u16 body_sprite;                 // +0x06
    u8 skin_color;                   // +0x08
    u8 pad_09;
    u16 arms_sprite;                 // +0x0A
    u16 boots_sprite;                // +0x0C, widened from wire u8
    u8 boots_color;                  // +0x0E
    u8 pad_0F;
    u16 pants_sprite;                // +0x10, 0 or 1 from pants color
    u8 pants_color;                  // +0x12
    u8 pad_13;
    u16 armor_sprite;                // +0x14
    u8 unknown_16;                   // +0x16, SDrawHumanObjects writes 0
    u8 pad_17;
    u16 unknown_18;                  // +0x18, SDrawHumanObjects writes 0
    u16 weapon_sprite;               // +0x1A
    u16 accessory1_sprite;           // +0x1C
    u8 accessory1_color;             // +0x1E
    u8 pad_1F;
    u16 shield_sprite;               // +0x20, widened from wire u8
    u16 overcoat_sprite;             // +0x22
    u8 overcoat_color;               // +0x24
    u8 pad_25;
    u16 accessory2_sprite;           // +0x26
    u8 accessory2_color;             // +0x28
    u8 pad_29;
    u16 accessory3_sprite;           // +0x2A
    u8 accessory3_color;             // +0x2C
    u8 rest_position;                // +0x2D
    u8 is_translucent;               // +0x2E
    u8 face_shape;                   // +0x2F
};                                   // size 0x30

struct WorldObjectHumanLayout741 {
    u8 unknown_000[0x24];
    u32 entity_id;                   // +0x24
    u8 unknown_028[0x18];
    s32 tile_y;                      // +0x40
    s32 tile_x;                      // +0x44
    u8 unknown_048[0x48];
    ObjectImageSession *image_session; // +0x90
    u8 unknown_094[0x10];
    HumanAppearanceRecord741 appearance; // +0xA4
    bool nonblocking_human;          // +0xD4, body sprite 2
    bool is_translucent;             // +0xD5, true only when record value is 1
    u8 unknown_0D6[0x2E];
    bool uses_human_appearance;      // +0x104, false for monster disguise
    u8 unknown_105[0x0D];
    char name[0x80];                 // +0x112, other players
    u8 direction;                    // +0x192
    u8 unknown_193[0x5D];
};                                   // WorldObject_Human size 0x1F0

struct HumanObjectImageSessionLayout741 {
    u8 image_session_base[0x0C];
    HumanAppearanceRecord741 appearance; // +0x0C
    u8 unknown_03C[0x8DC];
};                                   // size 0x918
```

`WorldObject_User` derives from `WorldObject_Human` and adds 0x10 bytes, for a complete size of 0x200. Both classes therefore use the same offsets above. `image_session` points to `HumanObjectImageSession` for the normal form and `MonsterObjectImageSession` for the disguised form.

The normal handler keeps two copies of the record. The world-object copy is convenient for reading current logical appearance. The image-session copy owns resource and motion selection. Applying a new record replaces the image session, so callers should not retain the old session pointer.

Overcoats suppress the ordinary pants, armor, and arms part selectors. `unknown_18` is a real internal part-sprite slot, but this packet always clears it. `rest_position` selects a standing-motion setup, although its value names remain unresolved.

Packed [`SDrawHumanObjects`](../../network/server/051-0x33-draw-human-objects.md) variants `8` and `9` decode to body sprite `5` with M and W prefixes. `HumanObjectImageSession` then loads the small `MM005` or `WM005` motion family used for the swimming form.

Body sprite `2` sets `nonblocking_human`; swimming body sprite `5` does not. Packed variants `5` and `6`, or an explicit wire value of `1`, set `is_translucent`. The renderer uses that field to draw otherwise normal human layers translucently, including the server-selected See Invisible representation. These fields are separate from the [local action lock](session.md#local-user-action-state) and from static `SOTP.DAT` collision.

An invisible player still has a live object with `entity_id`, `tile_y`, and `tile_x`. For a viewer who cannot see that player, the server supplies an all-zero appearance record and empty display strings. Body sprite `0` remains blocking, but zero part selectors leave the image session with no visible human layers. For a viewer with See Invisible, the server supplies the real appearance with `is_translucent` enabled instead.

### Transient packet object

The RTTI `SDrawHumanObjects` object exists only while the decoded packet is being handled, but its layout is useful when pausing inside the handler:

```c
struct SDrawHumanObjectsPacketLayout741 {
    u8 server_packet_base[0x10];
    u8 decoded_appearance[0x32];    // +0x10, typed in BN as HumanAppearancePacketFields741
    u8 name_style;                  // +0x42
    u8 pad_43;
    s32 name_length;                // +0x44
    char name[0x100];               // +0x48
    s32 group_ad_length;            // +0x148
    char group_ad_text[0x100];      // +0x14C
    u8 direction;                   // +0x24C
    u8 pad_24D[3];
    u32 entity_id;                  // +0x250
    s32 tile_y;                     // +0x254, sign-extended wire u16
    s32 tile_x;                     // +0x258, sign-extended wire u16
    u8 unknown_25C[4];
    s32 light_mask_id;              // +0x260
};                                  // size 0x264
```

The packet-specific `decoded_appearance` area stores fields in a parser-friendly order. Binary Ninja has it typed as `HumanAppearancePacketFields741`. `render_copy_human_appearance_record` rearranges it into `HumanAppearanceRecord741`; the packet page gives the exact wire order.

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
