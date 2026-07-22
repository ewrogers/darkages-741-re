# World objects

World objects keep the appearance and map-art state needed by the live scene. These fields belong to individual world objects, not the logged-in character's compact session record.

## World lighting state

`WorldPane` retains lighting, map, view, transfer, and object-list state in one object. The earlier lighting, map, and dynamic-object structures were overlapping views of this same layout. The constructor now accounts for most of the large prefix:

```c
struct PointerVector16 {
    void *begin;
    void *end;
    void *capacity;
    u32 state;
};

struct WorldPaneLayout {
    Pane pane;                       // +0x000, size 0x190
    void *unknown_190;
    WorldObjectList *object_list;    // +0x194
    void *unknown_198;
    void *large_buffer_owner;        // +0x19C, constructed for 0x10000 bytes
    u8 unknown_1A0[0x20];
    void *temporary_layout_resource; // +0x1C0, released and cleared by constructor
    s32 map_width;                   // +0x1C4
    s32 map_height;                  // +0x1C8
    bool map_ready;                  // +0x1CC
    u8 pad_1CD[3];
    void *child_controller_1D0;
    void *child_controller_1D4;
    u8 unknown_1D8[8];
    u32 tab_map_reference_state;     // +0x1E0
    void *tab_map_controller;        // +0x1E4
    bool light_mask_active;          // +0x1E8, HEA or forced Darkness base
    bool object_light_masks_active;  // +0x1E9, Darkness mode 3
    u8 pad_1EA[2];
    PointerVector16 light_regions;   // +0x1EC, element meaning unresolved
    u32 unknown_1FC;
    u8 ambient_intensity;            // +0x200
    u8 unknown_201;
    u16 ambient_color;               // +0x202, packed 16-bit RGB
    void *render_helper;              // +0x204, allocated as a 0x30-byte object
    bool unknown_208;
    u8 pad_209[3];
    void *world_runtime;              // +0x20C, allocated as a 0x2CC-byte object
    u8 unknown_210[8];
    u32 unknown_218;                  // constructor writes 0x12
    u8 unknown_21C[0x10];
    Pane *child_pane;                 // +0x22C, created as a 0x190-byte Pane
    u32 unknown_230;
    u32 unknown_234;
    s32 view_y;                       // +0x238
    s32 view_x;                       // +0x23C
    bool unknown_240;
    u8 unknown_241[0x0B];
    u32 unknown_24C;
    u32 unknown_250;
    u8 unknown_254[4];
    u32 map_helper;                   // +0x258, four-byte subobject
    u8 time_step;                    // +0x25C, from SChangeHour
    u8 pad_25D[3];
    u32 map_flags;                    // +0x260, full SMapSize flags byte
    u8 weather_mode;                  // +0x264, map_flags & 0x0F
    u8 pad_265[3];
    u32 previous_map_number;          // +0x268
    u32 current_map_number;           // +0x26C
    u32 unknown_270;
    bool map_enabled;                 // +0x274, separate constructor-initialized state
    bool map_transfer_active;         // +0x275
    u8 map_transfer_progress;         // +0x276, SMapPart percentage
    u8 unknown_277;
    bool unknown_278;
    bool unknown_279;
    bool unknown_27A;
    u8 pad_27B;
    MapCellStorage *map_cell_storage; // +0x27C
    bool unknown_280;
    bool unknown_281;
    u8 pad_282[2];
    u32 unknown_284;
    u8 unknown_288;
    bool unknown_289;
    bool unknown_28A;
    u8 pad_28B;
    u32 unknown_28C;
    u32 unknown_290;
    u32 unknown_294;
    PointerVector16 unknown_vector_298;
    PointerVector16 unknown_vector_2A8;
    u8 unknown_2B8[0x10];
    u32 unknown_2C8;
    WorldUserFunc *user_functions;    // +0x2CC
};

typedef WorldPaneLayout WorldPaneLightingFields;
typedef WorldPaneLayout WorldPaneMapFields;
typedef WorldPaneLayout WorldPaneDynamicObjectFields;

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

`map_cell_storage` keeps `u16` width and height fields internally and owns `width * height` six-byte map-cell records. The only live-network resize path receives its dimensions from `SMapSize`, so the wider internal types do not restore the discarded high dimension bytes.

`map_transfer_active` is set when `SMapSize` cannot accept the local cache. Both `SMap` and `SMapPart` ignore their cell data while it is clear. `SMapPart` updates `map_transfer_progress` and clears the active flag after the final row; `SMap` only writes its rectangle and leaves both completion duties untouched.

The logical Tab-map reference begins at `+0x1E0`; its raw controller pointer is at `+0x1E4`. Flag `0x40` prevents that path before the class check, while class value 2 enables Rogue zoom when the map is allowed. The packet's string8 map name is parsed but not copied into these `WorldPane` fields by the main handler.

## World position fields

World objects keep tile coordinates as signed 32-bit integers in Y, X memory order:

```c
struct WorldObjectPositionFields {
    u8 object_identity_and_state[0x38];
    s32 render_offset_y;             // +0x38, pixel displacement
    s32 render_offset_x;             // +0x3C, pixel displacement
    s32 tile_y;                      // +0x40
    s32 tile_x;                      // +0x44
};
```

[`SUserPosition`](../../network/server/004-0x04-user-position.md) carries X, Y on the wire, sign-extends both words, writes these fields, and reindexes the local `WorldObject_User`. It then copies Y, X to `WorldPane.view_y` and `WorldPane.view_x` before rebuilding the visible map state.

Despite its RTTI name, [`SAddUser`](../../network/server/068-0x44-add-user.md) does not create, insert, position, or refresh this object. Its opcode-only packet has no active consumer in version 741.

## Dynamic object index

`WorldPane` owns one shared collection for humans, creatures, and ground items. It is not a flat object array. The pointer is the `WorldPaneLayout.object_list` field at `+0x194`.

```c
struct WorldObjectListFields {
    void *vtable;                     // +0x00
    u32 busy_tag;                     // +0x04, initialized to "busy"
    u32 unknown_08;
    u8 container_0C[0x10];
    u8 id_tree[0x10];                 // +0x1C, ordered entity-ID tree
    WorldObjectIdNode *id_tree_head;  // +0x20, sentinel and tree root links
    u8 container_2C[0x10];
    u8 container_3C[0x10];
    WorldObjectCell *cells;           // +0x4C, width * height records
    WorldObjectCell *cells_end;       // +0x50
    WorldObjectCell *cells_capacity;  // +0x54
    u32 unknown_58;
    s32 width;                        // +0x5C
    s32 height;                       // +0x60
    bool unknown_64;
    u8 pad_65[3];
};                                    // size 0x68

