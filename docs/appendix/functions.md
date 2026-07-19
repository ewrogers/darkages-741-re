# Function reference

This appendix is the address book for functions named in the main text. Static addresses assume preferred image base `0x00400000`. At runtime, use the loaded module base and the matching RVA.

Roles are short summaries from the checked-in Binary Ninja YAML exports. Those exports remain the source for full evidence and provenance.

## Application lifecycle and configuration

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `app_detect_bad_guy_marker` | `0x00431ED0` | high | Reconstructs %SystemRoot%\System32\Mscfg.dll and sets config +0x668 from file existence alone. |
| `app_config_ctor` | `0x00431FF0` | high | Constructs Config, loads Darkages.cfg, selects a distribution mode, and dispatches endpoint initialization. |
| `app_save_config` | `0x00432340` | high | Writes Darkages.cfg in text mode. |
| `app_configure_unitel_distribution` | `0x00433B40` | high | Empty dormant mode 2 initializer selected by Unitel.nfo in the unreferenced marker scanner. |
| `app_get_distribution_mode` | `0x00434EB0` | high | Caches and returns the distribution mode selected by app_select_distribution_mode. |
| `app_select_distribution_mode` | `0x00434EF0` | high | Returns the constant distribution mode 1 in this target. |
| `app_detect_distribution_mode_from_markers` | `0x00434F00` | high | Dormant unreferenced scanner that maps country and Korean ISP .nfo markers to distribution modes 1 through 15. |
| `app_derive_installation_id16` | `0x00436E10` | high | Applies the client's custom 0x1021-table recurrence to the four little-endian bytes of the persistent 32-bit installation ID. |
| `app_language_mode_from_distribution` | `0x004A49B0` | high | Maps distribution modes to Korean 0, English 1, Japanese 2, or Taiwan 3 language modes. |
| `app_get_text_code_page` | `0x004A4A30` | high | Returns the code-page value selected with the current language mode. |
| `app_get_language_message_label` | `0x004A4A60` | high | Maps language modes to msgkor.h, msgeng.h, msgjpn.h, or msgtai.h labels retained by the client. |
| `app_set_language_mode` | `0x004A4CE0` | high | Stores the language mode, selects the retained message label, and records code page 949 or 932 for Korean or Japanese. |
| `app_shutdown` | `0x004AC060` | high | Tears down runtime managers and panes, then closes and destroys the DAT archive singletons before window cleanup. |
| `app_set_post_exit_advertisement` | `0x004ACE00` | high | Copies the SAdvertisement string into a 65,536-byte application buffer, terminates it, and saves its length plus three numeric arguments for app_winmain. |
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
| `input_get_pointer_position` | `0x00466C40` | high | Copies EventMan's current pointer coordinates from +0x10 and +0x14 into the caller's two-word position. |
| `input_post_pointer_move` | `0x00466C80` | high | Public EventMan entry that honors input blocking before updating coordinates and emitting pointer type 0x00. |
| `input_begin_server_block` | `0x00466CC0` | high | Emits releases for held left and right mouse buttons, then opens the singleton ClockPane input blocker. |
| `input_end_server_block` | `0x00466D00` | high | Closes the singleton ClockPane used by the server-controlled input block. |
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
| `input_map_key_to_world_direction` | `0x005F0B50` | high | Maps all accepted movement-key aliases to the four cardinal Direction values 0 through 3. |

