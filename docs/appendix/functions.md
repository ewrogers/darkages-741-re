# Function reference

This appendix is the address book for functions named in the main text. Static addresses assume preferred image base `0x00400000`. At runtime, use the loaded module base and the matching RVA.

Roles are short summaries from the checked-in Binary Ninja YAML exports. Those exports remain the source for full evidence and provenance.

## Application lifecycle and configuration

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `app_config_ctor` | `0x00431FF0` | high | Constructs Config, loads Darkages.cfg, selects a distribution mode, and dispatches endpoint initialization. |
| `app_configure_unitel_distribution` | `0x00433B40` | high | Empty dormant mode 2 initializer selected by Unitel.nfo in the unreferenced marker scanner. |
| `app_get_distribution_mode` | `0x00434EB0` | high | Caches and returns the distribution mode selected by app_select_distribution_mode. |
| `app_select_distribution_mode` | `0x00434EF0` | high | Returns the constant distribution mode 1 in this target. |
| `app_detect_distribution_mode_from_markers` | `0x00434F00` | high | Dormant unreferenced scanner that maps country and Korean ISP .nfo markers to distribution modes 1 through 15. |
| `app_is_japan_distribution_mode` | `0x004ACEE0` | high | Returns true when app_get_distribution_mode reports mode 13, selecting the create-user email and ISP-selector variant. |
| `app_set_working_directory_from_executable` | `0x004AD3A0` | high | Derives the executable directory from GetCommandLineA and makes it the process working directory. |
| `app_write_patch_info_and_launch_patcher` | `0x00528610` | high | Creates Patch/Info, writes the fixed handoff structure, launches Patcher2.exe without arguments, and exits the client. |
| `app_quit_after_patcher_launch` | `0x005287B0` | high | Destroys NewPatchPane, posts WM_QUIT, and terminates after the patcher launch attempt. |
| `app_handle_d_option_stub` | `0x0057A460` | high | Empty function called for the suffix of an uppercase -D command-line token. |
| `app_parse_command_line` | `0x0057A550` | high | Scans the WinMain command tail for space-delimited dash tokens and recognizes only uppercase D. |
| `app_winmain` | `0x0057A710` | high | Called by the CRT startup wrapper with the WinMain argument set. |

## Game loop

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `event_dispatcher_tick` | `0x00464180` | high | Main-thread tick that drains queued events and invokes at most 0x28 due TimerHandler callbacks. |
| `app_window_proc` | `0x004A9C30` | high | Window procedure that sends messages through the input translator before application-specific handling. |
| `app_run_message_loop` | `0x004AC750` | high | Records the main thread, drains PeekMessageA, and runs the EventDispatcher tick each loop. |

## Events

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `event_get_dispatcher` | `0x0041AE80` | high | Returns event_dispatcher_singleton_ptr. |
| `event_intro_video_frame_timer` | `0x0042E600` | high | Advances the two clips and posts intro state 2 when playback finishes. |
| `event_dispatcher_ctor` | `0x00463820` | high | Constructs the 0x1BC-byte EventDispatcher, queue, timer list, packet factory, capture state, and EventHandlerList. |
| `event_queue_push_copy` | `0x00463D10` | high | Copies exactly 0xA8 event bytes into the synchronized pointer queue. |
| `event_queue_pop_copy` | `0x00463D60` | high | Removes one queued event and copies exactly 0xA8 bytes to the caller. |
| `event_register_pane` | `0x00463E40` | high | Sets Pane +0x188 bit 0x02 and inserts the pane through EventHandlerList. |
| `event_unregister_pane` | `0x00463E80` | high | Clears Pane +0x188 bit 0x02 and removes the pane subtree from EventHandlerList. |
| `event_enqueue` | `0x00463F50` | high | Thin synchronized queue wrapper used when an event originates off the main thread. |
| `event_dispatch_immediate` | `0x00463F70` | high | Validates and centrally dispatches an Event, then performs family-specific owned-payload cleanup. |
| `event_dispatcher_tick_virtual` | `0x00464430` | high | Calls EventDispatcher primary-vtable +0x08, which resolves to event_dispatcher_tick. |
| `event_register_pane_internal` | `0x00464450` | high | Calls EventHandlerList virtual insert and refreshes dispatcher state. |
| `event_unregister_pane_internal` | `0x004644B0` | high | Calls EventHandlerList virtual subtree removal and refreshes dispatcher state. |
| `event_schedule_timer` | `0x00464520` | high | Inserts a five-dword TimerHandler entry into the dispatcher list ordered by due time. |
| `event_cancel_timers` | `0x00464630` | high | Notifies TimerHandler virtual +0x0C, removes matching timer entries, and refreshes next-due time. |
| `event_dispatch` | `0x004647C0` | high | Central dispatcher for capture, type 0x13 deserialization, pane-tree traversal, and type 0x14 special handling. |
| `event_dispatch_pane_tree` | `0x00464CF0` | high | Begins a root EventHandlerList iterator and invokes recursive pane-tree dispatch. |
| `event_dispatch_pane_subtree` | `0x00464D50` | high | Traverses immediate siblings and descendants child-first, with local pointer coordinates and consumed-result stopping. |
| `event_dispatch_to_pane` | `0x00464F40` | high | Maps pointer, keyboard/text, network, and application event families to Pane vtable slots. |
| `event_handler_list_ctor` | `0x00465AF0` | high | Constructs RTTI-backed EventHandlerList with a 0x0C-byte entry array and 16 iterator slots. |
| `event_handler_list_insert` | `0x00465C50` | high | Inserts a pane at parent depth plus one in the flattened preorder tree. |
| `event_handler_list_remove_subtree` | `0x00465D80` | high | Removes one entry and all following descendants with greater depth. |
| `event_handler_list_begin_children` | `0x00465E10` | high | Initializes a mutation-aware iterator at root depth or one depth below an existing iterator. |
| `event_handler_list_end_iterator` | `0x00466050` | high | Marks an EventHandlerList iterator slot unused. |
| `event_handler_list_next` | `0x00466080` | high | Returns the current pane entry and advances the depth-aware iterator. |
| `event_handler_list_advance_sibling` | `0x00466190` | high | Skips descendants and stops at the next valid entry with the iterator's target depth. |
| `event_ctor` | `0x00466680` | high | Constructs Event and initializes its signed type byte at +0x0C to 0xFF. |
| `event_is_pointer` | `0x004666E0` | high | Returns true for event types 0x00 through 0x07. |
| `event_is_keyboard_or_text` | `0x00466720` | high | Returns true for event types 0x08 through 0x0C. |
| `event_is_network` | `0x00466760` | high | Returns true only for event type 0x13. |
| `event_is_application` | `0x004667A0` | high | Returns true for event types 0x0D through 0x12. |
| `event_dispatch_or_queue` | `0x004670F0` | high | Dispatches on app_main_thread_id and copies the Event into the queue from any other thread. |
| `event_handle_intro_state` | `0x004ACA50` | high | Dispatches intro states 0, 1, and 2 around Bink playback. |