struct WorldObjectCellFields {
    u8 unknown_00[4];
    void *unknown_04;
    u8 unknown_08[0x30];
    u32 linear_index;                 // +0x38, y * width + x
    void *link_3C;
    void *link_40;
    u32 unknown_44;
    u32 unknown_48;
    void *object_heads[4];            // +0x4C, per-cell object groups
    void *unknown_5C;
};                                    // size 0x60

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
    void *vtable;                     // +0x00
    u32 ref_count;                    // +0x04
    void *secondary_vtable;           // +0x08
    u32 busy_tag;                     // +0x0C, initialized to "busy"
    u32 unknown_10;
    u8 small_container_14[0x10];
    u32 entity_id;                    // +0x24
    u8 draw_layer;                    // +0x28, monster 0x0A, item 4
    u8 pad_029[3];
    u32 broad_category;               // +0x2C, monster 2, item 8
    bool unknown_030;
    u8 collision_level;               // +0x31
    u8 pad_032[2];
    u32 unknown_034;                  // constructor writes 1
    s32 render_offset_y;              // +0x38
    s32 render_offset_x;              // +0x3C
    s32 tile_y;                       // +0x40
    s32 tile_x;                       // +0x44
    bool inserted;                    // +0x48
    u8 pad_049[3];
    s32 unknown_04C;                  // constructor writes -1
    void *speech_pane;                // +0x50, used by world speech path
    u32 speech_state;                 // +0x54
    WorldObject_Name_Pane *name_pane; // +0x58
    void *object_light_image;         // +0x5C
    s32 cached_light_bounds[4];       // +0x60
    u32 unknown_070;                  // constructor writes 2
    u8 ground_paint[8];               // +0x74
};                                    // size 0x7C
```

The `+0x38` and `+0x3C` pair is a render-time pixel displacement. Direction-aware movement code updates it independently of the authoritative tile coordinates. The `+0x50` and `+0x54` pair is reached by world speech, but the exact lifetime and value meanings remain unresolved. The final eight bytes are the record written by `world_object_set_ground_paint`; its inner color and mode fields are not yet split confidently.

`render_collect_world_objects` uses `draw_layer` directly as one of 32 ordered queues. Ground items normally use layer 4, living objects use layer 7, monsters use layer 10, and static map art uses layer 16.

The `SDrawObjects` creation helpers remove any existing entry with the same ID before inserting the replacement. Repeated descriptions are therefore replacements, not duplicate tree nodes.

### Creature and NPC-style objects

Both creatures and Mundanes, the game's NPCs, use exact RTTI class `WorldObject_Monster`.

```c
struct LivingMotionSlot {
    bool active;                      // +0x00
    u8 pad_01[3];
    u32 channel;                      // +0x04, 0 through 3
    u32 motion_value;                 // +0x08
    u16 parameter;                    // +0x0C
    u16 pad_0E;
    u32 expires_at_tick;              // +0x10, zero means no expiry
};                                    // size 0x14

