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
    u8 unknown_270[5];
    bool map_transfer_active;        // +0x275
    u8 map_transfer_progress;        // +0x276, SMapPart percentage
    u8 unknown_277[5];
    void *map_cell_storage;          // +0x27C
};
```

`map_cell_storage` keeps `u16` width and height fields internally and owns `width * height` six-byte map-cell records. The only live-network resize path receives its dimensions from `SMapSize`, so the wider internal types do not restore the discarded high dimension bytes.

`map_transfer_active` is set when `SMapSize` cannot accept the local cache. Both `SMap` and `SMapPart` ignore their cell data while it is clear. `SMapPart` updates `map_transfer_progress` and clears the active flag after the final row; `SMap` only writes its rectangle and leaves both completion duties untouched.

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

Despite its RTTI name, [`SAddUser`](../../network/server/068-0x44-add-user.md) does not create, insert, position, or refresh this object. Its opcode-only packet has no active consumer in version 741.

## Dynamic object index

`WorldPane` owns one shared collection for humans, creatures, and ground items. It is not a flat object array.

```c
struct WorldPaneDynamicObjectFields {
    u8 unknown_000[0x194];
    WorldObjectList *object_list;     // +0x194
};

struct WorldObjectListFields {
    u8 unknown_00[0x20];
    WorldObjectIdNode *id_tree_head;  // +0x20, sentinel and tree root links
    u8 unknown_24[0x28];
    WorldObjectCell *cells;           // +0x4C, width * height records
    u8 unknown_50[0x0C];
    s32 width;                        // +0x5C
    s32 height;                       // +0x60
};

struct WorldObjectIdNode {
    WorldObjectIdNode *left;          // +0x00
    WorldObjectIdNode *parent;        // +0x04
    WorldObjectIdNode *right;         // +0x08
    u32 entity_id;                    // +0x0C
    WorldObject *object;              // +0x10, reference-counted
    u8 tree_state[4];                 // +0x14, color/sentinel state and padding
};
```

The ID index is an MSVC ordered tree whose subobject begins at `WorldObjectList + 0x1C`; `+0x20` is its head or sentinel pointer. Lookup searches on the server's 32-bit `entity_id` and returns the reference-counted pointer at node `+0x10`.

The spatial side is dense. `cells` contains `width * height` records of `0x60` bytes, selected as `cells + (y * width + x) * 0x60`. The object-list insertion path updates the matching cell and the ID tree, then sets the object's `inserted` byte. Movement and direct position correction reindex the same object instead of changing its ID.

All dynamic classes begin with these useful common fields:

```c
struct WorldObjectCommonFields {
    u8 unknown_000[0x24];
    u32 entity_id;                    // +0x24
    u8 draw_layer;                    // +0x28, monster 0x0A, item 4
    u8 unknown_029[3];
    u32 broad_category;               // +0x2C, monster 2, item 8
    u8 unknown_030;
    u8 collision_level;               // +0x31
    u8 unknown_032[0x0E];
    s32 tile_y;                       // +0x40
    s32 tile_x;                       // +0x44
    bool inserted;                    // +0x48
    u8 unknown_049[0x0F];
    WorldObject_Name_Pane *name_pane; // +0x58
};
```

`render_collect_world_objects` uses `draw_layer` directly as one of 32 ordered queues. Ground items normally use layer 4, living objects use layer 7, monsters use layer 10, and static map art uses layer 16.

The `SDrawObjects` creation helpers remove any existing entry with the same ID before inserting the replacement. Repeated descriptions are therefore replacements, not duplicate tree nodes.

### Creature and NPC-style objects

Both creatures and Mundanes, the game's NPCs, use exact RTTI class `WorldObject_Monster`.

```c
struct WorldObjectMonsterLayout {
    WorldObjectCommonFields common; // through +0x5B
    u8 unknown_05C[0x34];
    MonsterObjectImageSession *image_session; // +0x90
    u8 unknown_094[0x7C];
    bool unknown_110;                 // +0x110, constructor writes 1
    u8 unknown_111;
    char living_name[0x80];           // +0x112, not filled by SDrawObjects
    u8 direction;                     // +0x192
    u8 unknown_193[0x59];
    u8 creature_type;                 // +0x1EC
    u8 unknown_1ED[3];
};                                    // size 0x1F0

struct MonsterPaletteMapping {
    u32 source_first;                 // +0x00, first source palette index
    u32 source_last;                  // +0x04, inclusive upper limit
    u32 palette_selector;             // +0x08, replaced from SDrawObjects
    u32 palette_family;               // +0x0C
};                                    // size 0x10