## Input

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `input_get_event_manager` | `0x00427380` | high | Returns input_event_manager_singleton_ptr. |
| `input_set_capture_pane` | `0x00464780` | high | Stores EventDispatcher +0x40 and calls SetCapture or ReleaseCapture on the main window. |
| `input_event_manager_ctor` | `0x004667E0` | high | Constructs RTTI EventMan state, key tables, pointer state, and the socket object. |
| `input_repeat_pointer_move_timer` | `0x00466B40` | high | EventMan TimerHandler callback that emits stored pointer coordinates and reschedules after 20 ms. |
| `input_post_pointer_move` | `0x00466C80` | high | Public EventMan entry that honors input blocking before updating coordinates and emitting pointer type 0x00. |
| `input_post_left_button_down` | `0x00466D10` | high | Public EventMan entry that honors input blocking before setting left-button state and emitting type 0x01 or 0x02. |
| `input_post_left_button_up` | `0x00466D50` | high | Public EventMan entry that clears left-button state before emitting pointer type 0x03. |
| `input_post_right_button_down` | `0x00466D80` | high | Public EventMan entry that honors input blocking before setting right-button state and emitting type 0x04 or 0x05. |
| `input_post_right_button_up` | `0x00466DC0` | high | Public EventMan entry that clears right-button state before emitting pointer type 0x06. |
| `input_post_mouse_wheel` | `0x00466DF0` | high | Public EventMan entry that honors input blocking before forwarding a Win32 wheel delta and message time. |
| `input_post_key_down` | `0x00466E20` | high | Public EventMan entry that honors input blocking before updating keyboard state and emitting type 0x08. |
| `input_post_key_up` | `0x00466E60` | high | Public EventMan entry that updates keyboard state and emits type 0x09. |
| `input_post_character` | `0x00466E90` | high | Public EventMan entry that emits one character as text event type 0x0B. |
| `input_post_ime_open_status_change` | `0x00466EB0` | high | Public EventMan entry that emits IME open-status event type 0x0D. |
| `input_post_committed_text` | `0x00466ED0` | high | Public EventMan entry that copies a NUL-terminated committed-text string into event type 0x0B. |
| `input_post_ime_composition_start` | `0x00466EF0` | high | Public EventMan entry that emits IME composition-start event type 0x0E. |
| `input_post_ime_composition_end` | `0x00466F30` | high | Public EventMan entry that emits IME composition-end event type 0x0F. |
| `input_post_ime_candidate_list_data` | `0x00466F50` | high | Public EventMan entry for candidate-list event type 0x10; its pointer ownership requires the native IME path. |
| `input_post_ime_candidate_list_close` | `0x00466F80` | high | Public EventMan entry that emits candidate-list-close event type 0x11. |
| `input_post_alternate_key` | `0x00466FA0` | medium | Public EventMan entry for type 0x0C; the exact semantic distinction from normal key events remains unresolved. |
| `input_emit_pointer_move` | `0x004672F0` | high | Builds pointer event type 0x00 from EventMan coordinates, flags, and message time. |
| `input_emit_left_button_down` | `0x004673F0` | high | Builds type 0x01 or synthesized double-click type 0x02 and sets the left-held flag. |
| `input_emit_left_button_up` | `0x00467680` | high | Builds pointer event type 0x03 and clears the left-held flag. |
| `input_emit_right_button_down` | `0x00467790` | high | Builds type 0x04 or synthesized double-click type 0x05 and sets the right-held flag. |
| `input_emit_right_button_up` | `0x00467A20` | high | Builds pointer event type 0x06 and clears the right-held flag. |
| `input_emit_mouse_wheel` | `0x00467B30` | high | Builds pointer event type 0x07 and normalizes the Win32 wheel delta by 120. |
| `input_emit_key_down` | `0x00467C10` | high | Updates scan-code and modifier state and builds keyboard event type 0x08. |
| `input_emit_key_up` | `0x00467E30` | high | Updates scan-code and modifier state and builds keyboard event type 0x09. |
| `input_emit_character` | `0x00467FE0` | high | Builds text event type 0x0B with the character, message time, and current modifiers. |
| `input_emit_ime_open_status_change` | `0x00468390` | high | Builds application event type 0x0D from an IME open-status value and message time. |
| `input_emit_committed_text` | `0x00468420` | high | Builds type 0x0B and copies at most 0x7F bytes of committed text into the Event object. |
| `input_emit_ime_composition_start` | `0x00468550` | high | Builds IME composition-start event type 0x0E. |
| `input_emit_ime_composition_update` | `0x004685F0` | high | Builds type 0x0A and copies at most 0x7F bytes of composition text into the Event object. |
| `input_emit_ime_composition_end` | `0x004686F0` | high | Builds IME composition-end event type 0x0F. |
| `input_emit_alternate_key` | `0x00468790` | medium | Builds keyboard-family type 0x0C after translating the scan code through EventMan key tables. |
| `input_emit_ime_candidate_list_data` | `0x004688A0` | high | Builds candidate-list event type 0x10 with pointer-bearing candidate data. |
| `input_emit_ime_candidate_list_close` | `0x00468940` | high | Builds candidate-list-close event type 0x11. |
| `input_translate_win32_message` | `0x0048E980` | high | Converts Win32 keyboard, character, IME, pointer, button, and wheel messages to internal events. |