struct WorldObjectMonsterLayout {
    WorldObjectCommonFields common;   // +0x000 through +0x07B
    void *motion_records_begin;       // +0x07C
    void *motion_records_end;         // +0x080
    void *motion_records_capacity;    // +0x084
    u32 unknown_088;
    bool unknown_08C;
    u8 pad_08D[3];
    MonsterObjectImageSession *image_session; // +0x090
    ObjectImageSession *alternate_image_session; // +0x094
    bool is_local_user;               // +0x098, normally false here
    u8 pad_099[3];
    void *monster_sprite_resource;    // +0x09C
    u32 image_session_configuration;  // +0x0A0
    u8 monster_state_0A4[0x30];       // meaning unresolved
    bool nonblocking;                 // +0x0D4
    bool is_translucent;              // +0x0D5
    u8 pad_0D6[2];
    Canvas *composite_canvas;         // +0x0D8
    u8 unknown_0DC[0x20];
    bool image_or_motion_dirty;       // +0x0FC
    u8 pad_0FD[3];
    u32 motion_generation;            // +0x100
    bool uses_human_appearance;       // +0x104
    bool transition_active;           // +0x105
    u8 unknown_106[0x0A];
    bool image_enabled;               // +0x110, constructor writes 1
    bool unknown_111;
    char living_name[0x80];           // +0x112, not filled by SDrawObjects
    u8 direction;                     // +0x192
    u8 pad_193;
    LivingMotionSlot motion_slots[4]; // +0x194
    u32 render_extent_y;              // +0x1E4, resource-derived
    u32 render_extent_x;              // +0x1E8, resource-derived
    u8 creature_type;                 // +0x1EC
    u8 pad_1ED[3];
};                                    // size 0x1F0

struct MonsterPaletteMapping {
    u32 source_first;                 // +0x00, first source palette index
    u32 source_last;                  // +0x04, inclusive upper limit
    u32 palette_selector;             // +0x08, replaced from SDrawObjects
    u32 palette_family;               // +0x0C
};                                    // size 0x10