## UI

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `ui_agreement_dialog_pane_ctor` | `0x00402430` | high | Constructs RTTI-backed AgreementDialogPane from _nagree.txt, attaches OK and Cancel controls, inserts the current greeting, and registers the pane. |
| `ui_agreement_dialog_handle_action` | `0x004028F0` | high | Action 0 closes and unregisters the agreement pane without sending a packet. |
| `ui_browser_dialog_ctor` | `0x00415CB0` | high | Constructs exact RTTI BrowserDialogPane with an embedded BrowserControlPane; when no response or initial URL is supplied, sends CWebBoard action 0. |
| `ui_browser_dialog_apply_web_board` | `0x004165A0` | high | Accepts SWebBoard actions 0 and 1, installs domain and boardinfo WinINet cookies, sets the embedded browser base URL, and navigates to start_url. |
| `ui_browser_dialog_handle_network_event` | `0x00416A50` | high | BrowserDialogPane's network-event handler dispatches exact RTTI SWebBoard opcode 0x62 to its cookie and navigation path. |
| `ui_browser_dialog_handle_timer` | `0x00416AB0` | high | Timer 0x572 opens Web Board Request Timeout after 20 seconds and closes the waiting BrowserDialogPane. |
| `ui_browser_control_set_base_url` | `0x00417910` | high | Copies a bounded base URL into BrowserControlPane's browser state. |
| `ui_browser_control_navigate` | `0x00417A40` | high | Converts the URL and optional header to BSTR values and calls the embedded IWebBrowser navigation method. |
| `ui_browser_window_set_base_url` | `0x00419650` | high | Copies a bounded base URL into BrowserWindow's browser state. |
| `ui_browser_window_navigate` | `0x00419700` | high | Navigates BrowserWindow's embedded IWebBrowser to the supplied URL and optional header. |
| `ui_bottom_buttons_pane_ctor` | `0x0041B040` | high | Constructs exact RTTI class BtmButtonsPane_A, initializes its state, and immediately sends the empty CSelfLook request. |
| `ui_bottom_buttons_handle_network_event` | `0x0041B690` | high | BtmButtonsPane_A network-event handler routes SStatus to the parcel/mail updater and SSelfLook to the profile-response path. |
| `ui_bottom_buttons_handle_timer` | `0x0041B710` | high | BtmButtonsPane_A TimerHandler callback retries CSelfLook for timer 0x03000000 while the initial profile request is pending. |
| `ui_bottom_buttons_set_group_invitation_state` | `0x0041B810` | high | Applies the server-authoritative SSelfLook group-open value to the bottom-button state, clears the group-button pending action, and invalidates the pane. |
| `ui_bottom_buttons_apply_self_look` | `0x0041BC10` | high | Consumes SSelfLook in BtmButtonsPane_A and applies is_group_open before redrawing; this is the only group-icon state update after CGroupToggle. |
| `ui_bottom_buttons_handle_action` | `0x0041BE30` | high | Handles the three bottom-button actions; the group action marks itself pending, sends CGroupToggle, and then requests SSelfLook without changing the icon optimistically. |
| `ui_legend_list_draw_item` | `0x0042BA20` | high | Draws one Self Look legend record by icon, resolves its color through palette slot 0, and renders its text. |
| `ui_new_legend_dialog_action` | `0x0042CA50` | high | The RTTI-backed NewLegendDialogPane action normalizes line breaks, ends profile text at the fifth break, and saves profile.txt. |
| `ui_legend_dialog_apply_self_look` | `0x0042CD80` | high | Clears and rebuilds the older LegendDialogPane list from SSelfLook's fixed-size legend records. |
| `ui_intro_video_pane_ctor` | `0x0042DFF0` | high | Initializes the CIPane vtable and Bink-backed video state. |
| `ui_intro_video_begin_sequence` | `0x0042E1F0` | high | Stores two clip resources and starts the first clip. |
| `ui_get_intro_video_pane` | `0x0042E7D0` | high | Returns the global CIPane instance at 0x006DA3A0. |
| `ui_show_input_block_clock` | `0x0042E800` | high | Creates the exact RTTI ClockPane singleton when absent and activates its 50 ms animated wait-cursor path. |
| `ui_hide_input_block_clock` | `0x0042E890` | high | Closes and destroys the active ClockPane singleton when present. |
| `ui_clock_pane_ctor` | `0x0042E8C0` | high | Constructs the 0x1A0-byte exact RTTI ClockPane, loads lodclk.epf metadata, centers it on the current pointer, and registers it in the screen and event trees. |
| `ui_clock_pane_show` | `0x0042EB00` | high | Selects root cursor mode 3, shows ClockPane, draws its next frame, and schedules timer 0x1234 at 50 ms. |
| `ui_clock_pane_close` | `0x0042EBA0` | high | Cancels timer 0x1234, hides ClockPane, restores cursor mode 0, and notifies the optional cursor observer. |
| `ui_clock_pane_timer_callback` | `0x0042EC00` | high | Advances the lodclk.epf frame modulo the loaded frame count and requeues timer 0x1234 using the existing 50 ms interval. |
| `ui_clock_pane_handle_keyboard_event` | `0x0042EC70` | high | Returns true for every keyboard or text event so lower panes do not receive it while ClockPane is active. |
| `ui_clock_pane_handle_pointer_event` | `0x0042EC80` | high | Re-centers ClockPane on pointer-move events and returns true for every pointer event, consuming clicks and wheel input. |
| `ui_clock_pane_set_frame` | `0x0042ED00` | high | Loads and draws one lodclk.epf frame when its signed 16-bit selector differs from ClockPane +0x198. |
| `ui_clock_pane_dtor` | `0x0042EDC0` | high | Destroys ClockPane and clears its Singleton&lt;ClockPane&gt; registration before the optional object free. |
| `ui_has_clock_pane` | `0x0042EE70` | high | Reports whether clock_pane_singleton_ptr is non-null. |
| `ui_get_clock_pane` | `0x0042EE90` | high | Returns the active ClockPane singleton pointer. |
| `ui_create_user_dialog_ctor` | `0x0043C370` | high | Constructs RTTI class CreateUserDialogPane from _ncreate.txt, attaches appearance controls and account fields, and registers the pane for events and timers. |
| `ui_create_user_draw` | `0x0043D190` | high | Draws the creation preview using gender at +0x674, hair style at +0x676, and hair-color palette index at +0x678. |
| `ui_create_user_handle_pointer_event` | `0x0043DC80` | high | Handles CreateUserDialogPane appearance clicks, including gender selection and conversion of the 2-by-7 hair-color swatch grid into palette indexes. |
| `ui_create_user_handle_action` | `0x0043EAD0` | high | Collects name, password, confirmation, and distribution-dependent account text; checks matching passwords and schedules the create-user send timer. |
| `ui_create_user_timer` | `0x0043F410` | high | CreateUserDialogPane TimerHandler callback; timer 3 sends CNewUser after the form action schedules a 200 ms delay. |
| `ui_dialog_pane_ctor` | `0x00445260` | high | Constructs DialogPane over Pane and initializes its control collection and interaction fields. |
| `ui_dialog_add_control` | `0x00445670` | high | Creates DialogPane +0x594 on first use and inserts the supplied control pointer. |
| `ui_dialog_set_default_action` | `0x004457D0` | high | Stores a validated attachment-order control index at DialogPane +0x598; Enter and Space dispatch through this index. |
| `ui_dialog_set_cancel_action` | `0x00445820` | high | Stores a validated attachment-order control index at DialogPane +0x59C; the inherited keyboard handler dispatches Escape through this index. |
| `ui_dialog_handle_pointer_event` | `0x00445A20` | high | DialogPane primary-vtable +0x48 implementation for hit testing, child dispatch, hover, pressed state, and actions. |
| `ui_dialog_handle_keyboard_event` | `0x00445FF0` | high | DialogPane primary-vtable +0x4C implementation for focus traversal and focused-control dispatch. |
| `ui_dialog_handle_application_event` | `0x004462D0` | high | DialogPane primary-vtable +0x54 implementation that forwards application and IME events to the focused control. |
| `ui_dialog_hit_test_control` | `0x004468C0` | high | Walks DialogPane controls, checks each rectangle, and calls control virtual +0x78 for a local hit-zone code. |
| `ui_dialog_set_focused_control` | `0x00446BC0` | high | Transitions DialogPane +0x5AC between control indexes and invokes old/new focus hooks. |
| `ui_dialog_focus_previous_control` | `0x00446CD0` | high | Searches backward with wrapping for an enabled, focusable control. |
| `ui_dialog_focus_next_control` | `0x00446DD0` | high | Searches forward with wrapping for an enabled, focusable control. |
| `ui_dialog_dispatch_pointer_to_control` | `0x00446FE0` | high | Converts pointer coordinates to control-local space, calls control virtual +0x48, and restores the event. |
| `ui_alert_pane_ctor` | `0x00448000` | high | Constructs exact RTTI class AlertPane from counted display text, a parent pane, and one or two button assets. |
| `ui_window_message_dialog_pane_ctor` | `0x004488C0` | high | Builds the standard scrollable or alternate woodbook-style SMessage popup from an explicit byte buffer. |
| `ui_equip_pane_handle_network_event` | `0x0045D970` | high | Exact RTTI class EquipPane routes SAddEquip, SRemoveEquip, and SSelfLook from its primary-vtable network-event slot. |
| `ui_equip_pane_apply_self_look` | `0x0045FDC0` | high | Copies SSelfLook identity, nation, group, class, and legend state into EquipPane and its dependent panes. |
| `ui_equip_pane_add_equipment_from_packet` | `0x004601D0` | high | Converts the SAddEquip slot to an index and stores sprite, dye, name, current durability, and maximum durability in EquipPane's 18-entry arrays. |
| `ui_equip_pane_remove_equipment_from_packet` | `0x004602B0` | high | Clears the selected EquipPane sprite, name, and durability fields without clearing the retained dye byte. |
| `ui_pane_schedule_timer` | `0x00464050` | high | Schedules a timer for a Pane by passing its TimerHandler subobject at +0x11C. |
| `ui_pane_cancel_timers` | `0x00464740` | high | Converts a Pane pointer to TimerHandler +0x11C and cancels matching timers. |
| `ui_exchange_dialog_ctor` | `0x00469560` | high | Constructs the exact RTTI ExchangeDialog from _nexch.txt, attaches its offer controls, registers it under GUIBackPane, and stores the Started event ID at +0x630. |
| `ui_exchange_dialog_dtor` | `0x00469E70` | high | Decrements the modal count, unregisters ExchangeDialog from event and screen routing, and runs the DialogPane destructor. |
| `ui_exchange_dialog_handle_action` | `0x00469FF0` | high | Maps attachment-order action 0 to CExchange Accept 0x05 and action 1 to Cancel 0x04. |
| `ui_exchange_dialog_handle_inventory_drop` | `0x0046A030` | high | Reads the source InvItemPane one-based slot and sends CExchange AddItem 0x01. |
| `ui_exchange_dialog_handle_network_event` | `0x0046A1E0` | high | Consumes decoded opcode 0x42 and forwards it to the ExchangeDialog server-event dispatcher. |
| `ui_exchange_dialog_dispatch_server_event` | `0x0046A240` | high | Routes SExchange events 0x01 through 0x05 to quantity, item, gold, cancelled, and accepted handlers. |
| `ui_exchange_handle_count_request` | `0x0046A690` | high | Reads SExchange event 0x01 slot and creates AddItemWithCountDialog with that slot and the active exchange ID. |
| `ui_exchange_handle_item_added` | `0x0046A760` | high | Reads event 0x02 party, index, tagged u16 sprite, dye byte, and string8 name, then updates MyExchange for party zero or YourExchange otherwise. |
| `ui_exchange_handle_gold_added` | `0x0046A900` | high | Reads event 0x03 party and big-endian u32 gold, then updates MyMoney for party zero or YourMoney otherwise. |
| `ui_exchange_handle_cancelled` | `0x0046A9E0` | high | Skips the party byte, opens the supplied string8 message in a one-button alert, and removes ExchangeDialog immediately. |
| `ui_exchange_handle_accepted` | `0x0046AB20` | high | Marks the indicated party accepted and opens the final message alert only when both local and other acknowledgement flags are set. |
| `ui_field_map_balloon_pane_ctor` | `0x00474310` | high | Constructs exact RTTI FieldMapBalloonPane, loads its EPF and optional palette, and retains its parent FieldMapPane for animation completion. |
| `ui_field_map_balloon_handle_timer` | `0x00474660` | high | FieldMapBalloonPane TimerHandler callback advances the marker every 50 ms and schedules FieldMapPane completion event 1 when movement ends. |
| `ui_field_map_balloon_set_target` | `0x00474A50` | high | Stores the marker target, movement-step count, correlation time, and parent completion-event selector; equal current and target coordinates collapse the step count to zero. |
| `ui_field_map_pane_ctor` | `0x00474BC0` | high | Constructs exact RTTI FieldMapPane over Pane and its TimerHandler secondary base before initializing the field assets and server nodes. |
| `ui_field_map_pane_initialize` | `0x00474D40` | high | Loads the selected field asset family, builds one image or text point pane per server node, and positions the initial marker from the zero-based current-node index. |
| `ui_field_map_pane_register_screen` | `0x00475370` | high | Registers FieldMapPane and its point children, attaches optional local point animations, and creates the animated FieldMapBalloonPane marker at the current node. |
| `ui_field_map_pane_draw` | `0x00475B40` | high | Draws the field-map background loaded from frame 0 of the field-name EPF. |
| `ui_field_map_pane_handle_timer` | `0x00475BD0` | high | FieldMapPane TimerHandler event 0 selects a server node and starts marker movement; correlated event 1 sends CFieldMap for the selected node and restores legend.pal. |
| `ui_field_map_point_pane_ctor` | `0x00476050` | high | Constructs exact RTTI FieldMapPointPane and retains node index, checksum, map ID, destination coordinates, screen coordinates, name, and parent pane. |
| `ui_field_map_point_handle_pointer` | `0x00476120` | high | FieldMapPointPane primary-vtable pointer handler updates hover state and sends a left-button release to the parent's timer path as the selected node index. |
| `ui_text_field_map_point_pane_ctor` | `0x00476490` | high | Constructs exact RTTI TextFieldMapPointPane for a server node that has no matching local presentation record. |
| `ui_image_field_map_point_pane_ctor` | `0x00476740` | high | Constructs exact RTTI ImageFieldMapPointPane with icon and position metadata matched locally by the server node name. |
| `ui_load_field_map_assets` | `0x00476EE0` | high | Loads the field-name EPF background, optional PAL, required TXT metadata, palette list, and locally styled waypoint records. |
| `ui_game_message_pane_ctor` | `0x0047C2A0` | high | Constructs the RTTI-backed four-row floating GameMessagePane used for short colored notices. |
| `ui_game_message_pane_append_formatted_rgb` | `0x0047C5C0` | high | Parses inline color markup and appends colored byte cells to the fading GameMessagePane overlay. |
| `ui_game_message_pane_append_bytes` | `0x0047C6F0` | high | Writes colored byte cells into the current floating-message row, wrapping and rotating the four-row buffer. |
| `ui_game_message_pane_update_bounds` | `0x0047C9C0` | high | Recomputes the floating overlay bounds from the occupied rows and their widest line. |
| `ui_game_message_pane_discard_oldest_line` | `0x0047D120` | high | Rotates the four line records and clears the oldest row when the overlay fills. |
| `ui_text_truncate_dbcs_safe` | `0x0047D670` | high | Stops at the byte limit without leaving a Windows DBCS lead byte at the end. |
| `ui_append_game_message_palette` | `0x004803A0` | high | Resolves a palette entry to RGB and appends the text to GameMessagePane. |
| `ui_append_game_message_rgb` | `0x004803E0` | high | Appends text to the active GameMessagePane using explicit RGB bytes. |
| `ui_game_message_pane_exists` | `0x00480450` | high | Tests whether the GameMessagePane singleton currently exists. |
| `ui_get_game_message_pane` | `0x00480470` | high | Returns the active GameMessagePane singleton pointer. |
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
| `ui_hot_key_pane_ctor` | `0x00488320` | high | Constructs the RTTI-backed HotKeyPane, loads _nhotkem.txt and _nhotkey.txt, and registers it with the screen and event trees. |
| `ui_create_hot_key_pane` | `0x00488D00` | high | Allocates a 0x919C-byte HotKeyPane and calls ui_hot_key_pane_ctor; its only direct caller is GUIBackPane action 0. |
| `ui_image_pane_draw_content` | `0x0048DD30` | high | Draws an ImagePane image into the pane's own canvas. |
| `ui_inventory_pane_ctor` | `0x0048F7E0` | high | Constructs exact RTTI class InventoryPane_A, clears its 60 direct InvItemPane pointers, and initializes its selection state. |
| `ui_inventory_pane_handle_network_event` | `0x004900C0` | high | InventoryPane_A and derived ItemInventoryPane route SAddInventory, SRemoveInventory, and SStatus to their local update paths. |
| `ui_inventory_create_item` | `0x00490540` | high | Allocates a 0x248-byte RTTI InvItemPane, inserts it into one of 60 inventory slots, and passes all SAddInventory item fields to its constructor. |
| `ui_inventory_remove_slot` | `0x004907A0` | high | Releases the live InvItemPane for a one-based inventory slot and clears its direct pointer entry. |
| `ui_inventory_activate_slot` | `0x00490960` | high | Converts a one-based slot to InventoryPane_A's direct InvItemPane pointer entry and activates the item when that entry is live. |
| `ui_inventory_add_item_from_packet` | `0x004909E0` | high | Accepts SAddInventory slots 1 through 60, replaces an occupied UI slot, and creates a new InvItemPane from the decoded fields. |
| `ui_inventory_remove_item_from_packet` | `0x00490D30` | high | Accepts SRemoveInventory slots 1 through 60 and removes the matching live InvItemPane when present. |
| `ui_inventory_update_gold_from_status_packet` | `0x00490F10` | high | Copies SStatus gold into the inventory pane and redraws its currency display. |
| `ui_new_skill_inventory_pane_ctor` | `0x00491050` | high | Constructs exact RTTI class NewSkillInventoryPane with a 90-entry NewInventoryPane&lt;SkillInvItemPane&gt; base. |
| `ui_skill_inventory_action_delay_timer` | `0x004914B0` | high | NewSkillInventoryPane TimerHandler callback for ID 0; resolves the one-based slot payload and clears action_delay_active on the item currently occupying that slot. |
| `ui_skill_inventory_create_skill_item` | `0x004915B0` | high | Allocates a 0x348-byte SkillInvItemPane from the SAddSkill slot, icon, and name, then inserts it at slot - 1. |
| `ui_skill_inventory_remove_slot` | `0x00491670` | high | Converts a one-based skill slot to the skill inventory's zero-based removal index. |
| `ui_skill_inventory_handle_network_event` | `0x00491690` | high | NewSkillInventoryPane network-event handler routes SAddSkill, SRemoveSkill, and SActionDelay selector 1 to their UI paths. |
| `ui_skill_inventory_add_skill_from_packet` | `0x00491730` | high | Accepts SAddSkill slots 1 through 90, replaces an existing UI item, and constructs a new SkillInvItemPane. |
| `ui_skill_inventory_remove_skill_from_packet` | `0x004917D0` | high | Accepts SRemoveSkill slots 1 through 90 and removes the slot when its SkillInvItemPane pointer is non-null. |
| `ui_skill_inventory_apply_action_delay` | `0x00491850` | high | Accepts SActionDelay selector 1 and slots 1 through 90, sets the live item delay flag, starts the skill progress visual, and schedules the inventory expiry timer. |
| `ui_new_spell_inventory_pane_ctor` | `0x004919E0` | high | Constructs exact RTTI class NewSpellInventoryPane and initializes its 90-entry spell-item pointer array. |
| `ui_spell_inventory_action_delay_timer` | `0x00491F70` | high | NewSpellInventoryPane TimerHandler callback for ID 0; resolves the one-based slot payload and clears action_delay_active on the current spell item. |
| `ui_spell_inventory_create_spell_item` | `0x00492070` | high | Allocates SpellInvItemPane and passes the SAddSpell slot, icon, argument type, name, prompt, and cast-line count to its constructor. |
| `ui_spell_inventory_remove_slot` | `0x00492140` | high | Converts a one-based spell slot to the inventory container's zero-based index and removes the corresponding UI item. |
| `ui_spell_inventory_handle_network_event` | `0x00492160` | high | NewSpellInventoryPane network-event handler routes SAddSpell, SRemoveSpell, and SActionDelay selector 0 to the matching UI paths. |
| `ui_spell_inventory_add_spell_from_packet` | `0x00492200` | high | Accepts SAddSpell slots 1 through 90, replaces the existing UI entry, and constructs a new SpellInvItemPane. |
| `ui_spell_inventory_remove_spell_from_packet` | `0x004922B0` | high | Accepts SRemoveSpell slots 1 through 90 and removes the slot when its SpellInvItemPane pointer is non-null. |
| `ui_spell_inventory_apply_action_delay` | `0x00492330` | high | Accepts SActionDelay selector 0 and slots 1 through 90, sets the live spell item delay flag, and schedules the inventory expiry timer. |
| `ui_skill_inventory_set_item_at` | `0x00492B30` | high | Replaces a checked zero-based skill inventory entry and attaches the new SkillInvItemPane to its visible slot. |
| `ui_skill_inventory_remove_item_at` | `0x00492C00` | high | Checks a zero-based skill inventory index, releases its live UI item, and clears the pointer entry. |
| `ui_spell_inventory_remove_item_at` | `0x00493460` | high | Checks a zero-based spell inventory index, releases its live SpellInvItemPane through the shared UI owner, and clears the pointer entry. |
| `ui_item_pane_ctor` | `0x00495C60` | high | Constructs exact RTTI class ItemPane and stores an item sprite, 128-byte display name, and dye color. |
| `ui_inventory_item_set_display_name` | `0x00495DE0` | high | Replaces the InvItemPane display name through the same bounded 128-byte copy used by its ItemPane base. |
| `ui_inventory_item_ctor` | `0x00495E10` | high | Constructs exact RTTI class InvItemPane and retains slot, sprite, dye, display name, quantity, stack flag, maximum durability, and current durability. |
| `ui_inventory_item_handle_pointer_event` | `0x004963C0` | high | InvItemPane pointer-event handler starts a DraggedInvItemPane from the selected inventory item and its one-based source slot. |
| `ui_inventory_item_submit_drop_quantity` | `0x00496820` | high | Numeric-input callback sends the saved CDrop target and source item only when the submitted u32 quantity is nonzero. |
| `ui_inventory_item_submit_give_quantity` | `0x00496860` | high | Forwards a nonzero u32 quantity and saved living target object ID to CGive, but has no confirmed static reference in the live drag path. |
| `ui_inventory_item_send_drop` | `0x00496890` | high | InvItemPane virtual sender forwards target Y, target X, and quantity to the concrete CDrop builder. |
| `ui_inventory_item_send_give` | `0x004968C0` | high | InvItemPane virtual sender forwards a living target object ID and u32 quantity to the concrete CGive builder. |
| `ui_inventory_item_handle_timer` | `0x004968E0` | high | TimerHandler event 0 handles a world-tile drop; event 1 gives to a living object, sending quantity one for normal items or opening GiveGoldDialogPane for slot 60. |
| `ui_inventory_item_activate` | `0x00496E70` | high | InvItemPane activation wrapper reaches the shared CUse sender used by pointer and number-key activation. |
| `ui_inventory_item_is_denied` | `0x00496F30` | high | Copies the InvItemPane name and checks the RTTI-backed DeniedItemList item table; a match suppresses CUse locally. |
| `ui_drop_gold_dialog_ctor` | `0x004971B0` | high | Constructs exact RTTI class DropGoldDialogPane, retains the drag-selected Y and X, builds the _nmoney.txt controls, and focuses the amount input. |
| `ui_drop_gold_dialog_handle_action` | `0x00497560` | high | DropGoldDialogPane action 0 parses and submits CDropGold; action 1 closes the dialog without sending. |
| `ui_give_gold_dialog_ctor` | `0x00497710` | high | Constructs exact RTTI class GiveGoldDialogPane, retains the drag-selected living target object ID, builds the _nmoney.txt controls, and focuses the amount input. |
| `ui_give_gold_dialog_handle_action` | `0x00497AB0` | high | GiveGoldDialogPane action 0 parses and submits CGiveGold; action 1 closes the dialog without sending. |
| `ui_dragged_inventory_item_pane_ctor` | `0x00497C30` | high | Constructs exact RTTI class DraggedInvItemPane and retains the dragged item kind, inventory slot, and owner pane. |
| `ui_dragged_inventory_item_dispatch_drop` | `0x00497EC0` | high | Dispatches the dragged inventory-item record and pointer position through the pane tree to the selected drop target. |
| `ui_map_item_pane_handle_pointer_event` | `0x00498020` | high | Handles MapItem_Pane pointer events; a left double click inside the pane finds an empty inventory slot and sends CGet for the pane's world coordinates. |
| `ui_map_item_pane_handle_timer` | `0x00498400` | high | TimerHandler callback for MapItem_Pane; resolves an inventory slot when needed and sends CGet through the pane-owned builder. |
| `ui_skill_inventory_item_ctor` | `0x00498940` | high | Constructs exact RTTI class SkillInvItemPane and retains the SAddSkill icon, name, and one-based slot. |
| `ui_skill_item_start_cooldown_visual` | `0x00498AD0` | high | Sets progress to zero, records timeGetTime start and end values, marks the visual active, redraws, and schedules timer ID 0x10204 after 100 ms. |
| `ui_skill_item_set_cooldown_progress` | `0x00498B40` | high | Stores a changed 0 through 30 skill cooldown step and invalidates the item pane. |
| `ui_skill_item_cooldown_visual_timer` | `0x00498C10` | high | For timer ID 0x10204, maps elapsed time to 30 integer steps, redraws, and reschedules at 100 ms while the delay and visual-active flags remain set. |
| `ui_skill_inventory_item_handle_pointer_event` | `0x00498D40` | high | Skill item pointer handler checks complete-object offset +0x322 and blocks drag start, activation, and information actions while action-delayed. |
| `ui_skill_inventory_item_draw` | `0x004991D0` | high | Draws the skill icon, applies palette index 0x58 across a delayed icon, and palette index 0x18 below a vertical boundary derived from the 0 through 30 progress step. |
| `ui_skill_inventory_activate` | `0x004992F0` | high | Blocks activation while SActionDelay flag +0x322 or unresolved state +0x323 is set, then sends any configured skill text and reaches the CUseSkill sender. |
| `ui_skill_is_denied` | `0x004994C0` | high | Looks up the skill name in DeniedItemList mode 1 before CUseSkill construction; a match suppresses the packet. |
| `ui_skill_item_clear_action_delay` | `0x00499570` | high | Clears SkillInvItemPane +0x322 and invalidates the item rectangle. |
| `ui_skill_item_set_action_delay` | `0x004995A0` | high | Sets SkillInvItemPane +0x322 to one and invalidates the item rectangle. |
| `ui_spell_inventory_item_ctor` | `0x00499DE0` | high | Constructs exact RTTI class SpellInvItemPane and retains slot, icon, argument type, 128-byte name and prompt buffers, and cast_lines. |
| `ui_spell_inventory_item_handle_pointer_event` | `0x00499FB0` | high | Spell item pointer handler checks complete-object offset +0x297 and blocks drag start, activation, and information actions while action-delayed. |
| `ui_spell_inventory_item_draw` | `0x0049A420` | high | Draws the spell icon and applies palette index 0x58 across the complete icon while action_delay_active is set. |
| `ui_spell_begin_target_selection` | `0x0049A4E0` | high | Handles spell argument type 2 by creating a DraggedSpellInvItemPane for target selection. |
| `ui_spell_inventory_activate` | `0x0049A670` | high | Blocks activation while SActionDelay flag +0x297 is one, then dispatches SpellInvItemPane argument types 1 through 7; type 8 is not handled in this switch. |
| `ui_spell_open_string_input` | `0x0049A720` | high | Handles spell argument type 1 by opening RTTI class StringSpellInputPane with the SAddSpell prompt. |
| `ui_spell_open_number_inputs` | `0x0049A950` | high | Opens NumberArgsSpellInputPane for one through four numeric values selected by spell argument types 7, 6, 4, and 3. |
| `ui_spell_is_denied` | `0x0049AC90` | high | Looks up the spell name in DeniedItemList mode 2 before any cast delay starts; a match suppresses the cast. |
| `ui_spell_item_clear_action_delay` | `0x0049AE10` | high | Clears SpellInvItemPane +0x297 and invalidates the item rectangle. |
| `ui_spell_item_set_action_delay` | `0x0049AE40` | high | Sets SpellInvItemPane +0x297 to one and invalidates the item rectangle. |
| `ui_spell_text_input_submit` | `0x0049B190` | high | Builds the CUseSpell text form as opcode, slot, and unprefixed raw text bytes after a nonempty input is submitted. |
| `ui_spell_numeric_input_submit` | `0x0049B380` | high | Builds the numeric CUseSpell form as opcode, slot, and one through four big-endian u16 values selected by spell argument type. |
| `ui_spell_delay_control_pane_ctor` | `0x0049B6F0` | high | Constructs the exact RTTI class SpellDelayControlPane, allocates its 0x8C98-byte object, and initializes cast_active at +0x8C94 to zero. |
| `ui_spell_delay_control_pane_handle_network_event` | `0x0049B810` | high | Handles typed server opcode 0x48 for SpellDelayControlPane and dispatches it to ui_cancel_spell_delay. |
| `ui_spell_delay_timer_callback` | `0x0049B870` | high | Advances current_cast_line at complete-object offset +0x191 on one-second ticks, then sends the spell name, submits the queued CUseSpell, and clears cast_active on the final tick. |
| `ui_start_spell_cast` | `0x0049B900` | high | Copies CUseSpell to +0xB92, its length to +0x8C92, the spell name to +0x8B92, and cast counters to +0x190/+0x191 before beginning the delay sequence. |
| `ui_cancel_spell_delay` | `0x0049BA50` | high | Clears SpellDelayControlPane::cast_active at +0x8C94 and cancels every timer owned by the pane with the 0x7FFFFFFF wildcard. |
| `ui_load_spell_cast_lines` | `0x0049BD80` | high | Loads up to ten 256-byte per-spell cast strings from the current character's SpellBook.cfg data. |
| `ui_layout_parse_control` | `0x004A81F0` | high | Parses CONTROL, NAME, TYPE, RECT, IMAGE, VALUE, COLOR, and ENDCONTROL tokens. |
| `ui_layout_serialize_control` | `0x004A8820` | high | Writes one parsed control back to the same line-oriented layout grammar. |
| `ui_open_town_map_for_current_map` | `0x004AD250` | high | Opens exact RTTI TownMapPane in the built-in button mode, which selects _tcoord.txt from the active client map number. |
| `ui_open_town_map_for_key` | `0x004AD2E0` | high | Opens exact RTTI TownMapPane in server-keyed mode unless its singleton is already active. |
| `ui_has_town_map_pane` | `0x004AE090` | high | Reports whether the exact RTTI TownMapPane singleton is active. |
| `ui_get_town_map_pane` | `0x004AE0B0` | high | Returns the current exact RTTI TownMapPane singleton pointer. |
| `ui_main_menu_activate_selected_action` | `0x004B7520` | high | Dispatches the selected MainMenuPane entry to login, character creation, password change, homepage, credits, or exit behavior. |
| `ui_main_menu_handle_pointer_event` | `0x004B7BD0` | high | Rejects pointer input while MainMenuPane +0x500 is nonzero, then performs menu hit-testing and activation when the gate is clear. |
| `ui_main_menu_handle_keyboard_event` | `0x004B7D00` | high | Rejects keyboard input while MainMenuPane +0x500 is nonzero, then handles menu selection and activation when the gate is clear. |
| `ui_login_dialog_ctor` | `0x004BA180` | high | Constructs RTTI class LoginDialogPane from _nlogin.txt and attaches OK, Cancel, Name, and Password controls. |
| `ui_login_dialog_handle_key_event` | `0x004BA810` | high | Moves focus from Name to Password when Enter is pressed and otherwise delegates supported keyboard events to DialogPane. |
| `ui_login_dialog_handle_action` | `0x004BA8C0` | high | Action 0 reads LoginDialogPane controls 2 and 3 and sends CLogin; action 1 closes the dialog. |
| `ui_change_password_dialog_ctor` | `0x004BB2A0` | high | Constructs RTTI class ChangePasswordDialogPane from _npw.txt and attaches OK, Cancel, Name, existing-password, new-password, and confirmation controls. |
| `ui_change_password_handle_action` | `0x004BB840` | high | Handles ChangePasswordDialogPane action 0 as submit and action 1 as cancel. |
| `ui_change_password_submit` | `0x004BBA50` | high | Checks new-password confirmation locally, then sends directly in distribution modes 1 and 15 or opens the regional birthdate step. |
| `ui_input_birthdate_dialog_ctor` | `0x004BC220` | high | Constructs RTTI class InputBirthdateDialogPane from _npw2.txt for the regional password-change verification branch. |
| `ui_manufacture_dialog_ctor` | `0x004C20D0` | high | Constructs exact RTTI ManufactureDialogPane from lmanu.txt, attaches ten controls, applies the opening typed SManual, and registers the modal pane. |
| `ui_manufacture_dialog_dtor` | `0x004C25E0` | high | Clears the singleton, unregisters the pane from event routing, and runs the DialogPane destructor. |
| `ui_manufacture_dialog_apply_manual_packet` | `0x004C2BC0` | high | Applies typed SManual fields, validates the source inventory slot, requests recipe zero after a nonzero count, and stores recipe display state. |
| `ui_manufacture_dialog_handle_add_inventory` | `0x004C2E50` | high | Clears the optional selected slot when SAddInventory replaces that inventory entry. |
| `ui_manufacture_dialog_handle_remove_inventory` | `0x004C2EE0` | high | Clears a removed additional slot and closes the pane when SRemoveInventory removes the source manual slot. |
| `ui_manufacture_dialog_handle_keyboard_event` | `0x004C30A0` | high | Maps internal key values 0x80, 0x82, 0x93, and 0x94 to recipe request deltas -1, +1, -10, and +10 with bounds checks. |
| `ui_manufacture_dialog_handle_action` | `0x004C3230` | high | Maps attachment-order actions 0 through 3 to craft, close, next recipe, and previous recipe. |
| `ui_manufacture_dialog_handle_network_event` | `0x004C32F0` | high | Routes typed SManual 0x50, SAddInventory 0x0F, and SRemoveInventory 0x10 to the manufacture pane handlers. |
| `ui_manufacture_dialog_handle_pointer_event` | `0x004C3390` | high | Clears the optional additional inventory slot when the user clicks inside its canvas. |
| `ui_manufacture_dialog_reset_session` | `0x004C3490` | high | Resets manufacture ID, recipe count, and current recipe before applying a RecipeCount message. |
| `ui_manufacture_dialog_clear_recipe` | `0x004C34D0` | high | Clears index, sprite, all three recipe strings, additional-item mode, and the selected additional slot. |
| `ui_manufacture_dialog_refresh` | `0x004C3750` | high | Updates navigation controls, count text, recipe icon and strings, and the additional inventory-item preview. |
| `ui_manufacture_dialog_handle_additional_item_drop` | `0x004C3CA0` | high | When additional-item mode equals 1, copies a dropped inventory item's image and records its one-based slot. |
| `ui_manufacture_dialog_set_additional_slot` | `0x004C3E00` | high | Stores the one-byte inventory slot sent by CManual CraftRecipe; zero clears the selection. |
| `ui_server_item_menu_dialog_handle_network_event` | `0x004CAC20` | high | TaskListDialog::ServerItemMenuDialog3 network-event handler accepts SStatus updates containing progression and currency. |
| `ui_server_item_menu_update_gold_from_status_packet` | `0x004CAC90` | high | Copies SStatus gold into the server-item menu dialog and redraws its currency display. |
| `ui_merchant_face_menu_handle_action` | `0x004D74E0` | high | Exact RTTI MerchantDialogPane::FaceMenuDialog handler adjusts three word selectors and one five-step visual value; action 0x0F submits its special CMerchant form. |
| `ui_open_find_farmpet` | `0x004EAE40` | high | Mini-game selector 3 constructs, centers, and registers the exact RTTI FindFarmpet::FindFarmpetPane singleton. |
| `ui_find_farmpet_pane_handle_network_event` | `0x004EB000` | high | FindFarmpet::FindFarmpetPane accepts server opcode 0x64 and forwards it to its action-7 update method. |
| `ui_find_farmpet_apply_mini_game_update` | `0x004EC3E0` | high | Consumes only SMiniGame action 7, matching its first u32 against two tracked IDs and storing the second u32 as the corresponding value. |
| `ui_puzzle_game_ctor` | `0x004F2730` | high | Constructs exact RTTI Puzzle::Game in either selector-2 mode 1 or selector-4 mode 0 and builds its lpz_dlg.txt dialog. |
| `ui_puzzle_play_pane_handle_network_event` | `0x004F6A20` | high | Puzzle::PlayPane accepts server opcode 0x64 and forwards it to its action-7 update method. |
| `ui_puzzle_play_apply_mini_game_update` | `0x004F6A80` | high | Consumes only SMiniGame action 7 and forwards its two u32 values to the active Puzzle game state. |
| `ui_rope_skipping_game_ctor` | `0x00500B20` | high | Mini-game selector 1 constructs exact RTTI RopeSkipping::Game and its lminig.txt-backed GameDialogPane. |
| `ui_launch_mini_game` | `0x0050C400` | high | Maps SMiniGame action-4 selectors 1 through 4 to RopeSkipping, Puzzle mode 1, FindFarmpet, and Puzzle mode 0 respectively. |
| `ui_browser_game_control_handle_network_event` | `0x0050DC50` | high | MiniGame::BrowserGameControlPane dispatches exact RTTI SWebBoard opcode 0x62 through its web-board virtual method. |
| `ui_browser_game_control_apply_web_board` | `0x0050DCB0` | high | Accepts SWebBoard action 3, applies its derived base URL, and navigates to start_url plus a question mark and board_data. |
| `ui_group_ad_dialog_apply_model` | `0x00511F90` | high | Applies leader, group name, note, level range, totals, and five ordered maximum/current class pairs to GroupAdDialogPane controls. |
| `ui_group_ad_dialog_read_model` | `0x005120A0` | high | Reads the editable recruiting form and five ordered class maximums into the model used by CGroup RecruitStart. |
| `ui_group_ad_pane_apply_self_look` | `0x00513E80` | high | Builds GroupAdPane's recruiting model from SSelfLook; it copies name and note but omits the already-parsed leader string. |
| `ui_group_ad_info_dialog_handle_action` | `0x005140C0` | high | Routes GroupAdInfoDialogPane's join control to CGroup action 7 and then closes the dialog. |
| `ui_group_ad_show_recruit_info` | `0x00514230` | high | Converts SGroup action 4 into the recruiting UI model, preserving five maximum/current class pairs and summing both columns. |
| `ui_album_info_pane_ctor` | `0x0051BC70` | high | Constructs exact RTTI AlbumInfoPane and owns one AlbumViewPane. |
| `ui_album_view_pane_ctor` | `0x0051BFA0` | high | Constructs exact RTTI AlbumViewPane from llalbum.txt with Portrait, Del, and Save regions and an AlbumFile owner. |
| `ui_album_view_reload` | `0x0051C630` | high | Reloads the active character's album.dat through the AlbumViewPane AlbumFile object and invalidates the pane. |
| `ui_album_view_handle_action` | `0x0051D100` | high | Handles legacy album remove, save, and move confirmation events 0x1000 through 0x1003. |
| `ui_album_view_remove_portrait` | `0x0051EA20` | high | Clears the selected legacy album record, rewrites album.dat, and reloads the pane. |
| `ui_album_view_export_portrait_jpeg` | `0x0051EA70` | high | Legacy Save composites one album portrait and always writes the extensionless character portrait through the shared JFIF writer. |
| `ui_album_view_move_portrait` | `0x0051EEC0` | high | Moves a legacy album record, rewrites album.dat, and reloads the pane. |
| `ui_new_patch_pane_ctor` | `0x005283E0` | high | Constructs RTTI class NewPatchPane from SVersionCheck subtype 2, parsing required version and u8-length file names before starting the patch handoff. |
| `ui_npc_session_set_response_pending` | `0x0052C020` | high | Invokes the active NPC message pane's response-pending virtual after a merchant or pursuit response is queued; the pursuit implementation deactivates its nested answer pane, disables Previous and Next, and leaves Close available. |
| `ui_npc_session_update_speaker_art` | `0x0052C480` | high | Loads the NPC illustration for the active packet fields or switches to NPCTilePane when lookup or decoding fails. |
| `ui_npc_session_handle_network_event` | `0x0052C730` | high | Routes SScreenMenu 0x2F and SPursuitMessage 0x30 packet objects into their NPCSession update paths. |
| `ui_npc_session_open_screen_menu` | `0x0052C7B0` | high | Copies SScreenMenu state into NPCSession state 1, refreshes speaker art, and constructs exact RTTI NPC_Merchant_MessageDialog. |
| `ui_npc_session_open_pursuit_message` | `0x0052C950` | high | Closes on SPursuitMessage type 10 or copies the message into NPCSession state 2 and constructs exact RTTI NPC_Pursuit_MessageDialog. |
| `ui_npc_illustration_pane_ctor` | `0x0052CB20` | high | Constructs the RTTI-backed NPCIllustPane and initializes its pixmap view. |
| `ui_npc_illustration_pane_set_image` | `0x0052CBE0` | high | Resolves the NPC name and illustration index, sizes the pane to the loaded frame, and invalidates it for redraw. |
| `ui_npc_illustration_pane_draw` | `0x0052CC90` | high | Draws the selected illustration pixmap through the transparent software blitter. |
| `ui_npc_message_dialog_ctor` | `0x0052D460` | high | Constructs the shared lnpcd.txt-backed outer speaker name, content, and scrolling pane used by screen-menu and pursuit dialogs. |
| `ui_npc_message_dialog_close` | `0x0052D950` | high | Closes the owning NPCSession when present, or destroys a standalone NPC message pane, without sending a merchant or pursuit response. |
| `ui_npc_menu_dialog_ctor` | `0x0052DCB0` | high | Constructs the shared NPCMenuDialog base used by choice, input, item, skill, and spell subpanes. |
| `ui_npc_menu_dialog_handle_keyboard_event` | `0x0052DDF0` | high | Returns false for Escape so the outer NPC message dialog can handle its cancel action; all other keyboard events use the inherited DialogPane handler. |
| `ui_npc_illustration_load_pixmap` | `0x00531B30` | high | Resolves an NPC name and illustration index, then loads frame zero of the mapped image from npcbase.dat. |
| `ui_npc_illustration_asset_at` | `0x00531C40` | high | Returns one illustration filename from an NPC name record by zero-based index. |
| `ui_npc_illustration_file_manager_ctor` | `0x00531E10` | high | Opens npc/npcbase.dat, initializes the name map, and loads its npci.tbl fallback mapping. |
| `ui_npc_illustration_resolve_asset` | `0x00532120` | high | Looks up the exact NPC name, selects its indexed filename, and returns the npcbase.dat archive owner. |
| `ui_npc_illustration_handle_event` | `0x00532560` | high | Handles initialization and NPCIllust metadata availability events for NPCIllustFileMan. |
| `ui_npc_illustration_subscribe_metadata` | `0x005325D0` | high | Subscribes NPCIllustFileMan to the server-managed NPCIllust metadata table, retrying after one second when required. |
| `ui_npc_illustration_apply_metadata` | `0x00532620` | high | Applies exact NPC-name keys; repeated clearing means the final filename replaces earlier values in a multi-value metadata group. |
| `ui_npc_merchant_message_dialog_ctor` | `0x00534990` | high | Constructs exact RTTI NPC_Merchant_MessageDialog, attaches its outer buttons, and dispatches the SScreenMenu subtype. |
| `ui_npc_merchant_request_object_info` | `0x00534A90` | high | Top sends CRequestObjectInfo opcode 0x43 subtype 1 with the SScreenMenu target ID, then closes the active NPC session. |
| `ui_npc_merchant_message_handle_action` | `0x00534B70` | high | Routes base actions 0 through 3 to content handling, action 4 to Top object-info request, and action 5 to local close. |
| `ui_npc_dispatch_screen_menu_type` | `0x00534C40` | high | Maps SScreenMenu values 0 through 11 to text, input, server item, local item, server skill-spell, and local skill-spell models. |
| `ui_npc_server_item_menu_handle_network_event` | `0x0053A270` | high | NPCMenuDialog::NPCServerItemMenuDialog routes SStatus progression blocks to its gold-display updater. |
| `ui_npc_server_item_menu_update_gold_from_status_packet` | `0x0053A2D0` | high | Copies SStatus gold into the NPC server-item menu and redraws the dialog. |
| `ui_npc_pursuit_message_dialog_ctor` | `0x0053CC10` | high | Constructs exact RTTI NPC_Pursuit_MessageDialog, attaches Previous, Next, and Close after the four base message controls, and registers Close action 6 as the Escape cancel action. |
| `ui_npc_pursuit_dialog_set_response_pending` | `0x0053CD10` | high | Deactivates the nested answer pane, disables Previous and Next, and clears the default action after a CPursuit response; Close action 6 remains available. |
| `ui_npc_pursuit_message_handle_action` | `0x0053CD90` | high | Routes attachment-order actions 4, 5, and 6 to Previous, Next, and Close response builders. |
| `ui_npc_pursuit_build_subtype` | `0x0053CE70` | high | Applies speaker content and navigation flags, then constructs pursuit models for types 2, 3, 4, 5, 6, and 9. |
| `ui_npc_pursuit_protected_dialog_ctor` | `0x0053EBA0` | high | Constructs the lnpcnid.txt protected pursuit dialog with separate ID and masked-password edit controls plus submit and cancel. |
| `ui_npc_pursuit_protected_handle_action` | `0x0053ECD0` | high | Hands submission to the regional account manager and sends only after its accepted state; pending and error states stay in local UI paths. |
| `ui_option_pane_create_alert` | `0x00540580` | high | OptionPane alert factory selects five alert classes; type 4 allocates and constructs exact RTTI SafeQuitAlert. |
| `ui_game_setting_apply_local` | `0x00541D20` | high | Builds or toggles client-owned setting IDs 7 and 9 through 13 using fields in the global AppConfig object. |
| `ui_game_setting_dialog_ctor` | `0x00542370` | high | Constructs exact RTTI GameSettingDialog from _nsett.txt, attaches 13 setting controls, and requests server settings with CUserSetting ID 0. |
| `ui_game_setting_dialog_handle_network_event` | `0x00542BA0` | high | GameSettingDialog decoded-packet event handler routes SMessage opcode 0x0A to its dialog-specific handler. |
| `ui_game_setting_dialog_handle_message` | `0x00542C30` | high | Accepts SMessage type 0x07 and passes its counted text to the Game Settings response parser. |
| `ui_game_setting_dialog_activate` | `0x00542C60` | high | Sends CUserSetting for server-owned rows and changes AppConfig locally for client-owned rows. |
| `ui_game_setting_dialog_handle_keyboard_event` | `0x00542D50` | high | Maps number keys 1 through 9 and 0 to setting IDs 1 through 10. |
| `ui_game_setting_dialog_handle_action` | `0x00542DC0` | high | Dispatches the 13 row actions and calls app_save_config on normal dialog close. |
| `ui_game_setting_dialog_apply_message_text` | `0x005430D0` | high | Parses SMessage type 0x07 text as an ASCII-discriminated full setting list or single-row replacement. |
| `ui_safe_quit_alert_ctor` | `0x00544100` | high | Constructs exact RTTI SafeQuitAlert and immediately submits CQuit as bytes 0B 01. |
| `ui_safe_quit_alert_handle_network_event` | `0x00544220` | high | SafeQuitAlert primary-vtable network-event handler routes typed SQuit opcode 0x4C to its response helper. |
| `ui_safe_quit_alert_apply_quit_response` | `0x00544280` | high | When SQuit's consumed byte is 1, marks the alert approved, submits CQuit bytes 0B 00, replaces the alert text, and refreshes its control. |
| `ui_option_pane_handle_keyboard_event` | `0x005444B0` | high | OptionPane keyboard-event handler maps both X and x to construction of exact RTTI SafeQuitAlert. |
| `ui_open_user_confirm_from_message` | `0x005449D0` | high | Opens exact RTTI UserConfirmPane for SMessage type 0x11 with its main prompt, two bytes, and string8 reply context. |
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
| `ui_editable_paper_pane_ctor` | `0x0054A470` | high | Constructs exact RTTI EditablePaperPane and selects editable SEnterEditingMode parsing or read-only opcode 0x35 parsing from an explicit local mode. |
| `ui_editable_paper_initialize_editable` | `0x0054A530` | high | Parses raw SEnterEditingMode fields as slot, paper background, width blocks, height blocks, and string16 content before building the pane controls. |
| `ui_editable_paper_initialize_read_only` | `0x0054A680` | high | Parses raw server opcode 0x35 into the same EditablePaperPane with its local mode set read-only. |
| `ui_editable_paper_handle_action` | `0x0054A9B0` | high | EditablePaperPane dialog action 0 sends CExitEditingMode only in editable mode, then dismisses either editable or read-only panes. |
| `ui_dismiss_editable_paper` | `0x0054A9F0` | high | Unregisters EditablePaperPane from the screen and event systems and removes it from its owner without independently submitting text. |
| `ui_editable_paper_build_controls` | `0x0054AA30` | high | Converts wire tabs to editor carriage returns, computes 16-pixel block geometry, builds the editable or read-only text control, and centers the pane within the native 640 by 480 view. |
| `ui_popup_menu_open_for_user` | `0x0054BDB0` | high | Creates the exact RTTI PopupMenuPane singleton for a target object ID, positions it at the click, and registers it in the screen and event trees. |
| `ui_popup_menu_close` | `0x0054BF90` | high | Unregisters an open PopupMenuPane from screen and event routing, clears its open flag and target ID, and removes its embedded screen pane. |
| `ui_popup_menu_pane_ctor` | `0x0054C010` | high | Constructs the 0x36C-byte exact RTTI PopupMenuPane, loads lpopup.txt, and reads Box0 plus exactly three action rectangles. |
| `ui_popup_menu_update_group_label` | `0x0054C310` | high | Resolves the target name, checks the current group roster, and selects msg.tbl label 0x52, 0x53, or 0x54 for the middle action. |
| `ui_popup_menu_handle_pointer_event` | `0x0054C530` | high | PopupMenuPane primary-vtable +0x48 handler updates row hover, dispatches left presses, and closes on left or right press. |
| `ui_popup_menu_handle_keyboard_event` | `0x0054C6D0` | high | PopupMenuPane primary-vtable +0x4C handler closes the popup and returns false so keyboard or text input can continue. |
| `ui_popup_menu_draw` | `0x0054C6F0` | high | Draws the target name, three action rectangles, hover highlight, and localized labels for PopupMenuPane. |
| `ui_popup_menu_dispatch_action` | `0x0054C990` | high | Maps row 0 to CRequestObjectInfo subtype 1, row 1 to CGroup action 2, and row 2 to tell-target preparation. |
| `ui_popup_menu_hit_test_action` | `0x0054CBD0` | high | Tests the pointer against exactly three action rectangles and returns index 0 through 2 or -1. |
| `ui_open_say_input` | `0x0054F840` | high | Creates ChatInputPane in Say mode 0 or Shout mode 1 and formats the local name prefix as colon-space or exclamation-space. |
| `ui_open_tell_receiver_input` | `0x0054F9D0` | high | Creates exact RTTI class TellReceiverInputPane when the world keyboard handler receives the double-quote key. |
| `ui_open_tell_input` | `0x0054FAB0` | high | Formats the local arrow, target name, and colon prefix, then creates exact RTTI class TellInputPane. |
| `ui_open_block_listen_input` | `0x0054FBE0` | high | Creates and registers the singleton RTTI BlockListenInputPane when it is not already open. |
| `ui_chat_input_pane_ctor` | `0x0054FCA0` | high | Constructs ChatInputPane, retains the selected speech mode, and prepares its bounded editable text buffer. |
| `ui_tell_receiver_input_pane_ctor` | `0x0054FFE0` | high | Constructs TellReceiverInputPane, configures a 13-byte input maximum, and retains its submission callback. |
| `ui_tell_remember_target` | `0x005500B0` | high | Maintains ten recent tell recipients in 13-byte records. |
| `ui_tell_receiver_set_submit_callback` | `0x00550230` | high | Retains the callback and context used to open the message-input stage after recipient submission. |
| `ui_tell_receiver_input_submit` | `0x00550420` | high | Copies at most 12 recipient bytes, remembers the name, and invokes the retained callback. |
| `ui_tell_input_pane_ctor` | `0x005504A0` | high | Constructs TellInputPane, retains the target, and limits message bytes to 70 minus the visible prefix length. |
| `ui_block_listen_input_pane_ctor` | `0x00550720` | high | Constructs RTTI class BlockListenInputPane as a one-character command prompt. |
| `ui_block_listen_input_pane_dtor` | `0x005507F0` | high | Destroys BlockListenInputPane and clears its singleton subobject. |
| `ui_block_listen_input_handle_event` | `0x00550860` | high | Handles question mark in BlockListenInputPane by sending the list operation, then delegates other events to the base pane. |
| `ui_block_listen_select_operation` | `0x005508C0` | high | Maps A or a to AddToBlockListenInputPane and D or d to DeleteFromBlockListenInputPane. |
| `ui_add_to_block_listen_input_pane_ctor` | `0x00550B20` | high | Constructs exact RTTI class AddToBlockListenInputPane for an ignored-character name. |
| `ui_add_to_block_listen_submit` | `0x00550C00` | high | Copies up to 15 nonempty name bytes from AddToBlockListenInputPane and calls the add builder. |
| `ui_delete_from_block_listen_input_pane_ctor` | `0x00550DA0` | high | Constructs exact RTTI class DeleteFromBlockListenInputPane for an ignored-character name. |
| `ui_delete_from_block_listen_submit` | `0x00550E80` | high | Copies up to 15 nonempty name bytes from DeleteFromBlockListenInputPane and calls the remove builder. |
| `ui_block_listen_register_singleton` | `0x00551160` | high | Publishes the enclosing BlockListenInputPane through its global singleton pointer. |
| `ui_block_listen_unregister_singleton` | `0x005511A0` | high | Clears the global BlockListenInputPane pointer during destruction. |
| `ui_has_block_listen_input` | `0x005511E0` | high | Reports whether the transient BlockListenInputPane singleton is open. |
| `ui_score_pane_append_server_message` | `0x00552120` | high | Prepends a newline and appends an SMessage body to ScorePane when its length is at most 70 bytes. |
| `ui_score_pane_handle_message_packet` | `0x005521B0` | high | Accepts SMessage type 0x12 and forwards its byte string to ScorePane. |
| `ui_screen_hierarchy_ctor` | `0x005522B0` | high | Constructs the RTTI-backed HierList&lt;Screen&gt; used for spatial pane parentage. |
| `ui_screen_hierarchy_insert` | `0x00552370` | high | Adds a pane with spatial sibling and parent placement and sets Pane +0x188 bit 0x01. |
| `ui_screen_hierarchy_queue_remove` | `0x005525D0` | high | Clears Pane +0x188 bit 0x01 and queues or performs HierList&lt;Screen&gt; removal. |
| `ui_screen_hierarchy_get_absolute_origin` | `0x005528C0` | high | Accumulates pane origins through spatial parents until ui_screen_root_pane_ptr. |
| `ui_screen_hierarchy_find` | `0x00553260` | high | Recursively finds the HierList&lt;Screen&gt; node for a pane and optionally returns its owner list and index. |
| `ui_screen_pane_ctor` | `0x00553350` | high | Constructs the startup RTTI ScreenPane root with primary Pane and secondary TimerHandler vtables. |
| `ui_screen_pane_set_cursor_mode` | `0x00554330` | high | Stores the cursor image and hotspot table selector at root ScreenPane +0x27C and redraws the cursor state. |
| `ui_show_users_list_draw_row` | `0x0055AF60` | high | Draws one ShowUsersListPane row, resolves its final color through palette slot 0, and clamps the eight-state selector before choosing its visual. |
| `ui_show_users_pane_ctor` | `0x0055B2B0` | high | Constructs the RTTI-backed ShowUsers pane from _nusers.txt and attaches its controls. |
| `ui_show_users_pane_open` | `0x0055BFA0` | high | Opens or reveals ShowUsersPane after a response and schedules its 100 ms pane timer. |
| `ui_show_users_rebuild_visible_list` | `0x0055C3E0` | high | Builds visible user-list rows and overrides the server palette index with 0x80 for Friendlist.cfg or 0x24 for Familylist.cfg matches. |
| `ui_show_users_clear_lists` | `0x0055C760` | high | Clears the master and filtered ShowUsers row collections before a replacement list is applied. |
| `ui_spelled_view_pane_ctor` | `0x0056A740` | high | Constructs SpelledViewPane_A with ten empty icon/stage slots and the frame-0 spelled.epf background. |
| `ui_spelled_view_pane_handle_network_event` | `0x0056A8B0` | high | Routes exact RTTI SSpelled opcode 0x3A to the indicator update path. |
| `ui_spelled_view_pane_handle_timer` | `0x0056A910` | high | Updates pane visibility state without changing any icon or duration stage. |
| `ui_spelled_view_pane_draw` | `0x0056A980` | high | Draws up to ten group-2 icons and maps stages 1 through 6 to progressively larger colored bars. |
| `ui_spelled_view_pane_apply_packet` | `0x0056AC60` | high | Updates a matching icon, removes it for stage zero, or inserts a new nonzero icon into the first of ten empty slots. |
| `ui_status_info_pane_ctor` | `0x00573810` | high | Constructs exact RTTI StatusInfoPane, initializes the point count, control gate, selected index, selector table, and blink phase, and installs the TimerHandler secondary vtable. |
| `ui_status_info_handle_network_event` | `0x00573F90` | high | StatusInfoPane routes exact SStatus, SLevelPoint, and SChangeHour objects to their dedicated update paths. |
| `ui_status_info_timer_callback` | `0x00574440` | high | Receives the TimerHandler-adjusted StatusInfoPane pointer, toggles blink phase, redraws the pane, and schedules another 500 ms tick while stat_points is nonzero. |
| `ui_status_info_update_from_status_packet` | `0x00574B30` | high | Copies each present SStatus block into StatusInfoPane, including the same stat-button gate and point count used by SLevelPoint, but does not manage the blink timer. |
| `ui_status_info_apply_level_point_packet` | `0x00574D50` | high | Copies SLevelPoint's control gate and point count, clears pane timers, starts a 500 ms timer for a nonzero count, and invalidates the pane. |
| `ui_status_info_draw` | `0x00574ED0` | high | Draws StatusInfoPane values and uses has_stat_points plus blink_phase to gate and alternate the five stat-increase controls and point count. |
| `ui_status_info_format_values` | `0x005752D0` | high | Formats the main character-sheet values retained by StatusInfoPane after SStatus updates. |
| `ui_extra_status_info_format_values` | `0x00575AA0` | high | Formats attack and defense element names, magic resistance in ten-percent units, signed armor class, damage, and hit. |
| `ui_extra_status_info_update_from_status_packet` | `0x00575FB0` | high | Copies the SStatus modifiers block into ExtraStatusInfoPane's compact combat-stat fields. |
| `ui_extra_status_info_handle_network_event` | `0x00576040` | high | ExtraStatusInfoPane routes SStatus to its combat-stat updater. |
| `ui_terminal_pane_handle_server_data` | `0x00579090` | high | TerminalPane2 primary-vtable slot +0x50 scans initial wire bytes, handles ESC C and ESC S plus Telnet terminal negotiation, and queues CHello and CVersion. |
| `ui_text_insert_formatted` | `0x0057B300` | high | Forwards a NUL-terminated string to the rich text insertion and markup path. |
| `ui_text_copy_bytes` | `0x0057B420` | high | Copies the smaller of the requested byte count and current text length, appends a null terminator, and returns the copied length. |
| `ui_text_insert_color_markup` | `0x0057D310` | high | Recognizes lowercase three-byte {=a through {=x tokens and changes the following run's palette index. |
| `ui_text_enforce_max_bytes` | `0x0057F530` | high | Trims oldest TextEditPane bytes from the front when its configured byte limit is exceeded, preserving DBCS boundaries. |
| `ui_text_enforce_max_lines` | `0x0057F680` | high | Trims oldest TextEditPane lines when its configured line limit is exceeded. |
| `ui_line_input_copy_text` | `0x00584A00` | high | Calls the LineInputPane text control's bounded copy method and returns its copied byte length. |
| `ui_town_map_lookup_current_map` | `0x0058F640` | high | Finds the active map number in the five-value _tcoord.txt records and returns four placement values. |
| `ui_town_map_lookup_key` | `0x0058F6F0` | high | Finds a server-supplied key in the first field of a six-value _tncoord.txt record and returns its map asset number plus four placement values. |
| `ui_town_map_parse_coordinate_table` | `0x0058F7C0` | high | Parses decimal lines into five-value current-map records or six-value server-keyed records. |
| `ui_town_map_load_coordinate_tables` | `0x0058F9A0` | high | Loads and caches _tcoord.txt and _tncoord.txt for the two TownMapPane selection modes. |
| `ui_town_map_pane_current_map_ctor` | `0x0058FB50` | high | Constructs exact RTTI TownMapPane with use_server_key zero for the built-in map-button path. |
| `ui_town_map_pane_keyed_ctor` | `0x0058FBE0` | high | Constructs exact RTTI TownMapPane with use_server_key one and retains the SScreenShot payload key. |
| `ui_town_map_draw` | `0x0058FD00` | high | Rebuilds the TownMapPane canvas from the selected table entry and current marker frame. |
| `ui_town_map_draw_selected_entry` | `0x0058FD50` | high | Chooses _tcoord.txt or _tncoord.txt, resolves the town-map asset and placement values, and queues immediate close when no entry matches. |
| `ui_town_map_compose_view` | `0x0058FFC0` | high | Composes _t_back.spf, the selected _tN.spf and _tNn.spf images, and the tmuser.epf marker when the map matches. |
| `ui_town_map_close` | `0x00590940` | high | Cancels all TownMapPane timers, unregisters the pane, and removes it from the live UI. |
| `ui_town_map_handle_pointer_event` | `0x00590990` | high | Arms on pointer press and closes TownMapPane on the matching release. |
| `ui_town_map_handle_keyboard_event` | `0x005909E0` | high | Handles TownMapPane close commands and the ordinary local screenshot keyboard command; packet receipt does not invoke the screenshot branch. |
| `ui_town_map_timer_callback` | `0x00590AD0` | high | Advances the marker frame modulo seven, requeues timer 0 every 50 ms after the initial 100 ms delay, and closes on timer ID 0x4D2. |
| `ui_user_confirm_pane_ctor` | `0x005921C0` | high | Constructs the 0x73C-byte exact RTTI UserConfirmPane and stores the SMessage reply context at +0x634 through +0x738. |
| `ui_user_confirm_pane_send_ok` | `0x00592260` | high | UserConfirmPane's OK callback calls net_send_confirm with choice 1; the button label and reply were confirmed by project-owner runtime testing. |
| `ui_user_confirm_pane_send_cancel` | `0x00592280` | high | UserConfirmPane's Cancel callback calls net_send_confirm with choice 0; the button label and reply were confirmed by project-owner runtime testing. |
| `ui_gui_back_pane_handle_network_event` | `0x0059D1D0` | high | GUIBackPane routes SStatus packets containing vitals to its bars and SWindowChange to its lower-tray page selector. |
| `ui_gui_back_pane_apply_window_change` | `0x0059D370` | high | Maps SWindowChange codes 0 through 4 to Items, Skills, Spells, Chat, and Status while preserving GUIBackPane's expanded state. |
| `ui_gui_back_pane_update_vitals_from_status_packet` | `0x0059D6C0` | high | Copies current and maximum health and mana from SStatus into GUIBackPane bar targets. |
| `ui_gui_back_layout_init_common` | `0x0059D830` | high | Reads common named controls from one loaded GUIBackPane layout, including BTN_HELP and the other bottom actions. |
| `ui_gui_back_pane_ctor` | `0x0059FB60` | high | Constructs the RTTI-backed GUIBackPane and its two size-specific layout records and child panes. |
| `ui_gui_back_activate_action` | `0x005A0B70` | high | Dispatches GUIBackPane bottom-action IDs; action 0 creates HotKeyPane, while the other IDs open their normal panes or local actions. |
| `ui_gui_back_handle_pointer` | `0x005A0CF0` | high | Hit-tests six bottom-action rectangles on a left-button event; BTN_HELP is slot 0 and is passed to ui_gui_back_activate_action after click debounce. |
| `ui_gui_back_pane_draw` | `0x005A2050` | high | Draws GUIBackPane state, including selection of the network indicator image from the latest movement round-trip value. |
| `ui_gui_back_pane_set_network_latency` | `0x005A2B80` | high | Stores the latest matching CMove and SMove round-trip in GUIBackPane and invalidates the network-indicator region. |
| `ui_gui_back_pane_request_show_users` | `0x005A2C60` | high | GUIBackPane interface method that requests the current world-user list through CWho. |
| `ui_gui_back_get_page_expanded` | `0x005A2CC0` | high | Returns GUIBackPane's page_is_expanded flag at complete object offset +0x4FB0. |
| `ui_game_interface_activate_number_key` | `0x005A2D90` | high | Routes number keys by the selected GUIBackPane mode; item mode maps keys 1 through 9 and 0 to inventory slots 1 through 10. |
| `ui_gui_back_select_page_mode` | `0x005A2FB0` | high | Selects one GUIBackPane page, records its expanded flag, and applies normal or expanded geometry from the active small or large layout record. |
| `ui_gui_back_apply_layout` | `0x005A3900` | high | Selects one GUIBackPane layout and copies its bottom control rectangles into the six live action slots; BTN_HELP becomes slot 0. |
| `ui_inventory_select_buttons_handle_action` | `0x005A5210` | high | Handles local lower-tray selection buttons through the same page-mode interface used by SWindowChange, with additional paired-page toggles and collapse. |
| `ui_new_system_message_text_pane_ctor` | `0x005A8FB0` | high | Constructs the TextEditPane child that stores and renders persistent message history. |
| `ui_new_system_message_pane_handle_packet_event` | `0x005A9000` | high | Recognizes SMessage packet events and forwards them to the history type router. |
| `ui_new_system_message_pane_ctor` | `0x005A9060` | high | Constructs NewSystemMessagePane with one visible row, a TextEditPane child, and ten initial blank lines. |
| `ui_new_system_message_pane_set_visible_lines` | `0x005A9310` | high | Changes the visible history row count and recomputes the pane layout. |
| `ui_new_system_message_pane_update_layout` | `0x005A9420` | high | Repositions the history skin and TextEditPane child for the selected number of visible rows. |
| `ui_new_system_message_pane_handle_mouse_event` | `0x005A9890` | high | Handles the draggable history control and clamps the visible area to one through ten rows. |
| `ui_new_system_message_pane_append_history` | `0x005A9A20` | high | Accepts at most 70 bytes, prefixes a newline, normalizes carriage returns, and appends to persistent history. |
| `ui_new_system_message_pane_handle_message_packet` | `0x005A9B40` | high | Routes SMessage types 0x00 through 0x06, 0x0B, and 0x0C into persistent history. |
| `ui_report_movement_round_trip` | `0x005A9DA0` | high | Forwards one matching movement round-trip sample to the live GUIBackPane interface. |
| `ui_user_info_apply_portrait_body` | `0x005ACD10` | high | Decodes a portrait/profile body into UserInfoPane state and refreshes its portrait canvas and text. |
| `ui_user_info_handle_server_packet` | `0x005AD160` | high | The UserInfoPane vtable event handler sends the local portrait response when the decoded opcode is 0x49. |
| `ui_user_info_refresh_local_portrait` | `0x005AD5D0` | high | Builds the local portrait body and reapplies it to UserInfoPane without calling the network submitter. |
| `ui_user_info_timer` | `0x005AD600` | high | Timer 0x1241 calls the local portrait refresh after the profile editor saves. |
| `ui_user_info_reload_album` | `0x005B04A0` | high | Loads the active character's album.dat and repopulates the current nui_AlbumPane tiles. |
| `ui_user_info_export_album_portrait_jpeg` | `0x005B0580` | high | Current Save fills transparent pixels from _nportbk.spf, copies the prior extensionless portrait to .bak, and always writes JFIF. |
| `ui_user_info_handle_album_action` | `0x005B0AB0` | high | Maps album tile action 0 to Save confirmation event 0x1242 and action 1 to Remove confirmation event 0x1243. |
| `ui_user_info_update_status_from_packet` | `0x005B0C40` | high | Updates UserInfoPane's five attributes and signed armor class from present SStatus blocks. |
| `ui_user_info_apply_self_look` | `0x005B0D10` | high | Copies SSelfLook identity and nation fields into UserInfoPane, rebuilds its legend list, and reloads SClass metadata when the class changes. |
| `ui_user_info_add_equipment_from_packet` | `0x005B1070` | high | Maps SAddEquip slots 1 through 18 to UserInfoPane child-view indices 0 through 17 and forwards the visible item fields. |
| `ui_user_info_remove_equipment_from_packet` | `0x005B1100` | high | Maps a checked SRemoveEquip slot and asks the UserInfoPane child equipment view to clear that entry. |
| `ui_portrait_text_dialog_ctor` | `0x005B11A0` | high | Constructs RTTI-backed PortraitTextInputDialogPane from _nui_pi.txt and loads profile.txt. |
| `ui_portrait_text_dialog_action` | `0x005B1510` | high | Action 1 saves profile.txt and queues timer 0x1241; action 2 closes without saving. |
| `ui_open_user_info` | `0x005B1FA0` | high | Opens the singleton UserInfoPane and selects the requested local or other-user mode. |
| `ui_album_picture_dialog_ctor` | `0x005B24E0` | high | Constructs exact RTTI AlbumPicDialogPane from _nui_alb.txt and attaches SAVE before REMOVE. |
| `ui_album_picture_handle_action` | `0x005B2A00` | high | Forwards local action 0 or 1 with this tile's 0x1234-based event ID. |
| `ui_nui_album_pane_ctor` | `0x005B2A70` | high | Constructs exact RTTI nui_AlbumPane from _nui_al.txt and creates 100 picture dialogs. |
| `ui_nui_album_show_page_pair` | `0x005B31C0` | high | Displays 12 records as two six-item pages and labels the current adjacent page numbers. |
| `ui_nui_album_load_records` | `0x005B3320` | high | Clears all 100 tile previews and fills active entries from one loaded AlbumFile. |
| `ui_nui_album_handle_page_action` | `0x005B3700` | high | Moves the visible page base backward or forward by two, clamped to 0 through 15. |
| `ui_nui_album_handle_picture_action` | `0x005B3770` | high | Converts picture events 0x1234 through 0x1297 into parent album action and zero-based record index. |
| `ui_nui_legend_pane_apply_self_look` | `0x005B7ED0` | high | Clears and rebuilds RTTI class nui_LegendPane from SSelfLook's legend records. |
| `ui_map_loading_pane_ctor` | `0x005BA040` | high | Constructs RTTI class MapLoadingPane from _nloadm.txt, registers its singleton, and adds it as a visible screen pane at zero percent. |
| `ui_map_loading_pane_dtor` | `0x005BA2B0` | high | Unregisters MapLoadingPane from the screen and clears its global singleton during destruction. |
| `ui_map_loading_set_progress` | `0x005BA330` | high | Stores the SMapPart transfer percentage in MapLoadingPane and invalidates the pane for redraw. |
| `ui_map_loading_register_singleton` | `0x005BA5D0` | high | Publishes the enclosing MapLoadingPane through its global singleton pointer during construction. |
| `ui_map_loading_unregister_singleton` | `0x005BA610` | high | Clears the global MapLoadingPane pointer when it still refers to the pane being destroyed. |
| `ui_snow_particle_pane_ctor` | `0x005BD710` | high | Constructs one ImagePane-backed snow particle from a snowaNN.epf resource. |
| `ui_world_balloon_pane_ctor` | `0x005C4F00` | high | Constructs the timed world speech pane; modes 0 and 1 use a framed balloon, while mode 2 uses a text-only pane. |
| `ui_world_balloon_layout` | `0x005C5390` | high | Measures and positions wrapped speech text and the optional balloon frame relative to the speaking world object. |
| `ui_world_balloon_wrap_text` | `0x005C5490` | high | Wraps speech text into the compact line layout consumed by the world balloon renderer. |
| `ui_world_balloon_draw` | `0x005C5730` | high | Draws Say and Shout with a frame and draws Chant as centered text without a frame, using palette indexes 0xFF, 0x45, and 0x58. |
| `ui_world_pane_screen_to_tile` | `0x005C75A0` | high | Converts a screen-space point through the active world controller to map tile coordinates, or returns negative coordinates when no controller is available. |
| `ui_world_pane_set_blinded` | `0x005C7600` | high | Forwards the SStatus-derived blinded state from WorldPane to the world renderer. |
| `ui_world_show_speech` | `0x005CBF90` | high | Attaches a timed speech pane to a world object for the requested speech mode and duration. |
| `ui_world_pane_draw_to_target` | `0x005CE350` | high | Copies WorldPane output to its target and applies the ambient-color and 8-bit light-mask blend when lighting is active below intensity 0x20. |
| `ui_world_object_name_pane_ctor` | `0x005E3F00` | high | Constructs the 0x1DC-byte RTTI WorldObject_Name_Pane and retains at most 63 text bytes plus a NUL at +0x198. |
| `ui_world_pane_handle_living_object_message` | `0x005EF120` | high | Handles RTTI-backed WORLD_LIVING_OBJECT_MESSAGE traffic; give event 2 rejects the local character and dispatches TimerHandler event 1 with the target object ID to the source InvItemPane. |
| `ui_world_pane_handle_inventory_drop` | `0x005EF620` | high | Converts a dragged inventory item's pointer position to a bounded map tile and dispatches it to InvItemPane; it does not compare the tile with the player's position. |
| `ui_world_pane_handle_drop_event` | `0x005EF790` | high | Routes a dragged-pane drop through eligible child panes, then handles an unconsumed inventory-item drop against the world map. |
| `ui_world_pane_request_change_direction` | `0x005F0900` | high | Applies the requested direction to the local WorldObject_User immediately, then sends CChangeDirection. |
| `ui_world_pane_attack_from_keyboard` | `0x005F0BF0` | high | Handles the Space-key attack path and submits only when the previous accepted Space attack was absent or more than 100 ms ago. |
| `ui_world_pane_handle_direction_input` | `0x005F0C40` | high | Turns with CChangeDirection when requested facing differs; otherwise attempts one tile of movement. |
| `ui_world_pane_handle_keyboard_event` | `0x005F0D20` | high | Handles WorldPane keyboard commands; the Tab map-overlay path gives character class 2 the zoom-enabled configuration observed for Rogues. |
| `ui_world_handle_mini_game_server_packet` | `0x005F2350` | high | Handles SMiniGame action 8 subtype 1 as a world/map interaction, then forwards the packet to the common mini-game action handler. |
| `ui_world_pane_draw_content` | `0x005F27A0` | high | WorldPane content hook that draws the world when ready or clears the pane. |
| `ui_world_pane_reset_movement_state` | `0x005F4900` | medium | Resets WorldPane movement and queued-path state after authoritative position changes and the SMove direction-4 path. |
| `ui_world_pane_attack_target` | `0x005F4A70` | high | Faces and attacks an adjacent selected target through CAttack without using the Space-key throttle. |
| `ui_capture_self_portrait_to_album` | `0x005F5200` | high | Renders the local player to 48 by 56 pixels, enforces the 0xE10-second normal cooldown, captions the first free record with ctime, and saves album.dat. |
| `ui_has_map_loading_pane` | `0x005F6470` | high | Reports whether the global MapLoadingPane pointer is non-null. |
| `ui_get_map_loading_pane` | `0x005F6490` | high | Returns the current global MapLoadingPane pointer used by SMapPart progress handling. |
| `ui_close_map_loading_pane` | `0x005F64A0` | high | Invokes the deleting destructor for the current MapLoadingPane when a map transfer finishes. |
| `ui_apply_mini_game_server_packet` | `0x005F6AB0` | high | Launches selectors 1 through 4 for SMiniGame action 4 and consumes action 8 after the world-specific path. |
| `ui_open_town_map_from_screen_shot_packet` | `0x005F6BC0` | high | Reads SScreenShot's retained u8 key and opens TownMapPane in the server-keyed _tncoord.txt mode. |
| `ui_apply_block_input_server_packet` | `0x005F7AA0` | high | Maps SBlockInput state 0 to held-button release plus ClockPane creation and state 1 to ClockPane removal; other states are ignored. |
| `ui_open_manufacture_dialog_from_manual_packet` | `0x005F7AE0` | high | Creates the singleton ManufactureDialogPane only for SManual RecipeCount and ignores Recipe detail messages when no pane exists. |
| `ui_create_field_map_pane` | `0x005F88B0` | high | Allocates a 640 by 480 FieldMapPane, initializes it from decoded SFieldMap values, registers it with the screen root, and retains it in WorldPane. |
| `ui_world_capture_self_portrait_to_album` | `0x005F9B00` | high | WorldPane_Impl wrapper that invokes the album capture with zero, selecting the normal cooldown path. |
| `ui_world_pane_change_user_state` | `0x005F9E20` | high | WorldPane_Impl interface method that forwards a requested UserState to CChangeUserState. |
| `ui_world_pane_get_local_action_state` | `0x005F9E50` | high | WorldPane_Impl virtual getter returns the low-seven-bit SUserAppearance action state stored in WorldUserFunc. |
| `ui_world_pane_get_self_object_id` | `0x005F9EC0` | high | WorldPane_Impl virtual getter returns the SUserAppearance user ID stored in WorldUserFunc. |
| `ui_world_pane_get_appearance_unknown_final` | `0x005FA040` | high | WorldPane_Impl virtual getter returns the final parsed SUserAppearance byte; no client decision based on it is identified. |
| `ui_world_pane_get_guild_value` | `0x005FA0B0` | medium | WorldPane_Impl virtual getter returns the second post-ID SUserAppearance byte unchanged; project behavioral evidence associates it with guild state. |
| `ui_world_pane_get_character_class` | `0x005FA0E0` | high | WorldPane_Impl virtual getter returns the third post-ID SUserAppearance byte; the Tab map-overlay path gives value 2 the Rogue-only zoom-enabled configuration. |

## Network

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `net_send_web_board_dialog_request` | `0x004160A0` | high | Builds the exact two-byte CWebBoard action-0 body and starts BrowserDialogPane's 20-second response timer. |
| `net_percent_encode_web_board_cookie_value` | `0x00416810` | high | Percent-encodes reserved, unsafe, control, and non-ASCII bytes before BrowserDialogPane stores the boardinfo cookie. |
| `net_send_self_look` | `0x0041B840` | high | Builds the exact one-byte CSelfLook plaintext body as opcode 0x2D and submits length one. |
| `net_send_group_toggle` | `0x0041B8E0` | high | Builds and submits the exact one-byte CGroupToggle plaintext body containing only opcode 0x2F. |
| `net_send_field_map_command` | `0x00430D30` | high | Command-line CFieldMap builder writes opcode 0x3F, a zero checksum, and caller-supplied map ID, X, and Y words. |
| `net_parse_endpoint_override` | `0x00433010` | high | Parses a positional IPv4 address or hostname and optional port, but no active mode-1 path calls it. |
| `net_configure_default_endpoint` | `0x00433380` | high | Resolves da0.kru.com, applies the hardcoded IPv4 fallback, selects port 2610 or 2601, and loads or creates the registry-backed installation identifiers later sent by CLogin. |
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
| `net_send_new_user_request` | `0x0043D820` | high | Builds CNewUser opcode 0x02 with length-prefixed name, password, and distribution-dependent account text; Japan mode 13 appends a u16 ISP selector. |
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
| `net_send_exchange_start` | `0x0046A2F0` | medium | Builds CExchange as opcode 0x4A, action 0x00, and a big-endian u32 argument; no live static caller was recovered. |
| `net_send_exchange_accept` | `0x0046A390` | high | Builds opcode 0x4A, action 0x05, and ExchangeDialog +0x630. |
| `net_send_exchange_cancel` | `0x0046A440` | high | Builds opcode 0x4A, action 0x04, and the supplied target or exchange ID. |
| `net_send_exchange_set_gold` | `0x0046A4F0` | high | Builds opcode 0x4A, action 0x03, exchange ID, and big-endian u32 gold amount. |
| `net_send_exchange_add_item` | `0x0046A5C0` | high | Builds opcode 0x4A, action 0x01, exchange ID, and one-based u8 inventory slot. |
| `net_send_exchange_add_stackable_item` | `0x0046C2A0` | high | Builds opcode 0x4A, action 0x02, exchange ID, staged slot, and u8 quantity. |
| `net_request_family_name` | `0x004719B0` | high | EquipPane reaches this opcode-only 0x7A request paired with SFamilyName. |
| `net_send_field_map_selection` | `0x00476390` | high | Normal field-map UI builder writes opcode 0x3F followed by the selected node's checksum, map ID, X, and Y words. |
| `net_send_drop` | `0x00496C90` | high | Builds CDrop as opcode 0x08, source slot, target X, target Y, and u32 quantity. |
| `net_send_give` | `0x00496D90` | high | Builds the 10-byte CGive body as opcode 0x29, u8 source slot, u32 living target object ID, and u32 quantity. |
| `net_send_use_inventory_item` | `0x00496E90` | high | Checks the item denial list, then builds CUse as opcode 0x1C followed by the one-byte slot retained from SAddInventory. |
| `net_send_drop_gold` | `0x004975C0` | high | Parses a nonzero amount and builds CDropGold as opcode 0x24, u32 amount, u16 X, and u16 Y. |
| `net_send_give_gold` | `0x00497B10` | high | Parses a nonzero amount and builds the 9-byte CGiveGold body as opcode 0x2A, u32 amount, and u32 living target object ID. |
| `net_send_get_from_map_item_pane` | `0x00498550` | high | Builds CGet as opcode, destination slot, MapItem_Pane world X, and world Y. |
| `net_send_use_skill` | `0x00499420` | high | Builds CUseSkill as opcode 0x3E followed by the one-byte slot retained from SAddSkill. |
| `net_build_use_spell_target` | `0x0049AB60` | high | Builds CUseSpell as opcode, slot, u32 target ID, u16 X, and u16 Y, then queues the completed body for casting. |
| `net_build_use_spell_no_args` | `0x0049AD40` | high | Builds the slot-only CUseSpell form and queues the completed two-byte body for casting. |
| `net_send_spell_delay_request` | `0x0049BAB0` | high | Builds CSpellDelayRequest as opcode 0x4D followed by the one-byte cast-line count. |
| `net_send_spell_delay_say` | `0x0049BB40` | high | Builds CSpellDelaySay as opcode 0x4E followed by a string8 configured cast line or the final spell name. |
| `net_request_cash_shop` | `0x004A03B0` | high | ItemShop::ShoppingBagDialogPane sends the opcode 0x6C body during construction. |
| `net_send_quit` | `0x004B79C0` | high | Builds the opcode-only CQuit variant, submits one byte, tears down the current connection, then chooses a local TerminalPane2 restart or process-close path. |
| `net_handle_version_check` | `0x004B7F80` | high | Handles SVersionCheck opcode 0x00 outside the RTTI packet factory; subtype 0 installs transport state and subtype 2 constructs NewPatchPane for the Patcher2.exe handoff. |
| `net_handle_login_check` | `0x004B8420` | high | Handles SLoginCheck opcode 0x02; status zero enters session setup and failures carry a display message. |
| `net_handle_stipulation_raw` | `0x004B8570` | high | Handles the decoded-buffer form of SStipulation and requests the homepage first when its cached URL is absent. |
| `net_handle_stipulation` | `0x004B8890` | high | Handles an RTTI-backed SStipulation object and requests the homepage first when its cached URL is absent. |
| `net_dispatch_main_menu_events` | `0x004B8B70` | high | MainMenuPane routes decoded SVersionCheck and SLoginCheck byte buffers outside the packet factory. |
| `net_dispatch_main_menu_events` | `0x004B8B80` | high | Routes startup decoded buffers and RTTI packet objects to version, stipulation, transfer, and browser handlers. |
| `net_handle_transfer_server` | `0x004B9510` | high | Reconnects to the endpoint in STransferServer, then sends raw opcode 0x10, the opaque handoff token unchanged, and the common submission terminator. |
| `net_handle_browser` | `0x004B9B00` | high | Handles RTTI-backed SBrowser variants; subtype 3 caches the supplied homepage URL and marks it available. |
| `net_handle_advertisement_server_packet` | `0x004B9DA0` | high | MainMenuPane forwards the parsed SAdvertisement string, length, and three numeric fields into the application-wide deferred post-exit advertisement state. |
| `net_send_alive` | `0x004BA010` | high | MainMenuPane timer paths send opcode 0x71 and schedule another callback after 30 seconds. |
| `net_send_request_homepage` | `0x004BA0C0` | high | Builds CRequestHomepage fields 68 01; the common submission layer appends the transmitted zero byte. |
| `net_send_login_request` | `0x004BAA80` | high | Builds CLogin opcode 0x03 with two u8-length credential strings and a 16-byte masked installation block, submits it through the static-key path, then persists the submitted character name. |
| `net_dispatch_change_password_events` | `0x004BB8A0` | high | Routes raw lobby opcode 0x02 to the password-change result handler while ChangePasswordDialogPane is active. |
| `net_handle_change_password_result` | `0x004BBCB0` | high | Handles state-dependent lobby opcode 0x02; status 0 closes successfully, 0x0F resets the existing password, and other failures reset the new-password controls. |
| `net_send_change_password` | `0x004BC050` | high | Builds CChangePassword opcode 0x26 with u8-length name, existing password, and new password. |
| `net_calculate_login_block_integrity` | `0x004BCAD0` | high | Applies the custom 0x1021-table recurrence over the first 12 CLogin installation-block bytes. |
| `net_send_manual_recipe_request` | `0x004C26D0` | high | Builds CManual action 0 with the echoed manufacture ID and a zero-based u8 recipe index. |
| `net_send_manual_craft` | `0x004C27C0` | high | Builds CManual action 1 with the echoed manufacture ID, string8 recipe name, and additional inventory slot. |
| `net_read_manual_length_prefixed_text` | `0x004C3E50` | high | Reads 1-, 2-, 3-, or 4-byte big-endian lengths, copies a bounded prefix, terminates it, and advances over the full declared value. |
| `net_request_object_info` | `0x004CD350` | high | Merchant menu paths call this opcode 0x43 object information request. |
| `net_send_merchant_selection` | `0x004CFE60` | high | MerchantDialogPane::TextMenuDialogEx virtual method that builds and sends CMerchant opcode 0x39. |
| `net_send_merchant_face_menu_selection` | `0x004D77D0` | high | Sends opcode 0x39, target type, target ID, selector B, 1 if selector A is zero else 2, and selector C; this nine-byte body has no u16 pursuit ID. |
| `net_send_pursuit_selection` | `0x004DBC90` | high | MessageDialog and SimpleMessageDialog share this CPursuit opcode 0x3A selection method. |
| `net_dispatch_metadata_events` | `0x004E4D80` | high | MetaTableManager recognizes decoded SMetaData opcode 0x6F outside the packet factory. |
| `net_handle_metadata` | `0x004E4EA0` | high | Parses SMetaData table entries and validates or applies named metadata blobs. |
| `net_request_metadata` | `0x004E53F0` | high | Builds CMetaData operation 0 with a one-byte name length and the requested table name. |
| `net_metadata_uncompress` | `0x004E54F0` | high | Inflates metadata zlib data into a buffer capped at 0x20000 bytes. |
| `net_metadata_crc32` | `0x004E5790` | high | Calculates standard CRC32 over inflated metadata bytes. |
| `net_parse_metadata_table` | `0x004E57C0` | high | Parses big-endian group counts and length-prefixed metadata names and values. |
| `net_send_mini_game_close` | `0x0050C600` | high | Builds CMiniGame action 5 with no action-specific payload; both AbstractGame and FindFarmpet destruction paths call it. |
| `net_send_mini_game_action_6` | `0x0050C670` | high | Builds CMiniGame action 6 as one u8 value followed by a one-byte length and that many text bytes. |
| `net_send_web_board_game_request` | `0x0050C7C0` | high | Builds CWebBoard as opcode 0x73, action 3, selector_1, and selector_2 for web-backed in-game views. |
| `net_send_mini_game_action_7` | `0x0050C890` | high | Builds CMiniGame action 7 with one big-endian u32 nonzero client counter. |
| `net_send_group_request` | `0x00513960` | high | Builds CGroup action 2 with a string8 target name; SGroup action 5 and group UI paths call it. |
| `net_send_group_recruit_stop` | `0x00513A40` | high | Builds CGroup action 6 with the local character name to stop recruiting. |
| `net_send_group_recruit_start` | `0x00513B30` | high | Builds CGroup action 4 with local name, group name, note, level range, and five maximum class counts. |
| `net_send_group_recruit_join` | `0x00514140` | high | Builds CGroup action 7 with the leader retained by GroupAdInfoDialogPane. |
| `net_build_merchant_response_header` | `0x0052C1C0` | high | Writes CMerchant opcode 0x39, target type, big-endian target ID, and big-endian pursuit ID as the common eight-byte body. |
| `net_build_pursuit_response_header` | `0x0052C270` | high | Writes CPursuit opcode 0x3A, target type, target ID, pursuit ID, and step ID as the common ten-byte body. |
| `net_send_merchant_text_menu_selection` | `0x00535590` | high | Sends the selected row's pursuit ID and echoes the optional type-1 server argument in CMerchant. |
| `net_parse_merchant_text_menu` | `0x00535750` | high | Parses optional type-1 string8 argument, u8 row count, and repeated string8 text plus u16 pursuit ID. |
| `net_send_merchant_text_input` | `0x005359D0` | high | Sends CMerchant with optional type-3 server argument followed by the entered string8 text. |
| `net_parse_merchant_text_input_menu` | `0x00535BA0` | high | Parses the optional type-3 string8 server argument and the common u16 pursuit ID for a merchant text input. |
| `net_send_merchant_inventory_item_selection` | `0x005362A0` | high | Sends a selected local inventory slot; pursuit 0x004E uses the alternate literal-1, slot, literal-1 tail. |
| `net_parse_merchant_client_item_menu` | `0x00536390` | high | Parses pursuit ID and a u8 count of one-based local inventory slots, with one extra u32 per row for pursuit 0x004E. |
| `net_send_merchant_server_skill_spell_selection` | `0x00536620` | high | Sends the selected server-supplied skill or spell name as string8 after the CMerchant common header. |
| `net_parse_merchant_server_skill_spell_menu` | `0x00536AD0` | high | Parses pursuit ID and u16-counted graphic type, sprite, color, and string8 name records. |
| `net_send_merchant_client_skill_spell_selection` | `0x00536D60` | high | Sends one selected local spell-book or skill-book slot after the CMerchant common header. |
| `net_parse_merchant_client_skill_spell_menu` | `0x00536E00` | high | Parses pursuit ID and an optional u8-counted slot whitelist; absent or zero count enumerates all learned slots 1 through 89. |
| `net_send_merchant_server_item_selection` | `0x00538710` | high | Sends an ordinary selected item name or the pursuit-0x004B marker, u32 record ID, and u8 quantity tail. |
| `net_parse_merchant_server_item_menu` | `0x005388F0` | high | Parses ordinary server item records or the larger pursuit-0x004B record with ID, quantity, optional description, and two counters. |
| `net_send_pursuit_previous` | `0x0053D940` | high | Sends a no-argument CPursuit with current step minus one. |
| `net_send_pursuit_next` | `0x0053D9D0` | high | Sends a no-argument CPursuit with current step plus one. |
| `net_send_pursuit_close_current` | `0x0053DA90` | high | Sends a no-argument CPursuit with the current step before the pane closes locally. |
| `net_send_pursuit_menu_selection` | `0x0053DC30` | high | Sends current step plus one, argument type 1, and a one-based menu choice. |
| `net_parse_pursuit_menu_choices` | `0x0053DD00` | high | Parses a u8 choice count followed by that many string8 choices for pursuit types 2, 3, and 6. |
| `net_send_pursuit_say_and_menu_selection` | `0x0053DE00` | high | Sends CSay with the selected simple-menu text, then sends the normal type-1 CPursuit answer. |
| `net_send_pursuit_text_input` | `0x0053E070` | high | Sends current step plus one, argument type 2, and the entered string8 text. |
| `net_parse_pursuit_text_prompt` | `0x0053E1D0` | high | Parses string8 prolog, u8 maximum input bytes, and string8 epilog for pursuit types 4, 5, and 9. |
| `net_send_pursuit_say_and_text_input` | `0x0053E270` | high | Sends CSay with prolog, input, and epilog separated by spaces, then sends the normal type-2 CPursuit answer. |
| `net_send_pursuit_protected_text_result` | `0x0053F060` | high | Sends argument type 2 with the manager-produced nonempty string at protected dialog offset +0x638, rather than directly serializing both edit controls. |
| `net_send_user_setting` | `0x00542E60` | high | Builds the fixed two-byte CUserSetting body from opcode 0x1B and one setting ID. |
| `net_packet_preprocessor_handle_server_packet` | `0x005449A0` | high | PacketPreprocessor intercepts typed SMessage opcode 0x0A before pane-tree delivery and consumes only message type 0x11. |
| `net_send_exit_editing_mode` | `0x0054A7D0` | high | Copies up to 8000 edited bytes, converts carriage returns to wire tab bytes, and sends CExitEditingMode opcode 0x23 with retained slot and string16 content. |
| `net_send_popup_group_request` | `0x0054CA50` | high | Resolves the popup target name and builds CGroup opcode 0x2E action 2 with that counted name. |
| `net_build_send_portrait` | `0x0054CE10` | high | Builds opcode 0x4F with nested portrait and profile lengths after applying the local image checks. |
| `net_decode_portrait_profile_body` | `0x0054D570` | high | Reads the nested big-endian portrait and profile lengths used by the portrait body. |
| `net_send_say` | `0x0054FD90` | high | Builds CSay opcode 0x0E with the retained Say or Shout mode and a string8 message of at most 72 bytes. |
| `net_send_tell` | `0x00550590` | high | Builds CTell as opcode 0x19 followed by string8 target and string8 message; guild target ! and group target !! pass through unchanged. |
| `net_send_block_listen_list` | `0x00550AA0` | high | Submits CBlockListen as opcode 0x0D followed by operation 1 and no further fields. |
| `net_send_block_listen_add` | `0x00550C60` | high | Submits CBlockListen opcode 0x0D, operation 2, and a string8 character name. |
| `net_send_block_listen_remove` | `0x00550EE0` | high | Submits CBlockListen opcode 0x0D, operation 3, and a string8 character name. |
| `net_send_multi_server_selection` | `0x0055A090` | high | ServerSelectDialogPane sends opcode 0x57 with the selected configured server index. |
| `net_load_server_table` | `0x0055A240` | high | Loads mServer.tbl numeric lines plus transformed name and greeting text into fixed-size records. |
| `net_save_server_table` | `0x0055A490` | high | Saves server records and transforms the name and greeting text for file storage. |
| `net_transform_server_table_text` | `0x0055A650` | high | Leaves byte zero in place and swaps later byte pairs in a self-inverse text transform. |
| `net_apply_show_users` | `0x0055C7D0` | high | Parses the complete opcode 0x36 body, splits class_and_flags into class, bit 3, and an unresolved upper nibble, and rebuilds all filtered row collections. |
| `net_socket_ctor` | `0x00563910` | high | Constructs the Socket object and initializes packet-transform state. |
| `net_queue_seed_table_barrier` | `0x00563D70` | high | Queues communications command 10 with a one-byte seed selector and returns its waitable completion handle. |
| `net_queue_transfer_endpoint` | `0x00563DA0` | high | Queues communications command 4 with the IPv4 address and port supplied by STransferServer. |
| `net_reset_client_packet_sequence` | `0x00563DE0` | high | Resets the client-to-server encrypted-packet sequence to zero. |
| `net_submit_client_packet` | `0x00563E00` | high | Ordinary bodies gain a transmitted zero. |
| `net_queue_raw_stream_mode` | `0x00564070` | high | Queues communications command 7, whose worker-side case writes the socket raw-stream-mode byte. |
| `net_set_text_framing_enabled` | `0x00564120` | high | Writes the socket flag that selects printable text framing when true and binary 0xAA framing when false. |
| `net_write_u8` | `0x00564140` | high | Writes one byte to a packet body. |
| `net_write_u16be` | `0x00564160` | high | Writes a 16-bit value in network byte order. |
| `net_write_u24be` | `0x005641A0` | high | Writes the low 24 bits in network byte order; CMapRequest uses it for a zero-extended CRC16. |
| `net_write_u32be` | `0x005641F0` | high | Writes a 32-bit value in network byte order. |
| `net_read_u8` | `0x00564260` | high | Reads one byte from an opcode-first packet body. |
| `net_read_u16be` | `0x00564270` | high | Reads a 16-bit big-endian value from an opcode-first packet body. |
| `net_read_u32be` | `0x005642C0` | high | Reads a 32-bit big-endian value from an opcode-first packet body. |
| `net_socket_dispatch` | `0x005643D0` | high | Thread::Socket vtable method that dispatches open, close, reconnect, send, and receive operations. |
| `net_open_transport` | `0x005645C0` | high | Selects the TCP connection path when the configured transport selector is 5. |
| `net_close_transport` | `0x005646A0` | high | Closes the active socket and auxiliary transport handle when present. |
| `net_reconnect_transfer_endpoint` | `0x005647D0` | high | Disables old socket notifications, closes and resets transport state, connects to the supplied transfer endpoint, then sleeps for a fixed 1,000 ms. |
| `net_receive_pending_data` | `0x00564870` | high | Selects the active TCP receiver for transport selector 5 and the serial/modem receiver for selectors 1 through 4. |
| `net_send_client_packet` | `0x005648A0` | high | Selects the outbound opcode transform, then sends either an AA and u16be binary frame or printable records containing the same transformed body. |
| `net_send_text` | `0x00565130` | high | Sends a NUL-terminated string through the active transport. |
| `net_send_byte` | `0x005651B0` | high | Sends one byte through the active transport. |
| `net_connect_and_initialize_transport` | `0x00565210` | high | Initializes Winsock, connects to the configured endpoint, performs the active retry, and registers asynchronous socket events. |
| `net_apply_endpoint_and_connect` | `0x00566A00` | high | Stores a transfer IPv4 address and port in AppConfig, then runs the normal transport connection function. |
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
| `net_send_add_stat` | `0x005755C0` | high | Validates the selected StatusInfoPane control index, writes opcode 0x47 plus its constructor-defined selector, and submits the two-byte CAddStat body. |
| `net_wait_for_command_completion` | `0x00586100` | high | Waits indefinitely for a queued communications command, then removes and destroys its completion record. |
| `net_send_confirm` | `0x005922A0` | high | Builds CConfirm as opcode 0x31, the first server byte, button choice, second server byte, and echoed string8 context. |
| `net_server_packet_base_ctor` | `0x005959D0` | high | Constructs the base server packet object and stores its opcode. |
| `net_get_server_packet_opcode` | `0x00595A00` | high | Returns the opcode stored in a server packet base object. |
| `net_client_packet_base_ctor` | `0x00595A50` | high | Constructs the base client packet object and stores its opcode. |
| `net_packet_reader_ctor` | `0x00595B10` | high | Constructs the bounded reader used by server packet deserializers. |
| `net_packet_reader_read_u8` | `0x00595C20` | high | Reads one byte from a decoded server packet and advances the reader by one. |
| `net_packet_reader_read_u16be` | `0x00595C60` | high | Reads a big-endian 16-bit value from a decoded server packet and advances the reader by two. |
| `net_packet_reader_read_u24be` | `0x00595CA0` | high | Reads a big-endian 24-bit value and advances the decoded server-packet reader by three bytes. |
| `net_packet_reader_read_u32be` | `0x00595CE0` | high | Reads a big-endian 32-bit value from a decoded server packet and advances the reader by four. |
| `net_packet_reader_skip` | `0x00595D60` | high | Advances the decoded server-packet reader by a caller-supplied byte count without validating the skipped values. |
| `net_packet_reader_read_string8` | `0x00595DF0` | high | Reads a one-byte-length-prefixed byte string and appends a local NUL to the destination. |
| `net_server_packet_factory_ctor` | `0x00595F00` | high | Registers 61 opcode-specific server packet constructors in a 256-entry factory. |
| `net_deserialize_server_packet` | `0x005963F0` | high | Creates the registered server packet class and invokes its deserializer; it does not require the reader to consume the complete supplied body. |
| `net_create_server_packet` | `0x00596780` | high | Calls the registered constructor for a server opcode. |
| `net_action_delay_server_packet_ctor` | `0x00597160` | high | Passes opcode 0x3F to the server packet base and installs the exact RTTI SActionDelay vtable. |
| `net_deserialize_action_delay_server_packet` | `0x00597190` | high | Reads u8 selector at object +0x10, u8 one-based slot at +0x11, and big-endian u32 duration_seconds at +0x14. |
| `net_create_add_equip_server_packet` | `0x00597210` | high | Allocates a 0x124-byte RTTI SAddEquip object and calls its concrete constructor. |
| `net_add_equip_server_packet_ctor` | `0x00597290` | high | Passes opcode 0x37 to the server packet base and installs the exact SAddEquip vtable. |
| `net_deserialize_add_equip_server_packet` | `0x005972C0` | high | Reads slot, u16 sprite, dye, string8 name, one skipped byte, and two u32 durability values into SAddEquip. |
| `net_create_add_inventory_server_packet` | `0x00597380` | high | Allocates a 0x12C-byte RTTI SAddInventory object and calls its concrete constructor. |
| `net_add_inventory_server_packet_ctor` | `0x00597400` | high | Passes opcode 0x0F to the server packet base and installs the exact SAddInventory vtable. |
| `net_deserialize_add_inventory_server_packet` | `0x00597430` | high | Reads slot, u16 sprite, dye color, string8 name, u32 quantity, stack flag, current durability, and maximum durability into SAddInventory. |
| `net_create_add_skill_server_packet` | `0x00597510` | high | Allocates a 0x118-byte RTTI SAddSkill object and calls its concrete constructor. |
| `net_add_skill_server_packet_ctor` | `0x00597590` | high | Passes opcode 0x2C to the server packet base and installs the exact SAddSkill vtable. |
| `net_deserialize_add_skill_server_packet` | `0x005975C0` | high | Reads u8 slot, u16 icon, and string8 name into SAddSkill. |
| `net_create_add_spell_server_packet` | `0x00597640` | high | Allocates a 0x224-byte RTTI SAddSpell object and calls its concrete constructor. |
| `net_add_spell_server_packet_ctor` | `0x005976C0` | high | Passes opcode 0x17 to the server packet base and installs the exact SAddSpell vtable. |
| `net_deserialize_add_spell_server_packet` | `0x005976F0` | high | Reads slot, u16 icon, argument type, string8 name, string8 prompt, and cast_lines into SAddSpell. |
| `net_create_add_user_server_packet` | `0x005977B0` | high | Allocates exactly the 0x10-byte server packet base for exact RTTI SAddUser; the class has no derived fields. |
| `net_add_user_server_packet_ctor` | `0x00597830` | high | Passes opcode 0x44 to the server packet base and installs the exact SAddUser vtable. |
| `net_deserialize_add_user_server_packet` | `0x00597860` | high | Empty deserializer; SAddUser consumes no bytes after opcode 0x44. |
| `net_create_advertisement_server_packet` | `0x005978B0` | high | Allocates a zeroed 0x24-byte exact RTTI SAdvertisement object and calls its concrete constructor. |
| `net_advertisement_server_packet_ctor` | `0x00597930` | high | Passes opcode 0x5B to the common server packet base and installs the exact SAdvertisement vtable. |
| `net_deserialize_advertisement_server_packet` | `0x00597960` | high | Reads u16 argument_length, a counted byte view, u16 value_1, u16 value_2, and u8 value_3. |
| `net_create_bad_guy_server_packet` | `0x00597A10` | high | Allocates a 0x18-byte RTTI SBadGuy object and calls its concrete constructor. |
| `net_bad_guy_server_packet_ctor` | `0x00597A90` | high | Passes opcode 0x4A to the common server packet base and installs the exact SBadGuy vtable. |
| `net_deserialize_bad_guy_server_packet` | `0x00597AC0` | high | Reads SBadGuy as u8 mode, u8 marker byte, and u32 guard. |
| `net_create_block_input_server_packet` | `0x00597B40` | high | Allocates a zeroed 0x14-byte exact RTTI SBlockInput object and calls its concrete constructor. |
| `net_block_input_server_packet_ctor` | `0x00597BC0` | high | Passes opcode 0x51 to the common server packet base and installs the exact SBlockInput vtable. |
| `net_deserialize_block_input_server_packet` | `0x00597BF0` | high | Reads u8 state and, only when state is zero, one additional u8 that the active handler never uses. |
| `net_create_bounce_server_packet` | `0x00597C70` | high | Allocates a 0x18-byte RTTI SBounce object and calls its concrete constructor. |
| `net_bounce_server_packet_ctor` | `0x00597CF0` | high | Passes opcode 0x4B to the common server packet base and installs the exact SBounce vtable. |
| `net_deserialize_bounce_server_packet` | `0x00597D20` | high | Reads a big-endian u16 body length, retains a view of that many decoded bytes, and advances the packet reader. |
| `net_deserialize_browser_packet` | `0x00597E50` | high | Parses SBrowser subtypes 1 and 2 as two u16be-length byte strings and subtype 3 as one u8-length homepage URL. |
| `net_create_change_direction_server_packet` | `0x00597F30` | high | Allocates the 0x18-byte RTTI SChangeDirection object and invokes its concrete constructor. |
| `net_change_direction_server_packet_ctor` | `0x00597FB0` | high | Passes opcode 0x11 to the server packet base and installs the exact SChangeDirection vtable. |
| `net_deserialize_change_direction_server_packet` | `0x00597FE0` | high | Reads SChangeDirection as u32 user_id followed by u8 direction. |
| `net_create_change_hour_server_packet` | `0x00598050` | high | Allocates a 0x14-byte RTTI SChangeHour object and calls its concrete constructor. |
| `net_change_hour_server_packet_ctor` | `0x005980D0` | high | Passes opcode 0x20 to the server packet base and installs the exact SChangeHour vtable. |
| `net_deserialize_change_hour_server_packet` | `0x00598100` | high | Reads exactly one u8 time step into SChangeHour object offset +0x10 and leaves any remaining body bytes unread. |
| `net_decode_s_change_weather` | `0x00598210` | high | Reads the one-byte SChangeWeather payload; the main gameplay dispatcher has no opcode 0x1F consumer. |
| `net_create_check_time_server_packet` | `0x00598270` | high | Allocates a 0x14-byte SCheckTime object containing the packet base and one u32 server value. |
| `net_check_time_server_packet_ctor` | `0x005982F0` | high | Passes opcode 0x68 to the server packet base and installs the exact SCheckTime vtable. |
| `net_deserialize_check_time_server_packet` | `0x00598320` | high | Reads one big-endian u32 server_value into SCheckTime object offset +0x10. |
| `net_create_draw_human_objects_server_packet` | `0x005984C0` | high | Allocates a 0x264-byte RTTI SDrawHumanObjects object and invokes its concrete constructor. |
| `net_draw_human_objects_server_packet_ctor` | `0x00598540` | high | Passes opcode 0x33 to the server packet base and installs the exact SDrawHumanObjects vtable. |
| `net_deserialize_draw_human_objects_server_packet` | `0x00598570` | high | Parses X, Y, direction, entity ID, the complete normal or monster-disguise appearance variant, name style, name, group-ad text, and the normal variant's u8 light-mask selector. |
| `net_create_draw_objects_server_packet` | `0x005989C0` | high | Allocates the 0x30-byte RTTI SDrawObjects object and invokes its concrete constructor. |
| `net_draw_objects_server_packet_ctor` | `0x00598A40` | high | Passes opcode 0x07 to the server packet base, installs the exact SDrawObjects vtable, and constructs its retained body reader. |
| `net_deserialize_draw_objects_server_packet` | `0x00598AB0` | high | Reads the u16 entity count and retains a reader over all remaining variable-length records. |
| `net_reset_draw_objects_record_reader` | `0x00598B10` | high | Rewinds the retained SDrawObjects body reader and resets its consumed-record count. |
| `net_read_draw_object_record` | `0x00598B30` | high | Reads one common X, Y, entity ID, and tagged sprite prefix followed by the creature or ground-item variant. |
| `net_create_effect_layer_server_packet` | `0x00598D30` | high | Allocates the 0x28-byte RTTI SEffectLayer object and invokes its concrete constructor. |
| `net_effect_layer_server_packet_ctor` | `0x00598DB0` | high | Passes opcode 0x29 to the server packet base and installs the exact SEffectLayer vtable. |
| `net_deserialize_effect_layer_server_packet` | `0x00598DE0` | high | Reads the target ID and conditional object or tile form, including X-before-Y coordinates when target_id is zero. |
| `net_exchange_server_packet_ctor` | `0x00598F50` | high | Passes opcode 0x42 to the server packet base and installs the exact RTTI SExchange vtable. |
| `net_deserialize_exchange_server_packet` | `0x00598F80` | high | Reads the six event-dependent SExchange bodies and retains the item sprite as its raw big-endian u16. |
| `net_create_field_map_server_packet` | `0x00599210` | high | Allocates the exact RTTI SFieldMap object and invokes its concrete constructor. |
| `net_field_map_server_packet_ctor` | `0x00599290` | high | Passes opcode 0x2E to the server packet base and installs the exact SFieldMap vtable. |
| `net_deserialize_field_map_server_packet` | `0x005992C0` | high | Reads field-name string8, node count, current-node index, and each node's screen position, name, checksum, map ID, X, and Y. |
| `net_create_group_server_packet` | `0x00599440` | high | Allocates the 0x420-byte exact RTTI SGroup object and invokes its concrete constructor. |
| `net_group_server_packet_ctor` | `0x005994C0` | high | Passes opcode 0x63 to the server packet base and installs the exact SGroup vtable. |
| `net_deserialize_group_server_packet` | `0x005994F0` | high | Reads action 1 and 5 as string8 names, action 4 as recruiting details with five maximum/current pairs, and no body for every other action. |
| `net_create_level_point_server_packet` | `0x00599940` | high | Allocates the 0x14-byte exact RTTI SLevelPoint object and invokes its concrete constructor. |
| `net_level_point_server_packet_ctor` | `0x005999C0` | high | Passes opcode 0x3D to the server packet base and installs the exact SLevelPoint vtable. |
| `net_deserialize_level_point_server_packet` | `0x005999F0` | high | Reads exactly two u8 payload fields: has_stat_points followed by stat_points. |
| `net_create_manual_server_packet` | `0x00599A60` | high | Allocates a 0x34-byte exact RTTI SManual object and calls its concrete constructor. |
| `net_manual_server_packet_ctor` | `0x00599AE0` | high | Passes opcode 0x50 to the common server packet base and installs the exact SManual vtable. |
| `net_deserialize_manual_server_packet` | `0x00599B10` | high | Reads the common two-byte ID and message type, then RecipeCount or the complete Recipe variant including the trailing additional-item mode. |
| `net_create_map_server_packet` | `0x00599C60` | high | Allocates the 0x1C-byte exact RTTI SMap object and invokes its concrete constructor. |
| `net_map_server_packet_ctor` | `0x00599CE0` | high | Passes opcode 0x06 to the server packet base and installs the exact RTTI SMap vtable. |
| `net_deserialize_map_server_packet` | `0x00599D10` | high | Reads u8 start X, start Y, rectangle width, and rectangle height, then retains a pointer to the remaining map-cell records. |
| `net_create_map_size_server_packet` | `0x00599EE0` | high | Allocates the fixed-size RTTI SMapSize object and invokes its concrete constructor. |
| `net_map_size_server_packet_ctor` | `0x00599F60` | high | Passes opcode 0x15 to the server packet base and installs the exact SMapSize vtable. |
| `net_deserialize_map_size_server_packet` | `0x00599F90` | high | Reads u16be map number, four bytes, u24be cache value, and string8 name; the handler uses u8 dimensions and ignores the fourth byte. |
| `net_create_message_server_packet` | `0x0059A050` | high | Allocates the RTTI-backed SMessage object registered for server opcode 0x0A. |
| `net_message_server_packet_ctor` | `0x0059A0D0` | high | Constructs SMessage with opcode 0x0A and installs its concrete vtable. |
| `net_deserialize_message_server_packet` | `0x0059A100` | high | Reads the message type, the type-0x11-only prefix, a u16 message length, and the message bytes. |
| `net_create_mini_game_server_packet` | `0x0059A1C0` | high | Allocates the 0x1C-byte RTTI-backed SMiniGame object registered for server opcode 0x64. |
| `net_mini_game_server_packet_ctor` | `0x0059A240` | high | Constructs SMiniGame with opcode 0x64 and installs its concrete vtable. |
| `net_deserialize_mini_game_server_packet` | `0x0059A270` | high | Reads the action plus one u8 for actions 3, 4, and 8 or two big-endian u32 values for action 7. |
| `net_motion_server_packet_ctor` | `0x0059A3F0` | high | Passes opcode 0x1A to the server packet base and installs the exact RTTI SMotion vtable. |
| `net_deserialize_motion_server_packet` | `0x0059A420` | high | Reads u32 object_id, u8 animation, and u16 duration_10ms. |
| `net_move_server_packet_ctor` | `0x0059A520` | high | Passes opcode 0x0B to the server packet base and installs the exact RTTI SMove vtable. |
| `net_deserialize_move_server_packet` | `0x0059A550` | high | Reads direction, four big-endian coordinate words, and the echoed movement step into the fixed SMove packet object. |
| `net_pursuit_message_server_packet_ctor` | `0x0059AA00` | high | Passes opcode 0x30 to the server packet base and installs the exact RTTI SPursuitMessage vtable. |
| `net_deserialize_pursuit_message_server_packet` | `0x0059AA70` | high | Reads the SPursuitMessage common fields, conditional content, and owned subtype tail; type 10 stops after the type byte. |
| `net_create_quit_server_packet` | `0x0059ACA0` | high | Allocates a 0x14-byte RTTI SQuit object and calls its concrete constructor. |
| `net_quit_server_packet_ctor` | `0x0059AD20` | high | Passes opcode 0x4C to the server packet base and installs the exact RTTI SQuit vtable. |
| `net_deserialize_quit_server_packet` | `0x0059AD50` | high | Reads exactly one u8 after the opcode into SQuit offset +0x10; observed following zero bytes are not consumed. |
| `net_create_remove_equip_server_packet` | `0x0059ADB0` | high | Allocates a 0x14-byte RTTI SRemoveEquip object and calls its concrete constructor. |
| `net_remove_equip_server_packet_ctor` | `0x0059AE30` | high | Passes opcode 0x38 to the server packet base and installs the exact SRemoveEquip vtable. |
| `net_deserialize_remove_equip_server_packet` | `0x0059AE60` | high | Reads the one-byte SRemoveEquip slot and widens it into the packet object's 16-bit field. |
| `net_create_remove_inventory_server_packet` | `0x0059AEC0` | high | Allocates a 0x14-byte RTTI SRemoveInventory object and calls its concrete constructor. |
| `net_remove_inventory_server_packet_ctor` | `0x0059AF40` | high | Passes opcode 0x10 to the server packet base and installs the exact SRemoveInventory vtable. |
| `net_deserialize_remove_inventory_server_packet` | `0x0059AF70` | high | Reads the one-byte inventory slot into SRemoveInventory object offset +0x10. |
| `net_create_remove_skill_server_packet` | `0x0059B0E0` | high | Allocates a 0x14-byte RTTI SRemoveSkill object and calls its concrete constructor. |
| `net_remove_skill_server_packet_ctor` | `0x0059B160` | high | Passes opcode 0x2D to the server packet base and installs the exact SRemoveSkill vtable. |
| `net_deserialize_remove_skill_server_packet` | `0x0059B190` | high | Reads the one-byte SRemoveSkill slot into object offset +0x10. |
| `net_create_remove_spell_server_packet` | `0x0059B1F0` | high | Allocates a 0x14-byte RTTI SRemoveSpell object and calls its concrete constructor. |
| `net_remove_spell_server_packet_ctor` | `0x0059B270` | high | Passes opcode 0x18 to the server packet base and installs the exact SRemoveSpell vtable. |
| `net_deserialize_remove_spell_server_packet` | `0x0059B2A0` | high | Reads the one-byte SRemoveSpell slot into object offset +0x10. |
| `net_create_request_crc_server_packet` | `0x0059B300` | high | Allocates the 0x14-byte exact RTTI SRequestCRC object and invokes its concrete constructor. |
| `net_request_crc_server_packet_ctor` | `0x0059B380` | high | Passes opcode 0x3B to the server packet base and installs the exact SRequestCRC vtable. |
| `net_deserialize_request_crc_server_packet` | `0x0059B3B0` | high | Reads the complete SRequestCRC body as one big-endian u16 challenge. |
| `net_server_request_portrait_ctor` | `0x0059B490` | high | Constructs RTTI-backed SRequestPortrait and passes opcode 0x49 to the server packet base. |
| `net_server_request_portrait_deserialize` | `0x0059B4C0` | high | Returns without reading fields, which confirms that SRequestPortrait has no body after the opcode. |
| `net_create_say_server_packet` | `0x0059B510` | high | Allocates the RTTI-backed SSay object registered for server opcode 0x0D. |
| `net_say_server_packet_ctor` | `0x0059B590` | high | Constructs SSay with opcode 0x0D and installs its concrete vtable. |
| `net_deserialize_say_server_packet` | `0x0059B5C0` | high | Reads speech mode 0, 1, or 2, a u32 sender world-object ID, and string8 speech text. |
| `net_screen_menu_server_packet_ctor` | `0x0059B6C0` | high | Passes opcode 0x2F to the server packet base and installs the exact RTTI SScreenMenu vtable. |
| `net_deserialize_screen_menu_server_packet` | `0x0059B730` | high | Reads the SScreenMenu common fields, string16 content, and remaining subtype bytes into an owned packet reader. |
| `net_create_screen_shot_server_packet` | `0x0059B8B0` | high | Allocates the 0x14-byte exact RTTI SScreenShot object and invokes its concrete constructor. |
| `net_screen_shot_server_packet_ctor` | `0x0059B930` | high | Passes opcode 0x6B to the server packet base and installs the exact SScreenShot vtable. |
| `net_deserialize_screen_shot_server_packet` | `0x0059B960` | high | Reads exactly one u8 payload field, used by the consumer as a keyed town-map table selector. |
| `net_create_self_look_server_packet` | `0x0059B9C0` | high | Allocates the 0x9C64-byte RTTI SSelfLook object and invokes its concrete constructor. |
| `net_self_look_server_packet_ctor` | `0x0059BA40` | high | Passes opcode 0x39 to the server packet base and installs the exact SSelfLook vtable. |
| `net_deserialize_self_look_server_packet` | `0x0059BA70` | high | Parses nation and profile text, the optional recruiting block, class metadata, and repeated legend marks. |
| `net_create_self_save_ok_server_packet` | `0x0059BD80` | high | Allocates only the 0x10-byte common server-packet size for the RTTI SSelfSaveOK object. |
| `net_self_save_ok_server_packet_ctor` | `0x0059BE00` | high | Passes opcode 0x21 to the server packet base and installs the exact SSelfSaveOK vtable; the class has no concrete payload deserializer. |
| `net_create_sound_effect_server_packet` | `0x0059BE80` | high | Allocates the 0x14-byte RTTI SSoundEffect object and invokes its concrete constructor. |
| `net_sound_effect_server_packet_ctor` | `0x0059BF00` | high | Passes opcode 0x19 to the server packet base and installs the exact SSoundEffect vtable. |
| `net_deserialize_sound_effect_server_packet` | `0x0059BF30` | high | Reads one sound byte and only a second track byte for mode 0xFF; no trailing u16 is consumed. |
| `net_create_spell_delay_cancel_server_packet` | `0x0059BFC0` | high | Allocates the common 0x10-byte exact RTTI SSpellDelayCancel object and invokes its concrete constructor. |
| `net_spell_delay_cancel_server_packet_ctor` | `0x0059C040` | high | Passes opcode 0x48 to the server packet base and installs the exact SSpellDelayCancel vtable. |
| `net_deserialize_spell_delay_cancel_server_packet` | `0x0059C070` | high | Returns without reading any payload fields, confirming that SSpellDelayCancel contains only its opcode. |
| `net_create_spelled_server_packet` | `0x0059C0C0` | high | Allocates the 0x14-byte exact RTTI SSpelled object and invokes its concrete constructor. |
| `net_spelled_server_packet_ctor` | `0x0059C140` | high | Passes opcode 0x3A to the server packet base and installs the exact SSpelled vtable. |
| `net_deserialize_spelled_server_packet` | `0x0059C170` | high | Reads a big-endian u16 icon followed by one u8 discrete duration stage. |
| `net_create_static_object_state_server_packet` | `0x0059C1E0` | high | Allocates the exact RTTI SStaticObjectState object and calls its concrete constructor. |
| `net_static_object_state_server_packet_ctor` | `0x0059C260` | high | Passes opcode 0x32 to the common server packet base and installs the exact SStaticObjectState vtable. |
| `net_deserialize_static_object_state_server_packet` | `0x0059C290` | high | Reads a u8 count followed by four u8 fields per record: x, y, state, and side. |
| `net_create_status_server_packet` | `0x0059C360` | high | Allocates a 0x7C-byte RTTI SStatus object and invokes its concrete constructor. |
| `net_status_server_packet_ctor` | `0x0059C3E0` | high | Passes opcode 0x08 to the server packet base and installs the exact SStatus vtable. |
| `net_deserialize_status_server_packet` | `0x0059C410` | high | Parses SStatus privilege and conditional stats, vitals, progression, modifiers, standalone state, and mail-state fields. |
| `net_deserialize_stipulation_packet` | `0x0059C8E0` | high | Parses SStipulation mode 0 as a u32be greeting CRC32 and mode 1 as u16be length plus compressed bytes. |
| `net_deserialize_transfer_server_packet` | `0x0059CA40` | high | Parses STransferServer as a u32be IPv4 value, u16be port, and u8-length opaque handoff token. |
| `net_create_user_appearance_server_packet` | `0x0059CAC0` | high | Allocates the fixed-size RTTI SUserAppearance object and invokes its concrete constructor. |
| `net_user_appearance_server_packet_ctor` | `0x0059CB40` | high | Passes opcode 0x05 to the server packet base and installs the exact SUserAppearance vtable. |
| `net_deserialize_user_appearance_server_packet` | `0x0059CB70` | high | Reads u32 user ID followed by facing, raw guild value, character class, action state, and one final unknown byte. |
| `net_create_user_position_server_packet` | `0x0059CC20` | high | Allocates the 0x14-byte RTTI SUserPosition object and invokes its concrete constructor. |
| `net_user_position_server_packet_ctor` | `0x0059CCA0` | high | Passes opcode 0x04 to the server packet base and installs the exact SUserPosition vtable. |
| `net_deserialize_user_position_server_packet` | `0x0059CCD0` | high | Reads exactly u16 x and u16 y; the method returns without consuming four additional bytes observed in captures. |
| `net_create_web_board_server_packet` | `0x0059CD40` | high | Allocates a zeroed 0x314-byte exact RTTI SWebBoard object and calls its concrete constructor. |
| `net_web_board_server_packet_ctor` | `0x0059CDC0` | high | Passes opcode 0x62 to the common server packet base and installs the exact SWebBoard vtable. |
| `net_deserialize_web_board_server_packet` | `0x0059CDF0` | high | Reads action and three string8 buffers; action 3 omits base_url from the wire and derives it from start_url. |
| `net_create_window_change_server_packet` | `0x0059CF50` | high | Allocates the 0x14-byte exact RTTI SWindowChange object registered for server opcode 0x3E. |
| `net_window_change_server_packet_ctor` | `0x0059CFD0` | high | Passes opcode 0x3E to the common server packet base and installs the exact SWindowChange vtable. |
| `net_deserialize_window_change_server_packet` | `0x0059D000` | high | Reads the complete SWindowChange payload as one u8 window_code into packet object offset +0x10. |
| `net_send_who` | `0x0059D7D0` | high | Builds CWho as opcode 0x18 with no payload and submits the complete one-byte plaintext body. |
| `net_send_portrait_profile` | `0x005B1160` | high | Calls net_build_send_portrait and submits the result through net_submit_client_packet. |
| `net_dispatch_server_packet` | `0x005ED990` | high | Routes parsed server packet objects to gameplay handlers by opcode. |
| `net_handle_static_object_state_server_packet` | `0x005F1690` | high | Applies every record to the selected isometric static layer; state 0 targets pair column 1 and any nonzero state targets column 0. |
| `net_handle_status_server_packet` | `0x005F1A10` | high | Applies global SStatus effects by updating WorldUserFunc and setting blinded only when the raw blind code equals 0x08. |
| `net_handle_add_spell_server_packet` | `0x005F1AF0` | high | Forwards decoded SAddSpell fields to the WorldUserFunc session model stored by WorldPane. |
| `net_handle_remove_spell_server_packet` | `0x005F1B30` | high | Forwards decoded SRemoveSpell to WorldUserFunc vtable slot +0x14. |
| `net_handle_add_skill_server_packet` | `0x005F1B70` | high | Forwards decoded SAddSkill to WorldUserFunc vtable slot +0x18. |
| `net_handle_remove_skill_server_packet` | `0x005F1BB0` | high | Forwards decoded SRemoveSkill to WorldUserFunc vtable slot +0x1C. |
| `net_handle_map_size_server_packet` | `0x005F1BF0` | high | Applies u8 map dimensions, NoMap, Winter art, weather mode, local CRC16 cache validation, transfer state, and map lighting. |
| `net_handle_change_hour_server_packet` | `0x005F2160` | high | Stores the SChangeHour time step at WorldPane +0x25C and immediately recomputes map lighting. |
| `net_handle_exchange_started` | `0x005F2190` | high | Handles SExchange event 0x00 before a dialog exists, creates ExchangeDialog when UI state allows it, or replies with CExchange Cancel otherwise. |
| `net_handle_map_server_body` | `0x005F2840` | high | Consumes raw SMap opcode 0x06 as a u8 rectangle header followed by row-major ground and static tile triples, applying cells only while a cache-miss transfer is active. |
| `net_handle_map_part` | `0x005F2A60` | high | Consumes one raw SMapPart row into memory, creates MapLoadingPane on the first accepted row, updates row-index progress, and treats height minus one as completion without tracking earlier rows. |
| `net_handle_request_crc_server_body` | `0x005F2CF0` | high | Reads the raw u16 SRequestCRC challenge, feeds low then high byte through crc16_update from zero, and sends the resulting byte swap as CReplyCRC opcode 0x45. |
| `net_handle_user_appearance_server_packet` | `0x005F2E90` | high | Refreshes self identity on full SUserAppearance updates and always forwards the packet to WorldUserFunc for action-state storage. |
| `net_handle_user_position_server_packet` | `0x005F2F00` | high | Sign-extends SUserPosition x and y, updates and reindexes WorldObject_User when present, and recenters the WorldPane view. |
| `net_handle_move_server_packet` | `0x005F2FC0` | high | Uses SMove direction and previous coordinates to advance or correct the view, requests CRefreshUser on a direction-4 coordinate mismatch, and reports latency only for the current step echo. |
| `net_handle_draw_objects_server_packet` | `0x005F3150` | high | Walks every SDrawObjects record, replaces matching IDs, creates WorldObject_Monster or WorldObject_Item by tagged sprite range, applies creature palette selectors and names, and ignores unsupported ranges. |
| `net_handle_draw_human_objects_server_packet` | `0x005F3340` | high | Creates or refreshes WorldObject_User for the saved self ID and WorldObject_Human otherwise, applies normal or disguised appearance, updates names and optional group ads, and handles Darkness object lights. |
| `net_handle_change_direction_server_packet` | `0x005F3BB0` | high | Finds SChangeDirection.user_id, requests CRequestObject when absent, and applies direction only after an RTTI cast to WorldObject_Living. |
| `net_handle_motion_server_packet` | `0x005F3C80` | high | Finds SMotion.object_id, accepts living object kinds 1 and 2, converts the u16 timing from 10 ms units, and starts the requested class-specific body motion without a sound path. |
| `net_handle_say_server_packet` | `0x005F3E00` | high | Finds the SSay sender, requests a missing object without replaying the speech, and otherwise shows the selected three-second speech style without appending to history. |
| `net_handle_effect_layer_server_packet` | `0x005F3EB0` | high | Creates static, object-attached, or source-to-target moving world effects from SEffectLayer, including the 10000 through 11999 moving-effect selector range. |
| `net_send_get` | `0x005F4200` | high | Builds CGet as opcode 0x07, u8 destination slot, u16 X, and u16 Y. |
| `net_send_group_recruit_view` | `0x005F4340` | high | Builds CGroup action 5 with the selected recruitment name; the paired SGroup action 4 opens GroupAdInfoDialogPane. |
| `net_send_request_object` | `0x005F4430` | high | Builds CRequestObject as opcode 0x0C plus one u32 object ID; confirmed callers use it after a lookup misses or an expected living-object cast fails. |
| `net_send_attack` | `0x005F44B0` | high | Builds CAttack as opcode 0x13 with no payload and submits the complete one-byte plaintext body. |
| `net_send_change_direction` | `0x005F4510` | high | Builds CChangeDirection as opcode 0x11 plus one direction byte after WorldPane turns the local object optimistically. |
| `net_send_move` | `0x005F4580` | high | Builds CMove as opcode, direction, and an incremented rolling u8 step, then records the send time used by a matching SMove reply. |
| `net_send_refresh_user` | `0x005F4640` | high | WorldPane paths call this opcode-only 0x38 builder. |
| `net_send_emotion` | `0x005F46C0` | high | Builds CEmotion as opcode 0x1D followed by one caller-supplied u8 emotion request code. |
| `net_handle_bounce_server_packet` | `0x005F6A80` | high | Submits SBounce's counted embedded bytes directly as an ordinary opcode-first client body and performs no other game or UI action. |
| `net_handle_message_server_packet` | `0x005F6D80` | high | Routes SMessage to the floating GameMessagePane, WindowMessageDialogPane, or ScorePane according to its type byte. |
| `net_handle_enter_editing_mode_server_data` | `0x005F71C0` | high | WorldPane's raw opcode 0x1B branch allocates exact RTTI EditablePaperPane and constructs it in editable mode directly from the decoded body. |
| `net_handle_show_paper_server_data` | `0x005F7250` | high | WorldPane's raw opcode 0x35 branch constructs the same EditablePaperPane in read-only mode. |
| `net_send_check_time` | `0x005F7830` | high | Immediate response to SCheckTime opcode 0x68; builds CCheckTime as opcode 0x75, echoed u32 server_value, and one timeGetTime() u32 sample without local comparison or enforcement. |
| `net_handle_bad_guy_server_packet` | `0x005F7900` | high | Validates the SBadGuy mode and guard, creates and extends Mscfg.dll when possible, then forces client termination on both creation-success and creation-failure paths. |
| `net_handle_show_users` | `0x005F7B80` | high | Handles raw decoded server opcode 0x36, applies the replacement list, and opens the RTTI-backed ShowUsersPane. |
| `net_send_group_automatic_response` | `0x005F8620` | high | Builds CGroup opcode 0x2E, action 3, and a length-prefixed user string for the GroupAnswer automatic path. |
| `net_handle_group_server_packet` | `0x005F8720` | high | Handles SGroup by either opening the normal prompt or immediately sending CGroup action 3 according to AppConfig GroupAnswer. |
| `net_handle_field_map_server_data` | `0x005F8A10` | high | WorldPane's raw opcode 0x2E branch reparses the decoded SFieldMap body and creates the field-map pane instead of consuming the factory-built packet object. |
| `net_send_change_user_state` | `0x005FC790` | high | Normalizes UserState to 0 through 7, builds opcode 0x79 plus the state byte, and stores the same normalized local value. |
| `net_register_bad_guy_server_packet_factory` | `0x00667B20` | high | Registers the RTTI-backed SBadGuy constructor with the server_packet_factory startup path. |

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
| `render_get_human_image_library` | `0x0043FD60` | high | Returns the RTTI-backed HumanImageLib singleton. |
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
| `render_write_canvas_jpeg` | `0x0044D730` | high | Locks one canvas and sends its RGB16 pixels to the shared JFIF writer. |
| `render_get_direct_draw` | `0x0044D820` | high | Returns the DirectDraw wrapper singleton. |
| `render_get_palette_manager` | `0x0044D830` | high | Returns the RTTI-backed PaletteMan singleton. |
| `render_blit_image` | `0x0044DE30` | high | Draws a decoded Image with copy, blend, alpha, and special plane modes. |
| `render_blit_pixmap` | `0x0044FB80` | high | Draws an indexed PixMap with transparent zero pixels and several software blend modes. |
| `render_blit_canvas` | `0x00451E40` | high | Copies or blends one Canvas into another. |
| `render_canvas_blit_mask` | `0x004526C0` | high | Draws a one-bit bitmap mask into a 16-bit Canvas using the current foreground, background, and blend mode. |
| `render_blit_pixmap_with_palette_mappings` | `0x00453E60` | high | Draws indexed monster pixels while replacing configured source-index ranges through ordered palette-family and palette-selector mappings. |
| `render_average_pixels` | `0x004548B0` | high | Combines two 16-bit pixels with the fixed component-average lookup path. |
| `render_canvas_draw_glyph` | `0x00455910` | high | Resolves one 16-bit byte-code key through FontImageLib, blits its one-bit mask, and advances the Canvas cursor. |
| `render_canvas_draw_text` | `0x00455A30` | high | Splits an ANSI byte string with IsDBCSLeadByte, builds one LFT glyph mask per key, and draws it to the software Canvas. |
| `render_get_font_image_library` | `0x004566B0` | high | Returns the RTTI-backed FontImageLib singleton used by the active text renderer. |
| `render_effect_image_session_ctor` | `0x004575B0` | high | Opens the available EFA or EPF variant for one effect image session. |
| `render_get_effect_frame_image` | `0x00457FD0` | high | Lazily decodes and caches one requested effect frame image. |
| `render_effect_image_pool_clear` | `0x00458900` | high | Destroys every retained EffectImageSession and frees the effect-ID pointer array. |
| `render_effect_image_pool_get_frame` | `0x004589C0` | high | Creates one EffectImageSession on the first request for an effect ID, retains it, and asks it for the selected frame. |
| `render_get_effect_image_pool` | `0x00459460` | high | Returns the EffectImagePool singleton. |
| `render_get_icon_image_library` | `0x0045D7E0` | high | Returns the RTTI-backed IconImageLib singleton. |
| `render_font_image_library_ctor` | `0x0047B7D0` | high | Constructs RTTI class FontImageLib, registers its singleton, and loads the language-selected LFT entry. |
| `render_font_image_library_dtor` | `0x0047B860` | high | Destroys FontImageLib and unregisters its singleton. |
| `render_font_load_lft` | `0x0047B8C0` | high | Selects lod.lft, da.lft, yami.lft, or taiwan.lft by language mode and maps its glyph table and bitmap region. |
| `render_font_build_glyph_mask` | `0x0047BAE0` | high | Expands one LFT glyph's padded one-bit rows into the temporary mask and returns its bounds and advance. |
| `render_font_get_glyph_advance` | `0x0047BD60` | high | Returns one LFT advance width, with zero for control bytes and a nominal-width fallback for an omitted space. |
| `render_font_copy_legacy_hangul_glyph` | `0x0047BDE0` | high | Dormant fixed-font path that maps a CP949 Wansung or jamo code and copies its 24-byte glyph. |
| `render_font_copy_legacy_english_glyph` | `0x0047BE80` | high | Dormant fixed-font path that copies one 12-byte English glyph by byte index. |
| `render_font_copy_legacy_fallback_glyph` | `0x0047BEB0` | high | Copies the built-in 24-byte fallback used by an unsupported legacy Hangul code. |
| `render_font_load_legacy_english_fnt` | `0x0047BED0` | high | Dormant loader that places engNN.fnt at printable-ASCII index 0x21 in a 256-record table. |
| `render_font_load_legacy_hangul_fnt` | `0x0047BFB0` | high | Dormant loader that copies the selected 57,624-byte hanNN.fnt entry. |
| `render_font_map_legacy_hangul_code` | `0x0047C150` | high | Maps CP949 B0A1-C8FE syllables and A4A1-A4D3 jamo to the 2,401 fixed Hangul records. |
| `render_image_library_ctor` | `0x0048B2C0` | high | Constructs RTTI class ImageLib and registers its singleton; the object has no filename or decoded-frame cache fields. |
| `render_image_library_dtor` | `0x0048B330` | high | Unregisters and destroys the ImageLib singleton without releasing a shared image cache. |
| `render_load_main_archive_pixmap` | `0x0048BB90` | high | Resolves one requested frame synchronously through file_load_image_frame using the main archive. |
| `render_human_image_library_ctor` | `0x0048BD90` | high | Constructs RTTI class HumanImageLib and registers its singleton. |
| `render_human_image_library_dtor` | `0x0048BE00` | high | Releases the human image library's retained supporting data and unregisters its singleton. |
| `render_monster_image_library_ctor` | `0x0048D010` | high | Constructs RTTI class MonsterImageLib and registers its singleton. |
| `render_monster_image_library_dtor` | `0x0048D080` | high | Unregisters and destroys the MonsterImageLib singleton. |
| `render_icon_image_library_ctor` | `0x0048D590` | high | Constructs RTTI class IconImageLib and registers its singleton. |
| `render_icon_image_library_dtor` | `0x0048D610` | high | Unregisters and destroys the IconImageLib singleton. |
| `render_icon_load_pixmap` | `0x0048D670` | high | Derives an icon resource and frame from the icon kind and ID, builds a caller-owned pixmap view, and attaches the resolved palette selector. |
| `render_get_map_tile_library` | `0x004AE4E0` | high | Returns the MapTileImageLib singleton. |
| `render_get_monster_image_library` | `0x004AE880` | high | Returns the RTTI-backed MonsterImageLib singleton. |
| `render_map_background_images` | `0x004C5270` | high | Draws configured map background or bottom-layer images before world objects. |
| `render_palette_manager_ctor` | `0x00544B70` | high | Constructs RTTI class PaletteMan, registers its palette families, loads the installed PAL series, and packs them for the active 16-bit display mode. |
| `render_palette_resolve_table` | `0x00548510` | high | Decodes bits 24 through 30 as a family and the low 24 bits as a palette number, then returns its 256-entry packed-color table. |
| `render_palette_family_get_or_create` | `0x00548AB0` | high | Grows one palette-family vector in blocks of 16 and allocates a 0x200-byte packed table for a missing palette number. |
| `render_write_screenshot_bmp` | `0x005537F0` | high | Writes the completed client canvas as the first missing uncompressed 16-bit lod001.bmp through lod999.bmp name. |
| `render_screen_tree_frame` | `0x00554040` | high | Redraws the dirty root screen tree and presents the completed frame. |
| `render_screen_subtree` | `0x00555560` | high | Clips and draws one pane subtree through the vtable draw-to-target slot. |
| `render_probe_display_capabilities` | `0x0057A640` | high | Accepts 16-bit or 32-bit desktop color and selects 2x presentation at 1280 by 960 or larger, otherwise 1x on a supported smaller desktop. |
| `render_free_blend_tables` | `0x005933C0` | high | Frees both software component-blend lookup tables. |
| `render_build_blend_tables` | `0x00593490` | high | Builds the 256 by 256 lookup tables for five-bit and six-bit color components. |
| `render_blend_pixel` | `0x005936E0` | high | Blends two 16-bit RGB pixels using a selector and the component lookup tables. |
| `render_palette_pack_16bit` | `0x00593B00` | high | Packs 256 RGB colors for the active display mode while reserving packed zero for palette index zero. |
| `render_resolve_palette_index` | `0x00593D10` | high | Resolves an 8-bit UI color through palette slot 0, which startup loads from legend.pal. |
| `render_video_system_ctor` | `0x00593E20` | high | Constructs the RTTI-backed VideoSystem singleton. |
| `render_video_system_dtor` | `0x00593EA0` | high | Shuts down an active VideoSystem and deletes its DirectDraw wrapper. |
| `render_video_system_initialize` | `0x00593F30` | high | Creates presentation state, canvases, conversion helpers, and software blend tables. |
| `render_video_system_shutdown` | `0x00594250` | high | Releases the main canvas and renderer lookup helpers before VideoSystem deletion. |
| `render_present_frame` | `0x005942D0` | high | Presents the completed canvas through the DirectDraw or window DC path. |
| `render_convert_rgb565_to_xrgb8888` | `0x005949A0` | high | Converts RGB565 pixels to 32-bit output with optional 2x nearest-neighbor scaling. |
| `render_scale_2x_u16` | `0x005950F0` | high | Doubles a 16-bit image in both axes with nearest-neighbor copies. |
| `render_scale_2x_u32` | `0x005953A0` | high | Doubles a 32-bit image in both axes with nearest-neighbor copies. |
| `render_fill_light_mask_rect` | `0x005B8B50` | high | Fills a clipped rectangle in the 8-bit world light-mask surface with one intensity value. |
| `render_light_bitmap_ctor` | `0x005B8C90` | high | Constructs the RTTI-backed LightBitmap and loads frame zero from mask1%02d.epf using the supplied selector. |
| `render_static_tile_cache_ctor` | `0x005BA660` | high | Constructs the static HPF image cache and stores the base or alternate art mode. |
| `render_get_static_tile_image` | `0x005BA8D0` | high | Resolves one animated static tile through the selected stc or sts resource path. |
| `render_set_static_tile_bank` | `0x005BAB10` | high | Selects base stc or alternate sts static art and clears the static image cache on change. |
| `render_snow_weather_session_ctor` | `0x005BD950` | high | Creates the snow weather session, selects pane blend mode 7, and starts its 100 ms timer. |
| `render_spawn_snow_particles` | `0x005BDB70` | high | Places snow particle panes across and above the world view. |
| `render_update_snow_particles` | `0x005BDDA0` | high | Moves snow particles down, removes those below the view, and spawns replacements. |
| `render_create_snow_overlay` | `0x005C82C0` | high | Replaces the current weather session with WeatherSession_SnowParticle. |
| `render_invalidate_light_mask_region` | `0x005C8450` | high | Accumulates a dirty light-mask rectangle and invalidates the matching WorldPane region. |
| `render_hea_decode_mask` | `0x005C8540` | high | Expands HEA run words into an 8-bit light or occlusion mask. |
| `render_build_world_light_mask` | `0x005C8760` | high | Builds the ambient or HEA base mask and, when enabled, merges light images attached to visible world objects. |
| `render_set_object_light_mask` | `0x005CCA80` | high | Attaches or removes a mask1%02d.epf LightBitmap for a world object ID and invalidates its affected region. |
| `render_invalidate_object_light_region` | `0x005CD000` | high | Resolves an object's attached LightBitmap bounds and invalidates that region while object-light merging is active. |
| `render_invalidate_removed_object_light_region` | `0x005CD200` | high | Invalidates the last bounds of a removed object's light image while the world light mask is active. |
| `render_build_static_objects` | `0x005CD730` | high | Builds WorldObject_Static instances from the two static tile IDs in visible map cells. |
| `render_world_pane_content` | `0x005CE280` | high | Advances the visual frame and draws the world into the WorldPane canvas. |
| `render_use_base_ground_bank` | `0x005D2B70` | high | Selects tilea.bmp for the ground cache. |
| `render_use_alternate_ground_bank` | `0x005D2B90` | high | Selects tileas.bmp with tilea.bmp fallback for the ground cache. |
| `render_world_set_blinded` | `0x005D2DC0` | high | Stores the world-renderer blinded boolean and schedules the affected view for redraw. |
| `render_world_object` | `0x005D3190` | high | Calls the WorldObject virtual draw method at primary vtable slot 0x18. |
| `render_world_layer_queue` | `0x005D31D0` | high | Walks one sorted queue of visible world objects. |
| `render_collect_world_objects` | `0x005D3740` | high | Clips visible objects, assigns ordinary layers to 32 draw queues, retains layer-zero objects in a separate late queue, records the self entry, and draws the ordinary queues without clearing them afterward. |
| `render_world_frame` | `0x005D3F70` | high | Draws ground, map backgrounds, and sorted world objects for one world frame. |
| `render_replay_layer_zero_and_self` | `0x005D4360` | high | After the ordinary world frame, draws the separate layer-zero queue and replays the recorded self entry; the normal non-blinded state supplies the selector that makes living sprites use blend mode 3. |
| `render_ground_layer` | `0x005D6A50` | high | Updates and draws the cached visible ground-tile layer. |
| `render_set_ground_bank` | `0x005D7410` | high | Stores the active ground-bank selector and clears the cached ground layer. |
| `render_ground_tile` | `0x005D7690` | high | Copies one decoded isometric tile diamond into the ground cache canvas. |
| `render_effect_object` | `0x005DD380` | high | Draws a world effect frame with its selected software blend mode. |
| `render_update_effect_frame` | `0x005DD470` | high | Advances a world effect through its Effect.tbl frame sequence. |
| `render_item_object_get_bounds` | `0x005DE5A0` | high | Returns the item's draw rectangle and its fixed -16 to +16 tile-relative bounds through WorldObject_Item primary-vtable slot 0x14. |
| `render_item_object` | `0x005DE620` | high | Draws a ground item and computes mode 3 for a nonzero fade selector, although the original final body blit reloads the ordinary object mode instead of consuming that local result. |
| `render_copy_human_appearance_record` | `0x005DEF70` | high | Rearranges the parser-friendly SDrawHumanObjects appearance fields into the stable 0x30-byte HumanAppearanceRecord741 used by world objects and image sessions. |
| `render_living_object` | `0x005DF950` | high | Draws a living sprite with normal, highlighted, or transparent state. |
| `render_human_apply_appearance` | `0x005E0070` | high | Copies the packet-owned appearance record and forwards it to the live human object. |
| `render_human_apply_appearance_record` | `0x005E00C0` | high | Copies HumanAppearanceRecord741 to WorldObject_Human +0xA4, derives nonblocking and translucent state, creates the 0x918-byte HumanObjectImageSession, and refreshes direction and motion. |
| `render_monster_apply_appearance` | `0x005E0370` | high | Resolves the untagged monster sprite, creates MonsterObjectImageSession, applies Direction and up to four palette selectors, and refreshes motion. |
| `render_static_object_ctor` | `0x005E42F0` | high | Stores the static tile ID, side, image cache, SOTP render flags, and draw state. |
| `render_static_object` | `0x005E47E0` | high | Draws a fixed world object with its SOTP-selected software blend mode. |
| `render_select_human_part_sprite` | `0x005FD8D0` | high | Selects the sprite ID for each of 21 human body and equipment categories; an overcoat suppresses ordinary pants, armor, and arms parts. |
| `render_format_human_part_filename` | `0x005FDA90` | high | Builds gendered human-part EPF filenames; body resource 5 resolves through MM005 or WM005 motion files. |
| `render_human_walk_sequence_ctor` | `0x005FFCD0` | high | Builds a four-step or eight-step human walk interpolation sequence from fixed pixel, frame, and per-step delay tables. |
| `render_human_stand_motion_data_ctor` | `0x006000D0` | high | Constructs standing-motion data and resolves up to 21 body and equipment sprite parts from HumanAppearanceRecord741. |
| `render_create_human_stand_motion_data` | `0x00600670` | high | Allocates the initial standing-motion data for a human image session. |
| `render_monster_image_session_ctor` | `0x006017C0` | high | Constructs the 0xE4-byte RTTI MonsterObjectImageSession and resolves standing, attack, and movement resources for the selected monster sprite. |
| `render_monster_apply_palette_selectors` | `0x00601A20` | high | Copies at most four resource-defined 16-byte palette mappings, replaces their selector fields from packet bytes, and enables mapped monster rendering. |
| `render_monster_select_motion_sequence` | `0x00601DD0` | high | Accepts motion IDs 0x01, 0x83, 0x84, and 0x85, selects one of three cached monster motion resources, and leaves the caller's duration unchanged. |
| `render_human_image_session_ctor` | `0x00602240` | high | Constructs the 0x918-byte RTTI-backed HumanObjectImageSession and retains HumanAppearanceRecord741 at object offset +0x0C. |
| `render_human_select_motion_sequence` | `0x00602A40` | high | Selects fixed, table-driven, or appearance-dependent human body motions; normal table motions replace the caller duration with 500, 1000, or 1500 ms. |
| `render_human_select_walk_sequence` | `0x00602CA0` | high | Selects the remote-human, local coarse, or local smooth walk sequence; ScrollLevel chooses four 114 ms steps or eight 57 ms steps for WorldObject_User. |
| `render_merge_light_mask_max` | `0x006036B0` | high | Merges a rectangular 8-bit light image into the viewport mask by retaining the greater value at each pixel. |

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
| `file_album_record_replace_pixels` | `0x00402E30` | high | Replaces one runtime record's compressed blob, inflates width times height times two bytes, and converts the canonical 16-bit pixels for the active renderer when required. |
| `file_album_ctor` | `0x00403010` | high | Installs the exact RTTI AlbumFile vtable and clears its initialized and record-pointer fields. |
| `file_album_create` | `0x00403070` | high | Creates an empty 100-record album, builds the per-character album.dat path, saves its initial file, and reloads it. |
| `file_album_load` | `0x004031D0` | high | Reads the 0x40-byte header, accepts capacities 1 through 100, reads 0x60 bytes per record, and inflates every active payload. |
| `file_album_save` | `0x004035A0` | high | Recomputes active payload offsets and rewrites the header, complete record table, and compressed pixel payloads when dirty. |
| `file_album_close` | `0x004037E0` | high | Releases the runtime record array and its per-record compressed and inflated buffers. |
| `file_album_add_portrait` | `0x00403850` | high | Uses the first inactive record, zlib-compresses the supplied 16-bit pixels, and optionally stores time(NULL) in the album header. |
| `file_album_move_portrait` | `0x004039E0` | high | Copies an active source record and caption into a destination slot, then clears the source and marks the album dirty. |
| `file_album_remove_portrait` | `0x00403B10` | high | Clears one checked active record and marks the album dirty. |
| `file_album_get_portrait` | `0x00403B90` | high | Returns one active record's inflated pixels and writes its width and height. |
| `file_album_get_caption` | `0x00403C20` | high | Returns the 0x4C-byte caption field for an active record. |
| `file_album_set_caption` | `0x00403C80` | high | Copies a bounded caption into an active record and marks the album dirty. |
| `file_album_build_path` | `0x00403CF0` | high | Builds .\&lt;character&gt;\album.dat in the AlbumFile path buffer. |
| `file_album_get_last_capture_time` | `0x00403D70` | high | Returns the time_t value serialized at album header offset 0x04. |
| `file_album_get_capacity` | `0x00403D90` | high | Returns the album header capacity, normally 100. |
| `file_album_set_last_capture_time` | `0x00403DB0` | high | Updates the time_t value serialized at album header offset 0x04. |
| `file_album_is_dirty` | `0x00403DD0` | high | Returns the AlbumFile rewrite-needed flag. |
| `file_hpf_decode` | `0x004319B0` | high | Checks magic 0xFF02AA55, decodes symbols through an adaptive tree, and accepts raw input when magic is absent. |
| `file_hpf_tree_initialize` | `0x00431B80` | high | Builds the complete initial tree for byte symbols and the 256 terminator. |
| `file_hpf_decode_symbol` | `0x00431C40` | high | Reads bits least-significant bit first and walks the active HPF tree to a symbol leaf. |
| `file_hpf_rotate_tree` | `0x00431D20` | high | Applies the parent and sibling rotations used after every decoded HPF symbol. |
| `file_load_color_table` | `0x0044CD50` | medium | Loads color.tbl records and packs six RGB triples per record for the renderer. |
| `file_open_efa` | `0x00456F30` | high | Opens an EFA resource and returns its u32 frame count from header +0x04 and u32 frame interval from header +0x08. |
| `file_decode_efa_frame` | `0x00457030` | high | Inflates one zlib payload from a 0x40-byte EFA frame record and builds an Image view. |
| `file_load_effect_frame_table` | `0x00458ED0` | high | Parses Effect.tbl decimal frame sequences into per-effect tables. |
| `file_archive_xor_words` | `0x00471DC0` | high | XORs a buffer in 32-bit words for the extended DAT header and index path. |
| `file_archive_open` | `0x00471E00` | high | Opens resource or loose DAT input and maps either the legacy index or the extended chunked index. |
| `file_archive_find_entry` | `0x00472470` | high | Looks up a named entry in an opened archive. |
| `file_archive_get_entry_data` | `0x00472900` | high | Returns the mapped data pointer for an archive entry. |
| `file_get_main_archive` | `0x00472C70` | high | Lazily constructs and returns the archive object opened as Legend.dat with DarkAges.dat fallback during startup. |
| `file_load_variant_color_table` | `0x0047DEB0` | medium | Loads one numbered color table family used by renderable assets. |
| `file_hea_build_row_views` | `0x00487380` | high | Builds row pointers from HEA band thresholds and lookup offsets for a clipped region. |
| `file_hea_open` | `0x004875B0` | high | Maps the HEA header, band array, row offsets, and packed run stream. |
| `file_read_image_metadata` | `0x0048B390` | high | Reads shared EPF metadata or dispatches SPF metadata parsing. |
| `file_load_image_frame` | `0x0048B530` | high | Loads one EPF or SPF frame for the shared image library. |
| `file_load_image_pixmap` | `0x0048BBC0` | high | Loads one image frame into a pixmap view and applies the EPF palette selector when required. |
| `file_decode_jpeg_to_rgb16` | `0x004A1840` | high | Uses bundled IJG version 62 to decode an in-memory JPEG to renderer-native 16-bit pixels and returns its width and height. |
| `file_write_jpeg_from_rgb16` | `0x004A1AF0` | high | Converts RGB555 or RGB565 source pixels to RGB triples and writes JFIF with IJG defaults: quality 75 and 4:2:0 sampling. |
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
| `file_load_npc_info_table` | `0x005322A0` | high | Loads the hierarchical npci.tbl name-to-illustration mapping from npcbase.dat. |
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
| `map_resize_cells` | `0x005B9030` | high | Stores new u16 width and height, resizes the contiguous six-byte cell array, clears every cell, and marks the map dirty. |
| `map_set_id` | `0x005B90D0` | high | Stores the u16 map number used for cache naming and validation. |
| `map_set_cell` | `0x005B90F0` | high | Bounds-checks one X, Y coordinate, stores ground and two static u16 tile IDs in the six-byte row-major map cell, and marks map storage dirty. |
| `map_update_crc16` | `0x005B9180` | high | Calculates and caches the custom CRC16 across six bytes for each map cell. |
| `map_get_left_static_tile` | `0x005B9370` | high | Returns the u16 left static tile ID at map-cell offset 2. |
| `map_get_right_static_tile` | `0x005B93E0` | high | Returns the u16 right static tile ID at map-cell offset 4. |
| `file_read_map_cells` | `0x005B9450` | high | Opens the cache for shared reading, reads the complete expected row-major map body into temporary storage, copies it only after a full read, and closes the handle immediately. |
| `file_ensure_maps_directory` | `0x005B9640` | high | Asks Windows to create the maps directory before a map cache read or write. |
| `file_format_map_path` | `0x005B9660` | high | Formats the path maps backslash lod map-id dot map. |
| `file_write_map_cells` | `0x005B9680` | high | Opens the cache with wb and no Windows sharing, writes the complete contiguous map array without checking the write count, then closes the exclusive handle. |
| `map_static_map_ctor` | `0x005BB720` | high | Builds the static-object spatial index, inserting each left map static with internal side 1 and each right map static with internal side 0. |
| `map_apply_seasonal_tile_mode` | `0x005C7660` | high | Applies the SMapSize 0x80 flag to both ground and static tile storage. |
| `map_load_hea_resource` | `0x005C7870` | high | Opens the current map ID as a six-digit HEA resource and enables the WorldPane spatial light mask on success. |
| `map_get_sotp_render_flags` | `0x005CF360` | high | Returns the high-nibble SOTP render flags for one static tile ID. |
| `map_load_sotp_render_flags` | `0x005CF3B0` | high | Loads SOTP.DAT into a one-based high-nibble render-flag table. |
| `map_get_sotp_collision_flags` | `0x005CF4A0` | high | Returns the low-nibble SOTP direction mask for one static tile ID. |
| `map_load_sotp_collision_flags` | `0x005CF4F0` | high | Loads SOTP.DAT into a one-based low-nibble collision table. |
| `map_get_collision_level` | `0x005CF5E0` | high | Retains the highest WorldObject +0x31 collision level at one map cell, with fully blocked static SOTP supplying level 1 when no dynamic level does. |
| `map_get_tile_pixels` | `0x005D7610` | high | Gets one decoded ground-tile diamond from MapTileImageLib. |
| `map_refresh_collision_cache` | `0x005D8B90` | high | Refreshes dirty cells in the map's width-by-height byte collision cache with map_get_collision_level. |
| `map_can_move_direction` | `0x005EFFE0` | high | Checks bounds, the saved appearance action lock, dynamic occupants, CreatureType behavior, and direction-specific SOTP masks for a proposed move. |
| `map_try_move_local_player` | `0x005F09E0` | high | Checks the saved appearance action lock, dynamic occupants, and direction-specific SOTP collision, selects the ScrollLevel-controlled local walk sequence, and sends CMove. |
| `map_apply_weather_mode` | `0x005F26C0` | high | Creates Snow for mode 1, performs no local setup for project-named Rain mode 2, and enables black ambient plus object light masks for Darkness mode 3. |
| `map_finish_transfer` | `0x005F2DE0` | high | Destroys MapLoadingPane, advances the WorldPane map generation, and either applies prepared map storage immediately or schedules the alternate completion path. |
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
| `maybe_app_configure_distribution_mode_12` | `0x00436A10` | medium | Dormant mode 12 handler with no matching marker return; sets connection flags without installing an endpoint. |
| `maybe_ui_manufacture_dialog_ctor_from_body` | `0x004C1AD0` | medium | Duplicates the lmanu.txt construction path and applies a decoded opcode-first body, but no live static caller was recovered. |
| `maybe_ui_manufacture_dialog_apply_manual_body` | `0x004C2990` | medium | Applies RecipeCount or Recipe from a decoded opcode-first body for the duplicate raw-body pane path. |

## Other

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `metadata_denied_item_list_ctor` | `0x004407C0` | high | Constructs exact RTTI class DeniedItemList, creates three empty lookup containers, and starts metadata subscription. |
| `metadata_denied_item_list_subscribe` | `0x00440AA0` | high | Registers BItems, BSkills, and BSpells with MetaTableManager and retries after 1000 ms when the manager is unavailable. |
| `metadata_denied_item_list_apply_table` | `0x00440B20` | high | Replaces the current denial lists and routes metadata rows tagged Item, Skill, or Spell into their lookup containers. |
| `metadata_denied_item_list_handle_event` | `0x00440E70` | high | Applies an available denial metadata table or retries the table subscriptions. |
| `light_list_ctor` | `0x004AE8D0` | high | Constructs the RTTI LightList singleton and starts loading its cached Light metadata. |
| `light_list_load_metadata` | `0x004AEA80` | high | Requests the Light metadata table when available or schedules a one-second retry. |
| `light_list_find_map_time_entry` | `0x004AEAD0` | high | Finds an inclusive map and time-range entry and returns ambient RGB, intensity, and whether HEA use is permitted. |
| `crc16_buffer` | `0x00568870` | high | Applies the custom CRC16 update to a byte buffer starting from zero. |
| `startup_run_pending_patcher` | `0x0057A330` | high | Before normal startup, requires both Patch/Info and Patch/Script to relaunch Patcher2.exe; otherwise deletes both markers and continues. |
| `crc16_update` | `0x005B8F30` | high | Updates the custom CRC16 with table[crc high byte] XOR crc shifted left XOR input byte. |
| `world_direction_to_delta` | `0x005BE580` | high | Maps directions 0 through 3 to up, right, down, and left coordinate deltas; values above 3 have no defined result. |
| `world_step_coordinates` | `0x005BE600` | high | Applies the direction delta to a coordinate pair used by local movement and collision checks. |
| `world_apply_map_cells` | `0x005C7970` | high | Installs prepared map-cell storage into WorldPane and dependent world views, rebuilds a ready view at its current position, and invalidates world and lighting output. |
| `world_rebuild_view_at_position` | `0x005C7DF0` | high | Stores WorldPane view Y and X, updates the world renderer, rebuilds visible static objects and lighting, and invalidates the view. |
| `world_insert_object` | `0x005C8EA0` | high | Inserts one reference-counted WorldObject into WorldObjectList, coordinate, render, and observer state. |
| `world_reindex_object` | `0x005C92C0` | high | Updates a world object's spatial index entry after its tile coordinates change and refreshes dependent overlay state. |
| `world_find_object_by_id` | `0x005C9810` | high | Resolves a 32-bit server entity ID through the WorldPane-owned WorldObjectList at object offset +0x194. |
| `world_find_object_at_tile_by_category` | `0x005C9880` | high | Searches one world tile for the first object whose broad category at +0x2C matches the requested value; B-key pickup requests category 8 ground items. |
| `world_get_static_object_at_tile_side` | `0x005C9DE0` | high | Resolves one of the two static slots at a coordinate and requires exact RTTI WorldObject_Static; packet side 0 maps to left slot 1 and nonzero maps to right slot 0. |
| `world_remove_object_by_id` | `0x005C9FA0` | high | Finds an existing world object by ID, optionally creates its removal replacement, and detaches the original from shared indexes. |
| `world_create_monster_object` | `0x005CA4C0` | high | Replaces a matching ID, allocates RTTI WorldObject_Monster, stores Y and X, inserts it, and retains the packet creature type. |
| `world_create_item_object` | `0x005CAC60` | high | Replaces a matching ID, allocates RTTI WorldObject_Item from ID, Y, X, untagged sprite, and dye, then inserts it. |
| `world_create_object_attached_effect` | `0x005CB590` | high | Finds an existing world object, constructs an RTTI WorldObject_ObjectEffect with the requested Effect.tbl index and timer, attaches it to the object, and inserts it into the world. |
| `world_create_static_effect` | `0x005CB960` | high | Bounds-checks tile Y and X, constructs an RTTI WorldObject_StaticEffect at that map cell, and inserts it into the world. |
| `world_create_moving_effect_between_objects` | `0x005CBBF0` | high | Resolves source and target world objects, converts their positions, constructs an RTTI WorldObject_MovingEffect path between them, and inserts it into the world. |
| `world_create_object_name_pane` | `0x005CC670` | high | Finds a world object by ID, constructs RTTI WorldObject_Name_Pane from bounded text and style bytes, and attaches it to the object. |
| `world_object_set_name_pane` | `0x005DBA80` | high | Replaces the reference-counted WorldObject_Name_Pane pointer at common WorldObject offset +0x58. |
| `world_effect_start_animation` | `0x005DD1C0` | high | Registers an ordinary world effect with the image pool, prefers the resource's nonzero frame interval over the packet fallback, and schedules its frame timer. |
| `world_object_effect_ctor` | `0x005DD620` | high | Constructs the exact RTTI WorldObject_ObjectEffect with an Effect.tbl resource index, fallback frame interval, and owning object's facing direction. |
| `world_static_effect_ctor` | `0x005DD6D0` | high | Constructs the exact RTTI WorldObject_StaticEffect and retains its tile Y and X coordinates. |
| `world_human_object_ctor` | `0x005DDFC0` | high | Constructs exact RTTI WorldObject_Human by calling world_living_object_ctor, installing the Human vtables, and selecting draw layer 7. |
| `world_item_object_ctor` | `0x005DE280` | high | Constructs the 0xB8-byte RTTI WorldObject_Item and retains entity ID, Y, X, untagged sprite, resource context, and dye color. |
| `world_living_object_ctor` | `0x005DF230` | high | Constructs the RTTI WorldObject_Living base, including clearing its +0xD4 nonblocking state. |
| `world_living_object_refresh_motion` | `0x005E0550` | medium | Clears one live motion flag, invokes the object's motion refresh virtual, and reapplies its current facing; SMove direction 4 uses this when positions already agree. |
| `world_living_start_move` | `0x005E0590` | high | Updates a living object's direction and destination, starts its image-session movement sequence, and publishes the movement event. |
| `world_living_start_move_animation` | `0x005E0610` | high | Starts the current image session's movement sequence and passes the local ScrollLevel boolean to its class-specific selector. |
| `world_living_start_motion` | `0x005E0750` | high | Stores the facing direction, asks the current image session to select a body motion, and schedules its timer using the selector's final duration in milliseconds. |
| `world_living_object_set_direction` | `0x005E0880` | high | When facing changes, invokes the living-object transition hook, stores direction at +0x192, and refreshes the directional motion or image state. |
| `world_living_handle_timer_event` | `0x005E1800` | high | For motion timer 0x02000001, advances the living animation only when the scheduled generation matches the current motion, so an older timer cannot interrupt a newer motion. |
| `world_monster_object_ctor` | `0x005E2630` | high | Constructs the 0x1F0-byte RTTI WorldObject_Monster, retains creature_type at +0x1EC, and selects a type-dependent common collision level. |
| `world_moving_effect_ctor` | `0x005E2770` | high | Constructs the exact RTTI WorldObject_MovingEffect and builds its client-timed path between source and target world positions. |
| `world_moving_effect_start` | `0x005E3710` | high | Schedules a moving effect's path timer using the step interval computed from client effect data. |
| `world_static_set_tile_id` | `0x005E4900` | high | Writes the WorldObject_Static live tile ID, reloads its static image and bounds, and invalidates the object for drawing. |
| `world_static_handle_state_transition_message` | `0x005E4A30` | high | Handles scheduled message 0x01000001 by advancing the static state transition. |
| `world_static_transition_to_pair_column_1` | `0x005E4B20` | high | Finds the live tile ID in the 66-row pair table and starts a transition toward column 1. |
| `world_static_transition_to_pair_column_0` | `0x005E4BD0` | high | Finds the live tile ID in the 66-row pair table and starts a transition toward column 0. |
| `world_static_advance_state_transition` | `0x005E4C80` | high | Moves the pair column toward its requested endpoint, applies that tile ID, and reschedules after 150 ms only if another step remains. |
| `world_user_start_move` | `0x005E4FC0` | high | Refreshes WorldObject_User appearance state, then starts the common living-object move with the supplied ScrollLevel flag. |
| `world_object_list_insert` | `0x005E5D40` | high | Inserts an object into its 0x60-byte coordinate cell and the ordered entity-ID index, then marks WorldObject +0x48 inserted. |
| `world_object_list_find_by_id` | `0x005E73B0` | high | Searches the ordered ID tree beginning at WorldObjectList +0x1C and returns the reference-counted object pointer from node +0x10. |
| `world_set_view_position` | `0x005EEC70` | high | Publishes a Y, X world-view position and optionally rebuilds the visible world and camera state around it. |
| `world_get_self_user_object` | `0x005EEDB0` | high | Looks up the saved self object ID and RTTI-casts the result to WorldObject_User. |
| `world_update_map_lighting` | `0x005EF360` | high | Scales the stored SChangeHour time step, resolves the current map's Light metadata, updates ambient color and intensity, and conditionally loads its HEA mask. |
| `world_get_static_tile_id_from_object` | `0x005EFEC0` | high | Requires WorldObject_Static and returns its current live tile ID for the movement collision path. |
| `session_world_user_func_ctor` | `0x005FC5F0` | high | Constructs exact RTTI class WorldUserFunc and clears its fixed inventory, spell, and skill arrays. |
| `session_find_first_empty_inventory_slot` | `0x005FC900` | high | Returns the first absent inventory record in slots 1 through 60, or 0 when every slot is occupied. |
| `session_store_inventory_entry` | `0x005FCBB0` | high | Stores one compact 0x106-byte inventory record at WorldUserFunc + 0x1092 + (slot - 1) * 0x106. |
| `session_clear_inventory_entry` | `0x005FCC10` | high | Clears an inventory record's present flag, sprite, and name[0] without overwriting its dye byte or remaining name bytes. |
| `session_store_spell_entry` | `0x005FCC50` | high | Stores one 0x206-byte spell record at WorldUserFunc + 0x4DFA + (slot - 1) * 0x206. |
| `session_clear_spell_entry` | `0x005FCCD0` | high | Clears a spell record's present flag, argument type, name[0], and prompt[0] without overwriting the icon or remaining string bytes. |
| `session_store_skill_entry` | `0x005FCD20` | high | Stores one 0x104-byte skill record at WorldUserFunc + 0x10210 + (slot - 1) * 0x104. |
| `session_clear_skill_entry` | `0x005FCD80` | high | Clears a skill record's present flag and name[0] without overwriting its icon or remaining name bytes. |
| `session_update_from_status_packet` | `0x005FCFD0` | high | Copies present SStatus privilege, core stats, vitals, total experience, gold, weight, and retained unknown bytes into WorldUserFunc. |
| `session_add_inventory_from_packet` | `0x005FD1C0` | high | Accepts SAddInventory slots 1 through 60 and stores sprite, dye color, and name in the compact WorldUserFunc record. |
| `session_remove_inventory_from_packet` | `0x005FD220` | high | Accepts SRemoveInventory slots 1 through 60 and logically clears the matching WorldUserFunc record. |
| `session_add_spell_from_packet` | `0x005FD260` | high | Accepts SAddSpell slots 1 through 89 and argument types 1 through 8 before updating WorldUserFunc spell storage. |
| `session_remove_spell_from_packet` | `0x005FD2E0` | high | Accepts SRemoveSpell slots 1 through 89 before clearing the matching WorldUserFunc spell record. |
| `session_add_skill_from_packet` | `0x005FD320` | high | Accepts SAddSkill slots 1 through 89 before storing the icon and name in WorldUserFunc. |
| `session_remove_skill_from_packet` | `0x005FD370` | high | Accepts SRemoveSkill slots 1 through 89 before clearing the matching WorldUserFunc skill record. |
| `session_update_from_user_appearance_packet` | `0x005FD3B0` | high | Stores user ID, cached facing, raw guild value, character class, final unknown byte, and action state &amp; 0x7F; bit 0 locks movement and actions, while wire bit 0x80 suppresses the other field updates. |
| `crc32_update` | `0x00604530` | high | Standard reflected IEEE CRC32 update with initial and final inversion. |
| `crt_time` | `0x00622873` | high | Reads the current Windows FILETIME and converts it to Unix-epoch seconds; CLogin passes the result to crt_srand. |
| `crt_srand` | `0x006275DE` | high | Stores the seed used by the client runtime random-number state. |
| `crt_rand` | `0x006275F0` | high | Implements the Microsoft runtime linear-congruential update and returns a 15-bit value. |