## UI

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `ui_new_legend_dialog_action` | `0x0042CA50` | high | The RTTI-backed NewLegendDialogPane action normalizes line breaks, ends profile text at the fifth break, and saves profile.txt. |
| `ui_intro_video_pane_ctor` | `0x0042DFF0` | high | Initializes the CIPane vtable and Bink-backed video state. |
| `ui_intro_video_begin_sequence` | `0x0042E1F0` | high | Stores two clip resources and starts the first clip. |
| `ui_get_intro_video_pane` | `0x0042E7D0` | high | Returns the global CIPane instance at 0x006DA3A0. |
| `ui_create_user_dialog_ctor` | `0x0043C370` | high | Constructs RTTI class CreateUserDialogPane from _ncreate.txt, attaches appearance controls and account fields, and registers the pane for events and timers. |
| `ui_create_user_draw` | `0x0043D190` | high | Draws the creation preview using gender at +0x674, hair style at +0x676, and hair-color palette index at +0x678. |
| `ui_create_user_handle_pointer_event` | `0x0043DC80` | high | Handles CreateUserDialogPane appearance clicks, including gender selection and conversion of the 2-by-7 hair-color swatch grid into palette indexes. |
| `ui_create_user_handle_action` | `0x0043EAD0` | high | Collects name, password, confirmation, and distribution-dependent account text; checks matching passwords and schedules the create-user send timer. |
| `ui_create_user_timer` | `0x0043F410` | high | CreateUserDialogPane TimerHandler callback; timer 3 sends CNewUser after the form action schedules a 200 ms delay. |
| `ui_dialog_pane_ctor` | `0x00445260` | high | Constructs DialogPane over Pane and initializes its control collection and interaction fields. |
| `ui_dialog_add_control` | `0x00445670` | high | Creates DialogPane +0x594 on first use and inserts the supplied control pointer. |
| `ui_dialog_handle_pointer_event` | `0x00445A20` | high | DialogPane primary-vtable +0x48 implementation for hit testing, child dispatch, hover, pressed state, and actions. |
| `ui_dialog_handle_keyboard_event` | `0x00445FF0` | high | DialogPane primary-vtable +0x4C implementation for focus traversal and focused-control dispatch. |
| `ui_dialog_handle_application_event` | `0x004462D0` | high | DialogPane primary-vtable +0x54 implementation that forwards application and IME events to the focused control. |
| `ui_dialog_hit_test_control` | `0x004468C0` | high | Walks DialogPane controls, checks each rectangle, and calls control virtual +0x78 for a local hit-zone code. |
| `ui_dialog_set_focused_control` | `0x00446BC0` | high | Transitions DialogPane +0x5AC between control indexes and invokes old/new focus hooks. |
| `ui_dialog_focus_previous_control` | `0x00446CD0` | high | Searches backward with wrapping for an enabled, focusable control. |
| `ui_dialog_focus_next_control` | `0x00446DD0` | high | Searches forward with wrapping for an enabled, focusable control. |
| `ui_dialog_dispatch_pointer_to_control` | `0x00446FE0` | high | Converts pointer coordinates to control-local space, calls control virtual +0x48, and restores the event. |
| `ui_pane_schedule_timer` | `0x00464050` | high | Schedules a timer for a Pane by passing its TimerHandler subobject at +0x11C. |
| `ui_pane_cancel_timers` | `0x00464740` | high | Converts a Pane pointer to TimerHandler +0x11C and cancels matching timers. |
| `ui_text_truncate_dbcs_safe` | `0x0047D670` | high | Stops at the byte limit without leaving a Windows DBCS lead byte at the end. |
| `ui_layout_find_cached_file` | `0x00481CE0` | high | Finds a parsed GUI layout by archive entry name in the layout manager cache. |
| `ui_layout_find_control` | `0x00481E30` | high | Finds one named control definition in the selected parsed layout. |
| `ui_layout_select_control` | `0x00482140` | high | Selects a control by name and takes the fatal invalid-layout path when it is missing. |
| `ui_layout_load` | `0x00482340` | high | Loads a named text layout from the DAT archive, parses its CONTROL blocks, and caches the result. |
| `ui_layout_get_control_rect` | `0x00482630` | high | Returns the selected control's four pane-local rectangle coordinates. |
| `ui_layout_get_control_type` | `0x004826B0` | high | Returns the selected control's TYPE integer. |
| `ui_layout_get_control_image` | `0x004826E0` | high | Returns one ordered IMAGE filename and frame index from the selected control. |
| `ui_layout_get_control_color` | `0x00482840` | high | Returns one ordered COLOR palette index from the selected control. |
| `ui_layout_get_control_value` | `0x00482870` | high | Returns one ordered VALUE integer from the selected control. |
| `ui_layout_create_image_button` | `0x004828A0` | high | Creates an ImageButtonControlPane from a named layout definition. |
| `ui_layout_build_image_button` | `0x004828E0` | high | Reads a rectangle, optional skin value, and up to three image states before constructing the button. |
| `ui_image_pane_draw_content` | `0x0048DD30` | high | Draws an ImagePane image into the pane's own canvas. |
| `ui_layout_parse_control` | `0x004A81F0` | high | Parses CONTROL, NAME, TYPE, RECT, IMAGE, VALUE, COLOR, and ENDCONTROL tokens. |
| `ui_layout_serialize_control` | `0x004A8820` | high | Writes one parsed control back to the same line-oriented layout grammar. |
| `ui_change_password_dialog_ctor` | `0x004BB2A0` | high | Constructs RTTI class ChangePasswordDialogPane from _npw.txt and attaches OK, Cancel, Name, existing-password, new-password, and confirmation controls. |
| `ui_change_password_handle_action` | `0x004BB840` | high | Handles ChangePasswordDialogPane action 0 as submit and action 1 as cancel. |
| `ui_change_password_submit` | `0x004BBA50` | high | Checks new-password confirmation locally, then sends directly in distribution modes 1 and 15 or opens the regional birthdate step. |
| `ui_input_birthdate_dialog_ctor` | `0x004BC220` | high | Constructs RTTI class InputBirthdateDialogPane from _npw2.txt for the regional password-change verification branch. |
| `ui_new_patch_pane_ctor` | `0x005283E0` | high | Constructs RTTI class NewPatchPane from SVersionCheck subtype 2, parsing required version and u8-length file names before starting the patch handoff. |
| `ui_pane_ctor` | `0x00549490` | high | Constructs Pane over Canvas and a secondary TimerHandler at +0x11C; initializes visible true at +0x130. |
| `ui_pane_accepts_input` | `0x00549BC0` | high | Returns true when Pane +0x130 is visible and its active region is non-empty. |
| `ui_pane_show` | `0x00549C00` | high | Sets Pane +0x130 visible and invalidates its region when required. |
| `ui_pane_hide` | `0x00549C40` | high | Clears Pane +0x130 visible, invalidates affected content, and releases owned mouse capture. |
| `ui_pane_invalidate` | `0x00549F60` | high | Marks a pane or supplied rectangle dirty so the pane tree redraws it. |
| `ui_pane_capture_mouse` | `0x0054A130` | high | Sets this pane as EventDispatcher capture owner and records Pane +0x178 true. |
| `ui_pane_release_mouse_capture` | `0x0054A160` | high | Clears EventDispatcher capture owner and records Pane +0x178 false. |
| `ui_pane_has_mouse_capture` | `0x0054A190` | high | Returns Pane +0x178. |
| `ui_pane_register_screen` | `0x0054A270` | high | Pane primary-vtable +0x38 wrapper that inserts the pane into HierList&lt;Screen&gt;. |
| `ui_pane_unregister_screen` | `0x0054A2C0` | high | Pane primary-vtable +0x3C wrapper that removes the pane from HierList&lt;Screen&gt;. |
| `ui_pane_register_event_handler` | `0x0054A310` | high | Pane primary-vtable +0x40 wrapper for insertion into EventHandlerList. |
| `ui_pane_unregister_event_handler` | `0x0054A360` | high | Pane primary-vtable +0x44 wrapper for removal from EventHandlerList. |
| `ui_pane_draw_to_target` | `0x0054A3F0` | high | Copies a pane canvas into its target canvas with the pane's selected blend mode. |
| `ui_screen_hierarchy_ctor` | `0x005522B0` | high | Constructs the RTTI-backed HierList&lt;Screen&gt; used for spatial pane parentage. |
| `ui_screen_hierarchy_insert` | `0x00552370` | high | Adds a pane with spatial sibling and parent placement and sets Pane +0x188 bit 0x01. |
| `ui_screen_hierarchy_queue_remove` | `0x005525D0` | high | Clears Pane +0x188 bit 0x01 and queues or performs HierList&lt;Screen&gt; removal. |
| `ui_screen_hierarchy_get_absolute_origin` | `0x005528C0` | high | Accumulates pane origins through spatial parents until ui_screen_root_pane_ptr. |
| `ui_screen_hierarchy_find` | `0x00553260` | high | Recursively finds the HierList&lt;Screen&gt; node for a pane and optionally returns its owner list and index. |
| `ui_screen_pane_ctor` | `0x00553350` | high | Constructs the startup RTTI ScreenPane root with primary Pane and secondary TimerHandler vtables. |
| `ui_terminal_pane_handle_server_data` | `0x00579090` | high | TerminalPane2 primary-vtable slot +0x50 scans initial wire bytes, handles ESC C and ESC S plus Telnet terminal negotiation, and queues CHello and CVersion. |
| `ui_text_insert_formatted` | `0x0057B300` | high | Forwards a NUL-terminated string to the rich text insertion and markup path. |
| `ui_text_insert_color_markup` | `0x0057D310` | high | Recognizes lowercase three-byte {=a through {=x tokens and changes the following run's palette index. |
| `ui_gui_back_handle_pointer` | `0x005A0CF0` | high | Handles GUIBackPane pointer input; BTN_HELP is present in the hover path but has no click action. |
| `ui_user_info_apply_portrait_body` | `0x005ACD10` | high | Decodes a portrait/profile body into UserInfoPane state and refreshes its portrait canvas and text. |
| `ui_user_info_handle_server_packet` | `0x005AD160` | high | The UserInfoPane vtable event handler sends the local portrait response when the decoded opcode is 0x49. |
| `ui_user_info_refresh_local_portrait` | `0x005AD5D0` | high | Builds the local portrait body and reapplies it to UserInfoPane without calling the network submitter. |
| `ui_user_info_timer` | `0x005AD600` | high | Timer 0x1241 calls the local portrait refresh after the profile editor saves. |
| `ui_portrait_text_dialog_ctor` | `0x005B11A0` | high | Constructs RTTI-backed PortraitTextInputDialogPane from _nui_pi.txt and loads profile.txt. |
| `ui_portrait_text_dialog_action` | `0x005B1510` | high | Action 1 saves profile.txt and queues timer 0x1241; action 2 closes without saving. |
| `ui_map_loading_pane_ctor` | `0x005BA040` | high | Constructs RTTI class MapLoadingPane from _nloadm.txt and registers it as a visible screen pane. |
| `ui_map_loading_set_progress` | `0x005BA330` | high | Stores the SMapPart transfer percentage in MapLoadingPane and invalidates the pane for redraw. |
| `ui_snow_particle_pane_ctor` | `0x005BD710` | high | Constructs one ImagePane-backed snow particle from a snowaNN.epf resource. |
| `ui_world_pane_draw_to_target` | `0x005CE350` | high | Copies WorldPane output to its target and applies an optional post-copy pixel effect. |
| `ui_world_pane_draw_content` | `0x005F27A0` | high | WorldPane content hook that draws the world when ready or clears the pane. |
| `ui_has_map_loading_pane` | `0x005F6470` | high | Reports whether the global MapLoadingPane pointer is non-null. |
| `ui_get_map_loading_pane` | `0x005F6490` | high | Returns the current global MapLoadingPane pointer used by SMapPart progress handling. |
| `ui_close_map_loading_pane` | `0x005F64A0` | high | Destroys the current MapLoadingPane when a map transfer finishes. |

## Network

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `net_parse_endpoint_override` | `0x00433010` | high | Parses a positional IPv4 address or hostname and optional port, but no active mode-1 path calls it. |
| `net_configure_default_endpoint` | `0x00433380` | high | Resolves da0.kru.com, applies the hardcoded IPv4 fallback, and selects port 2610 or 2601. |
| `net_configure_singapore_endpoint` | `0x00433820` | high | Dormant mode 15 initializer selected by singapore.nfo; installs fixed address bytes and port 2610 unless the positional override succeeds. |
| `net_configure_taiwan_endpoint` | `0x004338A0` | high | Dormant mode 14 initializer selected by an archived taiwan.nfo entry; reads iplookup.tbl or archive data and resolves the selected host. |
| `net_configure_japan_endpoint` | `0x00433AD0` | high | Dormant mode 13 initializer selected by japan.nfo; installs fixed address bytes and port 3460 unless the positional override succeeds. |
| `net_configure_lg_endpoint` | `0x00433F40` | high | Dormant mode 3 LG integration that loads chigamec.dll and calls WaitForSessionParameter for session and endpoint data. |
| `net_configure_thrunet_endpoint` | `0x004340C0` | high | Dormant mode 6 Thrunet integration that parses launcher or file data and uses thrunet.clsURLCHK. |
| `net_configure_sk_endpoint` | `0x004347E0` | high | Dormant mode 4 SK integration that parses launcher data and performs Netsgo-specific validation. |
| `net_configure_gameok_endpoint` | `0x00435320` | high | Dormant mode 7 GameOK integration that expects a /GameOK launcher form and derives endpoint data from it. |
| `net_configure_bixel_endpoint` | `0x00435670` | high | Dormant mode 8 Bixel integration that loads PrxyAuth.dll and expects Bixel launcher data. |
| `net_configure_excitegame_endpoint` | `0x00435A20` | high | Dormant mode 10 Excitegame integration that obtains endpoint data from an external launcher or COM-style provider. |
| `net_configure_kornetworld_endpoint` | `0x00436210` | high | Dormant mode 11 integration that expects /KWG, resolves game.kornetworld.com, and selects port 9000. |
| `net_configure_mihosoft_endpoint` | `0x00436620` | high | Dormant mode 9 integration that loads cjconnector.dll and parses a mihosoft launcher record. |
| `net_send_new_user_request` | `0x0043D820` | high | Builds CNewUser opcode 0x02 with length-prefixed name, password, and distribution-dependent account text; Japan mode 13 appends a u16be ISP selector. |
| `net_handle_new_user_validation_result` | `0x0043E360` | high | Parses the first creation result: status 0 sends appearance, 3 and 4 reset name, 5 through 10 reset both password controls, and 11 displays only the message. |
| `net_handle_new_user_completion_result` | `0x0043E7B0` | high | Parses the second creation result; status 0 displays localized success text, closes CreateUserDialogPane, and ignores body bytes after status. |
| `net_send_new_user_appearance` | `0x0043E8F0` | high | Accepted SNewUserCheck flow sends opcode 0x04 with hair style, one-based gender, and hair-color palette index. |
| `net_dispatch_create_user_events` | `0x0043F780` | high | CreateUserDialogPane routes decoded opcode 0x02 and alias 0x01 through the same state-specific creation-result handlers outside the packet factory. |
| `net_handle_new_user_check_opcode_1` | `0x0043F820` | high | Routes compiled SNewUserCheck alias opcode 0x01 according to CreateUserDialogPane creation stage. |
| `net_handle_new_user_check_opcode_2` | `0x0043F870` | high | Routes live SNewUserCheck opcode 0x02 according to CreateUserDialogPane creation stage. |
| `net_send_mercenary_action` | `0x0045C500` | high | EmployeeDialogPane calls this opcode 0x54 builder. |
| `net_init_mercenary_packet` | `0x0045D550` | high | Initializes the opcode 0x54 body prefix used by net_send_mercenary_action. |
| `net_send_group` | `0x00462DC0` | high | UserLookPane calls this opcode 0x2E builder with a length-prefixed user name. |
| `net_post_raw_server_bytes_event` | `0x00467000` | high | Copies a Winsock receive buffer without frame parsing and posts it through the network event family during initial raw-stream mode. |
| `net_post_decoded_server_packet_event` | `0x00467060` | high | Copies a decoded opcode-first server body and queues it as network packet event type 0x13. |
| `net_queue_raw_server_bytes_event` | `0x00468180` | high | Builds event type 0x13 around an owned raw receive buffer for TerminalPane2. |
| `net_queue_server_packet_event` | `0x00468220` | high | Builds and enqueues the event object used for a decoded server packet body. |
| `net_request_family_name` | `0x004719B0` | high | EquipPane reaches this opcode-only 0x7A request paired with SFamilyName. |
| `net_request_cash_shop` | `0x004A03B0` | high | ItemShop::ShoppingBagDialogPane sends the opcode 0x6C body during construction. |
| `net_handle_version_check` | `0x004B7F80` | high | Handles SVersionCheck opcode 0x00 outside the RTTI packet factory; subtype 0 installs transport state and subtype 2 constructs NewPatchPane for the Patcher2.exe handoff. |
| `net_handle_login_check` | `0x004B8420` | high | Handles SLoginCheck opcode 0x02; status zero enters session setup and failures carry a display message. |
| `net_handle_stipulation_raw` | `0x004B8570` | high | Handles the decoded-buffer form of SStipulation and requests the homepage first when its cached URL is absent. |
| `net_handle_stipulation` | `0x004B8890` | high | Handles an RTTI-backed SStipulation object and requests the homepage first when its cached URL is absent. |
| `net_dispatch_main_menu_events` | `0x004B8B70` | high | MainMenuPane routes decoded SVersionCheck and SLoginCheck byte buffers outside the packet factory. |
| `net_dispatch_main_menu_events` | `0x004B8B80` | high | Routes startup decoded buffers and RTTI packet objects to version, stipulation, transfer, and browser handlers. |
| `net_handle_transfer_server` | `0x004B9510` | high | Reconnects to the endpoint in STransferServer, then sends raw opcode 0x10, the opaque handoff token unchanged, and the common submission terminator. |
| `net_handle_browser` | `0x004B9B00` | high | Handles RTTI-backed SBrowser variants; subtype 3 caches the supplied homepage URL and marks it available. |
| `net_send_alive` | `0x004BA010` | high | MainMenuPane timer paths send opcode 0x71 and schedule another callback after 30 seconds. |
| `net_send_request_homepage` | `0x004BA0C0` | high | Builds CRequestHomepage fields 68 01; the common submission layer appends the transmitted zero byte. |
| `net_send_login_request` | `0x004BAA80` | high | Builds and submits client login opcode 0x03, then persists the submitted character name. |
| `net_dispatch_change_password_events` | `0x004BB8A0` | high | Routes raw lobby opcode 0x02 to the password-change result handler while ChangePasswordDialogPane is active. |
| `net_handle_change_password_result` | `0x004BBCB0` | high | Handles state-dependent lobby opcode 0x02; status 0 closes successfully, 0x0F resets the existing password, and other failures reset the new-password controls. |
| `net_send_change_password` | `0x004BC050` | high | Builds CChangePassword opcode 0x26 with u8-length name, existing password, and new password. |
| `net_send_manual_action` | `0x004C26D0` | high | ManufactureDialogPane calls this opcode 0x55 crafting action builder. |
| `net_request_object_info` | `0x004CD350` | high | Merchant menu paths call this opcode 0x43 object information request. |
| `net_send_merchant_selection` | `0x004CFE60` | high | MerchantDialogPane::TextMenuDialogEx virtual method that builds and sends CMerchant opcode 0x39. |
| `net_send_pursuit_selection` | `0x004DBC90` | high | MessageDialog and SimpleMessageDialog share this CPursuit opcode 0x3A selection method. |
| `net_dispatch_metadata_events` | `0x004E4D80` | high | MetaTableManager recognizes decoded SMetaData opcode 0x6F outside the packet factory. |
| `net_handle_metadata` | `0x004E4EA0` | high | Parses SMetaData table entries and validates or applies named metadata blobs. |
| `net_request_metadata` | `0x004E53F0` | high | Builds CMetaData operation 0 with a one-byte name length and the requested table name. |
| `net_metadata_uncompress` | `0x004E54F0` | high | Inflates metadata zlib data into a buffer capped at 0x20000 bytes. |
| `net_metadata_crc32` | `0x004E5790` | high | Calculates standard CRC32 over inflated metadata bytes. |
| `net_parse_metadata_table` | `0x004E57C0` | high | Parses big-endian group counts and length-prefixed metadata names and values. |
| `net_send_user_setting` | `0x00542E60` | high | OptionPane and GameSettingDialog call this opcode 0x1B builder. |
| `net_build_send_portrait` | `0x0054CE10` | high | Builds opcode 0x4F with nested portrait and profile lengths after applying the local image checks. |
| `net_decode_portrait_profile_body` | `0x0054D570` | high | Reads the nested big-endian portrait and profile lengths used by the portrait body. |
| `net_send_multi_server_selection` | `0x0055A090` | high | ServerSelectDialogPane sends opcode 0x57 with the selected configured server index. |
| `net_load_server_table` | `0x0055A240` | high | Loads mServer.tbl numeric lines plus transformed name and greeting text into fixed-size records. |
| `net_save_server_table` | `0x0055A490` | high | Saves server records and transforms the name and greeting text for file storage. |
| `net_transform_server_table_text` | `0x0055A650` | high | Leaves byte zero in place and swaps later byte pairs in a self-inverse text transform. |
| `net_socket_ctor` | `0x00563910` | high | Constructs the Socket object and initializes packet-transform state. |
| `net_reset_client_packet_sequence` | `0x00563DE0` | high | Resets the client-to-server encrypted-packet sequence to zero. |
| `net_submit_client_packet` | `0x00563E00` | high | Ordinary bodies are copied with an appended transmitted zero and a one-byte length increase before socket event command 6; opcodes 0x39 and 0x3A use a separate CRC wrapper. |
| `net_queue_raw_stream_mode` | `0x00564070` | high | Queues communications command 7, whose worker-side case writes the socket raw-stream-mode byte. |
| `net_set_text_framing_enabled` | `0x00564120` | high | Writes the socket flag that selects printable text framing when true and binary 0xAA framing when false. |
| `net_write_u8` | `0x00564140` | high | Writes one byte to a packet body. |
| `net_write_u16be` | `0x00564160` | high | Writes a 16-bit value in network byte order. |
| `net_write_u32be` | `0x005641F0` | high | Writes a 32-bit value in network byte order. |
| `net_read_u8` | `0x00564260` | high | Reads one byte from an opcode-first packet body. |
| `net_read_u16be` | `0x00564270` | high | Reads a 16-bit big-endian value from an opcode-first packet body. |
| `net_read_u32be` | `0x005642C0` | high | Reads a 32-bit big-endian value from an opcode-first packet body. |
| `net_socket_dispatch` | `0x005643D0` | high | Thread::Socket vtable method that dispatches open, close, reconnect, send, and receive operations. |
| `net_open_transport` | `0x005645C0` | high | Selects the TCP connection path when the configured transport selector is 5. |
| `net_close_transport` | `0x005646A0` | high | Closes the active socket and auxiliary transport handle when present. |
| `net_receive_pending_data` | `0x00564870` | high | Selects the active TCP receiver for transport selector 5 and the serial/modem receiver for selectors 1 through 4. |
| `net_send_client_packet` | `0x005648A0` | high | Selects the outbound opcode transform, then sends either an AA and u16be binary frame or printable records containing the same transformed body. |
| `net_send_text` | `0x00565130` | high | Sends a NUL-terminated string through the active transport. |
| `net_send_byte` | `0x005651B0` | high | Sends one byte through the active transport. |
| `net_connect_and_initialize_transport` | `0x00565210` | high | Initializes Winsock, connects to the configured endpoint, performs the active retry, and registers asynchronous socket events. |
| `net_open_serial_modem_transport` | `0x00566A40` | high | Opens COM1 through COM4 for transport selectors 1 through 4 and prepares Windows serial buffers and timeouts. |
| `net_configure_serial_modem_transport` | `0x00566BF0` | high | Applies the requested baud rate, 8-N-1 defaults, and hardware or XON/XOFF flow-control fields through SetCommState. |
| `net_close_socket` | `0x00566D90` | high | Calls closesocket and restores the socket field to INVALID_SOCKET. |
| `net_close_serial_modem_transport` | `0x00566DD0` | high | Closes the serial COM handle and restores INVALID_HANDLE_VALUE. |
| `net_receive_serial_modem_data` | `0x00566E00` | high | Posts initial serial bytes in raw-stream mode, then collects printable records, applies the normal server transform, and posts decoded packet events. |
| `net_receive_frames` | `0x00567070` | high | Posts raw startup receives, then reads binary or printable frames, selects inbound transform mode by opcode, and posts decoded bodies. |
| `net_read_transport_byte` | `0x00567870` | high | Refills the TCP buffer with recv and returns one buffered transport byte. |
| `net_is_printable_frame_byte` | `0x00567B70` | high | Accepts bytes 0x21 through 0x7A plus newline for the printable frame collector. |
| `net_decode_printable_frames` | `0x00567BB0` | high | Validates decimal record sequence and group counts, then decodes four private-alphabet bytes to each three output bytes. |
| `net_decrypt_server_packet` | `0x00567DE0` | high | Reads the independent server-to-client sequence, reverses the seed-table and static or derived key XOR passes, and writes a local zero after the returned decoded length without validating the final payload byte. |
| `net_encrypt_client_packet` | `0x00567FB0` | high | Writes and increments the client-to-server sequence for every encrypted packet, applies XOR passes, and appends MD5 and seed trailer bytes. |
| `net_xor_packet_bytes` | `0x00568230` | high | Common 32-bit and remainder XOR engine for expanded byte keys and seed-table words. |
| `net_queue_seed_xor_table_selector` | `0x00568380` | high | Queues the server-supplied selector so the socket path can rebuild the 256-entry seed XOR table. |
| `net_queue_static_key` | `0x005683A0` | high | Queues a server-supplied key and explicit length so the socket path can replace the static key. |
| `net_set_static_key` | `0x005683F0` | high | Stores a runtime static key and copies it four times into the expanded key buffer. |
| `net_build_md5_salt_source` | `0x005684B0` | high | Builds the 1024-byte salt source through repeated lowercase MD5-hex expansion of session_character_name. |
| `net_derive_packet_key` | `0x00568540` | high | Derives nine per-packet key bytes from two seeds and the MD5 salt source. |
| `net_build_seed_xor_table` | `0x00568650` | high | Builds one of ten deterministic 256-entry repeated-byte XOR tables for selectors 0 through 9; selector 0 is the compiled default. |
| `net_send_confirm` | `0x005922A0` | high | UserConfirmPane calls this opcode 0x31 confirmation builder. |
| `net_server_packet_base_ctor` | `0x005959D0` | high | Constructs the base server packet object and stores its opcode. |
| `net_get_server_packet_opcode` | `0x00595A00` | high | Returns the opcode stored in a server packet base object. |
| `net_client_packet_base_ctor` | `0x00595A50` | high | Constructs the base client packet object and stores its opcode. |
| `net_packet_reader_ctor` | `0x00595B10` | high | Constructs the bounded reader used by server packet deserializers. |
| `net_server_packet_factory_ctor` | `0x00595F00` | high | Registers 61 opcode-specific server packet constructors in a 256-entry factory. |
| `net_deserialize_server_packet` | `0x005963F0` | high | Creates the registered server packet class and invokes its deserializer; it does not require the reader to consume the complete supplied body. |
| `net_create_server_packet` | `0x00596780` | high | Calls the registered constructor for a server opcode. |
| `net_deserialize_browser_packet` | `0x00597E50` | high | Parses SBrowser subtypes 1 and 2 as two u16be-length byte strings and subtype 3 as one u8-length homepage URL. |
| `net_decode_s_change_weather` | `0x00598210` | high | Reads the one-byte SChangeWeather payload; the main gameplay dispatcher has no opcode 0x1F consumer. |
| `net_decode_s_map_size` | `0x00599F90` | high | Reads map ID, dimensions, flags, secondary mode, checksum, and map name from SMapSize. |
| `net_server_request_portrait_ctor` | `0x0059B490` | high | Constructs RTTI-backed SRequestPortrait and passes opcode 0x49 to the server packet base. |
| `net_server_request_portrait_deserialize` | `0x0059B4C0` | high | Returns without reading fields, which confirms that SRequestPortrait has no body after the opcode. |
| `net_server_sound_effect_deserialize` | `0x0059BF30` | high | Reads one SSoundEffect command byte and a second music byte only for command 0xFF. |
| `net_deserialize_stipulation_packet` | `0x0059C8E0` | high | Parses SStipulation mode 0 as a u32be greeting CRC32 and mode 1 as u16be length plus compressed bytes. |
| `net_deserialize_transfer_server_packet` | `0x0059CA40` | high | Parses STransferServer as a u32be IPv4 value, u16be port, and u8-length opaque handoff token. |
| `net_send_portrait_profile` | `0x005B1160` | high | Calls net_build_send_portrait and submits the result through net_submit_client_packet. |
| `net_dispatch_server_packet` | `0x005ED990` | high | Routes parsed server packet objects to gameplay handlers by opcode. |
| `net_handle_s_map_size` | `0x005F1BF0` | high | Applies map dimensions, seasonal art, weather mode, local map cache, and map setup state. |
| `net_handle_map_part` | `0x005F2A60` | high | Consumes the raw decoded SMapPart body, creates MapLoadingPane, applies repeated map records, updates percentage progress, and finalizes the last part. |
| `net_send_put_ground` | `0x005F4430` | high | Builds opcode 0x0C with one u32be value. |
| `net_send_change_direction` | `0x005F4510` | high | WorldPane paths call this opcode 0x11 direction builder. |
| `net_send_refresh_user` | `0x005F4640` | high | WorldPane paths call this opcode-only 0x38 builder. |
| `net_send_check_time` | `0x005F7830` | high | Direct response to SCheckTime opcode 0x68; echoes a server value and appends timeGetTime(). |

## Rendering

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `render_get_image_library` | `0x00404A00` | high | Returns the ImageLib singleton used for sprite and UI frames. |
| `render_blit_screen_rgb565` | `0x0040CD00` | high | Applies blend mode 0x6D to an RGB565 destination. |
| `render_blit_screen_rgb555` | `0x0040D0D0` | high | Applies blend mode 0x6D to an RGB555 destination. |
| `render_blit_screen_mode` | `0x0040D4A0` | high | Selects the RGB565 or RGB555 screen-style blend used by static render flag 0x80. |
| `render_screen_pixel_rgb555` | `0x0040EAE0` | high | Combines one RGB555 source and destination pixel with the screen-style component formula. |
| `render_screen_pixel_rgb565` | `0x0040EC20` | high | Combines one RGB565 source and destination pixel with the screen-style component formula. |
| `render_bink_open_clip` | `0x0042E2D0` | high | Calls BinkOpen, configures playback, and registers the frame timer. |
| `render_bink_present_frame` | `0x0042E440` | high | Uses BinkWait, BinkDoFrame, BinkCopyToBuffer, and BinkNextFrame. |
| `render_get_video_system` | `0x0042E7E0` | high | Returns the VideoSystem singleton. |
| `render_direct_draw_ctor` | `0x004494B0` | high | Constructs the RTTI-backed DirectDraw wrapper. |
| `render_direct_draw_dtor` | `0x00449550` | high | Runs DirectDraw wrapper cleanup during deletion. |
| `render_direct_draw_initialize` | `0x004495D0` | high | Creates DirectDraw, selects cooperative and display modes, and creates presentation surfaces. |
| `render_direct_draw_shutdown` | `0x00449CB0` | high | Releases the clipper and surfaces, restores display mode, and releases DirectDraw. |
| `render_direct_draw_flip` | `0x00449FA0` | high | Flips the attached DirectDraw backbuffer. |
| `render_direct_draw_present_canvas` | `0x00449FD0` | high | Copies a Canvas to the DirectDraw presentation surface and recovers a lost surface. |
| `render_canvas_ctor` | `0x0044A490` | high | Constructs the RTTI-backed Canvas object. |
| `render_canvas_attach_surface` | `0x0044AA30` | high | Attaches a Canvas to a DirectDraw surface. |
| `render_canvas_create_memory` | `0x0044AB80` | high | Allocates a 16-bit memory canvas with width aligned to four pixels. |
| `render_canvas_release` | `0x0044B0D0` | high | Releases the current Canvas storage. |
| `render_canvas_begin` | `0x0044B160` | high | Begins pixel access and locks a wrapped surface when needed. |
| `render_canvas_end` | `0x0044B1B0` | high | Ends pixel access and unlocks a wrapped surface when needed. |
| `render_get_direct_draw` | `0x0044D820` | high | Returns the DirectDraw wrapper singleton. |
| `render_blit_image` | `0x0044DE30` | high | Draws a decoded Image with copy, blend, alpha, and special plane modes. |
| `render_blit_pixmap` | `0x0044FB80` | high | Draws an indexed PixMap with transparent zero pixels and several software blend modes. |
| `render_blit_canvas` | `0x00451E40` | high | Copies or blends one Canvas into another. |
| `render_average_pixels` | `0x004548B0` | high | Combines two 16-bit pixels with the fixed component-average lookup path. |
| `render_effect_image_session_ctor` | `0x004575B0` | high | Opens the available EFA or EPF variant for one effect image session. |
| `render_get_effect_frame_image` | `0x00457FD0` | high | Lazily decodes and caches one requested effect frame image. |
| `render_get_effect_image_pool` | `0x00459460` | high | Returns the EffectImagePool singleton. |
| `render_get_map_tile_library` | `0x004AE4E0` | high | Returns the MapTileImageLib singleton. |
| `render_map_background_images` | `0x004C5270` | high | Draws configured map background or bottom-layer images before world objects. |
| `render_screen_tree_frame` | `0x00554040` | high | Redraws the dirty root screen tree and presents the completed frame. |
| `render_screen_subtree` | `0x00555560` | high | Clips and draws one pane subtree through the vtable draw-to-target slot. |
| `render_probe_display_capabilities` | `0x0057A640` | high | Probes the current DirectDraw display mode before normal application initialization. |
| `render_free_blend_tables` | `0x005933C0` | high | Frees both software component-blend lookup tables. |
| `render_build_blend_tables` | `0x00593490` | high | Builds the 256 by 256 lookup tables for five-bit and six-bit color components. |
| `render_blend_pixel` | `0x005936E0` | high | Blends two 16-bit RGB pixels using a selector and the component lookup tables. |
| `render_palette_pack_16bit` | `0x00593B00` | high | Packs 256 RGB colors for the active display mode while reserving packed zero for palette index zero. |
| `render_video_system_ctor` | `0x00593E20` | high | Constructs the RTTI-backed VideoSystem singleton. |
| `render_video_system_dtor` | `0x00593EA0` | high | Shuts down an active VideoSystem and deletes its DirectDraw wrapper. |
| `render_video_system_initialize` | `0x00593F30` | high | Creates presentation state, canvases, conversion helpers, and software blend tables. |
| `render_video_system_shutdown` | `0x00594250` | high | Releases the main canvas and renderer lookup helpers before VideoSystem deletion. |
| `render_present_frame` | `0x005942D0` | high | Presents the completed canvas through the DirectDraw or window DC path. |
| `render_convert_rgb565_to_xrgb8888` | `0x005949A0` | high | Converts RGB565 pixels to 32-bit output with optional 2x nearest-neighbor scaling. |
| `render_scale_2x_u16` | `0x005950F0` | high | Doubles a 16-bit image in both axes with nearest-neighbor copies. |
| `render_scale_2x_u32` | `0x005953A0` | high | Doubles a 32-bit image in both axes with nearest-neighbor copies. |
| `render_static_tile_cache_ctor` | `0x005BA660` | high | Constructs the static HPF image cache and stores the base or alternate art mode. |
| `render_get_static_tile_image` | `0x005BA8D0` | high | Resolves one animated static tile through the selected stc or sts resource path. |
| `render_set_static_tile_bank` | `0x005BAB10` | high | Selects base stc or alternate sts static art and clears the static image cache on change. |
| `render_snow_weather_session_ctor` | `0x005BD950` | high | Creates the snow weather session, selects pane blend mode 7, and starts its 100 ms timer. |
| `render_spawn_snow_particles` | `0x005BDB70` | high | Places snow particle panes across and above the world view. |
| `render_update_snow_particles` | `0x005BDDA0` | high | Moves snow particles down, removes those below the view, and spawns replacements. |
| `render_create_snow_overlay` | `0x005C82C0` | high | Replaces the current weather session with WeatherSession_SnowParticle. |
| `render_hea_decode_mask` | `0x005C8540` | high | Expands HEA run words into an 8-bit light or occlusion mask. |
| `render_build_static_objects` | `0x005CD730` | high | Builds WorldObject_Static instances from the two static tile IDs in visible map cells. |
| `render_world_pane_content` | `0x005CE280` | high | Advances the visual frame and draws the world into the WorldPane canvas. |
| `render_use_base_ground_bank` | `0x005D2B70` | high | Selects tilea.bmp for the ground cache. |
| `render_use_alternate_ground_bank` | `0x005D2B90` | high | Selects tileas.bmp with tilea.bmp fallback for the ground cache. |
| `render_world_object` | `0x005D3190` | high | Calls the WorldObject virtual draw method at primary vtable slot 0x18. |
| `render_world_layer_queue` | `0x005D31D0` | high | Walks one sorted queue of visible world objects. |
| `render_collect_world_objects` | `0x005D3740` | high | Clips visible objects and assigns them to one of 32 draw-layer queues. |
| `render_world_frame` | `0x005D3F70` | high | Draws ground, map backgrounds, and sorted world objects for one world frame. |
| `render_ground_layer` | `0x005D6A50` | high | Updates and draws the cached visible ground-tile layer. |
| `render_set_ground_bank` | `0x005D7410` | high | Stores the active ground-bank selector and clears the cached ground layer. |
| `render_ground_tile` | `0x005D7690` | high | Copies one decoded isometric tile diamond into the ground cache canvas. |
| `render_effect_object` | `0x005DD380` | high | Draws a world effect frame with its selected software blend mode. |
| `render_update_effect_frame` | `0x005DD470` | high | Advances a world effect through its Effect.tbl frame sequence. |
| `render_item_object` | `0x005DE620` | high | Draws a ground item with its normal or faded blend state. |
| `render_living_object` | `0x005DF950` | high | Draws a living sprite with normal, highlighted, or transparent state. |
| `render_static_object_ctor` | `0x005E42F0` | high | Stores the static tile ID, side, image cache, SOTP render flags, and draw state. |
| `render_static_object` | `0x005E47E0` | high | Draws a fixed world object with its SOTP-selected software blend mode. |

## Audio

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `audio_bgm_player_ctor` | `0x004056C0` | high | Constructs the RTTI-backed BGMPlayer, installs Miles file callbacks, and keeps one stream handle. |
| `audio_bgm_player_dtor` | `0x004057A0` | high | Stops the active music path and unregisters the BGMPlayer singleton. |
| `audio_bgm_shutdown` | `0x00405830` | high | Cancels fade timers, pauses and closes the stream, and clears its handle. |
| `audio_bgm_play_path` | `0x00405880` | high | Queues one path for the BGM transition state machine. |
| `audio_bgm_queue_track` | `0x004058B0` | high | Saves a pending music path and starts the fade timer. |
| `audio_bgm_queue_stop` | `0x004058F0` | high | Queues an empty path so the current music fades out and closes. |
| `audio_bgm_get_target_volume` | `0x00405920` | high | Returns the one-byte BGM target volume. |
| `audio_bgm_set_target_volume` | `0x00405940` | high | Changes the one-byte BGM target and schedules a fade tick when needed. |
| `audio_bgm_mute` | `0x004059A0` | high | Mutes the Miles stream output without replacing the stored target volume. |
| `audio_bgm_unmute` | `0x004059D0` | high | Restores stream output from the current fade volume. |
| `audio_bgm_file_open` | `0x00405A00` | high | Rewrites the logical .mp3 extension to .mus and opens the loose music file. |
| `audio_bgm_file_close` | `0x00405AB0` | high | Closes a BGM file handle for the Miles callback set. |
| `audio_bgm_file_seek` | `0x00405AD0` | high | Implements seek and position queries for the Miles BGM file callbacks. |
| `audio_bgm_file_read` | `0x00405B40` | high | Reads bytes for the Miles BGM file callbacks. |
| `audio_bgm_timer_callback` | `0x00405B80` | high | Advances timer ID 0 and schedules another BGM fade tick after 200 ms while needed. |
| `audio_bgm_transition_tick` | `0x00405BC0` | high | Fades the old stream to zero, replaces it, and fades the new stream toward the target. |
| `audio_bgm_schedule_tick` | `0x00405E20` | high | Schedules a 200 ms BGM transition timer through the shared event system. |
| `audio_get_sound_manager` | `0x004316E0` | high | Returns the SoundManager singleton pointer. |
| `audio_midi_play_file` | `0x00508D80` | high | Dormant standard MIDI play entry point with no static caller in the matching client. |
| `audio_midi_stop_or_restart` | `0x00508ED0` | high | Pauses, resets, or restarts the Windows MIDI stream according to its flags. |
| `audio_midi_start_stream` | `0x00509010` | high | Opens a Windows MIDI stream, prepares two buffers, and begins queued playback. |
| `audio_midi_free_buffers` | `0x005092E0` | high | Unprepares and frees the two MIDI stream buffers. |
| `audio_midi_stream_callback` | `0x005093B0` | high | Refills completed MIDI buffers and handles end or conversion failure. |
| `audio_midi_set_channel_volume` | `0x00509690` | high | Sends MIDI controller 7 volume for one channel after master scaling. |
| `audio_midi_set_master_volume` | `0x005096F0` | high | Rescales stored channel volumes; this entry point has no static caller. |
| `audio_midi_parse_smf` | `0x00509950` | high | Parses standard MThd and MTrk chunks from an archive-backed MIDI file. |
| `audio_sfx_player_ctor` | `0x00568A00` | high | Constructs SndEffectPlayer with the shared Miles driver and an empty sample cache. |
| `audio_sfx_player_dtor` | `0x00568AA0` | high | Stops and releases every cached Miles sample handle. |
| `audio_sfx_get_or_load` | `0x00568B60` | high | Loads numeric MP3 bytes from Legend.dat, with an active WAV fallback, or returns the cached handle. |
| `audio_sfx_play` | `0x00568DB0` | high | Applies the shared sound-effect volume and starts one cached Miles sample. |
| `audio_sfx_stop` | `0x00568E10` | high | Ends the cached Miles sample for one numeric sound ID. |
| `audio_sfx_stop_all` | `0x00568E50` | high | Ends every cached Miles sample handle. |
| `audio_sfx_set_volume` | `0x00568EA0` | high | Stores one sound-effect volume and applies it to every cached sample. |
| `audio_sfx_get_volume` | `0x00568F00` | high | Returns the one-byte sound-effect volume. |
| `audio_sound_manager_ctor` | `0x00568F20` | high | Constructs the RTTI-backed SoundManager and creates the Miles driver wrapper. |
| `audio_sound_manager_initialize` | `0x00568FC0` | high | Creates SndEffectPlayer and BGMPlayer after core SoundManager construction. |
| `audio_destroy_players` | `0x005690A0` | high | Stops and deletes both active audio players before Miles shutdown. |
| `audio_sound_manager_dtor` | `0x005690E0` | high | Destroys the players and Miles wrapper, then unregisters the SoundManager singleton. |
| `audio_get_sound_volume_level` | `0x00569170` | high | Converts the internal sound-effect volume back to a saved and UI level by dividing by 20. |
| `audio_set_sound_volume_level` | `0x005691A0` | high | Converts the saved and UI sound level to Miles units by multiplying by 20. |
| `audio_play_sound_effect` | `0x005691D0` | high | Public SoundManager entry point for a numeric sound-effect ID. |
| `audio_stop_sound_effect` | `0x00569200` | high | Public SoundManager entry point to stop one numeric sound-effect ID. |
| `audio_is_sound_enabled` | `0x00569290` | high | Returns the SoundManager sound-setting flag. |
| `audio_enable_sound` | `0x005692B0` | high | Sets the SoundManager sound-setting flag. |
| `audio_disable_sound` | `0x005692D0` | high | Stops every sound effect and clears the SoundManager sound-setting flag. |
| `audio_get_music_volume_level` | `0x00569300` | high | Converts the internal music target back to a saved and UI level by dividing by 20. |
| `audio_set_music_volume_level` | `0x00569340` | high | Multiplies the saved and UI music level by 20 and updates the fade target. |
| `audio_play_music_path` | `0x00569370` | high | Public SoundManager entry point that saves and queues one logical music path. |
| `audio_stop_music` | `0x005693C0` | high | Queues a music fade-out and clears the saved current path. |
| `audio_miles_driver_ctor` | `0x005693F0` | high | Starts Miles and requests a 22050 Hz, 16-bit, stereo digital driver with one retry. |
| `audio_miles_driver_dtor` | `0x00569470` | high | Closes the digital driver and shuts Miles down. |
| `audio_handle_sound_effect_packet` | `0x005F6B20` | high | Plays a numeric effect or changes music according to the decoded SSoundEffect form. |

## Maps and files

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `file_spf_view_initialize` | `0x004021D0` | high | Maps the SPF prefix, optional palette, frame table, and pixel blob. |
| `file_spf_get_frame` | `0x004022A0` | high | Returns one SPF frame view from its 0x20-byte record. |
| `file_hpf_decode` | `0x004319B0` | high | Checks magic 0xFF02AA55, decodes symbols through an adaptive tree, and accepts raw input when magic is absent. |
| `file_hpf_tree_initialize` | `0x00431B80` | high | Builds the complete initial tree for byte symbols and the 256 terminator. |
| `file_hpf_decode_symbol` | `0x00431C40` | high | Reads bits least-significant bit first and walks the active HPF tree to a symbol leaf. |
| `file_hpf_rotate_tree` | `0x00431D20` | high | Applies the parent and sibling rotations used after every decoded HPF symbol. |
| `file_load_color_table` | `0x0044CD50` | medium | Loads color.tbl records and packs six RGB triples per record for the renderer. |
| `file_open_efa` | `0x00456F30` | high | Opens an EFA resource and returns its frame count and table view. |
| `file_decode_efa_frame` | `0x00457030` | high | Inflates one zlib payload from a 0x40-byte EFA frame record and builds an Image view. |
| `file_load_effect_frame_table` | `0x00458ED0` | high | Parses Effect.tbl decimal frame sequences into per-effect tables. |
| `file_archive_xor_words` | `0x00471DC0` | high | XORs a buffer in 32-bit words for the extended DAT header and index path. |
| `file_archive_open` | `0x00471E00` | high | Opens resource or loose DAT input and maps either the legacy index or the extended chunked index. |
| `file_archive_find_entry` | `0x00472470` | high | Looks up a named entry in an opened archive. |
| `file_archive_get_entry_data` | `0x00472900` | high | Returns the mapped data pointer for an archive entry. |
| `file_load_variant_color_table` | `0x0047DEB0` | medium | Loads one numbered color table family used by renderable assets. |
| `file_hea_build_row_views` | `0x00487380` | high | Builds row pointers from HEA band thresholds and lookup offsets for a clipped region. |
| `file_hea_open` | `0x004875B0` | high | Maps the HEA header, band array, row offsets, and packed run stream. |
| `file_read_image_metadata` | `0x0048B390` | high | Reads shared EPF metadata or dispatches SPF metadata parsing. |
| `file_load_image_frame` | `0x0048B530` | high | Loads one EPF or SPF frame for the shared image library. |
| `file_load_message_table` | `0x004A4AA0` | high | Loads the line-oriented msg.tbl data from an archive or loose file. |
| `file_decode_ctf_map_tile` | `0x004C7000` | high | Palette-converts one alternate 784-byte indexed tile source to 16-bit pixels. |
| `file_decode_dtf_map_tile` | `0x004C7180` | high | Reads one alternate 1568-byte 16-bit tile source and converts color format when needed. |
| `file_tile_bank_storage_ctor` | `0x004C7280` | high | Opens one fixed-record raw tile bank and selects its palette path. |
| `file_decode_raw_map_tile` | `0x004C7390` | high | Extracts and palette-converts one 784-pixel diamond from a raw 56 by 27 indexed record. |
| `map_tile_library_ctor` | `0x004C7560` | high | Opens tilea.bmp as the base ground bank and tileas.bmp as the alternate bank. |
| `map_load_tile_pixels` | `0x004C78C0` | high | Applies ground animation, then loads the alternate bank with base-bank fallback when selected. |
| `file_load_metadata_compressed` | `0x004E5570` | high | Loads a cached compressed metadata file and inflates it for parsing. |
| `file_save_metadata_compressed` | `0x004E56E0` | high | Writes the original compressed metadata payload under the metafile directory. |
| `file_load_motion_effect_table` | `0x0050E840` | medium | Loads structured motion effect definitions from meffect.tbl. |
| `file_load_npc_info_table` | `0x005322A0` | medium | Loads the hierarchical npci.tbl text resource. |
| `file_load_field_palette_table` | `0x00546440` | high | Loads the pal*.tbl field palette range family. |
| `file_load_item_palette_table` | `0x00546980` | high | Loads itempal.tbl range mappings. |
| `file_load_effect_palette_table` | `0x00546C30` | high | Loads effpal.tbl range mappings and their palette family values. |
| `file_load_static_palette_table` | `0x00546EE0` | high | Loads stcpal.tbl mappings used by HPF static images. |
| `file_load_map_tile_palette_table` | `0x00547210` | high | Loads mptpal.tbl map tile palette mappings. |
| `file_palette_table_parse_ranges` | `0x00547810` | high | Parses two-token single IDs and three-token inclusive ID ranges from palette TBL files. |
| `file_palette_load_rgb` | `0x00548650` | high | Copies exactly 0x300 bytes of RGB triples and passes them to the 16-bit palette packer. |
| `file_save_character_profile` | `0x0054CD30` | high | Writes at most 0x172 bytes to profile.txt under the current character directory. |
| `file_decode_portrait_image` | `0x0054D680` | high | Decodes an in-memory portrait as a 56 by 48 JFIF JPEG or the legacy EPF form. |
| `file_initialize_skill_tables` | `0x00561490` | medium | Initializes the Skill_e.tbl and Skill_i.tbl table families. |
| `file_parse_skill_table` | `0x00561840` | medium | Parses numeric skill table rows while accepting semicolon comments. |
| `map_rotate_static_tile_mapping` | `0x00586900` | high | Rotates every static tile ID in an animation group to the next mapped ID. |
| `map_rotate_ground_tile_mapping` | `0x005869F0` | high | Rotates every ground tile ID in an animation group to the next mapped ID. |
| `map_advance_tile_animations` | `0x005872C0` | high | Advances animation counters and rotates a group when its delay expires. |
| `map_tile_animation_manager_ctor` | `0x005873A0` | high | Loads gndani.tbl and stcani.tbl and builds their animation groups. |
| `map_add_tile_animation_group` | `0x00587750` | high | Registers one tile-ID cycle and its delay from an animation-table line. |
| `map_apply_tile_animation_step` | `0x00587C90` | high | Rotates the ground or static mapping and invalidates the affected cached images. |
| `map_tile_animation_timer` | `0x00587D10` | high | Advances tile animation groups on a shared 100 ms timer. |
| `file_load_ground_attribute_table` | `0x0058B8C0` | high | Loads structured ground attributes from gndattr.tbl. |
| `file_build_character_path` | `0x00592DE0` | high | Builds .\&lt;character&gt;\.\&lt;filename&gt; from the active character name and supplied local filename. |
| `file_load_character_profile` | `0x005B13E0` | high | Reads at most 0x172 bytes from the current character's profile.txt into the editor buffer. |
| `file_save_portrait_dialog_profile` | `0x005B15C0` | high | Writes the dialog profile buffer to profile.txt after the 0x172-byte DBCS-safe cap. |
| `map_update_crc16` | `0x005B9180` | high | Calculates and caches the custom CRC16 across six bytes for each map cell. |
| `file_read_map_cells` | `0x005B9450` | high | Reads a row-major width times height array of six-byte map cells. |
| `file_format_map_path` | `0x005B9660` | high | Formats the path maps backslash lod map-id dot map. |
| `file_write_map_cells` | `0x005B9680` | high | Writes the same six-byte map-cell array consumed by the map reader. |
| `map_apply_seasonal_tile_mode` | `0x005C7660` | high | Applies the SMapSize 0x80 flag to both ground and static tile storage. |
| `map_get_sotp_render_flags` | `0x005CF360` | high | Returns the high-nibble SOTP render flags for one static tile ID. |
| `map_load_sotp_render_flags` | `0x005CF3B0` | high | Loads SOTP.DAT into a one-based high-nibble render-flag table. |
| `map_get_sotp_collision_flags` | `0x005CF4A0` | high | Returns the low-nibble SOTP direction mask for one static tile ID. |
| `map_load_sotp_collision_flags` | `0x005CF4F0` | high | Loads SOTP.DAT into a one-based low-nibble collision table. |
| `map_get_collision_level` | `0x005CF5E0` | high | Combines dynamic occupants and the two static SOTP masks at one map cell. |
| `map_get_tile_pixels` | `0x005D7610` | high | Gets one decoded ground-tile diamond from MapTileImageLib. |
| `map_can_move_direction` | `0x005EFFE0` | high | Checks bounds, dynamic occupants, and direction-specific SOTP masks for a proposed move. |
| `map_apply_weather_mode` | `0x005F26C0` | high | Creates snow for mode 1, performs no local setup for mode 2, and changes lighting state for mode 3. |
| `map_finish_transfer` | `0x005F2DE0` | high | Closes MapLoadingPane and either applies the completed map or schedules the alternate completion path. |
| `file_load_static_tile_pixmap` | `0x005FD500` | high | Opens and decodes one base or alternate static HPF resource into a pixmap view. |
| `file_open_static_tile` | `0x005FD700` | high | Opens stsNNNNN.hpf in alternate mode and falls back to stcNNNNN.hpf when missing. |
| `file_format_static_tile_path` | `0x005FD850` | high | Formats stcNNNNN.hpf for base art or stsNNNNN.hpf for alternate art. |
| `file_zlib_uncompress` | `0x006043B0` | high | Bundled zlib 1.1.3 uncompress entry shared by assets and network-managed data. |

## Crypto

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `crypto_md5_hex_string` | `0x004C7D80` | high | Hashes a NUL-terminated string and returns lowercase MD5 hexadecimal text. |
| `crypto_md5_bytes` | `0x004C7E30` | high | Hashes an explicit byte span and retains the raw MD5 digest. |

## Uncertain

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `maybe_security_check_mscfg_marker` | `0x00431ED0` | medium | Tests for Mscfg.dll under the system directory and sets config +0x668. |
| `maybe_app_configure_distribution_mode_12` | `0x00436A10` | medium | Dormant mode 12 handler with no matching marker return; sets connection flags without installing an endpoint. |

## Other

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `crc16_buffer` | `0x00568870` | high | Applies the custom CRC16 update to a byte buffer starting from zero. |
| `startup_run_pending_patcher` | `0x0057A330` | high | Before normal startup, requires both Patch/Info and Patch/Script to relaunch Patcher2.exe; otherwise deletes both markers and continues. |
| `crc16_update` | `0x005B8F30` | high | Updates the custom CRC16 with table[crc high byte] XOR crc shifted left XOR input byte. |
| `crc32_update` | `0x00604530` | high | Standard reflected IEEE CRC32 update with initial and final inversion. |
