# Friendly function index

This report preserves useful IDA names without committing the binary database. It is generated from `ida/exports/functions.yaml` and grouped by subsystem prefix. Functions are sorted by name inside each group.

## Scope

- Target: `Darkages.exe` reporting version `741`
- Preferred image base: `0x400000`
- Friendly functions exported: `568`
- Functions with an IDA-inferred signature: `204`
- Functions still using an unknown signature: `364`
- Total functions in the IDA database at export time: `11585`

The report includes friendly subsystem names such as `net_`, `ui_`, `render_`, `audio_`, and `config_`. Generic `sub_...` functions, imports, compiler helpers, and library symbols are excluded until they receive a project name.

## Reading the report

Addresses are static virtual addresses from the IDA database. If the module is relocated at runtime, subtract the preferred image base and add the actual module base.

Signatures come from IDA type information. They are useful working assumptions, not recovered source declarations. `unknown` means IDA does not currently have a useful prototype. Verify important calling conventions and arguments against callers, stack cleanup, register use, and disassembly before relying on them.

A function name records the current project interpretation. Names beginning with `maybe_` are intentionally provisional.

## Contributing function discoveries

When you identify or improve a function:

1. Rename and comment it in IDA using the repository [agent conventions](https://github.com/ewrogers/darkages-re-741/blob/main/AGENTS.md).
2. Add or update its entry in `ida/exports/functions.yaml`.
3. Preserve the static address and function size.
4. Export the IDA prototype when useful. Use `null` when the signature is not known.
5. Run `python tools/render_function_report.py`.
6. Update any focused subsystem or packet documentation affected by the discovery.
7. Run `python tools/check_docs.py` and `mdbook build`.

Keep subsystem prefixes and the functions within each group sorted by name. New prefixes are welcome when they are clear and consistently applied.

## Subsystem summary

| Prefix | Functions |
|---|---:|
| `audio_` | `2` |
| `chat_` | `11` |
| `config_` | `15` |
| `file_` | `28` |
| `map_` | `36` |
| `net_` | `357` |
| `object_` | `33` |
| `render_` | `18` |
| `startup_` | `7` |
| `ui_` | `61` |

## `audio_` functions

| Function | Address | Size | IDA-inferred signature |
|---|---:|---:|---|
| `audio_initialize_miles_driver` | `0x5693f0` | `0x7b` | `void *__thiscall(void *this)` |
| `audio_system_ctor` | `0x568f20` | `0x9d` | `void *__thiscall(void *this)` |

## `chat_` functions

| Function | Address | Size | IDA-inferred signature |
|---|---:|---:|---|
| `chat_append_game_message_palette` | `0x4803a0` | `0x3e` | unknown |
| `chat_append_game_message_rgb` | `0x4803e0` | `0x2f` | `int __cdecl(char *Str, char, char, char)` |
| `chat_game_message_pane_append_rgb` | `0x47c5c0` | `0x122` | `int __stdcall(char *Str, char, int, char, int)` |
| `chat_game_message_pane_ctor` | `0x47c2a0` | `0x23b` | unknown |
| `chat_game_message_pane_singleton` | `0x480470` | `0xa` | unknown |
| `chat_input_pane_ctor` | `0x54fca0` | `0xed` | `int __stdcall(__int16, __int16, int, int, char, char *Str, int)` |
| `chat_input_send_say` | `0x54fd90` | `0x244` | `int __thiscall(_BYTE *this)` |
| `chat_open_say_input` | `0x54f840` | `0x18c` | `int __cdecl(int, int, int, int, char, char *Str, int)` |
| `chat_show_object_balloon` | `0x5cbf90` | `0x2a1` | unknown |
| `chat_tell_input_send` | `0x550590` | `0x185` | `int __thiscall(const char *this)` |
| `chat_world_balloon_pane_ctor` | `0x5c4f00` | `0x3bd` | unknown |

## `config_` functions

| Function | Address | Size | IDA-inferred signature |
|---|---:|---:|---|
| `config_apply_command_line_endpoint_override` | `0x433010` | `0x366` | `unsigned __int8 __thiscall(void *this)` |
| `config_build_character_profile_path` | `0x592de0` | `0x9b` | `void __cdecl(char *path, unsigned int path_size)` |
| `config_client_settings_ctor` | `0x431ff0` | `0x30a` | `void *__thiscall(void *this, const char *filename)` |
| `config_derive_install_id_checksum16` | `0x436e10` | `0xd3` | `unsigned __int16 __cdecl(unsigned int install_id)` |
| `config_detect_bad_guy_marker` | `0x431ed0` | `0xd6` | `void __cdecl(void *config)` |
| `config_detect_region_from_nfo_markers` | `0x434f00` | `0x419` | `unsigned __int8 __thiscall(void *this)` |
| `config_init_dark_ages_endpoint_and_install_ids` | `0x433380` | `0x49b` | `void __thiscall(void *this)` |
| `config_init_taiwan_endpoint` | `0x4338a0` | `0x225` | `void __thiscall(void *this)` |
| `config_load_multi_server_table` | `0x55a240` | `0x24a` | `void __thiscall(void *this)` |
| `config_load_profile_file` | `0x54da60` | `0x8a` | `unsigned __int8 __thiscall(void *this)` |
| `config_profile_ctor` | `0x54d920` | `0xa3` | `void *__thiscall(void *this, const char *filename)` |
| `config_read_settings_file` | `0x432660` | `0x6f6` | unknown |
| `config_save_multi_server_table` | `0x55a490` | `0x1b5` | `void __thiscall(void *this)` |
| `config_swap_multi_server_text_pairs` | `0x55a650` | `0x18c` | `void __thiscall(void *this)` |
| `config_write_settings_file` | `0x432340` | `0x319` | unknown |

## `file_` functions

| Function | Address | Size | IDA-inferred signature |
|---|---:|---:|---|
| `file_efa_decode_frame` | `0x457030` | `0x57c` | unknown |
| `file_efa_load_frame` | `0x456fa0` | `0x82` | unknown |
| `file_efa_read_header` | `0x456f30` | `0x6a` | `unsigned __int8 __cdecl(const char *name, unsigned int *frame_count, unsigned int *frame_delay, void *archive)` |
| `file_effect_table_load` | `0x458ed0` | `0x332` | unknown |
| `file_fastfile_close_entry` | `0x472760` | `0x2d` | `void __thiscall(void *this, void *entry)` |
| `file_fastfile_ctor` | `0x471cd0` | `0x85` | `void *__thiscall(void *this)` |
| `file_fastfile_get_entry_data` | `0x472900` | `0x61` | `void *__thiscall(void *this, void *entry)` |
| `file_fastfile_get_entry_size` | `0x472be0` | `0x26` | `int __thiscall(void *this, void *entry)` |
| `file_fastfile_get_main_archive` | `0x472c70` | `0x86` | `void *__cdecl()` |
| `file_fastfile_open_archive` | `0x471e00` | `0x4c2` | `int __thiscall(void *this, const char *filename, unsigned int handle_capacity, unsigned int xor_key)` |
| `file_fastfile_open_entry` | `0x472470` | `0x2a8` | `void *__thiscall(void *this, const char *name)` |
| `file_fastfile_read_entry` | `0x472790` | `0xca` | `int __thiscall(void *this, void *entry, void *destination, unsigned int size)` |
| `file_hea_load` | `0x4875b0` | `0xdb` | `unsigned __int8 __thiscall(void *this, const char *name, void *archive)` |
| `file_hea_view_ctor` | `0x487310` | `0x2b` | `void *__thiscall(void *this)` |
| `file_hpf_codec_singleton` | `0x4ae480` | `0xa` | `void *__cdecl()` |
| `file_hpf_decode_symbol` | `0x431c40` | `0xdb` | `unsigned int __thiscall(void *this)` |
| `file_hpf_decompress` | `0x4319b0` | `0x1c4` | `void __thiscall(void *this, const void *source, unsigned int source_size, void **output, unsigned int *output_size)` |
| `file_hpf_decompress_legacy` | `0x431860` | `0x145` | `void __thiscall(void *this, const void *source, unsigned int source_size, void **output, unsigned int *output_size)` |
| `file_hpf_decompress_stub` | `0x431840` | `0x1f` | `void __thiscall(void *this, const void *source, unsigned int source_size, void **output, unsigned int *output_size)` |
| `file_hpf_tree_initialize` | `0x431b80` | `0xb5` | `void __thiscall(void *this)` |
| `file_hpf_update_tree` | `0x431d20` | `0xf8` | `void __thiscall(void *this, unsigned int symbol)` |
| `file_mpf_load` | `0x50f490` | `0x3ac` | `unsigned __int8 __thiscall(void *this, void *archive, const char *name, int *palette_out)` |
| `file_mpf_view_ctor` | `0x50f160` | `0x75` | `void *__thiscall(void *this)` |
| `file_palette_map_read_record` | `0x547810` | `0x2cb` | `unsigned __int8 __thiscall(void *this, int *first, int *second, int *third)` |
| `file_spf_resolve_frame` | `0x4022a0` | `0x189` | `unsigned __int8 __thiscall(void *this, unsigned int frame_index, void *output, int display_variant)` |
| `file_spf_view_init` | `0x4021d0` | `0xca` | `void *__thiscall(void *this, const void *entry_data)` |
| `file_xor_u32_words` | `0x471dc0` | `0x3e` | `void __cdecl(void *data, unsigned int size, unsigned int key)` |
| `file_zlib_uncompress` | `0x6043b0` | `0x9c` | `int __cdecl(unsigned __int8 *destination, unsigned int *destination_size, const unsigned __int8 *source, unsigned int source_size)` |

## `map_` functions

| Function | Address | Size | IDA-inferred signature |
|---|---:|---:|---|
| `map_build_static_world_objects` | `0x5cd730` | `0x792` | `void __thiscall(void *this)` |
| `map_build_tile_layers` | `0x5cd3c0` | `0x36d` | `void __thiscall(void *this)` |
| `map_can_move_direction` | `0x5effe0` | `0x914` | `unsigned __int8 __thiscall(void *this, int x, int y, unsigned __int8 direction, unsigned __int16 check_static)` |
| `map_decode_palette_tile` | `0x4c7390` | `0x10b` | `unsigned __int8 __thiscall(void *this, unsigned __int16 tile_index, unsigned __int16 *destination)` |
| `map_direction_delta` | `0x5be580` | `0x65` | `__int64 __cdecl(char direction)` |
| `map_ensure_cache_directory` | `0x5b9640` | `0x12` | `void __cdecl()` |
| `map_finish_loading` | `0x5f2de0` | `0x61` | `void __thiscall(void *this, unsigned __int8 success)` |
| `map_format_cache_filename` | `0x5b9660` | `0x1e` | `int __cdecl(int map_id, char *buffer, unsigned int buffer_size)` |
| `map_format_hpf_filename` | `0x5fd850` | `0x3f` | `int __cdecl(int resource_id, int resource_type, char *buffer, unsigned int buffer_size)` |
| `map_get_collision_level` | `0x5cf5e0` | `0x232` | `unsigned __int8 __thiscall(void *this, int x, int y)` |
| `map_grid_get_ground_tile` | `0x5b9300` | `0x64` | `unsigned __int16 __thiscall(void *this, int x, int y)` |
| `map_grid_get_static_a` | `0x5b9370` | `0x65` | `unsigned __int16 __thiscall(void *this, int x, int y)` |
| `map_grid_get_static_b` | `0x5b93e0` | `0x65` | `unsigned __int16 __thiscall(void *this, int x, int y)` |
| `map_grid_initialize` | `0x5b9030` | `0x99` | `void __thiscall(void *this, unsigned int width, unsigned int height)` |
| `map_grid_load_file` | `0x5b9450` | `0x1ea` | `unsigned __int8 __thiscall(void *this, unsigned __int16 map_id)` |
| `map_grid_save_file` | `0x5b9680` | `0xfd` | `unsigned __int8 __thiscall(void *this)` |
| `map_grid_set_id` | `0x5b90d0` | `0x17` | `void __thiscall(void *this, unsigned __int16 map_id)` |
| `map_grid_set_tile` | `0x5b90f0` | `0x88` | `void __thiscall(void *this, int x, int y, unsigned __int16 ground, unsigned __int16 static_a, unsigned __int16 static_b)` |
| `map_handle_s_map_part` | `0x5f2840` | `0x21a` | `unsigned __int8 __thiscall(void *this, const void *packet)` |
| `map_handle_s_map_row` | `0x5f2a60` | `0x28a` | `unsigned __int8 __thiscall(void *this, const void *packet)` |
| `map_handle_s_map_size` | `0x5f1bf0` | `0x56d` | `unsigned __int8 __thiscall(void *this, const void *packet)` |
| `map_load_animation_tables` | `0x5873a0` | `0x3aa` | unknown |
| `map_load_ground_attribute_table` | `0x58b8c0` | `0x68` | unknown |
| `map_load_hea_resource` | `0x5c7870` | `0xc3` | `void __thiscall(void *this, int resource_id)` |
| `map_load_hpf_resource` | `0x5fd700` | `0x144` | unknown |
| `map_load_sotp_collision_flags` | `0x5cf4f0` | `0xe4` | `void __thiscall(void *this)` |
| `map_load_sotp_render_flags` | `0x5cf3b0` | `0xe7` | `void __thiscall(void *this)` |
| `map_sotp_get_collision_flags` | `0x5cf4a0` | `0x43` | `unsigned __int8 __thiscall(void *this, int static_tile_id)` |
| `map_sotp_get_render_flags` | `0x5cf360` | `0x43` | `unsigned __int8 __thiscall(void *this, int static_tile_id)` |
| `map_step_coordinate` | `0x5be600` | `0x41` | `__int64 __cdecl(int y, int x, unsigned __int8 direction)` |
| `map_tile_bank_ctor` | `0x4c7280` | `0xb1` | `void *__thiscall(void *this, const char *name, int bank_kind)` |
| `map_tile_bank_manager_ctor` | `0x4c7560` | `0x211` | unknown |
| `map_tile_layer_add` | `0x5fa540` | `0x1a0` | `unsigned __int8 __thiscall(void *this, unsigned __int16 tile_id, int x, int y, int orientation)` |
| `map_world_attach_grid` | `0x5c7970` | `0x175` | `void __thiscall(void *this, void *map_grid)` |
| `map_world_pane_ctor` | `0x5c64f0` | `0x7ec` | `void *__thiscall(void *this)` |
| `map_world_static_object_ctor` | `0x5e42f0` | `0x169` | `void *__thiscall(void *this, int tile_id, unsigned __int8 orientation, int rendering_context, unsigned __int8 render_flags, unsigned __int8 extra_flag)` |

## `net_` functions

| Function | Address | Size | IDA-inferred signature |
|---|---:|---:|---|
| `net_advance_spell_delay_say_sequence` | `0x49b870` | `0x90` | `char __thiscall(int this, int, int, int)` |
| `net_build_c_spell_delay_say_step` | `0x49bb40` | `0x1a1` | `size_t __fastcall(size_t, int, unsigned __int8)` |
| `net_build_packet_key_table` | `0x5684b0` | `0x8d` | `int __stdcall(char *Str)` |
| `net_build_packet_salt_table` | `0x568650` | `0x1ee` | unknown |
| `net_calculate_c_login_checksum16` | `0x4bcad0` | `0x5c` | `unsigned __int16 __cdecl(const unsigned __int8 *data, int length)` |
| `net_calculate_dialog_crc16` | `0x568870` | `0x5c` | `__int16 __cdecl(int, int)` |
| `net_calculate_map_crc16` | `0x5b9180` | `0x176` | `int __thiscall(_DWORD)` |
| `net_connect_and_initialize_transport` | `0x565210` | `0x172f` | unknown |
| `net_crc16_update` | `0x5b8f30` | `0x28` | `int __cdecl(unsigned __int8, unsigned __int16)` |
| `net_create_s_action_delay` | `0x5970e0` | `0x74` | unknown |
| `net_create_s_add_equip` | `0x597210` | `0x77` | unknown |
| `net_create_s_add_inventory` | `0x597380` | `0x77` | unknown |
| `net_create_s_add_skill` | `0x597510` | `0x77` | unknown |
| `net_create_s_add_spell` | `0x597640` | `0x77` | unknown |
| `net_create_s_add_user` | `0x5977b0` | `0x74` | unknown |
| `net_create_s_advertisement` | `0x5978b0` | `0x74` | unknown |
| `net_create_s_bad_guy` | `0x597a10` | `0x74` | unknown |
| `net_create_s_block_input` | `0x597b40` | `0x74` | unknown |
| `net_create_s_bounce` | `0x597c70` | `0x74` | unknown |
| `net_create_s_browser` | `0x597da0` | `0x77` | unknown |
| `net_create_s_change_direction` | `0x597f30` | `0x74` | unknown |
| `net_create_s_change_hour` | `0x598050` | `0x74` | unknown |
| `net_create_s_change_weather` | `0x598160` | `0x74` | unknown |
| `net_create_s_check_time` | `0x598270` | `0x74` | unknown |
| `net_create_s_damage_effect` | `0x598380` | `0x74` | unknown |
| `net_create_s_draw_human_objects` | `0x5984c0` | `0x77` | unknown |
| `net_create_s_draw_objects` | `0x5989c0` | `0x74` | unknown |
| `net_create_s_effect_layer` | `0x598d30` | `0x74` | unknown |
| `net_create_s_exchange` | `0x598ed0` | `0x77` | unknown |
| `net_create_s_family_name` | `0x599100` | `0x77` | unknown |
| `net_create_s_field_map` | `0x599210` | `0x77` | unknown |
| `net_create_s_group` | `0x599440` | `0x77` | unknown |
| `net_create_s_item_shop` | `0x599640` | `0x74` | unknown |
| `net_create_s_level_point` | `0x599940` | `0x74` | unknown |
| `net_create_s_manual` | `0x599a60` | `0x74` | unknown |
| `net_create_s_map` | `0x599c60` | `0x74` | unknown |
| `net_create_s_map_part` | `0x599dc0` | `0x74` | unknown |
| `net_create_s_map_size` | `0x599ee0` | `0x77` | unknown |
| `net_create_s_message` | `0x59a050` | `0x77` | unknown |
| `net_create_s_mini_game` | `0x59a1c0` | `0x74` | unknown |
| `net_create_s_motion` | `0x59a370` | `0x74` | unknown |
| `net_create_s_move` | `0x59a4a0` | `0x74` | unknown |
| `net_create_s_move_object` | `0x59a600` | `0x74` | unknown |
| `net_create_s_multi` | `0x59a740` | `0x74` | unknown |
| `net_create_s_num_users` | `0x59a870` | `0x74` | unknown |
| `net_create_s_pursuit_message` | `0x59a980` | `0x77` | unknown |
| `net_create_s_quit` | `0x59aca0` | `0x74` | unknown |
| `net_create_s_remove_equip` | `0x59adb0` | `0x74` | unknown |
| `net_create_s_remove_inventory` | `0x59aec0` | `0x74` | unknown |
| `net_create_s_remove_objects` | `0x59afd0` | `0x74` | unknown |
| `net_create_s_remove_skill` | `0x59b0e0` | `0x74` | unknown |
| `net_create_s_remove_spell` | `0x59b1f0` | `0x74` | unknown |
| `net_create_s_request_crc` | `0x59b300` | `0x74` | unknown |
| `net_create_s_request_portrait` | `0x59b410` | `0x74` | unknown |
| `net_create_s_say` | `0x59b510` | `0x77` | unknown |
| `net_create_s_screen_menu` | `0x59b640` | `0x77` | unknown |
| `net_create_s_screen_shot` | `0x59b8b0` | `0x74` | unknown |
| `net_create_s_self_look` | `0x59b9c0` | `0x77` | unknown |
| `net_create_s_self_save_ok` | `0x59bd80` | `0x74` | unknown |
| `net_create_s_sound_effect` | `0x59be80` | `0x74` | unknown |
| `net_create_s_spell_delay_cancel` | `0x59bfc0` | `0x74` | unknown |
| `net_create_s_spelled` | `0x59c0c0` | `0x74` | unknown |
| `net_create_s_static_object_state` | `0x59c1e0` | `0x77` | unknown |
| `net_create_s_status` | `0x59c360` | `0x74` | unknown |
| `net_create_s_stipulation` | `0x59c830` | `0x74` | unknown |
| `net_create_s_transfer_server` | `0x59c990` | `0x77` | unknown |
| `net_create_s_user_appearance` | `0x59cac0` | `0x74` | unknown |
| `net_create_s_user_position` | `0x59cc20` | `0x74` | unknown |
| `net_create_s_web_board` | `0x59cd40` | `0x77` | unknown |
| `net_create_s_window_change` | `0x59cf50` | `0x74` | unknown |
| `net_create_server_packet_by_opcode` | `0x596780` | `0x5b` | unknown |
| `net_decrypt_server_packet_body` | `0x567de0` | `0x1cc` | unknown |
| `net_derive_packet_key` | `0x568540` | `0x10d` | unknown |
| `net_deserialize_server_packet` | `0x5963f0` | `0xcb` | unknown |
| `net_disconnect_transport` | `0x5647d0` | `0x96` | `void __thiscall(int this, int, __int16)` |
| `net_dispatch_communications_event` | `0x5643d0` | `0x154` | `void __thiscall(_BYTE *this, int, char *, void *)` |
| `net_dispatch_game_server_message` | `0x5ed990` | `0x7fd` | `char __thiscall(_DWORD *this, int)` |
| `net_dispatch_message_to_active_client` | `0x464f40` | `0xdf` | unknown |
| `net_dispatch_or_queue_received_message` | `0x4670f0` | `0x3b` | `int __stdcall(void *Src)` |
| `net_dispatch_received_message` | `0x4647c0` | `0x40e` | unknown |
| `net_encrypt_client_packet_body` | `0x567fb0` | `0x271` | `int __stdcall(char *, int, char *Src, char)` |
| `net_enqueue_communications_event` | `0x586210` | `0x56` | `BOOL __thiscall(HANDLE *this, int, int, int)` |
| `net_handle_s_bad_guy` | `0x5f7900` | `0x195` | `char __thiscall(void *this, void *packet)` |
| `net_handle_s_change_direction` | `0x5f3bb0` | `0xc8` | `unsigned char __thiscall(void *this, const void *packet)` |
| `net_handle_s_damage_effect` | `0x5f40f0` | `0x7e` | `unsigned char __thiscall(void *this, const void *packet)` |
| `net_handle_s_draw_human_objects` | `0x5f3340` | `0x5f0` | `unsigned char __thiscall(void *this, const void *packet)` |
| `net_handle_s_draw_objects` | `0x5f3150` | `0x1eb` | `unsigned char __thiscall(void *this, const void *packet)` |
| `net_handle_s_enter_editing_mode` | `0x5f71c0` | `0x87` | unknown |
| `net_handle_s_message` | `0x5f6d80` | `0x3fe` | unknown |
| `net_handle_s_motion` | `0x5f3c80` | `0x17b` | `unsigned char __thiscall(void *this, const void *packet)` |
| `net_handle_s_move` | `0x5f2fc0` | `0x13f` | `unsigned char __thiscall(void *this, const void *packet)` |
| `net_handle_s_move_object` | `0x5f3930` | `0x27a` | `unsigned char __thiscall(void *this, const void *packet)` |
| `net_handle_s_remove_objects` | `0x5f3100` | `0x4b` | `unsigned char __thiscall(void *this, const void *packet)` |
| `net_handle_s_request_crc` | `0x5f2cf0` | `0xe4` | `char __stdcall(int)` |
| `net_handle_s_say` | `0x5f3e00` | `0xa9` | unknown |
| `net_handle_s_show_paper` | `0x5f7250` | `0x87` | `char __stdcall(int)` |
| `net_handle_s_transfer_server_packet` | `0x4b9510` | `0x162` | `char __stdcall(int)` |
| `net_handle_s_user_appearance` | `0x5f2e90` | `0x67` | `unsigned char __thiscall(void *this, const void *packet)` |
| `net_handle_s_user_position` | `0x5f2f00` | `0xb6` | `unsigned char __thiscall(void *this, const void *packet)` |
| `net_handle_s_version_check_raw` | `0x4b7f80` | `0x494` | unknown |
| `net_init_s_action_delay_factory` | `0x667a40` | `0x19` | unknown |
| `net_init_s_add_equip_factory` | `0x667a60` | `0x19` | unknown |
| `net_init_s_add_inventory_factory` | `0x667a80` | `0x19` | unknown |
| `net_init_s_add_skill_factory` | `0x667aa0` | `0x19` | unknown |
| `net_init_s_add_spell_factory` | `0x667ac0` | `0x19` | unknown |
| `net_init_s_add_user_factory` | `0x667ae0` | `0x19` | unknown |
| `net_init_s_advertisement_factory` | `0x667b00` | `0x19` | unknown |
| `net_init_s_bad_guy_factory` | `0x667b20` | `0x19` | unknown |
| `net_init_s_block_input_factory` | `0x667b40` | `0x19` | unknown |
| `net_init_s_bounce_factory` | `0x667b60` | `0x19` | unknown |
| `net_init_s_browser_factory` | `0x667b80` | `0x19` | unknown |
| `net_init_s_change_direction_factory` | `0x667ba0` | `0x19` | unknown |
| `net_init_s_change_hour_factory` | `0x667bc0` | `0x19` | unknown |
| `net_init_s_change_weather_factory` | `0x667be0` | `0x19` | unknown |
| `net_init_s_check_time_factory` | `0x667c00` | `0x19` | unknown |
| `net_init_s_damage_effect_factory` | `0x667c20` | `0x19` | unknown |
| `net_init_s_draw_human_objects_factory` | `0x667c40` | `0x19` | unknown |
| `net_init_s_draw_objects_factory` | `0x667c60` | `0x19` | unknown |
| `net_init_s_effect_layer_factory` | `0x667c80` | `0x19` | unknown |
| `net_init_s_exchange_factory` | `0x667ca0` | `0x19` | unknown |
| `net_init_s_family_name_factory` | `0x667cc0` | `0x19` | unknown |
| `net_init_s_field_map_factory` | `0x667ce0` | `0x19` | unknown |
| `net_init_s_group_factory` | `0x667d00` | `0x19` | unknown |
| `net_init_s_item_shop_factory` | `0x667d20` | `0x19` | unknown |
| `net_init_s_level_point_factory` | `0x667d40` | `0x19` | unknown |
| `net_init_s_manual_factory` | `0x667d60` | `0x19` | unknown |
| `net_init_s_map_factory` | `0x667d80` | `0x19` | unknown |
| `net_init_s_map_part_factory` | `0x667da0` | `0x19` | unknown |
| `net_init_s_map_size_factory` | `0x667dc0` | `0x19` | unknown |
| `net_init_s_message_factory` | `0x667de0` | `0x19` | unknown |
| `net_init_s_mini_game_factory` | `0x667e00` | `0x19` | unknown |
| `net_init_s_motion_factory` | `0x667e20` | `0x19` | `int()` |
| `net_init_s_move_factory` | `0x667e40` | `0x19` | `int()` |
| `net_init_s_move_object_factory` | `0x667e60` | `0x19` | `int()` |
| `net_init_s_multi_factory` | `0x667e80` | `0x19` | unknown |
| `net_init_s_num_users_factory` | `0x667ea0` | `0x19` | unknown |
| `net_init_s_pursuit_message_factory` | `0x667ec0` | `0x19` | unknown |
| `net_init_s_quit_factory` | `0x667ee0` | `0x19` | unknown |
| `net_init_s_remove_equip_factory` | `0x667f00` | `0x19` | unknown |
| `net_init_s_remove_inventory_factory` | `0x667f20` | `0x19` | unknown |
| `net_init_s_remove_objects_factory` | `0x667f40` | `0x19` | unknown |
| `net_init_s_remove_skill_factory` | `0x667f60` | `0x19` | unknown |
| `net_init_s_remove_spell_factory` | `0x667f80` | `0x19` | unknown |
| `net_init_s_request_crc_factory` | `0x667fa0` | `0x19` | unknown |
| `net_init_s_request_portrait_factory` | `0x667fc0` | `0x19` | unknown |
| `net_init_s_say_factory` | `0x667fe0` | `0x19` | unknown |
| `net_init_s_screen_menu_factory` | `0x668000` | `0x19` | `int()` |
| `net_init_s_screen_shot_factory` | `0x668020` | `0x19` | unknown |
| `net_init_s_self_look_factory` | `0x668040` | `0x19` | unknown |
| `net_init_s_self_save_ok_factory` | `0x668060` | `0x19` | unknown |
| `net_init_s_sound_effect_factory` | `0x668080` | `0x19` | unknown |
| `net_init_s_spell_delay_cancel_factory` | `0x6680a0` | `0x19` | unknown |
| `net_init_s_spelled_factory` | `0x6680c0` | `0x19` | unknown |
| `net_init_s_static_object_state_factory` | `0x6680e0` | `0x19` | unknown |
| `net_init_s_status_factory` | `0x668100` | `0x19` | unknown |
| `net_init_s_stipulation_factory` | `0x668120` | `0x19` | unknown |
| `net_init_s_transfer_server_factory` | `0x668140` | `0x19` | unknown |
| `net_init_s_user_appearance_factory` | `0x668160` | `0x19` | unknown |
| `net_init_s_user_position_factory` | `0x668180` | `0x19` | unknown |
| `net_init_s_web_board_factory` | `0x6681a0` | `0x19` | unknown |
| `net_init_s_window_change_factory` | `0x6681c0` | `0x19` | unknown |
| `net_invoke_packet_factory` | `0x54ed50` | `0x20` | unknown |
| `net_maybe_build_c_profile_packet` | `0x54ce10` | `0x755` | `void *__cdecl(_DWORD *)` |
| `net_md5_bytes_to_hex` | `0x4c7cd0` | `0xa7` | unknown |
| `net_md5_digest` | `0x4c7e30` | `0x41` | `int __cdecl(void *Src, int)` |
| `net_md5_hex` | `0x4c7d80` | `0x59` | `int __cdecl(char *Str)` |
| `net_packet_factory_registry_ctor` | `0x596610` | `0xa2` | unknown |
| `net_packet_factory_registry_dtor` | `0x5966c0` | `0x6f` | unknown |
| `net_packet_reader_advance` | `0x595ee0` | `0x1c` | unknown |
| `net_packet_reader_current_ptr` | `0x595e50` | `0x17` | unknown |
| `net_packet_reader_init` | `0x595bf0` | `0x29` | unknown |
| `net_packet_reader_init_from_remaining` | `0x595e90` | `0x27` | unknown |
| `net_packet_reader_read_bytes` | `0x595d20` | `0x3e` | `int __thiscall(_DWORD *this, void *, int Size)` |
| `net_packet_reader_read_u16_be` | `0x595c60` | `0x34` | `__int16 __thiscall(_DWORD *this)` |
| `net_packet_reader_read_u16_sized_bytes` | `0x595dc0` | `0x30` | `int __stdcall(void *)` |
| `net_packet_reader_read_u24_be` | `0x595ca0` | `0x32` | unknown |
| `net_packet_reader_read_u32_be` | `0x595ce0` | `0x32` | `int __thiscall(_DWORD *this)` |
| `net_packet_reader_read_u8` | `0x595c20` | `0x32` | `int __thiscall(_DWORD)` |
| `net_packet_reader_read_u8_sized_bytes` | `0x595d90` | `0x30` | `size_t __thiscall(_DWORD *this, void *)` |
| `net_packet_reader_read_u8_string` | `0x595df0` | `0x2a` | `int __stdcall(void *)` |
| `net_packet_reader_remaining_size` | `0x595e70` | `0x17` | `int __thiscall(_DWORD *this)` |
| `net_packet_reader_rewind` | `0x595ec0` | `0x15` | unknown |
| `net_packet_reader_take_view` | `0x595d60` | `0x29` | unknown |
| `net_parse_s_enter_editing_mode_payload` | `0x54a530` | `0x14f` | unknown |
| `net_parse_s_show_paper_payload` | `0x54a680` | `0x14f` | `int __thiscall(_WORD *this, int)` |
| `net_poll_receive` | `0x564300` | `0xc8` | unknown |
| `net_process_incoming_transport_data` | `0x564870` | `0x2c` | `int __thiscall(_DWORD, _DWORD)` |
| `net_queue_received_packet_bytes` | `0x467060` | `0x67` | `int __stdcall(void *Src, size_t Size)` |
| `net_queue_set_packet_salt_seed` | `0x568380` | `0x1d` | unknown |
| `net_queue_set_primary_packet_key` | `0x5683a0` | `0x4c` | `int __stdcall(size_t Size, void *Src)` |
| `net_read_u16_be` | `0x564270` | `0x17` | unknown |
| `net_read_u24_be` | `0x564290` | `0x26` | unknown |
| `net_read_u32_be` | `0x5642c0` | `0x38` | unknown |
| `net_receive_binary_framed_data` | `0x567070` | `0x707` | unknown |
| `net_receive_legacy_framed_data` | `0x566e00` | `0x26b` | unknown |
| `net_register_server_packet_factories` | `0x595f00` | `0x422` | unknown |
| `net_register_server_packet_factory` | `0x596730` | `0x4e` | unknown |
| `net_release_server_packet` | `0x5964c0` | `0x85` | unknown |
| `net_reset_client_packet_sequence` | `0x563de0` | `0x12` | `int __thiscall(_DWORD)` |
| `net_s_action_delay_ctor` | `0x597160` | `0x21` | unknown |
| `net_s_action_delay_deserialize` | `0x597190` | `0x37` | unknown |
| `net_s_add_equip_ctor` | `0x597290` | `0x21` | unknown |
| `net_s_add_equip_deserialize` | `0x5972c0` | `0x7e` | unknown |
| `net_s_add_inventory_ctor` | `0x597400` | `0x21` | unknown |
| `net_s_add_inventory_deserialize` | `0x597430` | `0x91` | unknown |
| `net_s_add_skill_ctor` | `0x597590` | `0x21` | unknown |
| `net_s_add_skill_deserialize` | `0x5975c0` | `0x3f` | unknown |
| `net_s_add_spell_ctor` | `0x5976c0` | `0x21` | unknown |
| `net_s_add_spell_deserialize` | `0x5976f0` | `0x7c` | unknown |
| `net_s_add_user_ctor` | `0x597830` | `0x21` | unknown |
| `net_s_add_user_deserialize` | `0x597860` | `0xd` | unknown |
| `net_s_advertisement_ctor` | `0x597930` | `0x21` | unknown |
| `net_s_advertisement_deserialize` | `0x597960` | `0x66` | unknown |
| `net_s_bad_guy_ctor` | `0x597a90` | `0x21` | unknown |
| `net_s_bad_guy_deserialize` | `0x597ac0` | `0x37` | unknown |
| `net_s_block_input_ctor` | `0x597bc0` | `0x21` | unknown |
| `net_s_block_input_deserialize` | `0x597bf0` | `0x34` | unknown |
| `net_s_bounce_ctor` | `0x597cf0` | `0x21` | unknown |
| `net_s_bounce_deserialize` | `0x597d20` | `0x33` | unknown |
| `net_s_browser_ctor` | `0x597e20` | `0x21` | unknown |
| `net_s_browser_deserialize` | `0x597e50` | `0x9a` | unknown |
| `net_s_change_direction_ctor` | `0x597fb0` | `0x21` | unknown |
| `net_s_change_direction_deserialize` | `0x597fe0` | `0x29` | unknown |
| `net_s_change_hour_ctor` | `0x5980d0` | `0x21` | unknown |
| `net_s_change_hour_deserialize` | `0x598100` | `0x1b` | unknown |
| `net_s_change_weather_ctor` | `0x5981e0` | `0x21` | unknown |
| `net_s_change_weather_deserialize` | `0x598210` | `0x1b` | unknown |
| `net_s_check_time_ctor` | `0x5982f0` | `0x21` | unknown |
| `net_s_check_time_deserialize` | `0x598320` | `0x1b` | unknown |
| `net_s_damage_effect_ctor` | `0x598400` | `0x21` | unknown |
| `net_s_damage_effect_deserialize` | `0x598430` | `0x45` | unknown |
| `net_s_draw_human_objects_ctor` | `0x598540` | `0x21` | unknown |
| `net_s_draw_human_objects_deserialize` | `0x598570` | `0x3e7` | unknown |
| `net_s_draw_objects_ctor` | `0x598a40` | `0x64` | unknown |
| `net_s_draw_objects_deserialize` | `0x598ab0` | `0x5b` | unknown |
| `net_s_draw_objects_read_record` | `0x598b30` | `0x14a` | unknown |
| `net_s_draw_objects_rewind` | `0x598b10` | `0x20` | unknown |
| `net_s_effect_layer_ctor` | `0x598db0` | `0x21` | unknown |
| `net_s_effect_layer_deserialize` | `0x598de0` | `0xa9` | unknown |
| `net_s_exchange_ctor` | `0x598f50` | `0x21` | unknown |
| `net_s_exchange_deserialize` | `0x598f80` | `0x13b` | unknown |
| `net_s_family_name_ctor` | `0x599180` | `0x21` | unknown |
| `net_s_family_name_deserialize` | `0x5991b0` | `0x1c` | unknown |
| `net_s_field_map_ctor` | `0x599290` | `0x21` | unknown |
| `net_s_field_map_deserialize` | `0x5992c0` | `0x13f` | unknown |
| `net_s_group_ctor` | `0x5994c0` | `0x21` | unknown |
| `net_s_group_deserialize` | `0x5994f0` | `0x10b` | unknown |
| `net_s_item_shop_ctor` | `0x5996c0` | `0x6f` | unknown |
| `net_s_item_shop_deserialize` | `0x599730` | `0x4a` | unknown |
| `net_s_level_point_ctor` | `0x5999c0` | `0x21` | unknown |
| `net_s_level_point_deserialize` | `0x5999f0` | `0x29` | unknown |
| `net_s_manual_ctor` | `0x599ae0` | `0x21` | unknown |
| `net_s_manual_deserialize` | `0x599b10` | `0x104` | unknown |
| `net_s_map_ctor` | `0x599ce0` | `0x21` | unknown |
| `net_s_map_deserialize` | `0x599d10` | `0x67` | unknown |
| `net_s_map_part_ctor` | `0x599e40` | `0x21` | unknown |
| `net_s_map_part_deserialize` | `0x599e70` | `0x2a` | unknown |
| `net_s_map_size_ctor` | `0x599f60` | `0x21` | unknown |
| `net_s_map_size_deserialize` | `0x599f90` | `0x71` | unknown |
| `net_s_message_ctor` | `0x59a0d0` | `0x21` | unknown |
| `net_s_message_deserialize` | `0x59a100` | `0x7e` | unknown |
| `net_s_mini_game_ctor` | `0x59a240` | `0x21` | unknown |
| `net_s_mini_game_deserialize` | `0x59a270` | `0xa2` | unknown |
| `net_s_motion_ctor` | `0x59a3f0` | `0x21` | unknown |
| `net_s_motion_deserialize` | `0x59a420` | `0x3b` | unknown |
| `net_s_move_ctor` | `0x59a520` | `0x21` | unknown |
| `net_s_move_deserialize` | `0x59a550` | `0x65` | unknown |
| `net_s_move_object_ctor` | `0x59a680` | `0x21` | unknown |
| `net_s_move_object_deserialize` | `0x59a6b0` | `0x47` | unknown |
| `net_s_multi_ctor` | `0x59a7c0` | `0x21` | unknown |
| `net_s_multi_deserialize` | `0x59a7f0` | `0x33` | unknown |
| `net_s_num_users_ctor` | `0x59a8f0` | `0x21` | unknown |
| `net_s_num_users_deserialize` | `0x59a920` | `0x1c` | unknown |
| `net_s_pursuit_message_ctor` | `0x59aa00` | `0x67` | unknown |
| `net_s_pursuit_message_deserialize` | `0x59aa70` | `0x186` | unknown |
| `net_s_quit_ctor` | `0x59ad20` | `0x21` | unknown |
| `net_s_quit_deserialize` | `0x59ad50` | `0x1b` | unknown |
| `net_s_remove_equip_ctor` | `0x59ae30` | `0x21` | unknown |
| `net_s_remove_equip_deserialize` | `0x59ae60` | `0x20` | unknown |
| `net_s_remove_inventory_ctor` | `0x59af40` | `0x21` | unknown |
| `net_s_remove_inventory_deserialize` | `0x59af70` | `0x1b` | unknown |
| `net_s_remove_objects_ctor` | `0x59b050` | `0x21` | unknown |
| `net_s_remove_objects_deserialize` | `0x59b080` | `0x1b` | unknown |
| `net_s_remove_skill_ctor` | `0x59b160` | `0x21` | unknown |
| `net_s_remove_skill_deserialize` | `0x59b190` | `0x1b` | unknown |
| `net_s_remove_spell_ctor` | `0x59b270` | `0x21` | unknown |
| `net_s_remove_spell_deserialize` | `0x59b2a0` | `0x1b` | unknown |
| `net_s_request_crc_ctor` | `0x59b380` | `0x21` | unknown |
| `net_s_request_crc_deserialize` | `0x59b3b0` | `0x1c` | unknown |
| `net_s_request_portrait_ctor` | `0x59b490` | `0x21` | unknown |
| `net_s_request_portrait_deserialize` | `0x59b4c0` | `0xd` | unknown |
| `net_s_say_ctor` | `0x59b590` | `0x21` | unknown |
| `net_s_say_deserialize` | `0x59b5c0` | `0x38` | unknown |
| `net_s_screen_menu_ctor` | `0x59b6c0` | `0x67` | unknown |
| `net_s_screen_menu_deserialize` | `0x59b730` | `0xe2` | unknown |
| `net_s_screen_shot_ctor` | `0x59b930` | `0x21` | unknown |
| `net_s_screen_shot_deserialize` | `0x59b960` | `0x1b` | unknown |
| `net_s_self_look_ctor` | `0x59ba40` | `0x21` | unknown |
| `net_s_self_look_deserialize` | `0x59ba70` | `0x2c4` | unknown |
| `net_s_self_save_ok_ctor` | `0x59be00` | `0x21` | unknown |
| `net_s_self_save_ok_deserialize` | `0x59be30` | `0xd` | unknown |
| `net_s_sound_effect_ctor` | `0x59bf00` | `0x21` | unknown |
| `net_s_sound_effect_deserialize` | `0x59bf30` | `0x4c` | unknown |
| `net_s_spell_delay_cancel_ctor` | `0x59c040` | `0x21` | unknown |
| `net_s_spell_delay_cancel_deserialize` | `0x59c070` | `0xd` | unknown |
| `net_s_spelled_ctor` | `0x59c140` | `0x21` | unknown |
| `net_s_spelled_deserialize` | `0x59c170` | `0x2a` | unknown |
| `net_s_static_object_state_ctor` | `0x59c260` | `0x21` | unknown |
| `net_s_static_object_state_deserialize` | `0x59c290` | `0x8d` | unknown |
| `net_s_status_ctor` | `0x59c3e0` | `0x21` | unknown |
| `net_s_status_deserialize` | `0x59c410` | `0x3dc` | unknown |
| `net_s_stipulation_ctor` | `0x59c8b0` | `0x21` | unknown |
| `net_s_stipulation_deserialize` | `0x59c8e0` | `0x68` | unknown |
| `net_s_transfer_server_ctor` | `0x59ca10` | `0x21` | unknown |
| `net_s_transfer_server_deserialize` | `0x59ca40` | `0x3f` | unknown |
| `net_s_user_appearance_ctor` | `0x59cb40` | `0x21` | unknown |
| `net_s_user_appearance_deserialize` | `0x59cb70` | `0x61` | unknown |
| `net_s_user_position_ctor` | `0x59cca0` | `0x21` | unknown |
| `net_s_user_position_deserialize` | `0x59ccd0` | `0x2b` | unknown |
| `net_s_web_board_ctor` | `0x59cdc0` | `0x21` | unknown |
| `net_s_web_board_deserialize` | `0x59cdf0` | `0x115` | unknown |
| `net_s_window_change_ctor` | `0x59cfd0` | `0x21` | unknown |
| `net_s_window_change_deserialize` | `0x59d000` | `0x1b` | unknown |
| `net_send_c_add_stat` | `0x5755c0` | `0xb5` | `int __fastcall(int)` |
| `net_send_c_block_listen_action_1` | `0x550aa0` | `0x80` | `int()` |
| `net_send_c_block_listen_action_2` | `0x550c60` | `0x136` | `int __thiscall(void *this, const char *Src)` |
| `net_send_c_block_listen_action_3` | `0x550ee0` | `0x136` | `int __thiscall(void *this, const char *Src)` |
| `net_send_c_check_time` | `0x5f7830` | `0xcc` | `char __stdcall(int)` |
| `net_send_c_exit_editing_mode` | `0x54a7d0` | `0x1d7` | `int __thiscall(int this)` |
| `net_send_c_field_map_request` | `0x430d30` | `0xe5` | `int __stdcall(unsigned __int16, unsigned __int16, unsigned __int16)` |
| `net_send_c_field_map_selection` | `0x476390` | `0xfc` | `int __thiscall(int this)` |
| `net_send_c_give` | `0x496d90` | `0xd6` | `void __thiscall(unsigned __int8 *this, int, int)` |
| `net_send_c_login` | `0x4baa80` | `0x5d3` | `int __thiscall(void *this, const char *character_name, const char *password)` |
| `net_send_c_portrait` | `0x5b1160` | `0x34` | `char __stdcall(int)` |
| `net_send_c_put_request` | `0x5f4430` | `0x7a` | `int __thiscall(void *this, unsigned int object_id)` |
| `net_send_c_refresh` | `0x5f4640` | `0x72` | `int __thiscall(void *this)` |
| `net_send_c_request_family_name` | `0x4719b0` | `0x6e` | `int()` |
| `net_send_c_request_homepage` | `0x4ba0c0` | `0x8c` | `int()` |
| `net_send_c_spell_delay_request` | `0x49bab0` | `0x82` | `int __stdcall(char)` |
| `net_send_c_spell_delay_say` | `0x499330` | `0xea` | `size_t __thiscall(const char *this)` |
| `net_send_c_user_change_state` | `0x5fc790` | `0x90` | `int __thiscall(_DWORD *this, int)` |
| `net_send_client_packet` | `0x5648a0` | `0x777` | `int __thiscall(int this, char *, __int16)` |
| `net_set_primary_packet_key` | `0x5683f0` | `0xbd` | `int __stdcall(size_t Size, void *Src)` |
| `net_socket_ctor` | `0x563910` | `0x342` | `_DWORD *__thiscall(_DWORD *this, int)` |
| `net_socket_dtor` | `0x563c60` | `0xc3` | `int __thiscall(_DWORD *this)` |
| `net_socket_scalar_deleting_dtor` | `0x5688d0` | `0x2c` | `_DWORD *__thiscall(_DWORD *this, char)` |
| `net_submit_client_packet` | `0x563e00` | `0x262` | `int __thiscall(int this, char *Src, __int16)` |
| `net_transport_read_byte` | `0x567870` | `0x2f2` | `char __thiscall(int this, _BYTE *)` |
| `net_wrap_received_packet_message` | `0x468220` | `0xbe` | unknown |
| `net_write_c_packet_39_header` | `0x52c1c0` | `0xa1` | `__int16 __thiscall(int this, int, unsigned __int16)` |
| `net_write_c_packet_3a_header` | `0x52c270` | `0xc7` | `__int16 __thiscall(int this, int, unsigned __int16)` |
| `net_write_c_packet_54_header` | `0x45d550` | `0x8c` | `int __thiscall(_DWORD *this, int, unsigned __int8)` |
| `net_write_u16_be` | `0x564160` | `0x32` | `_BYTE *__cdecl(unsigned int, _BYTE *)` |
| `net_write_u24_be` | `0x5641a0` | `0x4a` | unknown |
| `net_write_u32_be` | `0x5641f0` | `0x65` | `_BYTE *__cdecl(unsigned int, _BYTE *)` |
| `net_write_u8` | `0x564140` | `0x1d` | `_BYTE *__cdecl(unsigned int, _BYTE *)` |
| `net_xor_packet_bytes` | `0x568230` | `0x12a` | `unsigned int __stdcall(int, unsigned int, unsigned int, int, int)` |

## `object_` functions

| Function | Address | Size | IDA-inferred signature |
|---|---:|---:|---|
| `object_collect_out_of_range` | `0x5c7af0` | `0x1d4` | `void __thiscall(void *this, int center_y, int center_x, int range, unsigned char include_static)` |
| `object_create_human` | `0x5ca140` | `0x373` | `void *__thiscall(void *this, void *out_shared, unsigned int object_id, int y, int x)` |
| `object_create_item` | `0x5cac60` | `0x339` | `void *__thiscall(void *this, void *out_shared, unsigned int object_id, int y, int x, unsigned short item_id, unsigned char flags)` |
| `object_create_monster` | `0x5ca4c0` | `0x363` | `void *__thiscall(void *this, void *out_shared, unsigned int object_id, int y, int x, unsigned char monster_class)` |
| `object_create_self_user` | `0x5ca830` | `0x425` | `void *__thiscall(void *this, void *out_shared, unsigned int object_id, int y, int x)` |
| `object_ctor` | `0x5db3f0` | `0x1df` | `void *__thiscall(void *this, unsigned int category, unsigned int object_id)` |
| `object_detach` | `0x5c9450` | `0x1fe` | unknown |
| `object_find` | `0x5c9810` | `0x6d` | `void *__thiscall(void *this, void *out_shared, unsigned int object_id)` |
| `object_get_local_user_id` | `0x5c7110` | `0x14` | `unsigned int __thiscall(void *this)` |
| `object_get_self_object_id` | `0x5c7150` | `0x14` | `unsigned int __thiscall(void *this)` |
| `object_get_self_user` | `0x5eedb0` | `0xb5` | `void *__thiscall(void *this)` |
| `object_handle_world_input_event` | `0x5f1480` | `0x106` | `unsigned char __thiscall(void *this, const void *input_event)` |
| `object_human_apply_appearance` | `0x5e0070` | `0x44` | unknown |
| `object_human_ctor` | `0x5ddfc0` | `0x56` | `void *__thiscall(void *this, unsigned int object_id)` |
| `object_insert` | `0x5c8ea0` | `0x216` | unknown |
| `object_item_ctor` | `0x5de280` | `0x153` | `void *__thiscall(void *this, int x, int y, unsigned short item_id, unsigned char flags, void *resource, unsigned int object_id)` |
| `object_list_erase` | `0x5e6020` | `0x264` | unknown |
| `object_list_find` | `0x5e73b0` | `0x1c8` | `void *__thiscall(void *this, void *out_shared, unsigned int object_id)` |
| `object_list_insert` | `0x5e5d40` | `0x16c` | unknown |
| `object_living_apply_monster_appearance` | `0x5e0370` | `0x1d3` | unknown |
| `object_living_ctor` | `0x5df230` | `0x210` | `void *__thiscall(void *this, unsigned int category, unsigned int object_id)` |
| `object_living_set_direction` | `0x5e0880` | `0x4c` | `void __thiscall(void *this, unsigned char direction)` |
| `object_living_set_name` | `0x5df590` | `0x28` | `void __thiscall(void *this, const char *name)` |
| `object_monster_ctor` | `0x5e2630` | `0x9b` | `void *__thiscall(void *this, unsigned int object_id, unsigned char monster_class)` |
| `object_prune_out_of_range` | `0x5c7cd0` | `0x111` | `void __thiscall(void *this, int center_y, int center_x, int range, unsigned char include_static)` |
| `object_rebuild_visible_area` | `0x5c7df0` | `0x13f` | `void __thiscall(void *this, int y, int x)` |
| `object_reindex` | `0x5c92c0` | `0x18d` | unknown |
| `object_remove_by_id` | `0x5c9fa0` | `0x195` | `void __thiscall(void *this, unsigned int object_id, unsigned char animate_removal)` |
| `object_reset_movement_sync_state` | `0x5f4900` | `0x8c` | `void __thiscall(void *this, unsigned char keep_generation)` |
| `object_set_local_user_id` | `0x5c70f0` | `0x19` | `void __thiscall(void *this, unsigned int object_id)` |
| `object_set_self_object_id` | `0x5c7130` | `0x19` | `void __thiscall(void *this, unsigned int object_id)` |
| `object_set_view_position` | `0x5eec70` | `0x65` | `void __thiscall(void *this, int y, int x, unsigned char rebuild_visible_state)` |
| `object_user_ctor` | `0x5e4e60` | `0x9f` | `void *__thiscall(void *this, unsigned int object_id)` |

## `render_` functions

| Function | Address | Size | IDA-inferred signature |
|---|---:|---:|---|
| `render_allocate_palette_id` | `0x548610` | `0x32` | `int __thiscall(void *this)` |
| `render_blit_image` | `0x44fb80` | `0x1848` | unknown |
| `render_convert_rgb24_palette` | `0x593b00` | `0xae` | `void __thiscall(void *this, unsigned __int16 *destination, const unsigned __int8 *rgb)` |
| `render_decode_image_entry` | `0x48b530` | `0x65f` | unknown |
| `render_detect_display_mode` | `0x57a640` | `0xc1` | `int __cdecl()` |
| `render_effect_load_frame` | `0x457fd0` | `0x655` | `unsigned __int8 __thiscall(void *this, int frame_index)` |
| `render_effect_resource_ctor` | `0x4575b0` | `0x799` | unknown |
| `render_initialize_directdraw` | `0x4495d0` | `0x6bd` | unknown |
| `render_initialize_video_system` | `0x593f30` | `0x313` | `int __thiscall(void *this, HWND window, int width, int height, int display_mode, int flags)` |
| `render_load_effect_palette_table` | `0x546c30` | `0x2aa` | unknown |
| `render_load_image_frame` | `0x48bbc0` | `0xbe` | unknown |
| `render_load_item_palette_table` | `0x546980` | `0x261` | unknown |
| `render_load_map_tile_palette_table` | `0x547210` | `0x32d` | unknown |
| `render_load_pal_family_table` | `0x546440` | `0x484` | unknown |
| `render_load_static_palette_table` | `0x546ee0` | `0x32d` | unknown |
| `render_register_rgb24_palette` | `0x548650` | `0x68` | `unsigned __int16 *__thiscall(void *this, int palette_id, const void *rgb)` |
| `render_select_mpf_frame` | `0x48d0e0` | `0x492` | unknown |
| `render_write_screenshot_bmp` | `0x5537f0` | `0x7c9` | unknown |

## `startup_` functions

| Function | Address | Size | IDA-inferred signature |
|---|---:|---:|---|
| `startup_handle_debug_option_stub` | `0x57a460` | `0x5` | `void __cdecl(const char *option_text)` |
| `startup_initialize_client` | `0x4a9f80` | `0x20d4` | `int __thiscall(void *this, HINSTANCE hInstance, int hPrevInstance, int command_line, int nCmdShow, void *startup_config)` |
| `startup_initialize_time_and_os_version` | `0x4a9690` | `0x20c` | `void __cdecl()` |
| `startup_parse_dash_options` | `0x57a550` | `0xed` | `void __cdecl(const char *command_line)` |
| `startup_run_pending_patcher` | `0x57a330` | `0x123` | `void __cdecl()` |
| `startup_set_working_directory_to_executable` | `0x4ad3a0` | `0x134` | `void __cdecl()` |
| `startup_win_main` | `0x57a710` | `0x395` | `int __stdcall(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)` |

## `ui_` functions

| Function | Address | Size | IDA-inferred signature |
|---|---:|---:|---|
| `ui_agreement_dialog_ctor` | `0x402430` | `0x427` | unknown |
| `ui_build_main_layout_geometry` | `0x5aa880` | `0x11a8` | unknown |
| `ui_bulletin_dialog_ctor` | `0x41d8b0` | `0x434` | unknown |
| `ui_change_password_dialog_ctor` | `0x4bb2a0` | `0x56f` | unknown |
| `ui_control_definition_add_color` | `0x4a5950` | `0x20` | unknown |
| `ui_control_definition_add_image` | `0x4a5890` | `0x20` | unknown |
| `ui_control_definition_add_value` | `0x4a58b0` | `0x20` | unknown |
| `ui_control_definition_reset` | `0x4a5610` | `0x121` | unknown |
| `ui_control_definition_set_name` | `0x4a5770` | `0xd0` | unknown |
| `ui_control_definition_set_rect` | `0x4a5860` | `0x2b` | unknown |
| `ui_control_definition_set_type` | `0x4a5840` | `0x18` | unknown |
| `ui_create_user_dialog_ctor` | `0x43c370` | `0xd05` | unknown |
| `ui_dismiss_paper_window` | `0x54a9f0` | `0x34` | `int __thiscall(_DWORD, _DWORD)` |
| `ui_event_info_dialog_ctor` | `0x5af460` | `0x3f6` | unknown |
| `ui_handle_paper_close_action` | `0x54a9b0` | `0x39` | `int __thiscall(_DWORD *this, int, int)` |
| `ui_hot_key_pane_ctor` | `0x488320` | `0x3f2` | unknown |
| `ui_image_button_ctor` | `0x439640` | `0xb4` | unknown |
| `ui_image_button_draw` | `0x439860` | `0x141` | unknown |
| `ui_image_button_handle_key_event` | `0x438590` | `0x68` | unknown |
| `ui_image_button_initialize_images` | `0x439700` | `0x123` | unknown |
| `ui_image_button_invalidate` | `0x4383a0` | `0x1a` | unknown |
| `ui_image_button_set_visual_state` | `0x438340` | `0x5a` | unknown |
| `ui_image_library_singleton` | `0x404a00` | `0xa` | unknown |
| `ui_language_table_ctor` | `0x4a4aa0` | `0x196` | `void *__thiscall(void *this)` |
| `ui_layout_build_image_button_scratch` | `0x4828a0` | `0x32` | unknown |
| `ui_layout_build_image_button_spec` | `0x4828e0` | `0x1f3` | unknown |
| `ui_layout_cache_lookup` | `0x481ce0` | `0x10f` | unknown |
| `ui_layout_cache_store` | `0x481e60` | `0x1a0` | unknown |
| `ui_layout_create_image_button` | `0x4832e0` | `0xae` | unknown |
| `ui_layout_find_control_definition` | `0x481e30` | `0x27` | unknown |
| `ui_layout_get_control_rect` | `0x482630` | `0x77` | unknown |
| `ui_layout_get_image_entry` | `0x4826e0` | `0x153` | unknown |
| `ui_layout_get_image_entry_into_scratch` | `0x482b90` | `0x2c` | unknown |
| `ui_layout_get_value_entry` | `0x482870` | `0x2c` | unknown |
| `ui_layout_load_from_archive` | `0x482340` | `0x2e4` | unknown |
| `ui_layout_manager_singleton` | `0x402ac0` | `0xa` | unknown |
| `ui_layout_parse_control_block` | `0x4a81f0` | `0x621` | unknown |
| `ui_layout_read_integer` | `0x4a9560` | `0x77` | unknown |
| `ui_layout_read_quoted_string` | `0x4a93c0` | `0x23` | unknown |
| `ui_layout_read_tag` | `0x4a9290` | `0x8f` | unknown |
| `ui_layout_read_token` | `0x4a9040` | `0x1ee` | unknown |
| `ui_layout_select_control` | `0x482140` | `0x1a6` | unknown |
| `ui_login_dialog_ctor` | `0x4ba180` | `0x610` | unknown |
| `ui_login_dialog_handle_control_action` | `0x4ba8c0` | `0xe8` | unknown |
| `ui_login_dialog_handle_key_event` | `0x4ba810` | `0xad` | unknown |
| `ui_main_menu_pane_ctor` | `0x4b6c70` | `0x746` | unknown |
| `ui_nui_album_pane_ctor` | `0x5b2a70` | `0x617` | unknown |
| `ui_nui_event_pane_ctor` | `0x5b3ee0` | `0x332` | unknown |
| `ui_nui_family_pane_ctor` | `0x5b4fb0` | `0x2bf` | unknown |
| `ui_nui_intro_pane_ctor` | `0x5b59f0` | `0x1003` | unknown |
| `ui_nui_legend_pane_ctor` | `0x5b7aa0` | `0x1c9` | unknown |
| `ui_nui_skill_spell_pane_ctor` | `0x5b80c0` | `0x2d8` | unknown |
| `ui_open_paper_window` | `0x54a470` | `0xb7` | `_DWORD *__thiscall(_DWORD *this, int, int)` |
| `ui_palette_get_rgb` | `0x593d40` | `0x5b` | unknown |
| `ui_portrait_text_input_dialog_ctor` | `0x5b11a0` | `0x226` | unknown |
| `ui_score_pane_append_rgb` | `0x5516c0` | `0x122` | `int __stdcall(char *Str, char, int, char, int)` |
| `ui_score_pane_append_s_message` | `0x552120` | `0x84` | `int __stdcall(const char *, __int16)` |
| `ui_score_pane_ctor` | `0x551260` | `0x23b` | unknown |
| `ui_score_pane_handle_s_message` | `0x5521b0` | `0x39` | `char __stdcall(int)` |
| `ui_skill_spell_info_dialog_ctor` | `0x5ae090` | `0x583` | unknown |
| `ui_window_message_dialog_ctor` | `0x4488c0` | `0x549` | `int __stdcall(int, void *Src, int, char)` |