struct MonsterObjectImageSessionLayout {
    u8 unknown_000[0x10];
    void *monster_sprite_resource;    // +0x10
    u8 unknown_014[0x89];
    bool palette_overrides_active;    // +0x9D
    u8 unknown_09E[2];
    MonsterPaletteMapping palette_mappings[4]; // +0xA0
    s32 palette_mapping_count;        // +0xE0, at most 4
};                                    // size 0xE4
```

The four creature bytes in [`SDrawObjects`](../../network/server/007-0x07-draw-objects.md) become the `palette_selector` fields. The client first copies each range description from the selected monster resource, then replaces only the selector. `palette_mapping_count` is the smaller of four and the number of ranges declared by that resource.

The `direction` byte belongs to the shared `WorldObject_Living` base. [`SChangeDirection`](../../network/server/017-0x11-change-direction.md) can update it on users, humans, and monsters after an RTTI check. A changed value also refreshes the object's directional motion or image state.

The packet's optional Mundane name does not populate `living_name`. It creates and attaches a separate name pane:

```c
struct WorldObjectNamePaneFields {
    u8 pane_bases_and_state[0x198];
    char text[0x40];                  // +0x198, at most 63 bytes plus NUL
    u8 style;                         // +0x1D8
    u8 option;                        // +0x1D9
    bool unknown_1DA;                 // +0x1DA
    u8 pad_1DB;
};                                    // size 0x1DC
```

`WorldObject_Monster.common.name_pane` points to this object. Both style bytes are zero for the `SDrawObjects` Mundane-name path.

Creature type is retained at `+0x1EC`. Construction maps types `1`, `2`, and `3` to `collision_level` values `0x96`, `0x8C`, and `0x82`; other values receive `0x78`. The map collision cache scans a tile's objects and keeps the highest value. Proposed movement also checks [`CreatureType`](../../network/protocol-types.md#creaturetype) directly: Passable value `1` never blocks, while normal instances of the other types do.

The inherited living-object byte at `+0xD4` is a separate nonblocking state. The living constructor clears it, and normal monster creation does not set it. Type `3`, project-named Solid, has a special movement branch that permits it only if this state has already become true. The client path that would set the state on a monster remains unresolved.

### Ground items

Ground items use exact RTTI class `WorldObject_Item`.

```c
struct WorldObjectItemLayout {
    WorldObjectCommonFields common; // through +0x5B
    u8 unknown_05C[0x20];
    u16 sprite;                       // +0x7C, 0x8000 tag removed
    u8 unknown_07E[2];
    void *item_resource_context;      // +0x80
    void *image;                      // +0x84
    s32 source_rect[4];               // +0x88
    s32 draw_rect[4];                 // +0x98
    s32 image_offset_x;               // +0xA8
    s32 image_offset_y;               // +0xAC
    s32 blend_mode;                   // +0xB0
    u8 dye_color;                     // +0xB4
    u8 unknown_0B5[3];
};                                    // size 0xB8
```

The packet retains only the untagged `sprite` and `dye_color` in the item object. Its two trailing bytes are parsed but never copied into this layout or used by the item-image refresh path.

## Human appearance

The normal form of `SDrawHumanObjects` is normalized into this 0x30-byte record before it reaches the renderer. The field order is not identical to the wire order.

```c
struct HumanAppearanceRecord {
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

struct WorldObjectHumanLayout {
    u8 unknown_000[0x24];
    u32 entity_id;                   // +0x24
    u8 unknown_028[0x18];
    s32 tile_y;                      // +0x40
    s32 tile_x;                      // +0x44
    u8 unknown_048[0x48];
    ObjectImageSession *image_session; // +0x90
    u8 unknown_094[0x10];
    HumanAppearanceRecord appearance; // +0xA4
    bool nonblocking_human;          // +0xD4, body sprite 2
    bool is_translucent;             // +0xD5, true only when record value is 1
    u8 unknown_0D6[0x2E];
    bool uses_human_appearance;      // +0x104, false for monster disguise
    u8 unknown_105[0x0D];
    char name[0x80];                 // +0x112, other players
    u8 direction;                    // +0x192
    u8 unknown_193[0x5D];
};                                   // WorldObject_Human size 0x1F0

struct HumanObjectImageSessionLayout {
    u8 image_session_base[0x0C];
    HumanAppearanceRecord appearance; // +0x0C
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
struct SDrawHumanObjectsPacketLayout {
    u8 server_packet_base[0x10];
    u8 decoded_appearance[0x32];    // +0x10, reconstructed as HumanAppearancePacketFields
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

The packet-specific `decoded_appearance` area stores fields in a parser-friendly order. The reconstructed type names it `HumanAppearancePacketFields`. `render_copy_human_appearance_record` rearranges it into `HumanAppearanceRecord`; the packet page gives the exact wire order.

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