struct MonsterObjectImageSessionLayout {
    void *vtable;                     // +0x00
    u32 ref_count;                    // +0x04
    void *current_motion_data;        // +0x08
    u32 unknown_0C;
    void *monster_sprite_resource;    // +0x10
    bool resource_valid;              // +0x14, constructor writes 1
    u8 pad_15[3];
    u32 unknown_18;
    void *standing_motion_resource;   // +0x1C
    void *alternate_motion_resource;  // +0x20
    void *direction_resources[3];     // +0x24
    u8 unknown_30[8];
    bool unknown_38;
    u8 pad_39[3];
    u8 frame_descriptor[0x28];        // +0x3C
    u8 animation_state[0x34];         // +0x64
    u32 session_configuration;        // +0x98
    u8 session_option;                // +0x9C
    bool palette_overrides_active;    // +0x9D
    u8 pad_09E[2];
    MonsterPaletteMapping palette_mappings[4]; // +0xA0
    s32 palette_mapping_count;        // +0xE0, at most 4
};                                    // size 0xE4
```

The four creature bytes in [`SDrawObjects`](../../network/server/007-0x07-draw-objects.md) become the `palette_selector` fields. The client first copies each range description from the selected monster resource, then replaces only the selector. `palette_mapping_count` is the smaller of four and the number of ranges declared by that resource.

The monster image session's former `+0x14` through `+0x9C` blob is resource and playback state. It retains standing and alternate motion resources, a three-entry directional resource set, a `0x28`-byte frame descriptor, and a `0x34`-byte animation state. Their boundaries and lifetimes are confirmed, but several inner selectors remain unresolved.

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

Living objects also own four timed motion slots at `+0x194`. Each slot records a channel, motion value, 16-bit parameter, and optional expiration tick. A zero expiration means the slot has no timeout; otherwise the client stores the current tick plus the supplied duration.

### Ground items

Ground items use exact RTTI class `WorldObject_Item`.

```c
struct WorldObjectItemLayout {
    WorldObjectCommonFields common;   // +0x000 through +0x07B
    u16 sprite;                       // +0x7C, 0x8000 tag removed
    u8 pad_07E[2];
    void *item_resource_context;      // +0x80
    void *image;                      // +0x84
    s32 source_rect[4];               // +0x88
    s32 draw_rect[4];                 // +0x98
    s32 image_offset_x;               // +0xA8
    s32 image_offset_y;               // +0xAC
    s32 blend_mode;                   // +0xB0
    u8 dye_color;                     // +0xB4
    bool pointer_press_armed;          // +0xB5
    u8 pad_0B6[2];
};                                    // size 0xB8
```

The packet retains only the untagged `sprite` and `dye_color` in the item object. Its two trailing bytes are parsed but never copied into this layout or used by the item-image refresh path.

`pointer_press_armed` is set only when a pointer-press event hits the item's small interaction rectangle. Release or cancel consumes and clears it, so it is input state rather than another packet field.

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
    WorldObjectCommonFields common;   // +0x000 through +0x07B
    void *motion_records_begin;       // +0x07C
    void *motion_records_end;         // +0x080
    void *motion_records_capacity;    // +0x084
    u32 unknown_088;
    bool unknown_08C;
    u8 pad_08D[3];
    ObjectImageSession *image_session; // +0x090
    ObjectImageSession *ground_tile_image_session; // +0x094
    bool is_local_user;               // +0x098
    u8 pad_099[3];
    void *human_resource_context;     // +0x09C
    u32 image_session_configuration;  // +0x0A0
    HumanAppearanceRecord appearance; // +0xA4
    bool nonblocking_human;          // +0xD4, body sprite 2
    bool is_translucent;             // +0xD5, true only when record value is 1
    u8 pad_0D6[2];
    Canvas *composite_canvas;         // +0x0D8
    u8 unknown_0DC[0x20];
    bool image_or_motion_dirty;       // +0x0FC
    u8 pad_0FD[3];
    u32 motion_generation;            // +0x100
    bool uses_human_appearance;      // +0x104, false for monster disguise
    bool transition_active;           // +0x105
    u8 unknown_106[0x0A];
    bool image_enabled;               // +0x110
    bool unknown_111;
    char name[0x80];                 // +0x112, other players
    u8 direction;                    // +0x192
    u8 pad_193;
    LivingMotionSlot motion_slots[4]; // +0x194
    u32 render_extent_y;              // +0x1E4, constructor writes 0x3D
    u32 render_extent_x;              // +0x1E8, constructor writes 0x49
    u8 unknown_1EC;
    bool ground_tile_height1_state;  // +0x1ED, from gndattr.tbl
    u8 pad_1EE[2];
};                                   // WorldObject_Human size 0x1F0

struct HumanFramePartRecord {
    u8 state[0x14];                  // inner pointers and selectors unresolved
};                                   // size 0x14

struct HumanFramePartCache {
    u8 header[0x20];
    HumanFramePartRecord parts[21];  // +0x20
    u8 state;                        // +0x1C4
    u8 tail[0x0B];
};                                   // size 0x1D0

struct HumanPartRenderState {
    u8 state[0x50];                  // one per body/equipment category
};                                   // size 0x50

struct HumanObjectImageSessionLayout {
    void *vtable;                     // +0x000
    u32 ref_count;                    // +0x004
    void *current_motion_data;        // +0x008
    HumanAppearanceRecord appearance; // +0x0C
    void *active_motion_data;         // +0x03C
    void *standing_motion_data;       // +0x040
    u8 direction;                     // +0x044
    u8 pad_045[3];
    HumanFramePartCache frame_part_cache; // +0x048
    bool frame_parts_cached;          // +0x218
    u8 pad_219[3];
    HumanPartRenderState part_render_states[21]; // +0x21C
    u32 render_state_header;          // +0x8AC
    u8 animation_state[0x34];         // +0x8B0
    u8 unknown_8E4[0x20];
    s32 mirrored_render_offset_a;     // +0x904
    u32 unknown_908;
    s32 mirrored_render_offset_b;     // +0x90C
    s32 directional_motion_delta_a;   // +0x910
    s32 directional_motion_delta_b;   // +0x914
};                                   // size 0x918
```

The human session carries two parallel 21-entry groups. The compact `0x14`-byte records cache selected part resources and frame choices; the `0x50`-byte records hold the corresponding render state. The constructor and frame builder establish the boundaries and category count, but the inner pointer and selector meanings are not yet complete. Mirroring swaps and negates the `+0x904` and `+0x90C` pair. The final pair is multiplied by direction tables as motion advances, so both pairs are signed render displacement rather than packet appearance fields.

`WorldObject_User` derives from `WorldObject_Human` and adds 0x10 bytes, for a complete size of 0x200. Both classes therefore use the same offsets above. `image_session` points to `HumanObjectImageSession` for the normal form and `MonsterObjectImageSession` for the disguised form. `world_human_get_active_image_session` prefers `ground_tile_image_session` when it is non-null and otherwise returns `image_session`.

`ground_tile_height1_state` is initialized to zero and refreshed after position-change messages. The world controller reads the object's current map cell, looks up its ground tile ID in `gndattr.tbl`, and copies the table entry's height-1 marker here. For the local User, a nonzero value enables the privilege-or-skill movement gate. It also suppresses ordinary Human motion starts and selects a cloned image-session snapshot until the state clears. See [Movement and swimming](../../systems/movement-and-swimming.md#ground-tile-state).

The normal handler keeps two copies of the record. The world-object copy is convenient for reading current logical appearance. The image-session copy owns resource and motion selection. Applying a new record replaces the image session, so callers should not retain the old session pointer.

Overcoats suppress the ordinary pants, armor, and arms part selectors. `unknown_18` is a real internal part-sprite slot, but this packet always clears it. `rest_position` selects a standing-motion setup, although its value names remain unresolved.

Packed [`SDrawHumanObjects`](../../network/server/051-0x33-draw-human-objects.md) forms `MaleHead` and `FemaleHead` decode to body sprite `5` with M and W prefixes. `HumanObjectImageSession` then loads the small `MM005` or `WM005` motion family used for the observed swimming appearance.

Body sprite `2` sets `nonblocking_human`; Head body sprite `5` does not. Packed `MaleInvisible` and `FemaleInvisible`, or an explicit wire value of `1`, set `is_translucent`. The renderer uses that field to draw otherwise normal human layers translucently, including the server-selected See Invisible representation. These fields are separate from the [local action lock](session.md#local-user-action-state) and from static `SOTP.DAT` collision.

Project-owner protocol vocabulary names the paired body-sprite-2 forms `MaleGhost` and `FemaleGhost`; both set `nonblocking_human`. `MaleJester` provides an M-prefix body-sprite-4 form without changing this field or translucency. The image session still initializes all 21 part categories for these bodies. Ghost armor absence is not a body flag in this structure and must come from the part selectors, overcoat suppression, or unavailable art.

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
