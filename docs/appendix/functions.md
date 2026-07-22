# Function reference

This appendix is the address book for functions named in the main text. Static addresses assume preferred image base `0x00400000`. At runtime, use the loaded module base and the matching RVA.

Roles are short summaries from the checked-in Binary Ninja YAML exports. Those exports remain the source for full evidence and provenance.

## Application lifecycle and configuration

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `app_detect_bad_guy_marker` | `0x00431ED0` | high | Reconstructs %SystemRoot%\System32\Mscfg.dll and sets config +0x668 from file existence alone. |
| `app_config_ctor` | `0x00431FF0` | high | Constructs Config, loads Darkages.cfg, selects a distribution mode, and dispatches endpoint initialization. |
| `app_save_config` | `0x00432340` | high | Writes Darkages.cfg in text mode. |
| `app_load_config_file` | `0x00432660` | high | Loads the versioned Darkages.cfg text fields, endpoint table, input mode, animation flag, and gated audio/game options. |
| `app_set_default_config` | `0x00432D60` | high | Installs distribution-specific endpoint defaults, input settings, fonts, animation, and level-3 audio defaults. |
| `app_configure_unitel_distribution` | `0x00433B40` | high | Empty dormant mode 2 initializer selected by Unitel.nfo in the unreferenced marker scanner. |
| `app_get_distribution_mode` | `0x00434EB0` | high | Caches and returns the distribution mode selected by app_select_distribution_mode. |
| `app_select_distribution_mode` | `0x00434EF0` | high | Returns the constant distribution mode 1 in this target. |
| `app_detect_distribution_mode_from_markers` | `0x00434F00` | high | Dormant unreferenced scanner that maps country and Korean ISP .nfo markers to distribution modes 1 through 15. |
| `app_derive_installation_id16` | `0x00436E10` | high | Applies the client's custom 0x1021-table recurrence to the four little-endian bytes of the persistent 32-bit installation ID. |
| `app_config_scalar_deleting_dtor` | `0x00436EF0` | high | Compiler scalar-deleting destructor for Config. |
| `app_config_singleton_register` | `0x00437930` | high | Registers the Config singleton. |
| `app_config_singleton_unregister` | `0x00437970` | high | Clears the Config singleton when the supplied instance owns it. |
| `app_context_dumper_from_thread_ctor` | `0x00437A40` | high | Constructs exact RTTI ContextDumper by capturing a thread CONTEXT and immediately collects bounded trace text. |
| `app_context_dumper_from_context_ctor` | `0x00437BB0` | high | Constructs exact RTTI ContextDumper from a supplied x86 CONTEXT and immediately collects bounded trace text. |
| `app_collect_stack_trace_text` | `0x00437D70` | high | Collects StackWalker frames into the bounded 8192-byte LCrash.nfo trace buffer with newline separators. |
| `app_exception_handler_ctor` | `0x00468AD0` | high | Constructs exact RTTI ExceptionHandler, installs app_unhandled_exception_filter, and retains the previous top-level filter. |
| `app_exception_handler_dtor` | `0x00468B10` | high | Restores the previous Win32 unhandled exception filter and clears the ExceptionHandler singleton. |
| `app_unhandled_exception_filter` | `0x00468EB0` | high | Top-level Win32 exception filter that writes LCrash.nfo and then chains to the previously installed filter. |
| `app_write_unhandled_exception_report` | `0x00468F00` | high | Writes LCrash.nfo as build/distribution text plus raw CS:EIP frames produced from EXCEPTION_POINTERS. |
| `app_get_exception_code_name` | `0x004690A0` | high | Maps common Win32 exception codes to names or formats an NTDLL fallback; the active LCrash writer discards the returned name. |
| `app_resolve_fault_module_section` | `0x00469390` | high | Uses VirtualQuery and PE section headers to resolve the fault address to module, section index, and offset; the active writer does not serialize the results. |
| `app_get_exception_handler` | `0x00469550` | high | Returns the application-wide ExceptionHandler singleton used by the filter, uploader, and live diagnostic builder. |
| `app_language_mode_from_distribution` | `0x004A49B0` | high | Maps distribution modes to Korean 0, English 1, Japanese 2, or Taiwan 3 language modes. |
| `app_get_text_code_page` | `0x004A4A30` | high | Returns the code-page value selected with the current language mode. |
| `app_get_language_message_label` | `0x004A4A60` | high | Maps language modes to msgkor.h, msgeng.h, msgjpn.h, or msgtai.h labels retained by the client. |
| `app_set_language_mode` | `0x004A4CE0` | high | Stores the language mode, selects the retained message label, and records code page 949 or 932 for Korean or Japanese. |
| `app_check_speedhack_clocks` | `0x004A98A0` | high | Compares several local time sources, counts differences greater than five seconds, and sends one SpeedHack CException report per process after repeated mismatches. |
| `app_shutdown` | `0x004AC060` | high | Tears down runtime managers and panes, then closes and destroys the DAT archive singletons before window cleanup. |
| `app_set_post_exit_advertisement` | `0x004ACE00` | high | Copies the SAdvertisement string into a 65,536-byte application buffer, terminates it, and saves its length plus three numeric arguments for app_winmain. |
| `app_is_japan_distribution_mode` | `0x004ACEE0` | high | Returns true when app_get_distribution_mode reports mode 13, selecting the create-user email and ISP-selector variant. |
| `app_set_working_directory_from_executable` | `0x004AD3A0` | high | Derives the executable directory from GetCommandLineA and makes it the process working directory. |
| `app_write_patch_info_and_launch_patcher` | `0x00528610` | high | Creates Patch/Info, writes the fixed handoff structure, launches Patcher2.exe without arguments, and exits the client. |
| `app_quit_after_patcher_launch` | `0x005287B0` | high | Destroys NewPatchPane, posts WM_QUIT, and terminates after the patcher launch attempt. |
| `app_stack_walker_from_thread_ctor` | `0x0056D4E0` | high | Constructs exact RTTI StackWalker and captures the supplied thread or current thread into an x86 CONTEXT. |
| `app_stack_walker_from_context_ctor` | `0x0056D540` | high | Constructs exact RTTI StackWalker and copies the supplied 0x2CC-byte x86 CONTEXT. |
| `app_stack_walker_format_next_frame` | `0x0056D660` | high | Calls DbgHelp StackWalk for IMAGE_FILE_MACHINE_I386 and formats flags-1 output as raw CS:EIP text. |
| `app_handle_d_option_stub` | `0x0057A460` | high | Empty function called for the suffix of an uppercase -D command-line token. |
| `app_parse_command_line` | `0x0057A550` | high | Scans the WinMain command tail for space-delimited dash tokens and recognizes only uppercase D. |
| `app_winmain` | `0x0057A710` | high | Called by the CRT startup wrapper with the WinMain argument set. |

## Game loop

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `event_dispatcher_tick` | `0x00464180` | high | Drains queued events, samples timeGetTime for ordered due timers, yields 5 ms when the next timer is more than 20 ms away, and invokes at most 0x28 due callbacks. |
| `app_window_proc` | `0x004A9C30` | high | Window procedure that sends messages through the input translator before application-specific handling. |
| `app_run_message_loop` | `0x004AC750` | high | Records the main thread, drains PeekMessageA, runs the EventDispatcher tick, performs an auxiliary clock check after more than 100 ms, and yields 1 ms after 402 tight passes. |

## Events

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `event_get_dispatcher` | `0x0041AE80` | high | Returns event_dispatcher_singleton_ptr. |
| `event_intro_video_frame_timer` | `0x0042E600` | high | Advances the two clips and posts intro state 2 when playback finishes. |
| `event_dispatcher_ctor` | `0x00463820` | high | Constructs the 0x1BC-byte EventDispatcher, queue, timer list, packet factory, capture state, and EventHandlerList. |
| `event_allocate_or_reuse` | `0x00463C40` | high | Returns a pooled Event pointer from EventDispatcher +0x28 when available, otherwise allocates 0xA8 bytes and calls event_ctor. |
| `event_recycle` | `0x00463CF0` | high | Returns an Event pointer to the separate pool at EventDispatcher +0x28 without using an intrusive Event field. |
| `event_queue_push_copy` | `0x00463D10` | high | Copies exactly 0xA8 event bytes into the synchronized pointer queue. |
| `event_queue_pop_copy` | `0x00463D60` | high | Removes one queued event and copies exactly 0xA8 bytes to the caller. |
| `event_register_pane` | `0x00463E40` | high | Sets Pane +0x188 bit 0x02 and inserts the pane through EventHandlerList. |
| `event_unregister_pane` | `0x00463E80` | high | Clears Pane +0x188 bit 0x02 and removes the pane subtree from EventHandlerList. |
| `event_enqueue` | `0x00463F50` | high | Thin synchronized queue wrapper used when an event originates off the main thread. |
| `event_dispatch_immediate` | `0x00463F70` | high | Validates and centrally dispatches an Event, then performs family-specific owned-payload cleanup. |
| `event_arm_hidden_keyboard_sequence` | `0x00464120` | high | Arms a ten-second keyboard-sequence reader for literal nim@wmfRpa and a later wake timer; no static caller is present in this build. |
| `event_dispatcher_tick_virtual` | `0x00464430` | high | Calls EventDispatcher primary-vtable +0x08, which resolves to event_dispatcher_tick. |
| `event_register_pane_internal` | `0x00464450` | high | Calls EventHandlerList virtual insert and refreshes dispatcher state. |
| `event_unregister_pane_internal` | `0x004644B0` | high | Calls EventHandlerList virtual subtree removal and refreshes dispatcher state. |
| `event_schedule_timer` | `0x00464520` | high | Inserts a five-dword TimerHandler entry ordered by due time, using the dispatcher sample, a fresh timeGetTime value, or the current callback's due time as its scheduling base. |
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
| `event_ctor` | `0x00466680` | high | Calls lobject_ctor, installs the RTTI-backed Event vtable, and initializes the signed type byte at +0x0C to -1; +0x08 remains untouched. |
| `event_dtor` | `0x004666B0` | high | Restores the Event vtable, resets signed type to -1, and calls lobject_dtor, which clears the live cookie. |
| `event_is_pointer` | `0x004666E0` | high | Returns true for event types 0x00 through 0x07. |
| `event_is_keyboard_or_text` | `0x00466720` | high | Returns true for event types 0x08 through 0x0C. |
| `event_is_network` | `0x00466760` | high | Returns true only for event type 0x13. |
| `event_is_application` | `0x004667A0` | high | Returns true for event types 0x0D through 0x12. |
| `event_dispatch_or_queue` | `0x004670F0` | high | Dispatches on app_main_thread_id and copies the Event into the queue from any other thread. |
| `event_scalar_deleting_dtor` | `0x004689D0` | high | Calls event_dtor and frees the Event when the MSVC deleting-destructor flag requests it. |
| `event_handle_intro_state` | `0x004ACA50` | high | Dispatches intro states 0, 1, and 2 around Bink playback. |

## Input

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `input_get_event_manager` | `0x00427380` | high | Returns input_event_manager_singleton_ptr. |
| `input_set_capture_pane` | `0x00464780` | high | Stores EventDispatcher +0x40 and calls SetCapture or ReleaseCapture on the main window. |
| `input_event_manager_ctor` | `0x004667E0` | high | Constructs RTTI EventMan state, key tables, pointer state, a client-owned 1,000 ms double-click window, and the socket object. |
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
| `input_emit_left_button_down` | `0x004673F0` | high | Builds type 0x01 or synthesized double-click type 0x02; a match requires the same saved button, less than 1,000 ms, and Manhattan distance at most two logical pixels. |
| `input_emit_left_button_up` | `0x00467680` | high | Builds pointer event type 0x03 and clears the left-held flag. |
| `input_emit_right_button_down` | `0x00467790` | high | Builds type 0x04 or synthesized double-click type 0x05 using the same client-owned time and distance thresholds as the left path. |
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
| `ui_agreement_dialog_pane_dtor` | `0x00402860` | high | Destroys the exact RTTI AgreementDialogPane, unregisters it from pane events and its singleton, then runs the DialogPane base destructor. |
| `ui_agreement_dialog_handle_action` | `0x004028F0` | high | Action 0 closes and unregisters the agreement pane without sending a packet. |
| `ui_agreement_dialog_handle_keyboard_event` | `0x004029F0` | high | AgreementDialogPane's keyboard-event override delegates directly to the DialogPane implementation. |
| `ui_agreement_dialog_pane_scalar_deleting_dtor` | `0x00402A10` | high | Runs the AgreementDialogPane destructor and conditionally frees the complete object for the scalar-deleting-destructor vtable slot. |
| `ui_agreement_dialog_register_singleton` | `0x00402A40` | high | Registers the complete AgreementDialogPane pointer from its Singleton subobject at object offset 0x630. |
| `ui_agreement_dialog_unregister_singleton` | `0x00402A80` | high | Clears the AgreementDialogPane singleton only when it still refers to the complete object derived from the 0x630 secondary base. |
| `ui_get_layout_manager` | `0x00402AC0` | high | Returns the global layout manager used by pane constructors and named-control lookup helpers. |
| `ui_agreement_dialog_pane_timer_deleting_dtor_thunk` | `0x00402AD0` | high | Adjusts the TimerHandler secondary-base pointer by -0x11C and tail-calls the AgreementDialogPane scalar deleting destructor. |
| `ui_alpha_screen_pane_ctor` | `0x00403E90` | high | Constructs the exact RTTI AlphaScreenPane over Pane and selects its palette-resolved fill color. |
| `ui_alpha_screen_pane_dtor` | `0x00403F20` | high | Releases AlphaScreenPane's retained child-pointer array, then runs the Pane base destructor. |
| `ui_alpha_screen_pane_draw_content` | `0x00403FC0` | high | Fills the AlphaScreenPane content rectangle with its selected Canvas color. |
| `ui_alpha_screen_pane_rebuild_gradient_mask` | `0x00403FE0` | high | Rebuilds AlphaScreenPane's per-column alpha-mask buffers from the pane bounds and fills them with the configured gradient. |
| `ui_segmented_alpha_screen_pane_ctor` | `0x00404110` | high | Constructs exact RTTI AlphaScreenPaneSegmented and creates 33 colored child panes with linearly stepped pane values. |
| `ui_segmented_alpha_screen_pane_dtor` | `0x00404260` | high | Destroys all 33 child panes, then runs the Pane base destructor for AlphaScreenPaneSegmented. |
| `ui_segmented_alpha_screen_pane_register_screen` | `0x00404300` | high | Registers the parent, divides its rectangle into 33 vertical child strips, registers each child, and clears each child canvas with the shared color. |
| `ui_segmented_alpha_screen_pane_unregister_screen` | `0x00404440` | high | Unregisters all 33 child strips before unregistering the AlphaScreenPaneSegmented parent. |
| `ui_alpha_screen_pane_scalar_deleting_dtor` | `0x004044A0` | high | Runs the AlphaScreenPane destructor and conditionally frees the complete object. |
| `ui_segmented_alpha_screen_pane_scalar_deleting_dtor` | `0x004044D0` | high | Runs the AlphaScreenPaneSegmented destructor and conditionally frees the complete object. |
| `ui_alpha_screen_pane_timer_deleting_dtor_thunk` | `0x00404500` | high | Adjusts a TimerHandler secondary-base pointer by -0x11C and tail-calls the AlphaScreenPane scalar deleting destructor. |
| `ui_segmented_alpha_screen_pane_timer_deleting_dtor_thunk` | `0x00404510` | high | Adjusts a TimerHandler secondary-base pointer by -0x11C and tail-calls the AlphaScreenPaneSegmented scalar deleting destructor. |
| `ui_animation_pane_ctor` | `0x00404590` | high | Constructs exact RTTI AnimationPane, clears its playing state, and marks it uninitialized until an image is loaded. |
| `ui_animation_pane_load` | `0x004045E0` | high | Stops prior playback, stores the image and palette settings, reads image dimensions and frame count, selects the starting frame, and registers the pane rectangle. |
| `ui_animation_pane_start` | `0x00404750` | high | Starts an initialized idle AnimationPane at frame zero and schedules timer ID 0. |
| `ui_animation_pane_stop` | `0x004047B0` | high | Cancels this pane's timers, restores its configured starting frame, clears the playing state, and invalidates the pane. |
| `ui_animation_pane_timer_callback` | `0x00404840` | high | Handles timer ID 0, advances the frame modulo frame_count while active, invalidates the pane, and requeues the stored interval. |
| `ui_animation_pane_draw_content` | `0x004048F0` | high | Loads the current image frame and blits it into the AnimationPane canvas when initialized and in range. |
| `ui_animation_pane_scalar_deleting_dtor` | `0x004049D0` | high | Runs the Pane base destructor for AnimationPane and conditionally frees the complete object. |
| `ui_animation_pane_timer_deleting_dtor_thunk` | `0x00404A10` | high | Adjusts a TimerHandler secondary-base pointer by -0x11C and tail-calls the AnimationPane scalar deleting destructor. |
| `ui_background_story_pane_ctor` | `0x00414720` | high | Constructs exact RTTI BkStoryPane as a full-screen Pane, registers it, starts a 150 ms timer, and hides the cursor. |
| `ui_background_story_pane_dtor` | `0x00414860` | high | Restores both BkStoryPane vtables and runs the Pane base destructor. |
| `ui_background_story_pane_handle_pointer_event` | `0x00414890` | high | Consumes pointer events and advances the story on event subtype 3 while a page is active. |
| `ui_background_story_pane_handle_keyboard_event` | `0x004149A0` | high | Consumes keyboard events; Enter and Space advance the story and Escape closes the pane. |
| `ui_background_story_pane_draw_content` | `0x00414AE0` | high | Primary-vtable content hook at slot +0x5C that draws the active story stage until stage 7. |
| `ui_background_story_pane_close` | `0x00414B10` | high | Restores the palette and cursor, unregisters BkStoryPane, and destroys it through the normal pane path. |
| `ui_background_story_pane_draw_page` | `0x00414BC0` | high | Loads the stage-specific background palette and EPF, draws the page, and renders the currently revealed story lines. |
| `ui_background_story_pane_draw_story_line` | `0x00414E60` | high | Selects text color and position, then draws one buffered background-story line to the pane canvas. |
| `ui_background_story_pane_timer_callback` | `0x00414ED0` | high | Advances the visible story-line count, invalidates the pane, and requeues timer ID 0 after 150 ms. |
| `ui_background_story_pane_read_next_page` | `0x00414F60` | high | Reads the current story1.tbl through story7.tbl stream into fixed line buffers and returns page or stage termination state. |
| `ui_staff_pane_ctor` | `0x004151D0` | high | Constructs exact RTTI StaffPane, registers it full-screen, starts a 20 ms timer, loads staff text, hides the cursor, and loads staff.epf. |
| `ui_staff_pane_dtor` | `0x00415320` | high | Restores both StaffPane vtables and runs the Pane base destructor. |
| `ui_staff_pane_handle_pointer_event` | `0x00415350` | high | Consumes pointer events and closes StaffPane on event subtype 3. |
| `ui_staff_pane_handle_keyboard_event` | `0x004153A0` | high | Consumes keyboard events and closes StaffPane when Escape is pressed. |
| `ui_staff_pane_draw_content` | `0x004153F0` | high | Primary-vtable content hook at slot +0x5C that draws staff.epf and the currently scrolling staff lines. |
| `ui_staff_pane_close` | `0x004154C0` | high | Restores the palette and cursor, unregisters StaffPane, and queues it through the BlackHole deferred-deletion owner. |
| `ui_staff_pane_draw_line` | `0x00415530` | high | Selects text color and scroll-relative position, then draws one buffered staff line. |
| `ui_staff_pane_timer_callback` | `0x004155C0` | high | Advances the 20 ms staff animation and closes the pane when the loaded frame count is reached. |
| `ui_staff_pane_load_text` | `0x00415680` | high | Reads DBCS-aware lines from staff.tbl in the archive into fixed 40-byte pane buffers. |
| `ui_background_story_pane_scalar_deleting_dtor` | `0x00415890` | high | Runs the BkStoryPane destructor and conditionally frees the complete object. |
| `ui_staff_pane_scalar_deleting_dtor` | `0x004158C0` | high | Runs the StaffPane destructor and conditionally frees the complete object. |
| `ui_staff_pane_timer_deleting_dtor_thunk` | `0x004158F0` | high | Adjusts a TimerHandler secondary-base pointer by -0x11C and tail-calls the StaffPane scalar deleting destructor. |
| `ui_background_story_pane_timer_deleting_dtor_thunk` | `0x00415900` | high | Adjusts a TimerHandler secondary-base pointer by -0x11C and tail-calls the BkStoryPane scalar deleting destructor. |
| `ui_browser_dialog_ctor` | `0x00415CB0` | high | Constructs exact RTTI BrowserDialogPane with an embedded BrowserControlPane; when no response or initial URL is supplied, sends CWebBoard action 0. |
| `ui_browser_dialog_dtor` | `0x00416020` | high | Destroys exact RTTI BrowserDialogPane, clears its singleton pointer, and runs the DialogPane base destructor. |
| `ui_browser_dialog_apply_web_board_raw_buffer` | `0x00416140` | medium | Unreferenced alternate SWebBoard path that parses three byte-length strings from a raw buffer, installs domain and boardinfo cookies, saves the base URL, and navigates. |
| `ui_browser_dialog_apply_web_board` | `0x004165A0` | high | Accepts SWebBoard actions 0 and 1, installs domain and boardinfo WinINet cookies, sets the embedded browser base URL, and navigates to start_url. |
| `ui_browser_dialog_close` | `0x00416990` | high | Unregisters and detaches BrowserDialogPane, shuts down its embedded browser control, and queues the pane for deferred deletion. |
| `ui_browser_dialog_handle_keyboard_event` | `0x00416A10` | high | Consumes BrowserDialogPane's close-key event byte 0x90 and delegates all other keyboard events to the base dialog handler. |
| `ui_browser_dialog_handle_network_event` | `0x00416A50` | high | BrowserDialogPane's network-event handler dispatches exact RTTI SWebBoard opcode 0x62 to its cookie and navigation path. |
| `ui_browser_dialog_handle_timer` | `0x00416AB0` | high | Timer 0x572 opens Web Board Request Timeout after 20 seconds and closes the waiting BrowserDialogPane. |
| `ui_browser_control_ctor` | `0x00416C90` | high | Constructs exact RTTI BrowserControlPane, creates its child HWND and WebBrowser ActiveX object, installs the COM client interfaces, and optionally navigates. |
| `ui_browser_control_dtor` | `0x004172E0` | high | Destroys BrowserControlPane's ControlPane, TimerHandler, and COM-interface subobjects after releasing the embedded browser and child-window wrapper. |
| `ui_browser_control_shutdown` | `0x004173C0` | high | Hides the browser, removes its event advisory connection, releases the WebBrowser object, destroys the child HWND, and restores focus. |
| `ui_browser_control_register_screen` | `0x00417530` | high | Registers BrowserControlPane as a screen and moves its embedded child HWND to the pane rectangle. |
| `ui_browser_control_capture_window` | `0x004175B0` | high | Copies the visible browser child window into a supplied destination DC with BitBlt; screenshot capture calls this helper. |
| `ui_browser_control_draw_content` | `0x00417710` | high | Draws centered browser status text into the pane canvas while the embedded child window is hidden. |
| `ui_browser_control_set_visible` | `0x004177D0` | high | Shows or hides the browser child HWND and synchronizes cursor state and the browser message filter. |
| `ui_browser_control_set_3d_border_enabled` | `0x004178C0` | high | Controls whether IDocHostUIHandler adds DOCHOSTUIFLAG_NO3DBORDER, then refreshes IWebBrowser so the host flags are applied. |
| `ui_browser_control_set_base_url` | `0x00417910` | high | Copies a bounded base URL into BrowserControlPane's browser state. |
| `ui_browser_control_set_navigation_timeout_ms` | `0x00417960` | high | Sets BrowserControlPane's navigation-timeout interval in milliseconds and cancels the active timeout event when set to zero. |
| `ui_browser_control_set_status_text` | `0x004179F0` | high | Copies or clears BrowserControlPane's bounded status text and invalidates the pane for redraw. |
| `ui_browser_control_navigate` | `0x00417A40` | high | Converts the URL and optional header to BSTR values and calls the embedded IWebBrowser navigation method. |
| `ui_browser_control_navigate_exception_cleanup` | `0x00417C03` | high | Releases navigation SAFEARRAY and BSTR temporaries, shuts down the embedded browser, and clears exception state. |
| `ui_browser_control_get_document_cookie` | `0x00417C70` | high | Queries the browser Document interface, reads its cookie BSTR, and converts it into the client's string representation. |
| `ui_browser_control_set_document_cookie` | `0x00417DF0` | high | Queries the browser Document interface and assigns a formatted name=value cookie BSTR. |
| `ui_browser_control_query_interface` | `0x00417F00` | high | BrowserControlPane COM QueryInterface implementation that returns the adjusted subobject for each supported IID. |
| `ui_browser_control_ole_client_site_add_ref` | `0x00418110` | high | IOleClientSite AddRef vtable entry; this embedded site uses a fixed reference count and returns 2. |
| `ui_browser_control_ole_client_site_release` | `0x00418120` | high | IOleClientSite Release vtable entry; this embedded site uses a fixed reference count and returns 1. |
| `ui_browser_control_ole_client_site_save_object` | `0x00418130` | high | IOleClientSite SaveObject vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_client_site_get_moniker` | `0x00418140` | high | IOleClientSite GetMoniker vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_client_site_get_container` | `0x00418150` | high | IOleClientSite GetContainer vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_client_site_show_object` | `0x00418160` | high | IOleClientSite ShowObject vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_client_site_on_show_window` | `0x00418170` | high | IOleClientSite OnShowWindow vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_client_site_request_new_object_layout` | `0x00418180` | high | IOleClientSite RequestNewObjectLayout vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_in_place_site_get_window` | `0x00418190` | high | IOleInPlaceSite GetWindow vtable entry that returns BrowserControlPane's child HWND. |
| `ui_browser_control_ole_in_place_site_context_sensitive_help` | `0x004181B0` | high | IOleInPlaceSite ContextSensitiveHelp vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_in_place_site_can_in_place_activate` | `0x004181C0` | high | IOleInPlaceSite CanInPlaceActivate vtable entry that returns S_OK. |
| `ui_browser_control_ole_in_place_site_on_in_place_activate` | `0x004181D0` | high | IOleInPlaceSite OnInPlaceActivate vtable entry that returns S_OK. |
| `ui_browser_control_ole_in_place_site_on_ui_activate` | `0x004181E0` | high | IOleInPlaceSite OnUIActivate vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_in_place_site_get_window_context` | `0x004181F0` | high | IOleInPlaceSite GetWindowContext vtable entry that supplies the child HWND client rectangle as position and clip bounds. |
| `ui_browser_control_ole_in_place_site_scroll` | `0x00418220` | high | IOleInPlaceSite Scroll vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_in_place_site_on_ui_deactivate` | `0x00418230` | high | IOleInPlaceSite OnUIDeactivate vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_in_place_site_on_in_place_deactivate` | `0x00418240` | high | IOleInPlaceSite OnInPlaceDeactivate vtable entry that returns S_OK. |
| `ui_browser_control_ole_in_place_site_discard_undo_state` | `0x00418250` | high | IOleInPlaceSite DiscardUndoState vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_in_place_site_deactivate_and_undo` | `0x00418260` | high | IOleInPlaceSite DeactivateAndUndo vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_ole_in_place_site_on_pos_rect_change` | `0x00418270` | high | IOleInPlaceSite OnPosRectChange vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_browser_events_get_ids_of_names` | `0x00418280` | high | DWebBrowserEvents2 IDispatch GetIDsOfNames vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_browser_events_get_type_info` | `0x00418290` | high | DWebBrowserEvents2 IDispatch GetTypeInfo vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_browser_events_get_type_info_count` | `0x004182A0` | high | DWebBrowserEvents2 IDispatch GetTypeInfoCount vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_browser_events_invoke` | `0x004182B0` | high | DWebBrowserEvents2 Invoke sink that handles navigation, new-window, document-complete, and related browser DISPIDs and blocks disallowed URLs. |
| `ui_browser_control_doc_host_enable_modeless` | `0x004186C0` | high | IDocHostUIHandler EnableModeless vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_filter_data_object` | `0x004186D0` | high | IDocHostUIHandler FilterDataObject vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_get_drop_target` | `0x004186E0` | high | IDocHostUIHandler GetDropTarget vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_get_external` | `0x004186F0` | high | IDocHostUIHandler GetExternal vtable entry that clears the output pointer and returns E_NOTIMPL. |
| `ui_browser_control_doc_host_get_host_info` | `0x00418710` | high | IDocHostUIHandler GetHostInfo vtable entry that fills the 20-byte host-info structure and selects the browser-host flags. |
| `ui_browser_control_doc_host_get_option_key_path` | `0x00418750` | high | IDocHostUIHandler GetOptionKeyPath vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_hide_ui` | `0x00418760` | high | IDocHostUIHandler HideUI vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_on_doc_window_activate` | `0x00418770` | high | IDocHostUIHandler OnDocWindowActivate vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_on_frame_window_activate` | `0x00418780` | high | IDocHostUIHandler OnFrameWindowActivate vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_resize_border` | `0x00418790` | high | IDocHostUIHandler ResizeBorder vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_show_context_menu` | `0x004187A0` | high | IDocHostUIHandler ShowContextMenu vtable entry that returns S_OK and suppresses the embedded browser's default context menu. |
| `ui_browser_control_doc_host_show_ui` | `0x004187B0` | high | IDocHostUIHandler ShowUI vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_translate_accelerator` | `0x004187C0` | high | IDocHostUIHandler TranslateAccelerator vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_translate_url` | `0x004187D0` | high | IDocHostUIHandler TranslateUrl vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_update_ui` | `0x004187E0` | high | IDocHostUIHandler UpdateUI vtable entry that returns E_NOTIMPL. |
| `ui_browser_control_doc_host_show_help` | `0x004187F0` | high | IDocHostShowUI ShowHelp vtable entry that returns S_OK. |
| `ui_browser_control_doc_host_show_message` | `0x00418800` | high | IDocHostShowUI ShowMessage vtable entry that returns S_OK and suppresses the browser's default message UI. |
| `ui_browser_control_window_proc` | `0x00418810` | high | WNDPROC registered by BrowserControlPane; retrieves the pane from GWL_USERDATA and routes messages to its pane-aware handler. |
| `ui_browser_control_handle_window_message` | `0x00418860` | high | Validates the browser child window's WM_PAINT and suppresses minimize, maximize, move, size, and close system commands. |
| `ui_browser_control_pre_translate_message` | `0x00418980` | high | Visible-browser message filter that gives the active browser object first chance at keyboard messages and handles client close and screenshot shortcuts. |
| `ui_browser_window_ctor` | `0x00418B90` | high | Constructs exact RTTI BrowserWindow, creates its child HWND and WebBrowser ActiveX object, installs the COM client and event interfaces, and optionally navigates. |
| `ui_browser_window_dtor` | `0x004190F0` | high | Destroys exact RTTI BrowserWindow, restores its five COM interface vtables, releases the browser object, and unregisters its singleton. |
| `ui_browser_window_shutdown` | `0x00419160` | high | Hides BrowserWindow, removes its browser-event advisory connection, closes and releases IWebBrowser, destroys the child HWND, and restores focus. |
| `ui_browser_window_capture_window` | `0x004192A0` | high | Copies the visible BrowserWindow child HWND into a Canvas DC at coordinates relative to the main client window. |
| `ui_browser_window_set_bounds` | `0x00419400` | high | Moves BrowserWindow's child HWND and updates the embedded IOleInPlaceObject position and clipping rectangles. |
| `ui_browser_window_set_visible` | `0x00419520` | high | Shows or hides BrowserWindow, synchronizes cursor modes, and installs or removes its message pre-translation callback. |
| `ui_browser_window_set_3d_border_enabled` | `0x00419600` | high | Controls whether IDocHostUIHandler adds DOCHOSTUIFLAG_NO3DBORDER, then refreshes IWebBrowser so the host flags are applied. |
| `ui_browser_window_set_base_url` | `0x00419650` | high | Copies a bounded base URL into BrowserWindow's browser state. |
| `ui_browser_window_set_navigation_timeout_ms` | `0x004196A0` | medium | Stores the dormant BrowserWindow navigation-timeout field initialized by its constructor to 30,000 ms; no caller or active timer use is present. |
| `ui_browser_window_navigate` | `0x00419700` | high | Navigates BrowserWindow's embedded IWebBrowser to the supplied URL and optional header. |
| `ui_browser_window_navigate_exception_cleanup` | `0x004198BD` | high | Releases navigation SAFEARRAY and BSTR temporaries, shuts down BrowserWindow, and clears exception state. |
| `ui_browser_window_get_document_cookie` | `0x00419920` | high | Queries BrowserWindow's document interface, reads its cookie BSTR, and returns converted thread-ANSI bytes. |
| `ui_browser_window_set_document_cookie` | `0x00419AA0` | high | Queries BrowserWindow's document interface and assigns a formatted name=value cookie BSTR. |
| `ui_browser_window_query_interface` | `0x00419BB0` | high | BrowserWindow COM QueryInterface implementation that returns the adjusted subobject for each supported IID. |
| `ui_browser_window_ole_client_site_add_ref` | `0x00419D80` | high | IOleClientSite AddRef vtable entry; BrowserWindow uses a fixed reference count and returns 2. |
| `ui_browser_window_ole_client_site_release` | `0x00419D90` | high | IOleClientSite Release vtable entry; BrowserWindow uses a fixed reference count and returns 1. |
| `ui_browser_window_ole_client_site_save_object` | `0x00419DA0` | high | IOleClientSite SaveObject vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_client_site_get_moniker` | `0x00419DB0` | high | IOleClientSite GetMoniker vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_client_site_get_container` | `0x00419DC0` | high | IOleClientSite GetContainer vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_client_site_show_object` | `0x00419DD0` | high | IOleClientSite ShowObject vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_client_site_on_show_window` | `0x00419DE0` | high | IOleClientSite OnShowWindow vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_client_site_request_new_object_layout` | `0x00419DF0` | high | IOleClientSite RequestNewObjectLayout vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_in_place_site_get_window` | `0x00419E00` | high | IOleInPlaceSite GetWindow vtable entry that returns BrowserWindow's child HWND. |
| `ui_browser_window_ole_in_place_site_context_sensitive_help` | `0x00419E20` | high | IOleInPlaceSite ContextSensitiveHelp vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_in_place_site_can_in_place_activate` | `0x00419E30` | high | IOleInPlaceSite CanInPlaceActivate vtable entry that returns S_OK. |
| `ui_browser_window_ole_in_place_site_on_in_place_activate` | `0x00419E40` | high | IOleInPlaceSite OnInPlaceActivate vtable entry that returns S_OK. |
| `ui_browser_window_ole_in_place_site_on_ui_activate` | `0x00419E50` | high | IOleInPlaceSite OnUIActivate vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_in_place_site_get_window_context` | `0x00419E60` | high | IOleInPlaceSite GetWindowContext entry that supplies the child-window client rectangle as position and clipping bounds. |
| `ui_browser_window_ole_in_place_site_scroll` | `0x00419E90` | high | IOleInPlaceSite Scroll vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_in_place_site_on_ui_deactivate` | `0x00419EA0` | high | IOleInPlaceSite OnUIDeactivate vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_in_place_site_on_in_place_deactivate` | `0x00419EB0` | high | IOleInPlaceSite OnInPlaceDeactivate vtable entry that returns S_OK. |
| `ui_browser_window_ole_in_place_site_discard_undo_state` | `0x00419EC0` | high | IOleInPlaceSite DiscardUndoState vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_in_place_site_deactivate_and_undo` | `0x00419ED0` | high | IOleInPlaceSite DeactivateAndUndo vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_ole_in_place_site_on_pos_rect_change` | `0x00419EE0` | high | IOleInPlaceSite OnPosRectChange vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_browser_events_get_ids_of_names` | `0x00419EF0` | high | DWebBrowserEvents2 IDispatch GetIDsOfNames vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_browser_events_get_type_info` | `0x00419F00` | high | DWebBrowserEvents2 IDispatch GetTypeInfo vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_browser_events_get_type_info_count` | `0x00419F10` | high | DWebBrowserEvents2 IDispatch GetTypeInfoCount vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_browser_events_invoke` | `0x00419F20` | high | DWebBrowserEvents2 Invoke sink that filters navigation, tracks document completion, reveals BrowserWindow, and handles related DISPIDs. |
| `ui_browser_window_doc_host_enable_modeless` | `0x0041A200` | high | IDocHostUIHandler EnableModeless vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_filter_data_object` | `0x0041A210` | high | IDocHostUIHandler FilterDataObject vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_get_drop_target` | `0x0041A220` | high | IDocHostUIHandler GetDropTarget vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_get_external` | `0x0041A230` | high | IDocHostUIHandler GetExternal entry that clears the output pointer and returns E_NOTIMPL. |
| `ui_browser_window_doc_host_get_host_info` | `0x0041A250` | high | IDocHostUIHandler GetHostInfo entry that fills DOCHOSTUIINFO and conditionally adds DOCHOSTUIFLAG_NO3DBORDER. |
| `ui_browser_window_doc_host_get_option_key_path` | `0x0041A290` | high | IDocHostUIHandler GetOptionKeyPath vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_hide_ui` | `0x0041A2A0` | high | IDocHostUIHandler HideUI vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_on_doc_window_activate` | `0x0041A2B0` | high | IDocHostUIHandler OnDocWindowActivate vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_on_frame_window_activate` | `0x0041A2C0` | high | IDocHostUIHandler OnFrameWindowActivate vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_resize_border` | `0x0041A2D0` | high | IDocHostUIHandler ResizeBorder vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_show_context_menu` | `0x0041A2E0` | high | IDocHostUIHandler ShowContextMenu entry that returns S_OK and suppresses the default browser context menu. |
| `ui_browser_window_doc_host_show_ui` | `0x0041A2F0` | high | IDocHostUIHandler ShowUI vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_translate_accelerator` | `0x0041A300` | high | IDocHostUIHandler TranslateAccelerator vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_translate_url` | `0x0041A310` | high | IDocHostUIHandler TranslateUrl vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_update_ui` | `0x0041A320` | high | IDocHostUIHandler UpdateUI vtable entry that returns E_NOTIMPL. |
| `ui_browser_window_doc_host_show_help` | `0x0041A330` | high | IDocHostShowUI ShowHelp vtable entry that returns S_OK. |
| `ui_browser_window_doc_host_show_message` | `0x0041A340` | high | IDocHostShowUI ShowMessage entry that returns S_OK and suppresses the browser's default message UI. |
| `ui_browser_window_window_proc` | `0x0041A350` | high | WNDPROC registered by BrowserWindow; retrieves the object from GWL_USERDATA and routes messages to its instance-aware handler. |
| `ui_browser_window_handle_window_message` | `0x0041A3A0` | high | Validates BrowserWindow's WM_PAINT and suppresses minimize, maximize, move, size, and close system commands. |
| `ui_browser_window_pre_translate_message` | `0x0041A4C0` | high | Visible-BrowserWindow message filter that gives IOleInPlaceActiveObject first chance at keys and handles close and screenshot shortcuts. |
| `ui_browser_dialog_scalar_deleting_dtor` | `0x0041A6E0` | high | Runs BrowserDialogPane's destructor and conditionally frees the complete object. |
| `ui_browser_control_scalar_deleting_dtor` | `0x0041A920` | high | Runs BrowserControlPane's destructor and conditionally frees the complete object. |
| `ui_browser_dialog_singleton_register` | `0x0041ACA0` | high | Registers the complete BrowserDialogPane pointer from its Singleton secondary-base constructor. |
| `ui_browser_dialog_singleton_unregister` | `0x0041ACE0` | high | Clears the BrowserDialogPane singleton when its secondary-base destructor still owns the registered object. |
| `ui_browser_control_singleton_register` | `0x0041AD20` | high | Registers the complete BrowserControlPane pointer from its Singleton secondary-base constructor. |
| `ui_browser_control_singleton_unregister` | `0x0041AD60` | high | Clears the BrowserControlPane singleton when its secondary-base destructor still owns the registered object. |
| `ui_browser_control_singleton_exists` | `0x0041ADA0` | high | Returns whether the BrowserControlPane singleton currently contains an object. |
| `ui_browser_control_singleton_get` | `0x0041ADC0` | high | Returns the current BrowserControlPane singleton pointer. |
| `ui_browser_window_singleton_register` | `0x0041ADD0` | high | Registers the complete BrowserWindow pointer from its Singleton secondary-base constructor. |
| `ui_browser_window_singleton_unregister` | `0x0041AE10` | high | Clears the BrowserWindow singleton when its secondary-base destructor still owns the registered object. |
| `ui_browser_window_singleton_exists` | `0x0041AE50` | high | Returns whether the BrowserWindow singleton currently contains an object. |
| `ui_browser_window_singleton_get` | `0x0041AE70` | high | Returns the current BrowserWindow singleton pointer. |
| `ui_browser_window_ole_in_place_site_release_thunk` | `0x0041AE90` | high | Adjusts IOleInPlaceSite this by -4 and tail-calls BrowserWindow's shared Release implementation. |
| `ui_browser_control_ole_in_place_site_release_thunk` | `0x0041AEA0` | high | Adjusts IOleInPlaceSite this by -4 and tail-calls BrowserControlPane's shared Release implementation. |
| `ui_browser_window_browser_events_release_thunk` | `0x0041AEB0` | high | Adjusts DWebBrowserEvents2 this by -8 and tail-calls BrowserWindow's shared Release implementation. |
| `ui_browser_control_browser_events_release_thunk` | `0x0041AEC0` | high | Adjusts DWebBrowserEvents2 this by -8 and tail-calls BrowserControlPane's shared Release implementation. |
| `ui_browser_control_timer_deleting_dtor_thunk` | `0x0041AED0` | high | Adjusts TimerHandler this by -0x11C and tail-calls BrowserControlPane's scalar-deleting destructor. |
| `ui_browser_window_doc_host_ui_release_thunk` | `0x0041AEE0` | high | Adjusts IDocHostUIHandler this by -0xC and tail-calls BrowserWindow's shared Release implementation. |
| `ui_browser_window_ole_in_place_site_add_ref_thunk` | `0x0041AEF0` | high | Adjusts IOleInPlaceSite this by -4 and tail-calls BrowserWindow's shared AddRef implementation. |
| `ui_browser_control_doc_host_ui_release_thunk` | `0x0041AF00` | high | Adjusts IDocHostUIHandler this by -0xC and tail-calls BrowserControlPane's shared Release implementation. |
| `ui_browser_control_ole_in_place_site_add_ref_thunk` | `0x0041AF10` | high | Adjusts IOleInPlaceSite this by -4 and tail-calls BrowserControlPane's shared AddRef implementation. |
| `ui_browser_window_doc_host_show_ui_release_thunk` | `0x0041AF20` | high | Adjusts IDocHostShowUI this by -0x10 and tail-calls BrowserWindow's shared Release implementation. |
| `ui_browser_window_browser_events_add_ref_thunk` | `0x0041AF30` | high | Adjusts DWebBrowserEvents2 this by -8 and tail-calls BrowserWindow's shared AddRef implementation. |
| `ui_browser_control_doc_host_show_ui_release_thunk` | `0x0041AF40` | high | Adjusts IDocHostShowUI this by -0x10 and tail-calls BrowserControlPane's shared Release implementation. |
| `ui_browser_control_browser_events_add_ref_thunk` | `0x0041AF50` | high | Adjusts DWebBrowserEvents2 this by -8 and tail-calls BrowserControlPane's shared AddRef implementation. |
| `ui_browser_window_ole_in_place_site_query_interface_thunk` | `0x0041AF60` | high | Adjusts IOleInPlaceSite this by -4 and tail-calls BrowserWindow's shared QueryInterface implementation. |
| `ui_browser_window_doc_host_ui_add_ref_thunk` | `0x0041AF70` | high | Adjusts IDocHostUIHandler this by -0xC and tail-calls BrowserWindow's shared AddRef implementation. |
| `ui_browser_control_ole_in_place_site_query_interface_thunk` | `0x0041AF80` | high | Adjusts IOleInPlaceSite this by -4 and tail-calls BrowserControlPane's shared QueryInterface implementation. |
| `ui_browser_control_doc_host_ui_add_ref_thunk` | `0x0041AF90` | high | Adjusts IDocHostUIHandler this by -0xC and tail-calls BrowserControlPane's shared AddRef implementation. |
| `ui_browser_window_browser_events_query_interface_thunk` | `0x0041AFA0` | high | Adjusts DWebBrowserEvents2 this by -8 and tail-calls BrowserWindow's shared QueryInterface implementation. |
| `ui_browser_window_doc_host_show_ui_add_ref_thunk` | `0x0041AFB0` | high | Adjusts IDocHostShowUI this by -0x10 and tail-calls BrowserWindow's shared AddRef implementation. |
| `ui_browser_control_browser_events_query_interface_thunk` | `0x0041AFC0` | high | Adjusts DWebBrowserEvents2 this by -8 and tail-calls BrowserControlPane's shared QueryInterface implementation. |
| `ui_browser_control_doc_host_show_ui_add_ref_thunk` | `0x0041AFD0` | high | Adjusts IDocHostShowUI this by -0x10 and tail-calls BrowserControlPane's shared AddRef implementation. |
| `ui_browser_window_doc_host_ui_query_interface_thunk` | `0x0041AFE0` | high | Adjusts IDocHostUIHandler this by -0xC and tail-calls BrowserWindow's shared QueryInterface implementation. |
| `ui_browser_dialog_timer_deleting_dtor_thunk` | `0x0041AFF0` | high | Adjusts TimerHandler this by -0x11C and tail-calls BrowserDialogPane's scalar-deleting destructor. |
| `ui_browser_control_doc_host_ui_query_interface_thunk` | `0x0041B000` | high | Adjusts IDocHostUIHandler this by -0xC and tail-calls BrowserControlPane's shared QueryInterface implementation. |
| `ui_browser_window_doc_host_show_ui_query_interface_thunk` | `0x0041B010` | high | Adjusts IDocHostShowUI this by -0x10 and tail-calls BrowserWindow's shared QueryInterface implementation. |
| `ui_browser_control_doc_host_show_ui_query_interface_thunk` | `0x0041B020` | high | Adjusts IDocHostShowUI this by -0x10 and tail-calls BrowserControlPane's shared QueryInterface implementation. |
| `ui_bottom_buttons_pane_ctor` | `0x0041B040` | high | Constructs exact RTTI class BtmButtonsPane_A, initializes its state, and immediately sends the empty CSelfLook request. |
| `ui_bottom_buttons_pane_dtor` | `0x0041B1F0` | high | Destroys BtmButtonsPane_A, cancels timers, unregisters screen and event handling, and runs the Pane destructor. |
| `ui_bottom_buttons_apply_layout` | `0x0041B280` | high | Applies GUI-back geometry, unions the pane and three button rectangles, stores local button bounds, and invalidates BtmButtonsPane_A. |
| `ui_bottom_buttons_handle_mouse_event` | `0x0041B490` | high | Hit-tests three bottom buttons, updates hover and tooltip state, and dispatches the clicked action. |
| `ui_bottom_buttons_handle_keyboard_event` | `0x0041B5F0` | high | Honors input suppression and maps client key events 0x8B and 0x8C to bottom-button actions. |
| `ui_bottom_buttons_handle_network_event` | `0x0041B690` | high | BtmButtonsPane_A network-event handler routes SStatus to the parcel/mail updater and SSelfLook to the profile-response path. |
| `ui_bottom_buttons_handle_timer` | `0x0041B710` | high | BtmButtonsPane_A TimerHandler callback retries CSelfLook for timer 0x03000000 while the initial profile request is pending. |
| `ui_bottom_buttons_set_group_invitation_state` | `0x0041B810` | high | Applies the server-authoritative SSelfLook group-open value to the bottom-button state, clears the group-button pending action, and invalidates the pane. |
| `ui_bottom_buttons_update_parcel_mail_from_status_packet` | `0x0041B950` | high | Finds the parcel or mail indicator in variable-length SStatus fields, starts or stops its 500 ms flash timer, and invalidates the pane. |
| `ui_bottom_buttons_apply_self_look` | `0x0041BC10` | high | Consumes SSelfLook in BtmButtonsPane_A and applies is_group_open before redrawing; this is the only group-icon state update after CGroupToggle. |
| `ui_bottom_buttons_draw_content` | `0x0041BC80` | high | Draws the bottom-buttons background, three normal or pressed buttons, optional flashing parcel indicator, and remaining overlay state. |
| `ui_bottom_buttons_handle_action` | `0x0041BE30` | high | Handles the three bottom-button actions; the group action marks itself pending, sends CGroupToggle, and then requests SSelfLook without changing the icon optimistically. |
| `ui_bottom_buttons_clear_pending_action` | `0x0041BF50` | high | Clears one of three pending-action bytes and invalidates the bottom-buttons pane. |
| `ui_bottom_buttons_hit_test` | `0x0041BF80` | high | Returns the button index whose stored rectangle contains a point, or -1. |
| `ui_bottom_buttons_get_button_rect` | `0x0041C010` | high | Copies the stored local rectangle for bottom-button index 0, 1, or 2. |
| `ui_bottom_buttons_scalar_deleting_dtor` | `0x0041C0B0` | high | Runs the BtmButtonsPane_A destructor and conditionally frees the complete object. |
| `ui_bottom_buttons_singleton_exists` | `0x0041C0E0` | high | Returns whether the BtmButtonsPane_A singleton contains an object. |
| `ui_bottom_buttons_singleton_get` | `0x0041C100` | high | Returns the current BtmButtonsPane_A singleton pointer. |
| `ui_bottom_buttons_timer_deleting_dtor_thunk` | `0x0041C110` | high | Adjusts TimerHandler this by -0x11C and tail-calls the BtmButtonsPane_A scalar-deleting destructor. |
| `ui_rect_union` | `0x0041C120` | high | Writes the bounding union of two rectangles, treating an empty rectangle as absent. |
| `ui_bulletin_session_ctor` | `0x0041C280` | high | Constructs exact RTTI BulletinSession and applies the initial decoded SBulletin body. |
| `ui_bulletin_session_dtor` | `0x0041C410` | high | Destroys BulletinSession, closes and queues retained history dialogs, unregisters the pane, releases session state, and runs the Pane destructor. |
| `ui_bulletin_session_close` | `0x0041C530` | high | Closes BulletinSession auxiliary UI, hides and unregisters the pane, and queues the session for deferred deletion. |
| `ui_bulletin_session_go_back` | `0x0041C570` | high | Closes the current dialog and activates the previous history entry, or closes the session at the first entry. |
| `ui_bulletin_session_go_forward` | `0x0041C610` | high | Closes the current dialog and activates the next history entry, or closes the session when no current entry exists. |
| `ui_bulletin_session_get_previous_dialog` | `0x0041C6A0` | high | Finds a retained dialog in BulletinSession's ten-entry history and returns its predecessor. |
| `ui_bulletin_get_dialog_bounds` | `0x0041C720` | medium | Copies the client-global bulletin dialog rectangle; an earlier global-rectangle copy is immediately overwritten. |
| `ui_bulletin_session_open_new_article_dialog` | `0x0041C780` | high | Constructs NewArticleDialog at the shared bounds and pushes it onto BulletinSession history. |
| `ui_bulletin_session_open_new_mail_dialog` | `0x0041C840` | high | Constructs NewMailDialog at the shared bounds with the supplied recipient and pushes it onto BulletinSession history. |
| `ui_bulletin_session_create_screen_dimmer` | `0x0041C900` | high | Allocates a mode-5 ScreenDimmer and stores it on BulletinSession. |
| `ui_bulletin_session_create_active_screen_dimmer` | `0x0041C990` | high | Marks BulletinSession's dimmer state active, then allocates and stores a mode-5 ScreenDimmer. |
| `ui_bulletin_session_handle_network_event` | `0x0041C9B0` | high | Routes server opcode 0x31 decoded bulletin bodies to BulletinSession's server-body dispatcher. |
| `ui_bulletin_session_get_dialog` | `0x0041CA10` | high | Returns one of BulletinSession's ten retained dialog pointers for an index from 0 through 9. |
| `ui_bulletin_session_push_dialog` | `0x0041CA50` | high | Prunes forward history, attaches a dialog, advances the active index and count, and activates the new dialog. |
| `ui_bulletin_session_apply_server_body` | `0x0041CC40` | high | Routes SBulletin response types 1 through 5 to board-list, article-list, article, mail-list, and mail UI. |
| `ui_bulletin_dialog_ctor` | `0x0041CD70` | high | Constructs BulletinDialogPane and initializes its session owner, dialog type, close state, and retained payload pointer. |
| `ui_bulletin_dialog_request_close` | `0x0041CDE0` | high | Detaches the dialog from its external owner field and schedules immediate close timer 0x10011. |
| `ui_bulletin_dialog_handle_timer` | `0x0041CE30` | high | Handles timer 0x10011 by closing the complete BulletinDialogPane. |
| `ui_bulletin_dialog_close` | `0x0041CE60` | high | Closes the owning BulletinSession, or hides, unregisters, and queues a standalone BulletinDialogPane. |
| `ui_bulletin_dialog_handle_keyboard_event` | `0x0041CEB0` | high | Handles bulletin close and navigation keys, focused-control text input, and DialogPane fallback. |
| `ui_bulletin_dialog_activate` | `0x0041D090` | high | Registers BulletinDialogPane screen and event state, applies shared bounds, and invokes its final activation hook. |
| `ui_bulletin_dialog_go_back` | `0x0041D1A0` | high | Asks the owning BulletinSession to return to the previous retained dialog. |
| `ui_bulletin_dialog_create_screen_dimmer` | `0x0041D1D0` | high | Lazily allocates and stores a mode-5 ScreenDimmer for BulletinDialogPane. |
| `ui_bulletin_dialog_handle_network_event` | `0x0041D270` | high | Routes server opcode 0x31 bodies to the concrete dialog's bulletin-body handler. |
| `ui_bulletin_dialog_handle_pointer_event` | `0x0041D2D0` | high | Records last pointer positions for event families 1 and 3, then delegates to DialogPane. |
| `ui_bulletin_open_board_list` | `0x0041D350` | high | Creates exact RTTI BoardListDialog for SBulletin response type 1. |
| `ui_bulletin_open_article_list` | `0x0041D410` | high | Creates exact RTTI ArticleListDialog for SBulletin response type 2. |
| `ui_bulletin_open_article` | `0x0041D4F0` | high | Creates exact RTTI ArticleDialog for SBulletin response type 3, or an alert when its board ID is zero. |
| `ui_bulletin_open_mail_list` | `0x0041D660` | high | Creates exact RTTI MailListDialog for SBulletin response type 4. |
| `ui_bulletin_open_mail` | `0x0041D740` | high | Creates exact RTTI MailDialog for SBulletin response type 5, or an alert when its mailbox ID is zero. |
| `ui_board_list_dialog_ctor` | `0x0041D8B0` | high | Loads _nbdlist.txt and parses a heading plus repeated u16 board ID and string8 name records. |
| `ui_board_list_dialog_open_selected_board` | `0x0041DCF0` | high | Sends the initial list request for BoardListPane's selected board and activates BulletinSession's ScreenDimmer. |
| `ui_board_list_dialog_handle_action` | `0x0041DD50` | high | Handles BoardListDialog action 0 by opening the selection and action 1 by starting close animation. |
| `ui_board_list_dialog_update_open_button` | `0x0041DD90` | high | Enables or disables the open button according to whether BoardListPane has a valid selection. |
| `ui_board_list_dialog_handle_timer` | `0x0041DE20` | high | Advances the three-step 100 ms vertical open or close animation and reschedules timer 0x10111. |
| `ui_board_list_dialog_start_open_animation` | `0x0041DFE0` | high | Initializes BoardListDialog's three-step opening animation and schedules timer 0x10111 for 100 ms. |
| `ui_board_list_dialog_start_close_animation` | `0x0041E0B0` | high | Initializes BoardListDialog's three-step closing animation and schedules timer 0x10111 for 100 ms. |
| `ui_board_list_pane_ctor` | `0x0041E180` | high | Constructs BoardListPane over ListPane with 18-pixel rows and board-list style flags. |
| `ui_board_list_pane_add_entry` | `0x0041E1D0` | high | Builds a row from a signed 16-bit board ID and bounded title, then appends it to BoardListPane. |
| `ui_board_list_pane_request_selected_board` | `0x0041E230` | high | Looks up the selected row and sends the initial bulletin list request for its board ID. |
| `ui_board_list_pane_activate_selected_board` | `0x0041E270` | high | Resolves the owning BoardListDialog and invokes its selected-board open path. |
| `ui_board_list_pane_draw_entry` | `0x0041E2B0` | high | Draws one board row with selection-specific padding and the title stored after its two-byte board ID. |
| `ui_article_list_dialog_ctor` | `0x0041E490` | high | Loads _narlist.txt, parses the article-list response body, and adds its optional Hilight control for any nonzero SStatus privilege. |
| `ui_article_list_dialog_open_selected_article` | `0x0041EC40` | high | Sends the selected article-detail request and activates the owning BulletinSession's ScreenDimmer. |
| `ui_article_list_dialog_highlight_selected_article` | `0x0041ECB0` | high | Requests a highlight-state change and creates the dialog ScreenDimmer when accepted. |
| `ui_article_list_dialog_delete_selected_article` | `0x0041ED10` | high | Starts selected-article deletion and creates the dialog ScreenDimmer when accepted. |
| `ui_article_list_dialog_select_article` | `0x0041ED70` | high | Finds the ArticleListPane row matching an article identifier and selects it. |
| `ui_article_list_dialog_remove_selected_rows` | `0x0041EDC0` | high | Removes selected ArticleListPane rows and refreshes action controls. |
| `ui_article_list_dialog_request_latest_page` | `0x0041EE10` | high | Requests the newest article page with start ID 0x7FFF and page marker 0xFFF0. |
| `ui_article_list_dialog_open_new_article` | `0x0041EE60` | high | Asks the owning BulletinSession to construct and push NewArticleDialog. |
| `ui_article_list_dialog_request_older_page` | `0x0041EE80` | high | Uses the final article ID minus one for an older-page request, with 0x7FFF as the empty-list fallback. |
| `ui_article_list_dialog_handle_keyboard_event` | `0x0041EED0` | high | Handles ArticleListDialog keyboard commands and enables modifier-based multi-selection only for a nonzero privilege. |
| `ui_article_list_dialog_handle_action` | `0x0041F1F0` | high | Dispatches ArticleListDialog actions for open, compose, delete, back, close, and highlight. |
| `ui_article_list_update_action_controls` | `0x0041F2E0` | high | Enables or disables article-list actions from current selection state, including the privileged Hilight control. |
| `ui_article_list_apply_server_body` | `0x0041F450` | high | Routes active-list SBulletin response types 2, 7, and 8. |
| `ui_article_list_apply_list_reply` | `0x0041F4E0` | high | Parses bulletin subtype-2 article-list rows and appends them to ArticleListPane. |
| `ui_article_list_apply_post_reply` | `0x0041F840` | high | Consumes SBulletin response 8 status, optionally shows an alert, and refreshes the article list. |
| `ui_article_list_show_operation_reply` | `0x0041F940` | high | Consumes SBulletin response 7 status plus string8 message and creates DeleteReplyAlert. |
| `ui_article_list_confirm_delete` | `0x0041FAE0` | high | Builds the article delete confirmation and preserves the privileged modifier-based multi-selection. |
| `ui_index_selection_clear` | `0x0041FC90` | high | Clears the fixed-capacity integer selection set used by ArticleListPane. |
| `ui_index_selection_remove` | `0x0041FCB0` | high | Removes a selected integer by replacing it with the final entry and decrementing the count. |
| `ui_index_selection_add` | `0x0041FD00` | high | Adds an absent integer when selection capacity remains; an existing value is already successful. |
| `ui_index_selection_find` | `0x0041FD60` | high | Returns an integer's selection-set index, or -1 when absent. |
| `ui_index_selection_get_items` | `0x0041FDB0` | high | Writes the selection count and returns its contiguous integer array. |
| `ui_article_list_handle_selection_change` | `0x0041FDD0` | high | Maintains privileged toggle and range selection from the live keyboard modifiers and invalidates changed rows. |
| `ui_article_list_pane_ctor` | `0x00420040` | high | Constructs exact RTTI ArticleListPane and allocates its multi-selection storage only for a nonzero privilege. |
| `ui_article_list_pane_dtor` | `0x00420160` | high | Destroys ArticleListPane, frees auxiliary selection storage, and runs the ListPane destructor. |
| `ui_article_list_upsert_row` | `0x004201E0` | high | Builds a row, finds its descending article-ID position, replaces an existing match or inserts a new row, and refreshes list state. |
| `ui_article_list_request_selected_article` | `0x00420310` | high | Sends the article-detail request for the selected row and caller-supplied board ID. |
| `ui_article_list_delete_selected` | `0x00420360` | high | Deletes the current article when unprivileged or sends one request for every selected article when privileged. |
| `ui_article_list_highlight_selected` | `0x00420450` | high | Highlights the current article when unprivileged or sends one request for every selected article when privileged. |
| `ui_article_list_select_article` | `0x00420550` | high | Finds a row by signed article ID and selects it when present. |
| `ui_article_list_remove_selected_rows` | `0x00420590` | high | Removes the current row when unprivileged or sorts and removes every selected row when privileged. |
| `ui_article_list_request_latest_page` | `0x00420700` | high | Requests the newest article page with start ID 0x7FFF and page marker 0xFFF0. |
| `ui_article_list_request_older_page` | `0x00420730` | high | Uses the final row ID minus one as the older-page start, falling back to 0x7FFF for an empty list. |
| `ui_article_list_find_article` | `0x004207A0` | high | Returns the row index matching a signed article ID, or -1. |
| `ui_article_list_find_insert_position` | `0x00420800` | high | Finds the descending article-ID insertion point; an existing match returns its index with bit 31 set. |
| `ui_article_list_handle_keyboard_event` | `0x00420880` | high | Delegates keyboard handling and requests an older page when navigation reaches the loaded end. |
| `ui_article_list_handle_pointer_event` | `0x00420910` | high | Delegates pointer handling and requests an older page when the visible range reaches the loaded end. |
| `ui_article_list_activate_selected_article` | `0x00420970` | high | Resolves the owning ArticleListDialog and invokes its open-selected action. |
| `ui_article_list_draw_row` | `0x004209B0` | high | Draws article rows and uses palette index 0x58 for privileged multi-selected rows. |
| `ui_article_dialog_ctor` | `0x004211A0` | high | Loads _narti.txt and parses article navigation, author, date, title, and string16 content. |
| `ui_article_dialog_delete_article` | `0x00421AC0` | high | Sends the delete request for the current board and article, then creates a ScreenDimmer. |
| `ui_article_dialog_restore_list_selection` | `0x00421B10` | high | Finds the previous ArticleListDialog and reselects the current article ID there. |
| `ui_article_dialog_handle_keyboard_event` | `0x00421B50` | high | Handles back, navigation, compose, and delete keys with BulletinDialogPane fallback. |
| `ui_article_dialog_handle_action` | `0x00421CB0` | high | Dispatches controls for previous or next article, compose, delete confirmation, back, and close. |
| `ui_article_dialog_navigate` | `0x00421D40` | high | Clamps the adjacent article ID, sends a direction-tagged navigation request, and activates ScreenDimmer. |
| `ui_article_dialog_open_new_article` | `0x00421E20` | high | Returns to the previous bulletin dialog and opens NewArticleDialog. |
| `ui_article_dialog_confirm_delete` | `0x00421E50` | high | Allocates ConfirmDeleteAlert bound to ArticleDialog. |
| `ui_article_apply_server_body` | `0x00421EE0` | high | Routes active-article SBulletin response type 7 to the operation reply UI. |
| `ui_article_dialog_apply_delete_reply` | `0x00421F40` | high | Removes ScreenDimmer, parses the delete-reply message, and creates DeleteReplyAlert. |
| `ui_delete_reply_alert_ctor` | `0x004222E0` | high | Constructs DeleteReplyAlert with the server message, owning bulletin dialog, and success flag. |
| `ui_delete_reply_alert_handle_action` | `0x00422370` | high | Dismisses DeleteReplyAlert and updates the owning article or mail list after successful deletion. |
| `ui_new_article_dialog_ctor` | `0x00422420` | high | Constructs NewArticleDialog from _nartin.txt and attaches Send, Cancel, Author, Title, and Content controls. |
| `ui_new_article_dialog_refresh_article_list` | `0x00422780` | high | Finds the previous ArticleListDialog and requests its newest page. |
| `ui_new_article_dialog_submit` | `0x004227B0` | high | Sends the article-post request, creates ScreenDimmer, and returns to the previous dialog on immediate success. |
| `ui_new_article_dialog_handle_keyboard_event` | `0x00422850` | high | Handles tab focus, default Enter, cancel Escape, and focused text-control input. |
| `ui_new_article_dialog_apply_server_body` | `0x00422A10` | high | Accepts bulletin subtype-6 post replies and dispatches their body. |
| `ui_new_article_dialog_apply_post_reply` | `0x00422A70` | high | Removes ScreenDimmer, parses the post reply, and creates TransferReplyAlert. |
| `ui_transfer_reply_alert_ctor` | `0x00422E50` | high | Constructs TransferReplyAlert with the server message, owning dialog, and success flag. |
| `ui_transfer_reply_alert_handle_action` | `0x00422EA0` | high | Dismisses TransferReplyAlert, refreshes the prior article list, and returns through history on success. |
| `ui_mail_list_dialog_ctor` | `0x00422EE0` | high | Loads _nmaill.txt and parses the mail-list response body. |
| `ui_mail_list_dialog_open_selected_mail` | `0x00423650` | high | Sends the selected mail-detail request and activates BulletinSession's ScreenDimmer. |
| `ui_mail_list_dialog_delete_selected_mail` | `0x004236C0` | high | Starts deletion of selected mail and creates the dialog ScreenDimmer. |
| `ui_mail_list_dialog_select_mail` | `0x00423720` | high | Finds the MailListPane row matching a mail identifier and selects it. |
| `ui_mail_list_dialog_remove_selected_rows` | `0x00423770` | high | Removes selected MailListPane rows and refreshes action controls. |
| `ui_mail_list_dialog_request_latest_page` | `0x004237C0` | high | Requests the newest mail-list page for the dialog's mailbox selector. |
| `ui_mail_list_dialog_open_new_mail` | `0x00423810` | high | Opens NewMailDialog with an empty recipient. |
| `ui_mail_list_dialog_reply_to_selected_mail` | `0x00423830` | high | Copies the selected sender into a bounded buffer and opens NewMailDialog with that recipient. |
| `ui_mail_list_dialog_confirm_delete` | `0x004238D0` | high | Allocates ConfirmDeleteAlert bound to MailListDialog in mail-deletion mode. |
| `ui_mail_list_dialog_request_older_page` | `0x00423960` | high | Requests the mail page preceding the final loaded row ID. |
| `ui_mail_list_dialog_handle_keyboard_event` | `0x004239B0` | high | Maps mail-list keyboard shortcuts to paging, compose, reply, open, delete, back, and base handling. |
| `ui_mail_list_dialog_handle_action` | `0x00423B90` | high | Dispatches mail-list control actions for paging, compose, reply, open, delete, and close. |
| `ui_mail_list_update_action_controls` | `0x00423C50` | high | Enables or disables Open, Reply, and Delete controls from the current mail-list selection. |
| `ui_mail_list_apply_server_body` | `0x00423D50` | high | Routes active-mail-list SBulletin response types 4 and 7. |
| `ui_mail_list_apply_list_reply` | `0x00423DD0` | high | Parses a mailbox list reply and appends its rows to MailListPane. |
| `ui_mail_list_apply_delete_reply` | `0x00424130` | high | Parses a mail-delete reply, removes the dimmer, and opens the result alert. |
| `ui_mail_list_pane_ctor` | `0x004242C0` | high | Constructs the RTTI-backed MailListPane with its mailbox context. |
| `ui_mail_list_insert_row` | `0x00424330` | high | Builds and inserts one mail row in descending ID order unless it is a duplicate. |
| `ui_mail_list_request_selected_mail` | `0x004243F0` | high | Sends a mail-body request for the selected row. |
| `ui_mail_list_delete_selected` | `0x00424440` | high | Sends a mail-delete request for the selected row. |
| `ui_mail_list_select_mail` | `0x00424490` | high | Finds and selects a loaded mail row by ID. |
| `ui_mail_list_reselect_current` | `0x004244D0` | high | Reapplies the pane's current list selection. |
| `ui_mail_list_pane_handle_keyboard_event` | `0x00424500` | high | Delegates keyboard input and requests an older page when the loaded row count is below capacity. |
| `ui_mail_list_pane_handle_pointer_event` | `0x00424560` | high | Delegates pointer input and requests an older page when scrolling reaches the loaded end. |
| `ui_mail_list_request_latest_page` | `0x004245C0` | high | Requests the newest mailbox page with the initial 0x7FFF cursor. |
| `ui_mail_list_request_older_page` | `0x004245F0` | high | Requests the page before the final loaded mail ID. |
| `ui_mail_list_copy_selected_sender` | `0x00424660` | high | Copies the selected row's sender into a caller buffer. |
| `ui_mail_list_find_mail` | `0x004246A0` | high | Linearly finds a loaded row by signed mail ID. |
| `ui_mail_list_find_insert_position` | `0x00424700` | high | Finds the descending-ID insertion point and rejects duplicate IDs. |
| `ui_mail_list_activate_selected_mail` | `0x00424780` | high | Resolves the owning MailListDialog and opens the selected mail. |
| `ui_mail_list_draw_row` | `0x004247C0` | high | Draws one mail row with read state, sender, date, reply count, and title. |
| `ui_mail_dialog_ctor` | `0x00424E00` | high | Loads _nmailr.txt and parses mail navigation, author, date, title, and string16 content. |
| `ui_mail_dialog_delete_current` | `0x00425770` | high | Requests deletion of the displayed mail and returns to the previous bulletin dialog. |
| `ui_mail_dialog_return_to_list` | `0x004257D0` | high | Returns to the mail list and reselects the displayed mail ID. |
| `ui_mail_dialog_handle_keyboard_event` | `0x00425810` | high | Maps keyboard shortcuts to mail navigation, compose, reply, delete, back, and base handling. |
| `ui_mail_dialog_handle_action` | `0x00425980` | high | Dispatches mail-dialog control actions for navigation, compose, reply, delete, back, and close. |
| `ui_mail_dialog_request_adjacent_mail` | `0x00425A20` | high | Sends a previous-or-next mail request and creates a screen dimmer. |
| `ui_mail_dialog_compose_new` | `0x00425B00` | high | Returns from the current mail and opens a blank new-mail dialog. |
| `ui_mail_dialog_reply_to_sender` | `0x00425B30` | high | Returns from the current mail and opens a reply addressed to its sender. |
| `ui_mail_dialog_confirm_delete` | `0x00425B70` | high | Allocates and opens the confirmation alert for the displayed mail. |
| `ui_mail_apply_server_body` | `0x00425C00` | high | Routes active-mail SBulletin response type 7 to the operation reply UI. |
| `ui_mail_dialog_apply_delete_reply` | `0x00425C60` | high | Removes the dimmer, parses a mail-delete result message, and displays it. |
| `ui_mail_delete_reply_alert_ctor` | `0x00426000` | high | Constructs RTTI-backed MailDeleteReplyAlert and stores the server result byte. |
| `ui_mail_delete_reply_alert_accept` | `0x00426050` | high | Returns through the mail dialog to its list and reselects the displayed mail. |
| `ui_new_mail_dialog_ctor` | `0x00426080` | high | Constructs NewMailDialog from _nmails.txt with recipient, title, content, Send, and Cancel controls. |
| `ui_new_mail_dialog_refresh_mail_list` | `0x00426490` | high | Asks the previous MailListDialog to reload its newest page. |
| `ui_new_mail_dialog_send` | `0x004264C0` | high | Sends the composed mail, creates a dimmer, and closes on immediate success. |
| `ui_new_mail_dialog_handle_keyboard_event` | `0x00426560` | high | Handles tab focus traversal, default action, cancellation, and focused-control keyboard input. |
| `ui_new_mail_dialog_apply_server_body` | `0x00426700` | high | Routes bulletin new-mail server subcommand 6 to the transfer-reply parser. |
| `ui_new_mail_dialog_apply_transfer_reply` | `0x00426760` | high | Removes the dimmer, parses transfer result text, and opens MailTransferReplyAlert. |
| `ui_mail_transfer_reply_alert_ctor` | `0x00426C00` | high | Constructs RTTI-backed MailTransferReplyAlert and stores the transfer result byte. |
| `ui_mail_transfer_reply_alert_accept` | `0x00426C50` | high | Refreshes the prior mail list and returns to it when transfer succeeds. |
| `ui_mail_confirm_delete_alert_ctor` | `0x00426C90` | high | Constructs ConfirmDeleteAlert for the displayed mail and stores its mode. |
| `ui_bulletin_session_scalar_deleting_dtor` | `0x00426DA0` | high | Destroys BulletinSession and optionally frees its complete object. |
| `ui_bulletin_dialog_scalar_deleting_dtor` | `0x00426DE0` | high | Destroys BulletinDialogPane and optionally frees its complete object. |
| `ui_board_list_dialog_scalar_deleting_dtor` | `0x00426E30` | high | Destroys BoardListDialog and optionally frees its complete object. |
| `ui_board_list_pane_scalar_deleting_dtor` | `0x00426E90` | high | Destroys BoardListPane and optionally frees its complete object. |
| `ui_article_list_dialog_scalar_deleting_dtor` | `0x00426EC0` | high | Destroys ArticleListDialog and optionally frees its complete object. |
| `ui_article_list_pane_scalar_deleting_dtor` | `0x00426EF0` | high | Destroys ArticleListPane and optionally frees its complete object. |
| `ui_article_dialog_scalar_deleting_dtor` | `0x00426F20` | high | Destroys ArticleDialog and optionally frees its complete object. |
| `ui_delete_reply_alert_scalar_deleting_dtor` | `0x00426F50` | high | Destroys DeleteReplyAlert and optionally frees its complete object. |
| `ui_new_article_dialog_scalar_deleting_dtor` | `0x00426FF0` | high | Destroys NewArticleDialog and optionally frees its complete object. |
| `ui_transfer_reply_alert_scalar_deleting_dtor` | `0x00427020` | high | Destroys TransferReplyAlert and optionally frees its complete object. |
| `ui_mail_list_dialog_scalar_deleting_dtor` | `0x00427050` | high | Destroys MailListDialog and optionally frees its complete object. |
| `ui_mail_list_pane_scalar_deleting_dtor` | `0x00427080` | high | Destroys MailListPane and optionally frees its complete object. |
| `ui_mail_dialog_scalar_deleting_dtor` | `0x004270B0` | high | Destroys MailDialog and optionally frees its complete object. |
| `ui_mail_delete_reply_alert_scalar_deleting_dtor` | `0x004270E0` | high | Destroys MailDeleteReplyAlert and optionally frees its complete object. |
| `ui_new_mail_dialog_scalar_deleting_dtor` | `0x00427110` | high | Destroys NewMailDialog and optionally frees its complete object. |
| `ui_mail_transfer_reply_alert_scalar_deleting_dtor` | `0x00427170` | high | Destroys MailTransferReplyAlert and optionally frees its complete object. |
| `ui_mail_confirm_delete_alert_scalar_deleting_dtor` | `0x004271B0` | high | Destroys ConfirmDeleteAlert and optionally frees its complete object. |
| `ui_bulletin_session_singleton_register` | `0x004271E0` | high | Registers the containing BulletinSession singleton. |
| `ui_bulletin_session_singleton_unregister` | `0x00427220` | high | Clears the BulletinSession singleton when it matches the containing object. |
| `ui_delete_reply_alert_singleton_register` | `0x00427260` | high | Registers the containing DeleteReplyAlert singleton. |
| `ui_delete_reply_alert_singleton_unregister` | `0x004272A0` | high | Clears the DeleteReplyAlert singleton when it matches the containing object. |
| `ui_delete_reply_alert_is_open` | `0x004272E0` | high | Returns whether a DeleteReplyAlert is registered. |
| `ui_bulletin_bang_user_batch_session_is_active` | `0x00427300` | high | Returns whether a BulletinBangUserBatchSession singleton is active. |
| `ui_bulletin_bang_user_batch_session_get` | `0x00427320` | high | Returns the active BulletinBangUserBatchSession singleton. |
| `ui_bulletin_bang_user_batch_session_destroy_active` | `0x00427330` | high | Destroys the active BulletinBangUserBatchSession when present. |
| `ui_mail_confirm_delete_alert_timer_scalar_deleting_dtor_thunk` | `0x004273A0` | high | Adjusts TimerHandler this and enters ConfirmDeleteAlert's scalar deleting destructor. |
| `ui_mail_list_pane_timer_scalar_deleting_dtor_thunk` | `0x004273B0` | high | Adjusts TimerHandler this and enters MailListPane's scalar deleting destructor. |
| `ui_mail_list_dialog_timer_scalar_deleting_dtor_thunk` | `0x004273C0` | high | Adjusts TimerHandler this and enters MailListDialog's scalar deleting destructor. |
| `ui_transfer_reply_alert_timer_scalar_deleting_dtor_thunk` | `0x004273D0` | high | Adjusts TimerHandler this and enters TransferReplyAlert's scalar deleting destructor. |
| `ui_mail_transfer_reply_alert_timer_scalar_deleting_dtor_thunk` | `0x004273E0` | high | Adjusts TimerHandler this and enters MailTransferReplyAlert's scalar deleting destructor. |
| `ui_article_list_pane_timer_scalar_deleting_dtor_thunk` | `0x004273F0` | high | Adjusts TimerHandler this and enters ArticleListPane's scalar deleting destructor. |
| `ui_bulletin_session_timer_scalar_deleting_dtor_thunk` | `0x00427400` | high | Adjusts TimerHandler this and enters BulletinSession's scalar deleting destructor. |
| `ui_board_list_pane_timer_scalar_deleting_dtor_thunk` | `0x00427410` | high | Adjusts TimerHandler this and enters BoardListPane's scalar deleting destructor. |
| `ui_bulletin_dialog_timer_scalar_deleting_dtor_thunk` | `0x00427420` | high | Adjusts TimerHandler this and enters BulletinDialogPane's scalar deleting destructor. |
| `ui_new_article_dialog_timer_scalar_deleting_dtor_thunk` | `0x00427430` | high | Adjusts TimerHandler this and enters NewArticleDialog's scalar deleting destructor. |
| `ui_article_list_dialog_timer_scalar_deleting_dtor_thunk` | `0x00427440` | high | Adjusts TimerHandler this and enters ArticleListDialog's scalar deleting destructor. |
| `ui_mail_delete_reply_alert_timer_scalar_deleting_dtor_thunk` | `0x00427450` | high | Adjusts TimerHandler this and enters MailDeleteReplyAlert's scalar deleting destructor. |
| `ui_article_dialog_timer_scalar_deleting_dtor_thunk` | `0x00427460` | high | Adjusts TimerHandler this and enters ArticleDialog's scalar deleting destructor. |
| `ui_mail_dialog_timer_scalar_deleting_dtor_thunk` | `0x00427470` | high | Adjusts TimerHandler this and enters MailDialog's scalar deleting destructor. |
| `ui_delete_reply_alert_timer_scalar_deleting_dtor_thunk` | `0x00427480` | high | Adjusts TimerHandler this and enters DeleteReplyAlert's scalar deleting destructor. |
| `ui_new_mail_dialog_timer_scalar_deleting_dtor_thunk` | `0x00427490` | high | Adjusts TimerHandler this and enters NewMailDialog's scalar deleting destructor. |
| `ui_board_list_dialog_timer_scalar_deleting_dtor_thunk` | `0x004274A0` | high | Adjusts TimerHandler this and enters BoardListDialog's scalar deleting destructor. |
| `ui_bulletin_string_list_pane_ctor` | `0x00427530` | high | Constructs StringListPane with a fixed line limit and reusable text buffer. |
| `ui_bulletin_string_list_pane_dtor` | `0x004275E0` | high | Releases StringListPane's text buffer and destroys its list-pane base. |
| `ui_bulletin_string_list_set_lines` | `0x00427630` | high | Replaces pane rows with DBCS-safe truncated strings. |
| `ui_bulletin_string_list_draw_row` | `0x00427750` | high | Draws one StringListPane row with its configured byte limit and color. |
| `ui_bulletin_bang_notify_dialog_ctor` | `0x004277E0` | high | Constructs BulletinBangNotifyDialog from lbang.txt. |
| `ui_bulletin_bang_notify_dialog_dtor` | `0x00427AF0` | high | Destroys BulletinBangNotifyDialog through its DialogPane base. |
| `ui_bulletin_bang_notify_dialog_handle_action` | `0x00427B20` | high | Reports OK or Cancel to the active bang session and queues dialog closure. |
| `ui_bulletin_bang_user_date_cache_initialize` | `0x00427C20` | high | Allocates the process-local user warning-date map. |
| `ui_bulletin_bang_user_date_cache_shutdown` | `0x00427CB0` | high | Destroys and frees the process-local user warning-date map. |
| `ui_bulletin_bang_user_date_cache_lookup` | `0x00427D10` | high | Looks up a user name and returns its cached warning date. |
| `ui_bulletin_bang_user_date_cache_insert` | `0x00427E20` | high | Inserts a user name and warning date when absent. |
| `ui_bulletin_bang_user_batch_session_ctor` | `0x00427F90` | high | Constructs and registers BulletinBangUserBatchSession and initializes its user-date cache. |
| `ui_bulletin_bang_user_batch_session_dtor` | `0x00428000` | high | Shuts down the cache, unregisters the singleton, and destroys BatchSession. |
| `ui_bulletin_bang_user_batch_session_timer_callback` | `0x00428220` | high | Starts or cancels the batch on timer 0x1000 and delegates lower timer IDs. |
| `ui_bulletin_bang_user_batch_session_enqueue_user` | `0x00428290` | high | Queues a selected user warning job when its persisted date permits one. |
| `ui_bulletin_bang_process_user_warning` | `0x00428690` | high | Updates a user's warning record and sends bulletin-abuse warning commands. |
| `ui_bulletin_bang_user_batch_job_ctor` | `0x004289D0` | high | Constructs BulletinBangUserBatchJob with its user, timing, text, severity, and date. |
| `ui_bulletin_bang_user_batch_job_dtor` | `0x00428AC0` | high | Destroys BulletinBangUserBatchJob and its embedded bases. |
| `ui_bulletin_bang_user_batch_job_execute` | `0x00428B30` | high | Processes the queued user warning and completes the batch job. |
| `ui_bulletin_bang_user_batch_job_queue_delete` | `0x00428B90` | high | Queues the batch job's embedded LObject for deferred deletion. |
| `ui_bulletin_string_list_pane_scalar_deleting_dtor` | `0x00428BE0` | high | Destroys StringListPane and optionally frees its complete object. |
| `ui_bulletin_bang_notify_dialog_scalar_deleting_dtor` | `0x00428C10` | high | Destroys BulletinBangNotifyDialog and optionally frees its complete object. |
| `ui_bulletin_bang_user_batch_session_scalar_deleting_dtor` | `0x00428CA0` | high | Destroys BulletinBangUserBatchSession and optionally frees its complete object. |
| `ui_bulletin_bang_user_batch_job_scalar_deleting_dtor` | `0x00428CD0` | high | Destroys BulletinBangUserBatchJob and optionally frees its complete object. |
| `ui_bulletin_bang_user_date_map_ctor` | `0x00428D00` | high | Constructs the red-black tree map for user warning dates. |
| `ui_bulletin_bang_user_date_map_dtor` | `0x00428D30` | high | Destroys the user warning-date map's nodes and sentinel. |
| `ui_bulletin_bang_user_date_map_erase` | `0x00428DD0` | high | Erases and rebalances one user warning-date map node. |
| `ui_bulletin_bang_user_date_map_find` | `0x004292B0` | high | Finds an exact string key and returns the map head sentinel when absent. |
| `ui_bulletin_bang_user_date_map_rotate_left` | `0x00429390` | high | Performs a red-black tree left rotation. |
| `ui_bulletin_bang_user_date_map_rotate_right` | `0x00429440` | high | Performs a red-black tree right rotation. |
| `ui_bulletin_bang_user_date_map_free_node` | `0x004294F0` | high | Frees one allocated user-date map node. |
| `ui_bulletin_bang_user_date_map_erase_range` | `0x00429520` | high | Erases a half-open iterator range, with a complete-tree clear fast path. |
| `ui_bulletin_bang_user_date_map_lower_bound` | `0x00429600` | high | Returns the first node whose key is not less than the requested string. |
| `ui_bulletin_bang_user_date_map_initialize_tree` | `0x004296A0` | high | Allocates and initializes the tree head sentinel and resets its size. |
| `ui_bulletin_bang_user_date_map_iterator_next` | `0x00429720` | high | Advances one in-order map iterator. |
| `ui_bulletin_bang_user_date_map_clear` | `0x004297D0` | high | Destroys all user-date nodes and resets the head sentinel. |
| `ui_bulletin_bang_user_date_map_iterator_ctor` | `0x00429830` | high | Constructs a map iterator from a node pointer. |
| `ui_bulletin_bang_user_date_map_erase_subtree` | `0x00429850` | high | Recursively destroys a user-date map subtree. |
| `ui_bulletin_bang_user_batch_session_singleton_register` | `0x004298C0` | high | Registers the containing BulletinBangUserBatchSession singleton. |
| `ui_bulletin_bang_user_batch_session_singleton_unregister` | `0x00429900` | high | Clears the batch-session singleton when it matches the containing object. |
| `ui_bulletin_bang_user_date_map_destroy_key` | `0x00429940` | high | Destroys the string key stored in one map node. |
| `ui_bulletin_bang_user_date_map_allocate_nodes` | `0x004299B0` | high | Allocates fixed 0x30-byte map nodes and throws std::bad_alloc on failure. |
| `ui_bulletin_bang_user_date_map_insert_unique` | `0x00429A20` | high | Finds or inserts a unique user string key. |
| `ui_bulletin_bang_user_date_map_link_and_rebalance` | `0x00429C80` | high | Links a prepared node and restores red-black tree invariants. |
| `ui_bulletin_bang_user_date_map_iterator_prev` | `0x00429F60` | high | Moves one in-order map iterator backward. |
| `ui_bulletin_bang_user_date_map_create_node` | `0x0042A020` | high | Allocates a map node and constructs its string-key and integer-date pair. |
| `ui_bulletin_bang_user_date_map_allocate_node` | `0x0042A1A0` | high | Allocates one map node and initializes its links and color flags. |
| `ui_bulletin_bang_user_date_map_construct_value` | `0x0042A1F0` | high | Constructs the string-key and integer-date value in a new map node. |
| `ui_bulletin_bang_user_date_pair_copy_ctor` | `0x0042A7A0` | high | Copy-constructs a user-name string and copies its integer date. |
| `ui_bulletin_bang_notify_dialog_timer_scalar_deleting_dtor_thunk` | `0x0042AD10` | high | Adjusts TimerHandler this and enters BulletinBangNotifyDialog's deleting destructor. |
| `ui_bulletin_bang_user_batch_job_lobject_scalar_deleting_dtor_thunk` | `0x0042AD20` | high | Adjusts LObject this and enters BulletinBangUserBatchJob's deleting destructor. |
| `ui_bulletin_string_list_pane_timer_scalar_deleting_dtor_thunk` | `0x0042AD30` | high | Adjusts TimerHandler this and enters StringListPane's deleting destructor. |
| `ui_legend_list_pane_ctor` | `0x0042B8F0` | high | Constructs exact RTTI LegendListPane and loads its eight legend images. |
| `ui_legend_list_pane_dtor` | `0x0042B9F0` | high | Restores LegendListPane vtables and destroys its ListPane base. |
| `ui_legend_list_draw_item` | `0x0042BA20` | high | Draws one Self Look legend record by icon, resolves its color through palette slot 0, and renders its text. |
| `ui_legend_list_contains_key` | `0x0042BB70` | high | Searches the current self-look legend records for an exact, case-sensitive hidden key match. |
| `ui_legend_dialog_ctor` | `0x0042BC00` | high | Constructs exact RTTI LegendDialogPane from llegends.txt. |
| `ui_legend_dialog_dtor` | `0x0042BFD0` | high | Unregisters LegendDialogPane and destroys its DialogPane base. |
| `ui_legend_dialog_handle_action` | `0x0042C050` | high | Closes the legacy legend dialog for action ID 2. |
| `ui_legend_dialog_handle_pointer_event` | `0x0042C080` | high | Tracks legend pointer coordinates and delegates in-bounds events. |
| `ui_legend_dialog_apply_list_body` | `0x0042C120` | high | Parses a counted legend-mark body into the legacy list. |
| `ui_portrait_control_pane_ctor` | `0x0042C300` | high | Constructs exact RTTI PortraitControlPane with no image. |
| `ui_portrait_control_set_pixmap` | `0x0042C340` | high | Renders a supplied pixmap into the portrait control or clears on null. |
| `ui_portrait_control_clear` | `0x0042C3F0` | high | Marks the portrait control blank and invalidates it. |
| `ui_portrait_control_draw` | `0x0042C420` | high | Draws the blank base appearance only when no image is present. |
| `ui_new_legend_dialog_ctor` | `0x0042C450` | high | Constructs exact RTTI NewLegendDialogPane from llegend2.txt in editable or read-only mode. |
| `ui_new_legend_dialog_dtor` | `0x0042C9C0` | high | Releases portrait state and destroys NewLegendDialogPane's DialogPane base. |
| `ui_new_legend_dialog_action` | `0x0042CA50` | high | The RTTI-backed NewLegendDialogPane action normalizes line breaks, ends profile text at the fifth break, and saves profile.txt. |
| `ui_new_legend_dialog_apply_list_body` | `0x0042CBA0` | high | Parses a counted legend-mark body into NewLegendDialogPane. |
| `ui_legend_dialog_apply_self_look` | `0x0042CD80` | high | Clears and rebuilds the older LegendDialogPane list from SSelfLook's fixed-size legend records. |
| `ui_new_legend_dialog_reload_profile_text` | `0x0042CE20` | high | Temporarily unlocks the profile editor and reloads its text buffer. |
| `ui_new_legend_dialog_apply_portrait_profile_body` | `0x0042CE70` | high | Decodes portrait/profile bytes and refreshes the dialog controls. |
| `ui_new_legend_dialog_draw` | `0x0042CF50` | high | Draws NewLegendDialogPane and overlays its portrait frame when a portrait exists. |
| `ui_new_legend_dialog_timer_callback` | `0x0042D010` | high | Handles timer ID 1 through the Change control callback. |
| `ui_new_legend_dialog_handle_pointer_event` | `0x0042D050` | high | Delegates only pointer events whose coordinates lie inside the dialog. |
| `ui_new_legend_dialog_handle_keyboard_event` | `0x0042D0D0` | high | Delegates keyboard input to the base dialog handler. |
| `ui_new_legend_dialog_contains_legend_key` | `0x0042D0F0` | high | Forwards a LegendInterface key lookup to LegendListPane. |
| `ui_legend_list_pane_scalar_deleting_dtor` | `0x0042D110` | high | Destroys LegendListPane and optionally frees its complete object. |
| `ui_legend_dialog_scalar_deleting_dtor` | `0x0042D170` | high | Destroys LegendDialogPane and optionally frees its complete object. |
| `ui_portrait_control_pane_scalar_deleting_dtor` | `0x0042D1A0` | high | Destroys PortraitControlPane and optionally frees its complete object. |
| `ui_new_legend_dialog_scalar_deleting_dtor` | `0x0042D1D0` | high | Destroys NewLegendDialogPane and optionally frees its complete object. |
| `ui_portrait_control_pane_timer_scalar_deleting_dtor_thunk` | `0x0042D200` | high | Adjusts TimerHandler this and enters PortraitControlPane's deleting destructor. |
| `ui_legend_list_pane_timer_scalar_deleting_dtor_thunk` | `0x0042D210` | high | Adjusts TimerHandler this and enters LegendListPane's deleting destructor. |
| `ui_legend_dialog_timer_scalar_deleting_dtor_thunk` | `0x0042D220` | high | Adjusts TimerHandler this and enters LegendDialogPane's deleting destructor. |
| `ui_new_legend_dialog_timer_scalar_deleting_dtor_thunk` | `0x0042D230` | high | Adjusts TimerHandler this and enters NewLegendDialogPane's deleting destructor. |
| `ui_chatting_pane_handle_network_event` | `0x0042D240` | high | Routes exact server opcodes 0x0D SSay and 0x0A SMessage to ChattingPane handlers. |
| `ui_chatting_pane_ctor` | `0x0042D2D0` | high | Constructs exact RTTI ChattingPane and seeds seven blank display lines. |
| `ui_chatting_pane_dtor` | `0x0042D3C0` | high | Stops transcript recording and destroys the TextEditPane base. |
| `ui_chatting_pane_handle_keyboard_event` | `0x0042D440` | high | Handles chat scrolling and toggles transcript recording on modified J. |
| `ui_chatting_pane_append_formatted_text` | `0x0042D670` | high | Parses DBCS text and inline color tokens, appends styled runs, and mirrors them to an active transcript. |
| `ui_chatting_pane_handle_say_packet` | `0x0042D830` | high | Copies an SSay text body and appends it with the say color. |
| `ui_chatting_pane_handle_message_packet` | `0x0042D940` | high | Maps accepted SMessage subtypes to chat colors and appends their bounded bodies. |
| `ui_chatting_pane_append_text_run` | `0x0042DA90` | high | Appends and colors one text run, preserves scrolling selection, and writes it to the transcript. |
| `ui_chatting_pane_start_recording` | `0x0042DBC0` | high | Creates a character-and-local-time transcript file and appends the recording-start marker. |
| `ui_chatting_pane_stop_recording` | `0x0042DCA0` | high | Appends the recording-end marker, closes the transcript file, and clears recording state. |
| `ui_chatting_pane2_forward_message_packet` | `0x0042DD00` | high | Maps ChattingPane2 message subtypes to colors and forwards their bodies to the global chat pane. |
| `ui_chatting_append_global_message` | `0x0042DDE0` | high | Forwards a null-terminated message to the global ChattingPane with a selected color. |
| `ui_chatting_append_global_message_bytes` | `0x0042DE20` | high | Bounds and normalizes message bytes before appending them to the global ChattingPane. |
| `ui_chatting_pane_scalar_deleting_dtor` | `0x0042DF00` | high | Destroys ChattingPane and optionally frees its complete object. |
| `ui_chatting_pane_timer_scalar_deleting_dtor_thunk` | `0x0042DF30` | high | Adjusts TimerHandler this and enters ChattingPane's scalar deleting destructor. |
| `ui_intro_video_start_if_available` | `0x0042DF50` | high | Creates CIPane when needed and begins the requested intro-video sequence. |
| `ui_intro_video_pane_ctor` | `0x0042DFF0` | high | Initializes the CIPane vtable and Bink-backed video state. |
| `ui_intro_video_pane_dtor` | `0x0042E170` | high | Unregisters exact RTTI CIPane, clears its singleton, and destroys Pane. |
| `ui_intro_video_begin_sequence` | `0x0042E1F0` | high | Stores two clip resources and starts the first clip. |
| `ui_intro_video_close_assets` | `0x0042E290` | high | Releases both intro-video archive handles through the main archive manager. |
| `ui_intro_video_handle_keyboard_event` | `0x0042E580` | high | Makes an active intro-video sequence advance immediately on keyboard input. |
| `ui_intro_video_handle_pointer_event` | `0x0042E5C0` | high | Makes an active intro-video sequence advance immediately on pointer input. |
| `ui_intro_video_pane_scalar_deleting_dtor` | `0x0042E700` | high | Destroys CIPane and optionally frees its complete object. |
| `ui_intro_video_pane_singleton_register` | `0x0042E750` | high | Registers the containing CIPane in the intro-video singleton slot. |
| `ui_intro_video_pane_singleton_unregister` | `0x0042E790` | high | Clears the intro-video singleton when it matches the containing CIPane. |
| `ui_get_intro_video_pane` | `0x0042E7D0` | high | Returns the global CIPane instance at 0x006DA3A0. |
| `ui_intro_video_pane_timer_scalar_deleting_dtor_thunk` | `0x0042E7F0` | high | Adjusts TimerHandler this and enters CIPane's scalar deleting destructor. |
| `ui_show_input_block_clock` | `0x0042E800` | high | Creates the exact RTTI ClockPane singleton when absent and activates its 50 ms animated wait-cursor path. |
| `ui_hide_input_block_clock` | `0x0042E890` | high | Closes and destroys the active ClockPane singleton when present. |
| `ui_clock_pane_ctor` | `0x0042E8C0` | high | Constructs the 0x1A0-byte exact RTTI ClockPane, loads lodclk.epf metadata, centers it on the current pointer, and registers it in the screen and event trees. |
| `ui_clock_pane_dtor` | `0x0042EA70` | high | Restores ClockPane vtables, unregisters it from the event and screen trees, clears its singleton registration, and destroys the Pane base. |
| `ui_clock_pane_show` | `0x0042EB00` | high | Selects root cursor mode 3, shows ClockPane, draws its next frame, and schedules timer 0x1234 at 50 ms. |
| `ui_clock_pane_close` | `0x0042EBA0` | high | Cancels timer 0x1234, hides ClockPane, restores cursor mode 0, and notifies the optional cursor observer. |
| `ui_clock_pane_timer_callback` | `0x0042EC00` | high | Advances the lodclk.epf frame modulo the loaded frame count and requeues timer 0x1234 using the existing 50 ms interval. |
| `ui_clock_pane_handle_keyboard_event` | `0x0042EC70` | high | Returns true for every keyboard or text event so lower panes do not receive it while ClockPane is active. |
| `ui_clock_pane_handle_pointer_event` | `0x0042EC80` | high | Re-centers ClockPane on pointer-move events and returns true for every pointer event, consuming clicks and wheel input. |
| `ui_clock_pane_set_frame` | `0x0042ED00` | high | Loads and draws one lodclk.epf frame when its signed 16-bit selector differs from ClockPane +0x198. |
| `ui_clock_pane_scalar_deleting_dtor` | `0x0042EDC0` | high | Runs the complete ClockPane destructor and optionally frees the object when the scalar-delete flag is set. |
| `ui_clock_pane_singleton_register` | `0x0042EDF0` | high | Stores the containing ClockPane pointer from its Singleton subobject. |
| `ui_clock_pane_singleton_unregister` | `0x0042EE30` | high | Clears the ClockPane singleton when it still refers to the containing object. |
| `ui_has_clock_pane` | `0x0042EE70` | high | Reports whether clock_pane_singleton_ptr is non-null. |
| `ui_get_clock_pane` | `0x0042EE90` | high | Returns the active ClockPane singleton pointer. |
| `ui_clock_pane_timer_scalar_deleting_dtor_thunk` | `0x0042EEA0` | high | Adjusts a TimerHandler this pointer back to ClockPane and enters its scalar deleting destructor. |
| `ui_command_history_add` | `0x00430E30` | high | Adds a command to a 256-entry history, moving duplicates to the newest position. |
| `ui_command_line_input_pane_ctor` | `0x00430F50` | high | Constructs the command-line input pane and initializes its local history state. |
| `ui_command_line_input_pane_handle_keyboard_event` | `0x00430FB0` | high | Handles command-line editing, history traversal, submission, and cancellation keys. |
| `ui_command_line_input_pane_submit` | `0x00431170` | high | Submits the current line for parsing and records nonempty input in command history. |
| `ui_command_line_input_pane_scalar_deleting_dtor` | `0x00431600` | high | Compiler scalar-deleting destructor for the command-line input pane. |
| `ui_command_line_input_pane_timer_scalar_deleting_dtor_thunk` | `0x004316F0` | high | Adjusted-this TimerHandler scalar-deleting destructor thunk for the command-line input pane. |
| `ui_unitel_pane_ctor` | `0x00436B20` | high | Constructs exact RTTI UnitelPane and initializes its legacy endpoint-integration state. |
| `ui_unitel_pane_dtor` | `0x00436BA0` | high | Destroys exact RTTI UnitelPane and its Pane base. |
| `ui_unitel_pane_apply_endpoint_message` | `0x00436C10` | high | Parses an ampersand-delimited Unitel host, port, and identifier message and updates the Config endpoint. |
| `ui_unitel_pane_scalar_deleting_dtor` | `0x004374E0` | high | Compiler scalar-deleting destructor for UnitelPane. |
| `ui_unitel_pane_singleton_register` | `0x004379B0` | high | Registers the UnitelPane singleton. |
| `ui_unitel_pane_singleton_unregister` | `0x004379F0` | high | Clears the UnitelPane singleton when the supplied instance owns it. |
| `ui_unitel_pane_timer_scalar_deleting_dtor_thunk` | `0x00437A30` | high | Adjusted-this TimerHandler scalar-deleting destructor thunk for UnitelPane. |
| `ui_control_set_focus_outline_enabled` | `0x00437E60` | high | Copies the dialog-wide focus-outline policy into ControlPane offset 0x19B. |
| `ui_control_ctor` | `0x00437E80` | high | Constructs exact RTTI ControlPane and initializes its control kind, rectangle, enabled state, palette index, and focus-outline flag. |
| `ui_control_set_color_index` | `0x00437F60` | high | Changes the ControlPane palette index and invalidates its rectangle. |
| `ui_control_enable` | `0x00437FA0` | high | Sets the common ControlPane enabled flag and invalidates the control. |
| `ui_control_disable` | `0x00437FE0` | high | Clears the common ControlPane enabled flag and invalidates the control. |
| `ui_progress_bar_control_ctor` | `0x00438020` | high | Constructs exact RTTI ProgressBarControlPane and loads its two bar pixmaps. |
| `ui_progress_bar_control_dtor` | `0x00438170` | high | Destroys ProgressBarControlPane through the ControlPane base. |
| `ui_progress_bar_control_draw` | `0x004381A0` | high | Draws the progress background and foreground segments using the current progress value. |
| `ui_button_control_ctor` | `0x00438290` | high | Constructs exact RTTI ButtonControlPane and initializes state, toggle lock, and focus. |
| `ui_button_control_dtor` | `0x00438310` | high | Destroys ButtonControlPane through the ControlPane base. |
| `ui_button_control_set_state` | `0x00438340` | high | Changes the button state unless toggle locking suppresses the transition. |
| `ui_button_control_invalidate` | `0x004383A0` | high | Invalidates the button rectangle. |
| `ui_button_control_set_toggle_lock` | `0x004383C0` | high | Sets the ButtonControlPane toggle-lock flag. |
| `ui_button_control_set_color_index` | `0x00438440` | high | Forwards palette-index changes to ControlPane. |
| `ui_button_control_enable` | `0x00438490` | high | Enables ButtonControlPane through ControlPane. |
| `ui_button_control_disable` | `0x004384D0` | high | Disables ButtonControlPane through ControlPane. |
| `ui_button_control_focus` | `0x00438510` | high | Sets the button focus flag and invalidates its rectangle. |
| `ui_button_control_unfocus` | `0x00438550` | high | Clears the button focus flag and invalidates its rectangle. |
| `ui_button_control_handle_keyboard_event` | `0x00438590` | high | Consumes Enter or Space and sends dialog action 8 with the control ID. |
| `ui_text_button_control_refresh_label` | `0x00438600` | high | Rebuilds the centered child label pane for TextButtonControlPane. |
| `ui_text_button_control_ctor` | `0x004386D0` | high | Constructs exact RTTI TextButtonControlPane and creates its child label pane. |
| `ui_text_button_control_dtor` | `0x00438810` | high | Destroys the owned label pane and ButtonControlPane base. |
| `ui_text_button_control_copy_label` | `0x004388C0` | high | Copies the child label into a bounded caller buffer. |
| `ui_text_button_control_register_screen` | `0x00438940` | high | Registers TextButtonControlPane and attaches its child label pane. |
| `ui_text_button_control_unregister_screen` | `0x00438A00` | high | Detaches the child label pane and unregisters TextButtonControlPane. |
| `ui_text_button_control_draw` | `0x00438A70` | high | Draws the text-button frame, focus feedback, and child label. |
| `ui_text_button_control_get_label_rect` | `0x00438CC0` | high | Computes the centered label rectangle inside TextButtonControlPane. |
| `ui_text_button_ex_control_refresh_label` | `0x00438DC0` | high | Rebuilds the centered child label pane for TextButtonExControlPane. |
| `ui_text_button_ex_control_ctor` | `0x00438E90` | high | Constructs exact RTTI TextButtonExControlPane and creates its child label pane. |
| `ui_text_button_ex_control_dtor` | `0x00438FD0` | high | Destroys the owned label pane and ButtonControlPane base. |
| `ui_text_button_ex_control_copy_label` | `0x00439080` | high | Copies the TextButtonEx label with DBCS-aware length clamping and a local terminator. |
| `ui_text_button_ex_control_register_screen` | `0x00439100` | high | Registers TextButtonEx and attaches its owned child text pane. |
| `ui_text_button_ex_control_unregister_screen` | `0x004391C0` | high | Detaches the owned child text pane and unregisters TextButtonEx. |
| `ui_text_button_ex_control_draw` | `0x00439230` | high | Draws an extended button frame from buttonex.epf or btn220.epf and then focus feedback. |
| `ui_text_button_ex_control_get_label_rect` | `0x004393C0` | high | Centers a 6-pixel-per-byte, 12-pixel-high label and clips it to the control bounds. |
| `ui_get_default_button_skin_rect` | `0x004394C0` | high | Loads and caches the first butt001.epf image bounds. |
| `ui_offset_default_button_skin_rect` | `0x00439560` | high | Returns the cached butt001.epf bounds offset by a caller-supplied origin. |
| `ui_image_button_control_ctor` | `0x00439640` | high | Constructs exact RTTI ImageButtonControlPane with three pixmap slots. |
| `ui_image_button_control_load_images` | `0x00439700` | high | Loads three consecutive butt001.epf frames or copies three caller-supplied pixmaps. |
| `ui_image_button_control_dtor` | `0x00439830` | high | Destroys ImageButtonControlPane through ButtonControlPane. |
| `ui_image_button_control_draw` | `0x00439860` | high | Draws the pixmap selected by button state and optional enabled focus feedback. |
| `ui_image_button_ex_control_ctor` | `0x004399B0` | high | Constructs exact RTTI ImageButtonExControlPane and its optional child label. |
| `ui_image_button_ex_control_dtor` | `0x00439AD0` | high | Destroys the owned ImageButtonEx label pane and ImageButtonControlPane base. |
| `ui_image_button_ex_control_set_label` | `0x00439B50` | high | Creates or refreshes the centered ImageButtonEx child text pane. |
| `ui_image_button_ex_control_register_screen` | `0x00439DC0` | high | Registers ImageButtonEx and attaches its child label pane. |
| `ui_image_button_ex_control_unregister_screen` | `0x00439E70` | high | Detaches the child label pane and unregisters ImageButtonEx. |
| `ui_radio_group_control_ctor` | `0x00439EB0` | high | Constructs exact RTTI RadioGroupControlPane with an empty option list. |
| `ui_radio_group_control_dtor` | `0x00439F00` | high | Destroys the owned radio-option list and ControlPane base. |
| `ui_radio_group_control_add_option` | `0x00439FB0` | high | Lazily creates the option collection and appends a bounded label plus rectangle. |
| `ui_radio_group_control_remove_option` | `0x0043A0E0` | high | Removes a radio option through the owned collection. |
| `ui_radio_group_control_set_selected` | `0x0043A110` | high | Invalidates the old and new option rectangles and stores the selected index. |
| `ui_radio_group_control_handle_mouse_event` | `0x0043A190` | high | Selects the hit radio option on a primary-button mouse event. |
| `ui_radio_group_control_hit_test` | `0x0043A220` | high | Returns a hit option index with bit 0x40 set or sentinel 7. |
| `ui_radio_group_control_draw` | `0x0043A2C0` | high | Draws every radio option in collection order. |
| `ui_radio_group_control_get_option_count` | `0x0043A320` | high | Returns the radio-option count or zero before allocation. |
| `ui_radio_group_control_get_option` | `0x0043A350` | high | Returns one radio-option record from the owned collection. |
| `ui_radio_group_control_get_option_rect` | `0x0043A380` | high | Copies one radio option's four-coordinate rectangle. |
| `ui_radio_group_control_draw_option` | `0x0043A3C0` | high | Draws one indicator and label using enabled, hover, and selected palette states. |
| `ui_scrollable_control_ctor` | `0x0043A790` | high | Constructs exact RTTI ScrollableControlPane around an owned child pane. |
| `ui_scrollable_control_dtor` | `0x0043A840` | high | Queues the owned child pane for destruction and destroys ControlPane. |
| `ui_scrollable_control_set_scroll_max` | `0x0043A8D0` | high | Selects a child scrollbar and clamps its maximum value to 0..30000. |
| `ui_scrollable_control_set_scroll_position` | `0x0043A900` | high | Selects a child scrollbar and updates its position within the configured maximum. |
| `ui_scrollable_control_get_scroll_max` | `0x0043A930` | high | Returns the selected child scrollbar maximum or zero when absent. |
| `ui_scrollable_control_get_scroll_position` | `0x0043A950` | high | Returns the selected child scrollbar position or zero when absent. |
| `ui_scrollable_control_set_rect` | `0x0043A970` | high | Updates the control rectangle and forwards the local rectangle to the child. |
| `ui_scrollable_control_handle_pointer_event` | `0x0043A9B0` | high | Forwards the primary-vtable +0x48 pointer event to the owned child pane. |
| `ui_scrollable_control_handle_keyboard_event` | `0x0043A9E0` | high | Forwards the primary-vtable +0x4C keyboard event to the owned child pane. |
| `ui_scrollable_control_handle_network_event` | `0x0043AA10` | high | Forwards the primary-vtable +0x50 network event and normalizes its consumed result. |
| `ui_scrollable_control_timer_callback` | `0x0043AA50` | high | Forwards TimerHandler callbacks to the owned child pane's TimerHandler subobject. |
| `ui_scrollable_control_enable` | `0x0043AA90` | high | Enables ScrollableControlPane through ControlPane. |
| `ui_scrollable_control_disable` | `0x0043AAB0` | high | Disables ScrollableControlPane through ControlPane. |
| `ui_scrollable_control_focus` | `0x0043AAD0` | high | Sets the scrollable control focus state and invalidates its rectangle. |
| `ui_scrollable_control_unfocus` | `0x0043AB10` | high | Clears the scrollable control focus state and invalidates its rectangle. |
| `ui_scrollable_control_register_screen` | `0x0043AB50` | high | Registers the control, updates the child's local rectangle, and attaches the child. |
| `ui_scrollable_control_unregister_screen` | `0x0043ACB0` | high | Detaches the owned child pane and unregisters ScrollableControlPane. |
| `ui_scrollable_control_draw` | `0x0043ACE0` | high | Draws the scrollable surface and uses palette index 31 for its active state. |
| `ui_text_edit_control_default_ctor` | `0x0043AD10` | high | Constructs an empty exact RTTI TextEditControlPane and captures the shared text-input service. |
| `ui_text_edit_control_ctor` | `0x0043ADE0` | high | Constructs TextEditControlPane, its text canvas, margins, initial text, and edit state. |
| `ui_text_edit_control_dtor` | `0x0043B0E0` | high | Destroys the child text canvas and ControlPane base. |
| `ui_text_edit_control_enable_masked_input` | `0x0043B190` | high | Enables masked input used by password, birth-date, and other sensitive fields. |
| `ui_text_edit_control_set_text_flag` | `0x0043B1C0` | high | Sets, clears, or queries one child text-canvas option bit. |
| `ui_text_edit_control_copy_text` | `0x0043B1F0` | high | Copies child text with DBCS-aware length clamping and a local terminator. |
| `ui_text_edit_control_is_empty` | `0x0043B270` | high | Reports whether the child text canvas contains zero bytes. |
| `ui_text_edit_control_clear_text` | `0x0043B2A0` | high | Removes the child canvas's full current text range. |
| `ui_text_edit_control_set_text` | `0x0043B2D0` | high | Clears the child canvas and inserts supplied formatted text. |
| `ui_text_edit_control_register_screen` | `0x0043B300` | high | Registers TextEditControlPane and attaches its child text canvas. |
| `ui_text_edit_control_unregister_screen` | `0x0043B3C0` | high | Detaches the child text canvas and unregisters TextEditControlPane. |
| `ui_text_edit_control_handle_pointer_event` | `0x0043B430` | high | Forwards primary-vtable +0x48 pointer input to the child text canvas. |
| `ui_text_edit_control_handle_keyboard_event` | `0x0043B460` | high | Forwards primary-vtable +0x4C keyboard input to the child text canvas. |
| `ui_text_edit_control_handle_application_event` | `0x0043B490` | high | Forwards primary-vtable +0x54 application or IME input to the child text canvas. |
| `ui_text_edit_control_unfocus` | `0x0043B4C0` | high | Leaves editing mode and collapses the child selection to the caret. |
| `ui_text_edit_control_focus` | `0x0043B550` | high | Enters editing mode, resets caret state, and optionally selects all text. |
| `ui_text_edit_control_set_max_bytes` | `0x0043B610` | high | Sets and immediately enforces the child text byte limit. |
| `ui_text_edit_control_set_max_lines` | `0x0043B640` | high | Sets and immediately enforces the child text line limit. |
| `ui_text_edit_control_draw_content` | `0x0043B670` | high | Draws the text-edit border and composites the child text canvas. |
| `ui_static_text_control_ctor` | `0x0043B750` | high | Constructs exact RTTI StaticTextControlPane and its noneditable child canvas. |
| `ui_static_text_control_dtor` | `0x0043B9E0` | high | Destroys StaticTextControlPane and its child canvas. |
| `ui_static_text_control_draw_content` | `0x0043BA90` | high | Composites the StaticText child canvas into the control. |
| `ui_static_text_control_handle_pointer_event` | `0x0043BB00` | high | Forwards pointer input only when the interaction flag is enabled. |
| `ui_static_text_control_handle_keyboard_event` | `0x0043BB30` | high | Forwards keyboard input only when the interaction flag is enabled. |
| `ui_static_text_control_handle_application_event` | `0x0043BB60` | high | Forwards application or IME input only when the interaction flag is enabled. |
| `ui_static_text_control2_ctor` | `0x0043BB90` | high | Constructs exact RTTI StaticTextControlPane2 as a noneditable text control. |
| `ui_static_text_control2_dtor` | `0x0043BC40` | high | Destroys StaticTextControlPane2 through TextEditControlPane. |
| `ui_progress_bar_ex_control_ctor` | `0x0043BC90` | high | Constructs exact RTTI ProgressBarControlPaneEx with fill and palette fields. |
| `ui_progress_bar_ex_control_dtor` | `0x0043BD00` | high | Destroys ProgressBarControlPaneEx through ControlPane. |
| `ui_progress_bar_ex_control_draw_content` | `0x0043BD30` | high | Draws a bordered proportional vertical fill from current and maximum values. |
| `ui_image_control_ctor` | `0x0043BE20` | high | Constructs exact RTTI ImageControlPane and copies its initial pixmap. |
| `ui_image_control_dtor` | `0x0043BEB0` | high | Destroys ImageControlPane through ControlPane. |
| `ui_image_control_set_image` | `0x0043BEE0` | high | Copies or clears the retained pixmap and invalidates the control. |
| `ui_image_control_draw_content` | `0x0043BF30` | high | Draws the ImageControlPane surface and retained pixmap. |
| `ui_control_scalar_deleting_dtor` | `0x0043BF80` | high | Compiler scalar-deleting destructor for ControlPane. |
| `ui_progress_bar_control_scalar_deleting_dtor` | `0x0043BFB0` | high | Compiler scalar-deleting destructor for ProgressBarControlPane. |
| `ui_button_control_scalar_deleting_dtor` | `0x0043BFE0` | high | Compiler scalar-deleting destructor for ButtonControlPane. |
| `ui_text_button_control_scalar_deleting_dtor` | `0x0043C010` | high | Compiler scalar-deleting destructor for TextButtonControlPane. |
| `ui_text_button_ex_control_scalar_deleting_dtor` | `0x0043C040` | high | Compiler scalar-deleting destructor for TextButtonExControlPane. |
| `ui_image_button_control_scalar_deleting_dtor` | `0x0043C070` | high | Compiler scalar-deleting destructor for ImageButtonControlPane. |
| `ui_image_button_ex_control_scalar_deleting_dtor` | `0x0043C0A0` | high | Compiler scalar-deleting destructor for ImageButtonExControlPane. |
| `ui_radio_group_control_scalar_deleting_dtor` | `0x0043C0D0` | high | Compiler scalar-deleting destructor for RadioGroupControlPane. |
| `ui_scrollable_control_scalar_deleting_dtor` | `0x0043C100` | high | Compiler scalar-deleting destructor for ScrollableControlPane. |
| `ui_text_edit_control_scalar_deleting_dtor` | `0x0043C130` | high | Compiler scalar-deleting destructor for TextEditControlPane. |
| `ui_static_text_control_scalar_deleting_dtor` | `0x0043C160` | high | Compiler scalar-deleting destructor for StaticTextControlPane. |
| `ui_static_text_control2_scalar_deleting_dtor` | `0x0043C190` | high | Compiler scalar-deleting destructor for StaticTextControlPane2. |
| `ui_progress_bar_ex_control_scalar_deleting_dtor` | `0x0043C1C0` | high | Compiler scalar-deleting destructor for ProgressBarControlPaneEx. |
| `ui_image_control_scalar_deleting_dtor` | `0x0043C1F0` | high | Compiler scalar-deleting destructor for ImageControlPane. |
| `ui_has_text_input_service` | `0x0043C220` | high | Reports whether the shared text-input service exists. |
| `ui_get_text_input_service` | `0x0043C240` | high | Returns the shared text-input service pointer. |
| `ui_image_control_timer_scalar_deleting_dtor_thunk` | `0x0043C250` | high | Adjusted-this TimerHandler deleting-destructor thunk for ImageControlPane. |
| `ui_progress_bar_control_timer_scalar_deleting_dtor_thunk` | `0x0043C260` | high | Adjusted-this TimerHandler deleting-destructor thunk for ProgressBarControlPane. |
| `ui_scrollable_control_timer_scalar_deleting_dtor_thunk` | `0x0043C270` | high | Adjusted-this TimerHandler deleting-destructor thunk for ScrollableControlPane. |
| `ui_text_button_ex_control_timer_scalar_deleting_dtor_thunk` | `0x0043C280` | high | Adjusted-this TimerHandler deleting-destructor thunk for TextButtonExControlPane. |
| `ui_progress_bar_ex_control_timer_scalar_deleting_dtor_thunk` | `0x0043C290` | high | Adjusted-this TimerHandler deleting-destructor thunk for ProgressBarControlPaneEx. |
| `ui_button_control_timer_scalar_deleting_dtor_thunk` | `0x0043C2A0` | high | Adjusted-this TimerHandler deleting-destructor thunk for ButtonControlPane. |
| `ui_static_text_control2_timer_scalar_deleting_dtor_thunk` | `0x0043C2B0` | high | Adjusted-this TimerHandler deleting-destructor thunk for StaticTextControlPane2. |
| `ui_static_text_control_timer_scalar_deleting_dtor_thunk` | `0x0043C2C0` | high | Adjusted-this TimerHandler deleting-destructor thunk for StaticTextControlPane. |
| `ui_text_edit_control_timer_scalar_deleting_dtor_thunk` | `0x0043C2D0` | high | Adjusted-this TimerHandler deleting-destructor thunk for TextEditControlPane. |
| `ui_image_button_control_timer_scalar_deleting_dtor_thunk` | `0x0043C2E0` | high | Adjusted-this TimerHandler deleting-destructor thunk for ImageButtonControlPane. |
| `ui_image_button_ex_control_timer_scalar_deleting_dtor_thunk` | `0x0043C2F0` | high | Adjusted-this TimerHandler deleting-destructor thunk for ImageButtonExControlPane. |
| `ui_radio_group_control_timer_scalar_deleting_dtor_thunk` | `0x0043C300` | high | Adjusted-this TimerHandler deleting-destructor thunk for RadioGroupControlPane. |
| `ui_text_button_control_timer_scalar_deleting_dtor_thunk` | `0x0043C310` | high | Adjusted-this TimerHandler deleting-destructor thunk for TextButtonControlPane. |
| `ui_control_timer_scalar_deleting_dtor_thunk` | `0x0043C320` | high | Adjusted-this TimerHandler deleting-destructor thunk for ControlPane. |
| `ui_create_user_dialog_ctor` | `0x0043C370` | high | Constructs RTTI class CreateUserDialogPane from _ncreate.txt, attaches appearance controls and account fields, and registers the pane for events and timers. |
| `ui_create_user_dialog_dtor` | `0x0043D080` | high | Destroys CreateUserDialogPane preview resources, bottom-button state, local appearance storage, and DialogPane. |
| `ui_create_user_draw` | `0x0043D190` | high | Draws the creation preview using gender at +0x674, hair style at +0x676, and hair-color palette index at +0x678. |
| `ui_create_user_find_palette_option_index` | `0x0043D5E0` | high | Finds the current appearance palette value in the 14-entry swatch table used by the selection marker. |
| `ui_create_user_update_submit_enabled` | `0x0043D620` | high | Enables submit only when required fields are nonempty and the optional paired fields are both empty or both populated. |
| `ui_create_user_advance_preview_frame` | `0x0043D7B0` | high | Advances the character preview through five frames and invalidates its rectangle. |
| `ui_create_user_handle_pointer_event` | `0x0043DC80` | high | Handles CreateUserDialogPane appearance clicks, including gender selection and conversion of the 2-by-7 hair-color swatch grid into palette indexes. |
| `ui_no_nexon_club_id_warning_pane_ctor` | `0x0043E9D0` | high | Constructs exact RTTI NoNexonClubIDWarningPane and stores its owner plus confirm and cancel timer IDs. |
| `ui_no_nexon_club_id_warning_confirm` | `0x0043EA30` | high | Schedules the stored confirmation timer on the owning create-user pane after 200 ms. |
| `ui_no_nexon_club_id_warning_cancel` | `0x0043EA80` | high | Schedules the stored cancellation timer on the owning create-user pane after 200 ms when configured. |
| `ui_create_user_handle_action` | `0x0043EAD0` | high | Collects name, password, confirmation, and distribution-dependent account text; checks matching passwords and schedules the create-user send timer. |
| `ui_create_user_timer` | `0x0043F410` | high | CreateUserDialogPane TimerHandler callback; timer 3 sends CNewUser after the form action schedules a 200 ms delay. |
| `ui_create_user_accept_opcode_30` | `0x0043F8C0` | high | Returns handled for raw server opcode 0x30 without reading the body or changing CreateUserDialogPane state. |
| `ui_create_user_dialog_scalar_deleting_dtor` | `0x0043FBE0` | high | Compiler scalar-deleting destructor for CreateUserDialogPane. |
| `ui_dialog_pane_scalar_deleting_dtor` | `0x0043FC10` | high | Compiler scalar-deleting destructor for exact RTTI DialogPane. |
| `ui_create_user_dialog_timer_scalar_deleting_dtor_thunk` | `0x0043FDA0` | high | Adjusted-this TimerHandler scalar-deleting destructor thunk for CreateUserDialogPane. |
| `ui_dialog_pane_timer_scalar_deleting_dtor_thunk` | `0x0043FDB0` | high | Adjusted-this TimerHandler scalar-deleting destructor thunk for DialogPane. |
| `ui_dialog_pane_ctor` | `0x00445260` | high | Constructs DialogPane over Pane; initializes default, cancel, focus, pressed, hover, and pointer-target control indexes to -1, with no-hit zones set to 7 where required. |
| `ui_dialog_pane_dtor` | `0x004453A0` | high | Destroys attached dialog controls in reverse attachment order, destroys the control collection, and then destroys the Pane base. |
| `ui_dialog_set_drag_bounds` | `0x004454F0` | high | Enables bounded dialog dragging and copies the minimum and maximum x/y coordinates used by the pointer handler. |
| `ui_dialog_clear_drag_bounds` | `0x00445550` | high | Disables the optional bounds that clamp dialog movement while dragging. |
| `ui_dialog_set_title_text` | `0x00445570` | high | Copies up to 0x400 bytes of dialog text into the pane and invalidates the dialog for redraw. |
| `ui_dialog_set_archive_background` | `0x004455B0` | high | Stores a background image name and either copies a supplied pixmap or loads it from the main image archive. |
| `ui_dialog_load_background_file` | `0x00445620` | high | Stores a background image path and loads the dialog pixmap through the general image-file loader. |
| `ui_dialog_add_control` | `0x00445670` | high | Creates DialogPane +0x594 on first use and inserts the supplied control pointer. |
| `ui_dialog_remove_control` | `0x00445770` | high | Removes the control at the selected attachment index from the dialog's local control collection. |
| `ui_dialog_get_control_count` | `0x004457A0` | high | Returns the number of attachment-order controls, or zero when the DialogPane has no control list. |
| `ui_dialog_set_default_action` | `0x004457D0` | high | Stores an attachment-order control index at DialogPane +0x598. |
| `ui_dialog_set_cancel_action` | `0x00445820` | high | Stores an attachment-order control index at DialogPane +0x59C. |
| `ui_dialog_register_screen` | `0x00445870` | high | Registers the dialog as a screen and attaches each local control to the dialog. |
| `ui_dialog_unregister_screen` | `0x00445970` | high | Detaches each local control, then unregisters the dialog screen. |
| `ui_dialog_handle_pointer_event` | `0x00445A20` | high | DialogPane primary-vtable +0x48 implementation for pane dragging, hit testing, child dispatch, visual-hover and secondary pointer-transition state, and same-control/same-zone click activation. |
| `ui_dialog_handle_keyboard_event` | `0x00445FF0` | high | DialogPane primary-vtable +0x4C implementation: Tab traverses focus, Enter and Space normally dispatch the default action, Escape dispatches cancel, and remaining input reaches the focused enabled control. |
| `ui_dialog_focused_control_uses_text_input` | `0x00446260` | high | Returns the enabled focused control's virtual text-input mode, or false when no eligible control has focus. |
| `ui_dialog_handle_application_event` | `0x004462D0` | high | DialogPane primary-vtable +0x54 implementation that forwards application and IME events to the focused control. |
| `ui_dialog_draw` | `0x00446360` | high | Runs the dialog background and content drawing hooks over the pane rectangle. |
| `ui_dialog_draw_background` | `0x004463C0` | high | Draws the configured dialog background or lazily loads the default DlgBack2.spf skin. |
| `ui_dialog_draw_default_frame` | `0x004464A0` | high | Draws the tiled default dialog frame when no named custom background is configured. |
| `ui_dialog_hit_test_control` | `0x004468C0` | high | Walks DialogPane controls, checks each rectangle, and calls control virtual +0x78 for a local hit-zone code. |
| `ui_dialog_update_hover_state` | `0x00446A10` | high | Updates DialogPane +0x5BC/+0x5C0 and sends visual hit-zone changes to the old and new controls; index -1 and zone 7 mean no hit. |
| `ui_dialog_update_pointer_target` | `0x00446AE0` | high | Updates the secondary pointer-transition target at +0x5C4/+0x5C8 and calls old-control or new-control transition hooks when the control or zone changes. |
| `ui_dialog_set_focused_control` | `0x00446BC0` | high | Transitions DialogPane +0x5AC between control indexes and invokes old/new focus hooks. |
| `ui_dialog_focus_previous_control` | `0x00446CD0` | high | Searches backward with wrapping for an enabled, focusable control. |
| `ui_dialog_focus_next_control` | `0x00446DD0` | high | Searches forward with wrapping for an enabled, focusable control. |
| `ui_dialog_dispatch_default_action` | `0x00446EE0` | high | Dispatches the enabled control selected by DialogPane +0x598 through the parent action handler with keyboard action code 8. |
| `ui_dialog_dispatch_cancel_action` | `0x00446F60` | high | Dispatches the enabled control selected by DialogPane +0x59C through the parent action handler with keyboard action code 8. |
| `ui_dialog_dispatch_pointer_to_control` | `0x00446FE0` | high | Converts pointer coordinates to control-local space, calls control virtual +0x48, and restores the event. |
| `ui_dialog_refresh_default_action_state` | `0x00447090` | high | Refreshes the default action control through the dialog hook and invalidates it when its enabled state changes. |
| `ui_alert_pane_ctor_wrapped_c_string` | `0x00447160` | high | Constructs an AlertPane from terminated text with caller-selected wrapping and one or two buttons. |
| `ui_alert_pane_ctor_c_string` | `0x004478A0` | high | Constructs an AlertPane from terminated text using the fixed 40-byte wrapping path and optional owner rectangle. |
| `ui_alert_pane_ctor` | `0x00448000` | high | Constructs exact RTTI class AlertPane from counted display text, a parent pane, and one or two button assets. |
| `ui_alert_pane_handle_action` | `0x00448770` | high | Dispatches the first or second alert choice for attachment actions 0 or 2, then closes and queues the pane. |
| `ui_yes_no_alert_pane_ctor` | `0x004487E0` | high | Constructs the exact RTTI YesNoAlertPane with Yes and No buttons and retained callback state. |
| `ui_yes_no_alert_pane_choose_yes` | `0x00448840` | high | Invokes the retained YesNoAlertPane callback with true. |
| `ui_yes_no_alert_pane_choose_no` | `0x00448880` | high | Invokes the retained YesNoAlertPane callback with false. |
| `ui_window_message_dialog_pane_ctor` | `0x004488C0` | high | Builds the standard scrollable or alternate woodbook-style SMessage popup from an explicit byte buffer. |
| `ui_window_message_dialog_close` | `0x00448E10` | high | Unregisters, hides, and queues the window-message dialog for deferred deletion. |
| `ui_window_message_dialog_handle_action` | `0x00448E50` | high | Closes the window-message dialog only for attachment action zero. |
| `ui_dialog_pane_scalar_deleting_dtor_variant` | `0x00448E80` | high | Runs the alternate DialogPane scalar deleting destructor associated with its RTTI vtable. |
| `ui_alert_pane_scalar_deleting_dtor` | `0x00448EB0` | high | Runs the exact RTTI AlertPane destructor and conditionally frees the complete object. |
| `ui_yes_no_alert_pane_scalar_deleting_dtor` | `0x00448EE0` | high | Runs the exact RTTI YesNoAlertPane destructor and conditionally frees the complete object. |
| `ui_window_message_dialog_pane_scalar_deleting_dtor` | `0x00448F10` | high | Runs the exact RTTI WindowMessageDialogPane destructor and conditionally frees the complete object. |
| `ui_dialog_pane_timer_scalar_deleting_dtor_variant_thunk` | `0x00448F40` | high | Adjusts the TimerHandler subobject pointer by 0x11C before the alternate DialogPane deleting destructor. |
| `ui_window_message_dialog_pane_timer_scalar_deleting_dtor_thunk` | `0x00448F50` | high | Adjusts the TimerHandler subobject pointer before the WindowMessageDialogPane deleting destructor. |
| `ui_alert_pane_timer_scalar_deleting_dtor_thunk` | `0x00448F60` | high | Adjusts the TimerHandler subobject pointer before the AlertPane deleting destructor. |
| `ui_yes_no_alert_pane_timer_scalar_deleting_dtor_thunk` | `0x00448F70` | high | Adjusts the TimerHandler subobject pointer before the YesNoAlertPane deleting destructor. |
| `ui_dragged_pane_set_pointer_origin` | `0x004566C0` | high | Stores pointer coordinates used as the DraggedPane movement and drop origin. |
| `ui_dragged_pane_ctor` | `0x004566F0` | high | Constructs exact RTTI DraggedPane, captures the mouse, and replaces any active dragged pane. |
| `ui_dragged_pane_dtor` | `0x00456830` | high | Destroys exact RTTI DraggedPane, releases retained state and mouse capture, and clears the active pointer. |
| `ui_dragged_pane_handle_pointer_event` | `0x004568F0` | high | Handles drag movement, hover, and release and dispatches the final drop through the screen hierarchy. |
| `ui_dragged_pane_handle_pointer_event_tail` | `0x00456997` | high | Compiler-split false-return tail inside the DraggedPane pointer-event handler. |
| `ui_dragged_pane_register_screen` | `0x00456C70` | high | Registers a DraggedPane, notifies its owner about the drag rectangle, and opens it. |
| `ui_dragged_pane_unregister_screen` | `0x00456D50` | high | Notifies the retained owner when required and unregisters the DraggedPane. |
| `ui_dragged_pane_handle_event_0x90` | `0x00456D90` | high | Consumes event family 8 code 0x90 according to the DraggedPane retained state flag. |
| `ui_dragged_pane_dispatch_drop_at_origin` | `0x00456DD0` | high | Finds the screen under the stored pointer origin and invokes the drop-target callback. |
| `ui_dragged_pane_scalar_deleting_dtor` | `0x00456EB0` | high | Runs the DraggedPane destructor and conditionally frees the complete object. |
| `ui_dragged_pane_timer_scalar_deleting_dtor_thunk` | `0x00456EE0` | high | Adjusts the TimerHandler pointer before the DraggedPane scalar deleting destructor. |
| `ui_emoticon_select_pane_ctor` | `0x00459470` | high | Constructs exact RTTI EmoticonSelectPane_A and initializes its eight option groups. |
| `ui_emoticon_select_pane_dtor` | `0x00459910` | high | Destroys exact RTTI EmoticonSelectPane_A and runs the Pane base destructor. |
| `ui_emoticon_select_pane_hit_test_option` | `0x00459940` | high | Returns the emoticon option containing a local pointer coordinate, or -1. |
| `ui_emoticon_select_pane_draw` | `0x004599D0` | high | Draws the selector background, eight option states, and current option description. |
| `ui_emoticon_select_pane_invalidate_option` | `0x00459BF0` | high | Invalidates one of the eight emoticon option rectangles. |
| `ui_emoticon_select_pane_set_option_description` | `0x00459C30` | high | Copies the fixed description string for one emoticon option. |
| `ui_emoticon_select_pane_invalidate_description` | `0x00459C70` | high | Invalidates the emoticon selector description rectangle. |
| `ui_emoticon_select_pane_open` | `0x00459C90` | high | Resets hover selection and registers and shows the selector once. |
| `ui_emoticon_select_pane_close` | `0x00459D00` | high | Unregisters and hides the emoticon selector when open. |
| `ui_emoticon_select_pane_handle_keyboard_event` | `0x00459D40` | high | Selects emoticons from numeric keys and handles selector close or refresh keys. |
| `ui_emoticon_select_pane_handle_pointer_event` | `0x00459EA0` | high | Updates hover state and commits an emoticon on pointer selection. |
| `ui_emoticon_select_pane_set_selected_option` | `0x00459FB0` | high | Clamps and stores the selected option and refreshes its description. |
| `ui_employee_dialog_ctor` | `0x0045AF00` | high | Constructs exact RTTI EmployeeDialogPane from lshop0.txt, applies an SMercenary Open body, registers the pane, and sends CMercenary RequestInfo. |
| `ui_employee_dialog_dtor` | `0x0045B7C0` | high | Unregisters and destroys EmployeeDialogPane and its attached controls. |
| `ui_employee_dialog_handle_action` | `0x0045BD90` | high | Routes employee-shop controls and item operations to the CMercenary action builders. |
| `ui_employee_dialog_timer_callback` | `0x0045C200` | high | Executes the employee pane's queued item, quantity, price, and confirmation operations on its TimerHandler callback. |
| `ui_employee_dialog_handle_network_event` | `0x0045C860` | high | Consumes decoded SMercenary bodies for the employee ID owned by this pane. |
| `ui_employee_dialog_apply_server_body` | `0x0045C8C0` | high | Dispatches SMercenary message codes 0 through 4. |
| `ui_employee_dialog_apply_open` | `0x0045CA10` | high | Reads gold, capacity, item count, and the initial employee records. |
| `ui_employee_dialog_apply_add_item` | `0x0045CBC0` | high | Reads one employee item record for SMercenary message code 1. |
| `ui_employee_dialog_apply_remove_item` | `0x0045CDB0` | high | Reads the u32 item ID for SMercenary message code 2 and removes the matching record. |
| `ui_employee_dialog_apply_start_trade` | `0x0045CE80` | high | Reads a previous item ID and replacement trade record for SMercenary message code 3. |
| `ui_employee_dialog_apply_request_response` | `0x0045D0A0` | high | Reads and displays the string8 response for SMercenary message code 4. |
| `ui_employee_dialog_rebuild_visible_items` | `0x0045D5E0` | high | Rebuilds the employee pane's visible item controls from the current records. |
| `ui_equip_pane_handle_network_event` | `0x0045D970` | high | Exact RTTI class EquipPane routes SAddEquip, SRemoveEquip, and SSelfLook from its primary-vtable network-event slot. |
| `ui_equip_pane_ctor` | `0x0045DA10` | high | Constructs exact RTTI class EquipPane over a 0x630-byte DialogPane base, 18 contiguous 0x34-byte slot-view records, profile text, named layout rectangles, and the worn-equipment arrays. |
| `ui_equip_pane_handle_action` | `0x0045F260` | high | EquipPane action 0x19 allocates the exact RTTI FamilyListDialogPane. |
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
| `ui_family_list_dialog_ctor` | `0x00471320` | high | Constructs FamilyListDialogPane from lfamily.txt, populates local rows, registers the pane, and sends CRequestFamilyName. |
| `ui_family_list_dialog_handle_network_event` | `0x00471A20` | high | Consumes exact RTTI SFamilyName while FamilyListDialogPane is open. |
| `ui_family_list_dialog_apply_family_name` | `0x00471AF0` | high | Copies the SFamilyName string8 bytes verbatim into the pane's 256-byte display buffer. |
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
| `ui_skill_inventory_change_slot` | `0x00491920` | high | Validates a NewSkillInventoryPane drag destination, rejects slots divisible by 36 and entries under SActionDelay, then requests CChangeSlot category 2. |
| `ui_new_spell_inventory_pane_ctor` | `0x004919E0` | high | Constructs exact RTTI class NewSpellInventoryPane and initializes its 90-entry spell-item pointer array. |
| `ui_spell_inventory_action_delay_timer` | `0x00491F70` | high | NewSpellInventoryPane TimerHandler callback for ID 0; resolves the one-based slot payload and clears action_delay_active on the current spell item. |
| `ui_spell_inventory_create_spell_item` | `0x00492070` | high | Allocates SpellInvItemPane and passes the SAddSpell slot, icon, argument type, name, prompt, and cast-line count to its constructor. |
| `ui_spell_inventory_remove_slot` | `0x00492140` | high | Converts a one-based spell slot to the inventory container's zero-based index and removes the corresponding UI item. |
| `ui_spell_inventory_handle_network_event` | `0x00492160` | high | NewSpellInventoryPane network-event handler routes SAddSpell, SRemoveSpell, and SActionDelay selector 0 to the matching UI paths. |
| `ui_spell_inventory_add_spell_from_packet` | `0x00492200` | high | Accepts SAddSpell slots 1 through 90, replaces the existing UI entry, and constructs a new SpellInvItemPane. |
| `ui_spell_inventory_remove_spell_from_packet` | `0x004922B0` | high | Accepts SRemoveSpell slots 1 through 90 and removes the slot when its SpellInvItemPane pointer is non-null. |
| `ui_spell_inventory_apply_action_delay` | `0x00492330` | high | Accepts SActionDelay selector 0 and slots 1 through 90, sets the live spell item delay flag, and schedules the inventory expiry timer. |
| `ui_spell_inventory_change_slot` | `0x004923F0` | high | Validates a NewSpellInventoryPane drag destination, rejects slots divisible by 36 and entries under SActionDelay, then requests CChangeSlot category 1. |
| `ui_skill_inventory_set_item_at` | `0x00492B30` | high | Replaces a checked zero-based skill inventory entry and attaches the new SkillInvItemPane to its visible slot. |
| `ui_skill_inventory_remove_item_at` | `0x00492C00` | high | Checks a zero-based skill inventory index, releases its live UI item, and clears the pointer entry. |
| `ui_spell_inventory_remove_item_at` | `0x00493460` | high | Checks a zero-based spell inventory index, releases its live SpellInvItemPane through the shared UI owner, and clears the pointer entry. |
| `ui_item_pane_ctor` | `0x00495C60` | high | Constructs exact RTTI class ItemPane and stores an item sprite, 128-byte display name, and dye color. |
| `ui_inventory_item_set_display_name` | `0x00495DE0` | high | Replaces the InvItemPane display name through the same bounded 128-byte copy used by its ItemPane base. |
| `ui_inventory_item_ctor` | `0x00495E10` | high | Constructs exact RTTI class InvItemPane and retains slot, sprite, dye, display name, quantity, stack flag, maximum durability, and current durability. |
| `ui_inventory_item_show_desc` | `0x00495FF0` | high | Builds an InvItemPane tooltip anchor, keeps it within 640 by 480, resolves the item's description provider, and opens the shared DescPane with the item as owner. |
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
| `ui_skill_inventory_item_get_base_name` | `0x00498B90` | high | Copies the retained skill name only through the suffix split position and appends a NUL terminator. |
| `ui_skill_item_cooldown_visual_timer` | `0x00498C10` | high | For timer ID 0x10204, maps elapsed time to 30 integer steps, redraws, and reschedules at 100 ms while the delay and visual-active flags remain set. |
| `ui_skill_inventory_item_handle_pointer_event` | `0x00498D40` | high | Skill item pointer handler checks complete-object offset +0x322 and blocks drag start, activation, and information actions while action-delayed. |
| `ui_skill_inventory_item_draw` | `0x004991D0` | high | Draws the skill icon, applies palette index 0x58 across a delayed icon, and palette index 0x18 below a vertical boundary derived from the 0 through 30 progress step. |
| `ui_skill_inventory_activate` | `0x004992F0` | high | Blocks activation while SActionDelay flag +0x322 or unresolved state +0x323 is set, then sends any configured skill text and reaches the CUseSkill sender. |
| `ui_skill_is_denied` | `0x004994C0` | high | Looks up the skill name in DeniedItemList mode 1 before CUseSkill construction; a match suppresses the packet. |
| `ui_skill_item_clear_action_delay` | `0x00499570` | high | Clears SkillInvItemPane +0x322 and invalidates the item rectangle. |
| `ui_skill_item_set_action_delay` | `0x004995A0` | high | Sets SkillInvItemPane +0x322 to one and invalidates the item rectangle. |
| `ui_parse_skill_spell_level_suffix` | `0x00499660` | high | Scans backward for a space plus parenthesized slash pair, parses the two sides with atoi, and returns the base-name split position; it does not test the literal Lev label. |
| `ui_spell_inventory_item_ctor` | `0x00499DE0` | high | Constructs exact RTTI class SpellInvItemPane and retains slot, icon, argument type, 128-byte name and prompt buffers, and cast_lines. |
| `ui_spell_inventory_item_get_base_name` | `0x00499F30` | high | Copies the retained spell name only through the suffix split position and appends a NUL terminator. |
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
| `ui_desc_pane_show` | `0x0049C6B0` | high | Creates the DescPane singleton as needed, optionally reloads content by item name, lays it out at an anchor, marks it active, and retains the optional hover owner. |
| `ui_close_desc_pane` | `0x0049C980` | high | Unregisters the current RTTI-backed DescPane from event and screen routing and clears its active state. |
| `ui_desc_pane_handle_network_event` | `0x0049CC30` | high | Closes DescPane when a decoded raw body begins with SExchange opcode 0x42 or SGroup opcode 0x63; it reads no packet fields. |
| `ui_item_shop_shopping_bag_ctor` | `0x0049F450` | high | Constructs exact RTTI ItemShop::ShoppingBagDialogPane from lshopba2.txt and sends CCashShop action 0. |
| `ui_item_shop_shopping_bag_dtor` | `0x0049F7E0` | high | Unregisters and destroys ShoppingBagDialogPane and its attached item controls. |
| `ui_item_shop_shopping_bag_handle_network_event` | `0x004A0550` | high | Consumes exact RTTI SItemShop in the shopping-bag pane. |
| `ui_item_shop_shopping_bag_apply_packet` | `0x004A05B0` | high | Replaces records for SItemShop variant 0 and clears the pane's busy state for variants 0 and 1. |
| `ui_item_shop_browser_dialog_ctor` | `0x004A09F0` | high | Constructs the separate exact RTTI ItemShop::ShopDialogPane around BrowserControlPane; no static constructor caller is present. |
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
| `ui_merchant_server_item_menu3_timer_callback` | `0x004CACD0` | high | TimerHandler callback installed by exact RTTI ServerItemMenuDialog3; subtype 1 applies the scroll offset and updates a row tooltip, while subtype 2 closes DescPane. |
| `ui_merchant_server_item_menu3_show_hover_desc` | `0x004CAD70` | high | Builds or repositions the older MerchantDialogPane server-item tooltip through the shared DescPane helper and retains the hovered row. |
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
| `ui_legend_info_pane_ctor` | `0x00515AB0` | high | Constructs the older local legend window and its class ability and seven event-category views. |
| `ui_legend_info_apply_class_metadata` | `0x005166E0` | high | Applies parsed SClass records to the older skill and spell tabs. |
| `ui_legend_info_apply_event_metadata` | `0x005168E0` | high | Applies one parsed SEvent table to the matching older event category. |
| `ui_legend_info_timer` | `0x00516980` | high | Requests the active SClass table and all seven SEvent tables for the older legend window. |
| `ui_spell_skill_view_draw` | `0x005184A0` | high | Draws learned, available, or locked ability rows with the matching numbered icon bank. |
| `ui_spell_skill_property_dialog_ctor` | `0x005191E0` | high | Builds the older ability detail pane and colors satisfied and failed requirements differently. |
| `ui_event_info_set_category_records` | `0x00519C40` | high | Assigns an SEvent record set to one of the older legend window event categories. |
| `ui_event_info_rebuild_category` | `0x00519EC0` | high | Rebuilds older event rows using completion, qualification, and prerequisite checks. |
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
| `ui_npc_list_menu_dialog_ctor` | `0x00530230` | high | Builds a nested NPC selection pane with a scrollable list and a separate default submit button. |
| `ui_npc_list_menu_dialog_handle_action` | `0x005302F0` | high | Handles the default submit action, delegates the selected row to the active model, and then closes or deactivates the nested pane. |
| `ui_npc_list_menu_submit_selected_row` | `0x00530450` | high | Reads the scroll control's selected row and calls the model's contextual CMerchant selection builder. |
| `ui_npc_item_list_row_queue_hover` | `0x005308F0` | high | Resolves a valid row and schedules the owner TimerHandler with its timer ID, a zero-millisecond delay, subtype 2, and the row's u16 index. |
| `ui_npc_item_list_row_queue_hover_close` | `0x00530960` | high | Schedules the owner TimerHandler with a zero-millisecond delay, subtype 3, and a zero payload when the row hover ends. |
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
| `ui_npc_build_screen_menu_list` | `0x00535080` | high | Constructs the type-specific list model for SScreenMenu types 5 through 9 and 11, then embeds it in NPCListMenuDialog. |
| `ui_npc_client_item_menu_ctor` | `0x00535C70` | high | Constructs NPCClientItemMenu for SScreenMenu types 5 and 11 and selects the pursuit-0x004E row variant when applicable. |
| `ui_npc_client_item_menu_count` | `0x00535D90` | high | Returns the server-supplied local inventory slot count used to build the scrollable list. |
| `ui_npc_client_item_menu_build_row` | `0x00535DB0` | high | Resolves one server-supplied slot against the live inventory and builds an active row from its local icon and name, plus the optional display value. |
| `ui_npc_client_skill_spell_menu_ctor` | `0x00536C80` | high | Constructs the shared local skill and spell list model before the exact derived type is installed. |
| `ui_npc_client_skill_menu_build_row` | `0x00536FE0` | high | Resolves one local skill slot and builds an active row from the learned skill's icon and retained name. |
| `ui_npc_client_skill_menu_initialize` | `0x00537260` | high | Parses the type-9 slot whitelist and falls back to enumerating the local skill book when the count is zero. |
| `ui_npc_client_skill_menu_enumerate_all` | `0x00537290` | high | Collects active learned skill slots 1 through 89 when the server supplies no nonzero whitelist. |
| `ui_npc_client_spell_menu_build_row` | `0x00537400` | high | Resolves one local spell slot and builds an active row from the learned spell's icon and retained name. |
| `ui_npc_client_spell_menu_initialize` | `0x00537680` | high | Parses the type-8 slot whitelist and falls back to enumerating the local spell book when the count is zero. |
| `ui_npc_client_spell_menu_enumerate_all` | `0x005376B0` | high | Collects active learned spell slots 1 through 89 when the server supplies no nonzero whitelist. |
| `ui_npc_server_item_menu_timer_callback` | `0x00539340` | high | NPCServerItemMenuDialog TimerHandler callback; timer ID 1 routes subtype 2 to the row tooltip update and subtype 3 to tooltip close. |
| `ui_npc_server_item_menu_handle_pointer_event` | `0x005393F0` | high | Stores pointer coordinates on move, closes the tooltip outside the visible client bounds, and then delegates to DialogPane pointer handling. |
| `ui_npc_server_item_menu_show_hover_desc` | `0x00539600` | high | Resolves a changed server-item row by name, opens DescPane near the pointer, repositions existing content for the same row, and refreshes the dialog's detail controls. |
| `ui_npc_server_item_menu_clear_hover_desc` | `0x00539A30` | high | Closes the shared DescPane and resets NPCServerItemMenuDialog's hovered-row field to -1. |
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
| `ui_friend_list_dialog_ctor` | `0x005435F0` | high | Constructs the exact RTTI FriendListDialog, loads _nfriend.txt, and creates twenty text-edit controls backed by the UserInfo friend slots. |
| `ui_friend_list_dialog_handle_action` | `0x00543C70` | high | Handles OK and Cancel; OK copies controls 2 through 21 into the twenty UserInfo friend slots and saves Friendlist.cfg. |
| `ui_safe_quit_alert_ctor` | `0x00544100` | high | Constructs exact RTTI SafeQuitAlert and immediately submits CQuit as bytes 0B 01. |
| `ui_safe_quit_alert_handle_network_event` | `0x00544220` | high | SafeQuitAlert primary-vtable network-event handler routes typed SQuit opcode 0x4C to its response helper. |
| `ui_safe_quit_alert_apply_quit_response` | `0x00544280` | high | When SQuit's consumed byte is 1, marks the alert approved, submits CQuit bytes 0B 00, replaces the alert text, and refreshes its control. |
| `ui_option_pane_handle_keyboard_event` | `0x005444B0` | high | OptionPane keyboard-event handler maps both X and x to construction of exact RTTI SafeQuitAlert. |
| `ui_open_user_confirm_from_message` | `0x005449D0` | high | Opens exact RTTI UserConfirmPane for SMessage type 0x11 with its main prompt, two bytes, and string8 reply context. |
| `ui_pane_ctor` | `0x00549490` | high | Constructs Pane over Canvas and a secondary TimerHandler at +0x11C; initializes visible true at +0x130. |
| `ui_pane_dtor` | `0x00549600` | high | Destroys Pane-owned helper objects, its TimerHandler secondary base, and the Canvas base. |
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
| `ui_screen_pane_handle_timer` | `0x005536A0` | high | Dispatches root ScreenPane timer IDs 0 through 4; ID 0 invokes the recurring render_screen_timer_tick service. |
| `ui_screen_pane_set_cursor_mode` | `0x00554330` | high | Stores the cursor image and hotspot table selector at root ScreenPane +0x27C and redraws the cursor state. |
| `ui_server_select_dialog_handle_server_event` | `0x00559DC0` | high | ServerSelectDialogPane primary-vtable slot 0x50 accepts an event packet only when its opcode is 0x56, then forwards the exact SMulti object to the dedicated handler. |
| `ui_server_select_dialog_handle_multi` | `0x00559E80` | high | Applies the SMulti replacement list, auto-selects row zero when exactly one record exists, and refreshes the ServerSelectDialogPane controls. |
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
| `ui_line_input_paste_clipboard` | `0x0057DD30` | high | Pastes clipboard text into LineInputPane only for distribution modes 1 or 15 or for any nonzero SStatus privilege. |
| `ui_text_enforce_max_bytes` | `0x0057F530` | high | Trims oldest TextEditPane bytes from the front when its configured byte limit is exceeded, preserving DBCS boundaries. |
| `ui_text_enforce_max_lines` | `0x0057F680` | high | Trims oldest TextEditPane lines when its configured line limit is exceeded. |
| `ui_line_input_copy_text` | `0x00584A00` | high | Calls the LineInputPane text control's bounded copy method and returns its copied byte length. |
| `ui_line_input_handle_event` | `0x00585040` | high | Handles Pane::LineInputPane events and suppresses Ctrl+V outside distribution modes 1 and 15 unless SStatus privilege is nonzero. |
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
| `ui_gui_back_toggle_layout` | `0x005A0B40` | high | Flips GUIBackPane between layout indexes 0 and 1 and passes the result to ui_gui_back_apply_layout. |
| `ui_gui_back_activate_action` | `0x005A0B70` | high | Dispatches GUIBackPane bottom-action IDs; action 0 creates HotKeyPane, while the other IDs open their normal panes or local actions. |
| `ui_gui_back_handle_pointer` | `0x005A0CF0` | high | Hit-tests six bottom-action rectangles on a left-button event; BTN_HELP is slot 0 and is passed to ui_gui_back_activate_action after click debounce. |
| `ui_gui_back_pane_draw` | `0x005A2050` | high | Draws GUIBackPane state, including selection of the network indicator image from the latest movement round-trip value. |
| `ui_gui_back_pane_set_network_latency` | `0x005A2B80` | high | Stores the latest matching CMove and SMove round-trip in GUIBackPane and invalidates the network-indicator region. |
| `ui_gui_back_pane_request_show_users` | `0x005A2C60` | high | GUIBackPane interface method that requests the current world-user list through CWho. |
| `ui_gui_back_get_page_expanded` | `0x005A2CC0` | high | Returns GUIBackPane's page_is_expanded flag at complete object offset +0x4FB0. |
| `ui_game_interface_activate_number_key` | `0x005A2D90` | high | Routes number keys by the selected GUIBackPane mode; item mode maps keys 1 through 9 and 0 to inventory slots 1 through 10. |
| `ui_gui_back_select_page_mode` | `0x005A2FB0` | high | Selects one GUIBackPane page, records its expanded flag, and applies normal or expanded geometry from the active small or large layout record. |
| `ui_gui_back_apply_layout` | `0x005A3900` | high | Reapplies the selected GUIBackPane and child-pane geometry, then sends the layout's MAP rectangle and view center through MapInterface to resize and invalidate WorldPane. |
| `ui_skill_spell_book_find_current_level` | `0x005A4440` | high | Scans 89 live spell or skill slots by stripped base name and returns the parsed left suffix value for the first exact match. |
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
| `ui_user_info_pane_ctor` | `0x005ABA30` | high | Constructs UserInfoPane, initializes seven page-enable flags, and creates page children with action IDs 0x101 through 0x107 at offsets +0x584 through +0x59C. |
| `ui_user_info_apply_portrait_body` | `0x005ACD10` | high | Decodes a portrait/profile body into UserInfoPane state and refreshes its portrait canvas and text. |
| `ui_user_info_handle_server_packet` | `0x005AD160` | high | The UserInfoPane vtable event handler sends the local portrait response when the decoded opcode is 0x49. |
| `ui_user_info_refresh_local_portrait` | `0x005AD5D0` | high | Builds the local portrait body and reapplies it to UserInfoPane without calling the network submitter. |
| `ui_user_info_timer` | `0x005AD600` | high | Timer 0x1241 calls the local portrait refresh after the profile editor saves. |
| `ui_user_info_apply_class_metadata` | `0x005ADB00` | high | Populates the local user profile skill or spell lists from parsed SClass records. |
| `ui_spell_skill_row_state` | `0x005ADD00` | high | Returns learned, available, or locked state by combining live inventory lookup with SClass requirements. |
| `ui_format_spell_skill_progress_requirement` | `0x005ADFB0` | high | Formats the SClass level, ability, and master progression requirement for the detail dialog. |
| `ui_skill_spell_format_level_requirement` | `0x005ADFB0` | high | Formats the SkillSpellInfoDialogPane LEV text from definition requirement fields and localized message strings, independently of the live name-suffix values. |
| `ui_skill_spell_info_dialog_ctor` | `0x005AE090` | high | Constructs exact RTTI SkillSpellInfoDialogPane from _nui_ske.txt, selects the skill or spell icon, retains definition fields, and joins at most 32 description lines. |
| `ui_skill_spell_info_dialog_draw` | `0x005AE710` | high | Draws the icon, level requirement, five colored stat requirements, definition name, subtitles, and description into the layout rectangles. |
| `ui_open_skill_spell_info_dialog` | `0x005AEA10` | high | Decodes the spell-or-skill inventory selection, resolves its definition, classifies learned and requirement state, constructs the detail pane, centers it, and opens it. |
| `ui_user_info_apply_event_metadata` | `0x005AF090` | high | Maps SEvent1 through SEvent7 into the new local profile event categories, merging the last two into category six. |
| `ui_event_row_state` | `0x005AF150` | high | Returns completed, available, or locked by checking the completion legend key before event requirements. |
| `ui_format_event_progress_bucket` | `0x005AF390` | high | Formats an event progression requirement from its qualification bucket digits. |
| `ui_event_info_dialog_ctor` | `0x005AF460` | high | Builds the new event detail dialog and selects incomplete summary or completed result text. |
| `ui_find_event_by_completion_key` | `0x005AFBD0` | high | Resolves an event prerequisite key to metadata so its title can be displayed. |
| `ui_user_info_reload_album` | `0x005B04A0` | high | Loads the active character's album.dat and repopulates the current nui_AlbumPane tiles. |
| `ui_user_info_export_album_portrait_jpeg` | `0x005B0580` | high | Current Save fills transparent pixels from _nportbk.spf, copies the prior extensionless portrait to .bak, and always writes JFIF. |
| `ui_user_info_handle_album_action` | `0x005B0AB0` | high | Maps album tile action 0 to Save confirmation event 0x1242 and action 1 to Remove confirmation event 0x1243. |
| `ui_user_info_update_status_from_packet` | `0x005B0C40` | high | Updates UserInfoPane's five attributes and signed armor class from present SStatus blocks. |
| `ui_user_info_apply_self_look` | `0x005B0D10` | high | Copies SSelfLook identity and nation fields into UserInfoPane, rebuilds its legend list, and reloads SClass metadata when the class changes. |
| `ui_user_info_add_equipment_from_packet` | `0x005B1070` | high | Maps SAddEquip slots 1 through 18 to UserInfoPane child-view indices 0 through 17 and forwards the visible item fields. |
| `ui_user_info_remove_equipment_from_packet` | `0x005B1100` | high | Maps a checked SRemoveEquip slot and asks the UserInfoPane child equipment view to clear that entry. |
| `ui_portrait_text_dialog_ctor` | `0x005B11A0` | high | Constructs RTTI-backed PortraitTextInputDialogPane from _nui_pi.txt and loads profile.txt. |
| `ui_portrait_text_dialog_action` | `0x005B1510` | high | Action 1 saves profile.txt and queues timer 0x1241; action 2 closes without saving. |
| `ui_other_user_info_ctor` | `0x005B1850` | high | Constructs exact RTTI UserInfoPane_ForOthers and applies a decoded SObjectInfo body. |
| `ui_other_user_info_apply_object_info_body` | `0x005B1900` | high | Reads entity ID, 18 implicitly ordered equipment records, user_state in the shared UserState domain, name, nation, title, group-open state, guild identity, legends, and the optional portrait/biography tail. |
| `ui_open_other_user_info_from_server_body` | `0x005B1DF0` | high | Creates or refreshes UserInfoPane_ForOthers and applies the decoded object-info body for its entity ID. |
| `ui_open_user_info` | `0x005B1FA0` | high | Opens the singleton UserInfoPane and selects the requested local or other-user mode. |
| `ui_user_info_visual_state_ctor` | `0x005B2110` | high | Constructs two arrays of seven 0x34-byte animation states inside the 0x3B8-byte UserInfoPane visual subobject at complete-object offset +0x1B4. |
| `ui_album_picture_dialog_ctor` | `0x005B24E0` | high | Constructs exact RTTI AlbumPicDialogPane from _nui_alb.txt and attaches SAVE before REMOVE. |
| `ui_album_picture_handle_action` | `0x005B2A00` | high | Forwards local action 0 or 1 with this tile's 0x1234-based event ID. |
| `ui_nui_album_pane_ctor` | `0x005B2A70` | high | Constructs exact RTTI nui_AlbumPane from _nui_al.txt and creates 100 picture dialogs. |
| `ui_nui_album_show_page_pair` | `0x005B31C0` | high | Displays 12 records as two six-item pages and labels the current adjacent page numbers. |
| `ui_nui_album_load_records` | `0x005B3320` | high | Clears all 100 tile previews and fills active entries from one loaded AlbumFile. |
| `ui_nui_album_handle_page_action` | `0x005B3700` | high | Moves the visible page base backward or forward by two, clamped to 0 through 15. |
| `ui_nui_album_handle_picture_action` | `0x005B3770` | high | Converts picture events 0x1234 through 0x1297 into parent album action and zero-based record index. |
| `ui_nui_event_pane_create` | `0x005B3E20` | high | Creates the new local profile event pane from the _nui_ev layout. |
| `ui_nui_event_pane_ctor` | `0x005B3EE0` | high | Constructs two visible event lists, previous and next controls, and six paged categories. |
| `ui_nui_event_add_row` | `0x005B4370` | high | Adds a new event row using leicon frames for completed, available, and locked states. |
| `ui_user_info_apply_legend_body` | `0x005B7D00` | high | Reads a u8 count followed by icon, color, string8 key, and string8 text legend records. |
| `ui_nui_legend_pane_apply_self_look` | `0x005B7ED0` | high | Clears and rebuilds RTTI class nui_LegendPane from SSelfLook's legend records. |
| `ui_nui_legend_contains_key` | `0x005B7F60` | high | Bridges new user-info checks to the live legend list exact-key lookup. |
| `ui_nui_skill_spell_pane_ctor` | `0x005B80C0` | high | Constructs separate skill and spell lists for the new local profile from the _nui_sk layout. |
| `ui_nui_skill_spell_add_row` | `0x005B8420` | high | Adds a new ability row using numbered skill or spell icon banks selected by learned, available, or locked state. |
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
| `ui_world_controller_pane_ctor` | `0x005C64F0` | high | Constructs WorldControllerPane, loads gndattr.tbl and both SOTP flag views, and initializes world rendering and object-controller state. |
| `ui_world_pane_screen_to_tile` | `0x005C75A0` | high | Converts a screen-space point through the active world controller to map tile coordinates, or returns negative coordinates when no controller is available. |
| `ui_world_pane_set_blinded` | `0x005C7600` | high | Forwards the SStatus-derived blinded state from WorldPane to the world renderer. |
| `ui_world_show_speech` | `0x005CBF90` | high | Attaches a timed speech pane to a world object for the requested speech mode and duration. |
| `ui_world_pane_draw_to_target` | `0x005CE350` | high | Copies WorldPane output to its target and applies the ambient-color and 8-bit light-mask blend when lighting is active below intensity 0x20. |
| `ui_world_controller_handle_object_message` | `0x005CE990` | high | Updates world indexes and rendering state for object messages, answers ground-attribute query selector 5, and invokes the object position-refresh virtual after movement. |
| `ui_world_object_name_pane_ctor` | `0x005E3F00` | high | Constructs the 0x1DC-byte RTTI WorldObject_Name_Pane and retains at most 63 text bytes plus a NUL at +0x198. |
| `ui_world_pane_handle_living_object_message` | `0x005EF120` | high | Handles RTTI-backed WORLD_LIVING_OBJECT_MESSAGE traffic; give event 2 rejects the local character and dispatches TimerHandler event 1 with the target object ID to the source InvItemPane. |
| `ui_world_pane_handle_inventory_drop` | `0x005EF620` | high | Converts a dragged inventory item's pointer position to a bounded map tile and dispatches it to InvItemPane; it does not compare the tile with the player's position. |
| `ui_world_pane_handle_drop_event` | `0x005EF790` | high | Rejects the drop while SUserAppearance action-state bit 0 is set; otherwise routes it through eligible child panes and handles an unconsumed inventory-item drop against the world map. |
| `ui_world_pane_request_change_direction` | `0x005F0900` | high | Applies the requested direction to the local WorldObject_User immediately, then sends CChangeDirection. |
| `ui_world_pane_attack_from_keyboard` | `0x005F0BF0` | high | Handles the Space-key attack path and submits only when the previous accepted Space attack was absent or more than 100 ms ago. |
| `ui_world_pane_handle_direction_input` | `0x005F0C40` | high | Turns with CChangeDirection when requested facing differs; otherwise attempts one tile of movement. |
| `ui_world_pane_handle_keyboard_event` | `0x005F0D20` | high | Handles WorldPane keyboard commands; the Tab map-overlay path gives character class 2 the zoom-enabled configuration observed for Rogues. |
| `ui_open_object_info_from_server_body` | `0x005F1590` | high | Resolves the body u32 entity ID to an existing living object before opening UserInfoPane_ForOthers. |
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
| `ui_open_employee_dialog_from_server_body` | `0x005F6BF0` | high | Creates EmployeeDialogPane only for an SMercenary category 1 Open body. |
| `ui_open_bulletin_session_from_server_body` | `0x005F6CD0` | high | Creates BulletinSession for a direct SBulletin body when no conflicting session is active and the admission flag check passes. |
| `ui_apply_block_input_server_packet` | `0x005F7AA0` | high | Maps SBlockInput state 0 to held-button release plus ClockPane creation and state 1 to ClockPane removal; other states are ignored. |
| `ui_open_manufacture_dialog_from_manual_packet` | `0x005F7AE0` | high | Creates the singleton ManufactureDialogPane only for SManual RecipeCount and ignores Recipe detail messages when no pane exists. |
| `ui_create_field_map_pane` | `0x005F88B0` | high | Allocates a 640 by 480 FieldMapPane, initializes it from decoded SFieldMap values, registers it with the screen root, and retains it in WorldPane. |
| `ui_world_capture_self_portrait_to_album` | `0x005F9B00` | high | WorldPane_Impl wrapper that invokes the album capture with zero, selecting the normal cooldown path. |
| `ui_world_pane_is_privileged` | `0x005F9D90` | high | MapUserInterface virtual getter returns whether WorldUserFunc privilege_level is nonzero; bulletin, line-input, and dormant screenshot branches consume it. |
| `ui_world_pane_get_privilege_level` | `0x005F9DC0` | high | MapUserInterface virtual getter returns raw WorldUserFunc privilege_level 0 through 3; the event dispatcher compares it exactly with 1 in a dormant timeout path. |
| `ui_world_pane_get_user_state` | `0x005F9DF0` | high | MapUserInterface virtual getter returns the low byte of the normalized UserState stored as a u32 at WorldUserFunc +0x1048. |
| `ui_world_pane_change_user_state` | `0x005F9E20` | high | WorldPane_Impl interface method that forwards a requested UserState to CChangeUserState. |
| `ui_world_pane_get_local_action_state` | `0x005F9E50` | high | WorldPane_Impl virtual getter returns the low-seven-bit SUserAppearance action state stored in WorldUserFunc; the item-inventory CChangeSlot category-0 sender is its only identified indirect consumer. |
| `ui_world_pane_get_self_object_id` | `0x005F9EC0` | high | WorldPane_Impl virtual getter returns the SUserAppearance user ID stored in WorldUserFunc. |
| `ui_world_pane_get_appearance_unknown_final` | `0x005FA040` | high | WorldPane_Impl virtual getter returns the final parsed SUserAppearance byte; no client decision based on it is identified. |
| `ui_world_pane_get_guild_value` | `0x005FA0B0` | medium | WorldPane_Impl virtual getter returns the second post-ID SUserAppearance byte unchanged; project behavioral evidence associates it with guild state. |
| `ui_world_pane_get_character_class` | `0x005FA0E0` | high | WorldPane_Impl virtual getter returns the third post-ID SUserAppearance byte; the Tab map-overlay path gives value 2 the Rogue-only zoom-enabled configuration. |
| `ui_world_pane_get_self_look_show_ability_metadata` | `0x005FA100` | high | Returns the SSelfLook show_ability_metadata byte widened and cached at WorldUserFunc +0x15C78. |
| `ui_world_pane_get_self_look_show_master_metadata` | `0x005FA130` | high | Returns the SSelfLook show_master_metadata byte widened and cached at WorldUserFunc +0x15C74. |
| `ui_world_pane_set_group_members_text` | `0x005FA220` | high | Forwards formatted SSelfLook group_members text to the WorldUserFunc fixed-record parser. |
| `ui_world_pane_get_group_member_entry` | `0x005FA250` | high | Returns WorldUserFunc +4 + index*0x41 without an internal bounds check; each entry holds a 64-byte name and one starred byte. |
| `ui_world_pane_get_group_member_count` | `0x005FA280` | high | Returns the parsed group-member count at WorldUserFunc +0x1044. |

## Network

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `net_send_web_board_dialog_request` | `0x004160A0` | high | Builds the exact two-byte CWebBoard action-0 body and starts BrowserDialogPane's 20-second response timer. |
| `net_percent_encode_web_board_cookie_value` | `0x00416810` | high | Percent-encodes reserved, unsafe, control, and non-ASCII bytes before BrowserDialogPane stores the boardinfo cookie. |
| `net_send_self_look` | `0x0041B840` | high | Builds the exact one-byte CSelfLook plaintext body as opcode 0x2D and submits length one. |
| `net_send_group_toggle` | `0x0041B8E0` | high | Builds and submits the exact one-byte CGroupToggle plaintext body containing only opcode 0x2F. |
| `net_send_bulletin_board_list_request` | `0x0041CBC0` | high | Writes derived CBulletin body 3B 01 when BulletinSession opens. |
| `net_send_bulletin_initial_list_request` | `0x0041E350` | high | Writes CBulletin action 2 with selected section ID, cursor 0x7FFF, and direction 0xF0. |
| `net_send_bulletin_article_list_request` | `0x00420D00` | high | Writes seven-byte CBulletin action 2 for article-list pagination. |
| `net_send_bulletin_article_request` | `0x00420E40` | high | Writes CBulletin action 3 with board ID, article ID, and direct-selection navigation 0. |
| `net_send_bulletin_highlight_request` | `0x00420F80` | high | Writes CBulletin action 7 for the optional _narlist.txt control spelled Hilight. |
| `net_send_bulletin_article_delete_request` | `0x00421090` | high | Writes six-byte CBulletin action 5 for each article selected for deletion. |
| `net_send_bulletin_article_navigation_request` | `0x004220D0` | high | Writes CBulletin action 3 with navigation 0xFF or 1 for Previous or Next. |
| `net_send_bulletin_article_delete_from_detail` | `0x00422210` | high | Writes six-byte CBulletin action 5 for the open article. |
| `net_send_bulletin_article_post` | `0x00422C00` | high | Writes CBulletin action 4 as board ID, string8 title, and string16 content. |
| `net_send_bulletin_mail_list_request` | `0x00424A40` | high | Writes seven-byte CBulletin action 2 for mail-list pagination. |
| `net_send_bulletin_mail_request` | `0x00424B80` | high | Writes CBulletin action 3 with mailbox ID, mail ID, and direct-selection navigation 0. |
| `net_send_bulletin_mail_list_delete_request` | `0x00424CC0` | high | Writes CBulletin action 5 with mailbox ID, mail ID, and the mail-list-only trailing zero. |
| `net_send_bulletin_mail_navigation_request` | `0x00425DF0` | high | Writes CBulletin action 3 with navigation 0xFF or 1 for Previous or Next. |
| `net_send_bulletin_mail_delete_from_detail` | `0x00425F30` | high | Writes six-byte CBulletin action 5 for the open mail entry. |
| `net_send_bulletin_mail` | `0x004268F0` | high | Writes CBulletin action 6 as mailbox ID, receiver, title, and string16 content. |
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
| `net_dispatch_create_user_events` | `0x0043F780` | high | CreateUserDialogPane routes decoded opcode 0x02 and alias 0x01 through state-specific creation-result handlers outside the packet factory, and accepts raw opcode 0x30 through a no-op path. |
| `net_handle_new_user_check_opcode_1` | `0x0043F820` | high | Routes compiled SNewUserCheck alias opcode 0x01 according to CreateUserDialogPane creation stage. |
| `net_handle_new_user_check_opcode_2` | `0x0043F870` | high | Routes live SNewUserCheck opcode 0x02 according to CreateUserDialogPane creation stage. |
| `net_send_mercenary_add_item` | `0x0045C500` | high | Builds CMercenary action 0 with inventory slot and u32 quantity. |
| `net_send_mercenary_withdraw_item` | `0x0045C5B0` | high | Builds CMercenary action 1 with item ID, quantity, and two trailing u16 values. |
| `net_send_mercenary_apply_price` | `0x0045C690` | high | Builds CMercenary action 2 with item ID, sell price, and buy price. |
| `net_send_mercenary_remove_item` | `0x0045C750` | high | Builds CMercenary action 3 with one item ID. |
| `net_send_mercenary_fire` | `0x0045C7C0` | high | Builds header-only CMercenary action 4. |
| `net_send_mercenary_request_info` | `0x0045C810` | high | Builds header-only CMercenary action 5 and is called immediately when EmployeeDialogPane opens. |
| `net_is_employee_server_body` | `0x0045C9B0` | high | Checks opcode 0x4F, category 1, and the pane's employee ID. |
| `net_is_employee_open_server_body` | `0x0045C9E0` | high | Checks the SMercenary header for category 1 and Open message code 0. |
| `net_read_employee_server_header` | `0x0045D120` | high | Reads the category, employee ID, and message code from a decoded opcode 0x4F body. |
| `net_read_employee_item_record` | `0x0045D1B0` | high | Reads employee item ID, sprite, color, name, optional description, unknown byte, quantity, sell price, and buy price. |
| `net_read_employee_trade_record` | `0x0045D380` | high | Reads the previous item ID and nonzero replacement item record used by StartTrade. |
| `net_init_mercenary_packet` | `0x0045D550` | high | Initializes the shared CMercenary header as opcode 0x54, category 1, employee ID, and action. |
| `net_send_group` | `0x00462DC0` | high | UserLookPane calls this opcode 0x2E builder with a length-prefixed user name. |
| `net_post_raw_server_bytes_event` | `0x00467000` | high | Copies a Winsock receive buffer without frame parsing and posts it through the network event family during initial raw-stream mode. |
| `net_post_decoded_server_packet_event` | `0x00467060` | high | Copies a decoded opcode-first server body and queues it as network packet event type 0x13. |
| `net_queue_raw_server_bytes_event` | `0x00468180` | high | Builds event type 0x13 around an owned raw receive buffer for TerminalPane2. |
| `net_queue_server_packet_event` | `0x00468220` | high | Builds and enqueues the event object used for a decoded server packet body. |
| `net_upload_and_delete_saved_crash_report` | `0x00468B40` | high | Reads at most 4096 text bytes from LCrash.nfo, conditionally sends CException report kind 1, and always attempts DeleteFileA. |
| `net_send_exception_report_text` | `0x00468D30` | high | Sends a 1..4095-byte in-memory diagnostic through the same CException report-kind-1 body used by saved crash reports. |
| `net_send_exchange_start` | `0x0046A2F0` | medium | Builds CExchange as opcode 0x4A, action 0x00, and a big-endian u32 argument; no live static caller was recovered. |
| `net_send_exchange_accept` | `0x0046A390` | high | Builds opcode 0x4A, action 0x05, and ExchangeDialog +0x630. |
| `net_send_exchange_cancel` | `0x0046A440` | high | Builds opcode 0x4A, action 0x04, and the supplied target or exchange ID. |
| `net_send_exchange_set_gold` | `0x0046A4F0` | high | Builds opcode 0x4A, action 0x03, exchange ID, and big-endian u32 gold amount. |
| `net_send_exchange_add_item` | `0x0046A5C0` | high | Builds opcode 0x4A, action 0x01, exchange ID, and one-based u8 inventory slot. |
| `net_send_exchange_add_stackable_item` | `0x0046C2A0` | high | Builds opcode 0x4A, action 0x02, exchange ID, staged slot, and u8 quantity. |
| `net_request_family_name` | `0x004719B0` | high | Builds and submits the opcode-only CRequestFamilyName body 7A. |
| `net_send_field_map_selection` | `0x00476390` | high | Normal field-map UI builder writes opcode 0x3F followed by the selected node's checksum, map ID, X, and Y words. |
| `net_send_inventory_change_slot` | `0x00490F40` | high | Writes CChangeSlot category 0 for item inventory, followed by one-based source and destination slots; it excludes slot 60 and suppresses this category while SUserAppearance action-state bit 0 is set. |
| `net_send_skill_change_slot` | `0x00492CE0` | high | Builds the four-byte CChangeSlot body with category 2, one-based source skill slot, and one-based destination skill slot. |
| `net_send_spell_change_slot` | `0x00493540` | high | Builds the four-byte CChangeSlot body with category 1, one-based source spell slot, and one-based destination spell slot. |
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
| `net_request_cash_shop_bag` | `0x004A03B0` | high | Builds CCashShop action 0 as the two-byte body 6C 00. |
| `net_request_cash_shop_item` | `0x004A0430` | high | Builds CCashShop action 1 with the selected SItemShop record type and u32 record ID. |
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
| `net_send_multi_server_selection` | `0x0055A090` | high | Submits CMulti operation 0 with the selected server record's stored ID, not its row index. |
| `net_request_multi_server_list` | `0x0055A150` | high | Submits CMulti operation 1 when ServerSelectDialogPane is constructed after a missing or mismatched local server-list CRC. |
| `net_load_server_table` | `0x0055A240` | high | Loads mServer.tbl numeric lines plus transformed name and greeting text into fixed-size records. |
| `net_save_server_table` | `0x0055A490` | high | Saves server records and transforms the name and greeting text for file storage. |
| `net_transform_server_table_text` | `0x0055A650` | high | Leaves byte zero in place and swaps later byte pairs in a self-inverse text transform. |
| `net_apply_multi_server_list` | `0x0055AAD0` | high | Inflates the SMulti slice into a 0x800-byte buffer, replaces the server table from its count and variable-length records, initializes greetings to one space, and saves mServer.tbl. |
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
| `net_create_damage_effect_server_packet` | `0x00598380` | high | Allocates the 0x18-byte exact RTTI SDamageEffect object and invokes its concrete constructor. |
| `net_damage_effect_server_packet_ctor` | `0x00598400` | high | Passes opcode 0x13 to the server packet base and installs the exact SDamageEffect vtable. |
| `net_deserialize_damage_effect_server_packet` | `0x00598430` | high | Reads u32 object_id followed by the unknown, health_percent, and sound_id_or_ff bytes. |
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
| `net_create_family_name_server_packet` | `0x00599100` | high | Allocates and constructs the exact RTTI SFamilyName packet object. |
| `net_family_name_server_packet_ctor` | `0x00599180` | high | Binds opcode 0x6D and installs the exact RTTI SFamilyName vtable. |
| `net_deserialize_family_name_server_packet` | `0x005991B0` | high | Reads one string8 family name and no other fields. |
| `net_create_field_map_server_packet` | `0x00599210` | high | Allocates the exact RTTI SFieldMap object and invokes its concrete constructor. |
| `net_field_map_server_packet_ctor` | `0x00599290` | high | Passes opcode 0x2E to the server packet base and installs the exact SFieldMap vtable. |
| `net_deserialize_field_map_server_packet` | `0x005992C0` | high | Reads field-name string8, node count, current-node index, and each node's screen position, name, checksum, map ID, X, and Y. |
| `net_create_group_server_packet` | `0x00599440` | high | Allocates the 0x420-byte exact RTTI SGroup object and invokes its concrete constructor. |
| `net_group_server_packet_ctor` | `0x005994C0` | high | Passes opcode 0x63 to the server packet base and installs the exact SGroup vtable. |
| `net_deserialize_group_server_packet` | `0x005994F0` | high | Reads action 1 and 5 as string8 names, action 4 as recruiting details with five maximum/current pairs, and no body for every other action. |
| `net_create_item_shop_server_packet` | `0x00599640` | high | Allocates and constructs the exact RTTI SItemShop packet object. |
| `net_item_shop_server_packet_ctor` | `0x005996C0` | high | Binds opcode 0x45 and installs the exact RTTI SItemShop vtable. |
| `net_deserialize_item_shop_server_packet` | `0x00599730` | high | Reads the SItemShop variant and, for variant 0, a u8 count followed by complete shopping-bag records. |
| `net_reset_item_shop_record_reader` | `0x00599780` | high | Resets the SItemShop record cursor before pane consumption. |
| `net_read_item_shop_record` | `0x005997B0` | high | Returns record type, ID, sprite, color, name, description, quantity, mode, and optional alternate description. |
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
| `net_create_multi_server_packet` | `0x0059A740` | high | Allocates the 0x18-byte exact RTTI SMulti object registered for server opcode 0x56. |
| `net_multi_server_packet_ctor` | `0x0059A7C0` | high | Passes opcode 0x56 to the server packet base and installs the exact SMulti vtable. |
| `net_deserialize_multi_server_packet` | `0x0059A7F0` | high | Reads a big-endian u16 compressed length and retains a pointer to exactly that many bytes from the decoded packet buffer. |
| `net_create_num_users_server_packet` | `0x0059A870` | high | Allocates the 0x14-byte exact RTTI SNumUsers object registered for server opcode 0x47. |
| `net_num_users_server_packet_ctor` | `0x0059A8F0` | high | Passes opcode 0x47 to the common server packet base and installs the exact SNumUsers vtable. |
| `net_deserialize_num_users_server_packet` | `0x0059A920` | high | Reads the complete SNumUsers payload as one big-endian u16 user_count; no opcode consumer was found in the target client. |
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
| `net_dispatch_server_packet` | `0x005ED9A0` | high | Checks decoded opcode 0x4F directly because SMercenary has no server-factory object, then calls the employee dialog opener. |
| `net_handle_static_object_state_server_packet` | `0x005F1690` | high | Applies every record to the selected isometric static layer; state 0 targets pair column 1 and any nonzero state targets column 0. |
| `net_handle_self_look_server_packet` | `0x005F1990` | high | Forwards SSelfLook to WorldUserFunc, then refreshes the live group-member matches immediately or after the existing one-second timer path. |
| `net_handle_status_server_packet` | `0x005F1A10` | high | Applies global SStatus effects by updating WorldUserFunc and setting blinded only when the raw blind code equals 0x08. |
| `net_handle_add_spell_server_packet` | `0x005F1AF0` | high | Forwards decoded SAddSpell fields to the WorldUserFunc session model stored by WorldPane. |
| `net_handle_remove_spell_server_packet` | `0x005F1B30` | high | Forwards decoded SRemoveSpell to WorldUserFunc vtable slot +0x14. |
| `net_handle_add_skill_server_packet` | `0x005F1B70` | high | Forwards decoded SAddSkill to WorldUserFunc vtable slot +0x18. |
| `net_handle_remove_skill_server_packet` | `0x005F1BB0` | high | Forwards decoded SRemoveSkill to WorldUserFunc vtable slot +0x1C. |
| `net_handle_map_size_server_packet` | `0x005F1BF0` | high | Applies u8 map dimensions, NoMap, Winter art, weather mode, local CRC16 cache validation, transfer state, and map lighting. |
| `net_handle_change_hour_server_packet` | `0x005F2160` | high | Stores the SChangeHour time step at WorldPane +0x25C and immediately recomputes map lighting. |
| `net_handle_exchange_started` | `0x005F2190` | high | Handles SExchange event 0x00 before a dialog exists. |
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
| `net_handle_damage_effect_server_packet` | `0x005F40F0` | high | Plays non-0xFF sound first, validates signed health_percent in 0 through 100, maps it to stage floor(percent / 4), and asks the world to replace the target's temporary meter. |
| `net_send_get` | `0x005F4200` | high | Builds CGet as opcode 0x07, u8 destination slot, u16 X, and u16 Y. |
| `net_send_group_recruit_view` | `0x005F4340` | high | Builds CGroup action 5 with the selected recruitment name; the paired SGroup action 4 opens GroupAdInfoDialogPane. |
| `net_send_request_object` | `0x005F4430` | high | Builds CRequestObject as opcode 0x0C plus one u32 object ID; confirmed callers use it after a lookup misses or an expected living-object cast fails. |
| `net_send_attack` | `0x005F44B0` | high | Builds CAttack as opcode 0x13 with no payload and submits the complete one-byte plaintext body. |
| `net_send_change_direction` | `0x005F4510` | high | Builds CChangeDirection as opcode 0x11 plus one direction byte after WorldPane turns the local object optimistically. |
| `net_send_move` | `0x005F4580` | high | Builds CMove as opcode, direction, and an incremented rolling u8 step, then records the send time used by a matching SMove reply. |
| `net_send_refresh_user` | `0x005F4640` | high | WorldPane paths call this opcode-only 0x38 builder. |
| `net_send_emotion` | `0x005F46C0` | high | Builds CEmotion as opcode 0x1D followed by one caller-supplied u8 emotion request code. |
| `net_handle_bounce_server_packet` | `0x005F6A80` | high | Submits SBounce's counted embedded bytes directly as an ordinary opcode-first client body and performs no other game or UI action. |
| `net_handle_bulletin_server_body` | `0x005F6CB0` | high | Forwards raw decoded opcode 0x31 to the BulletinSession opener. |
| `net_handle_message_server_packet` | `0x005F6D80` | high | Routes SMessage to the floating GameMessagePane, WindowMessageDialogPane, or ScorePane according to its type byte. |
| `net_handle_enter_editing_mode_server_data` | `0x005F71C0` | high | WorldPane's raw opcode 0x1B branch allocates exact RTTI EditablePaperPane and constructs it in editable mode directly from the decoded body. |
| `net_handle_show_paper_server_data` | `0x005F7250` | high | WorldPane's raw opcode 0x35 branch constructs the same EditablePaperPane in read-only mode. |
| `net_send_check_time` | `0x005F7830` | high | Immediate response to SCheckTime opcode 0x68; builds CCheckTime as opcode 0x75, echoed u32 server_value, and one timeGetTime() u32 sample without local comparison or enforcement. |
| `net_handle_bad_guy_server_packet` | `0x005F7900` | high | Validates the SBadGuy mode and guard, creates and extends Mscfg.dll when possible, then forces client termination on both creation-success and creation-failure paths. |
| `net_handle_show_users` | `0x005F7B80` | high | Handles raw decoded server opcode 0x36, applies the replacement list, and opens the RTTI-backed ShowUsersPane. |
| `net_handle_world_transfer_server_packet` | `0x005F7BB0` | high | Handles in-world STransferServer, reconnects, sends CTransferServer, then attempts the saved LCrash.nfo upload. |
| `net_send_group_automatic_response` | `0x005F8620` | high | Builds CGroup opcode 0x2E, action 3, and a length-prefixed user string for the GroupAnswer automatic path. |
| `net_handle_group_server_packet` | `0x005F8720` | high | Handles SGroup by either opening the normal prompt or immediately sending CGroup action 3 according to AppConfig GroupAnswer. |
| `net_handle_field_map_server_data` | `0x005F8A10` | high | WorldPane's raw opcode 0x2E branch reparses the decoded SFieldMap body and creates the field-map pane instead of consuming the factory-built packet object. |
| `net_send_change_user_state` | `0x005FC790` | high | Normalizes UserState to 0 through 7, builds opcode 0x79 plus the state byte, and stores the same normalized local value. |
| `net_register_bad_guy_server_packet_factory` | `0x00667B20` | high | Registers the RTTI-backed SBadGuy constructor with the server_packet_factory startup path. |

## Rendering

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `render_get_image_library` | `0x00404A00` | high | Returns the ImageLib singleton used for sprite and UI frames. |
| `render_set_blit_flip_flags` | `0x00405F20` | high | Encodes horizontal and vertical flip requests as bits 0 and 1 for the optimized software blitters. |
| `render_initialize_blit_dispatch` | `0x00405F60` | high | Selects RGB565 or RGB555 software rendering, builds its lookup tables, and installs the complete blitter dispatch table. |
| `render_shutdown_blit_dispatch` | `0x004060D0` | high | Frees the 16-bit blend tables and clears the software blitter dispatch pointers during video shutdown or reinitialization. |
| `render_build_16bit_blend_tables` | `0x004061A0` | high | Builds pixel-format-specific half-color, carry-bit, and component-maximum tables for optimized RGB565 or RGB555 blending. |
| `render_free_16bit_blend_tables` | `0x00406480` | high | Frees all six optimized 16-bit blend lookup buffers and clears their globals. |
| `render_build_16bit_blend_tables_thunk` | `0x00406580` | high | Tail-calls the 16-bit blend-table builder for compiler-generated initialization plumbing. |
| `render_free_16bit_blend_tables_thunk` | `0x004065A0` | high | Tail-calls the 16-bit blend-table cleanup for compiler-generated shutdown plumbing. |
| `render_blit_indexed_opaque` | `0x004065B0` | high | Maps every indexed source pixel through a 16-bit palette and copies it with all four horizontal and vertical flip combinations. |
| `render_blit_indexed_zero_transparent` | `0x00406900` | high | Copies indexed pixels through a local palette whose index 0 entry is forced to pixel value zero, with both-axis flipping. |
| `render_blit_indexed_transparent` | `0x00406D70` | high | Maps nonzero indexed pixels through a 16-bit palette while preserving destination pixels where the source index is zero. |
| `render_blit_indexed_transparent_duplicate` | `0x00407100` | high | Unreferenced duplicate of the indexed transparent palette blitter, including the same zero-index exclusion and flip cases. |
| `render_blit_16bit_opaque` | `0x00407490` | high | Copies packed 16-bit pixels with all four horizontal and vertical flip combinations. |
| `render_blit_16bit_inverted` | `0x00407700` | high | Copies packed 16-bit pixels after complementing every source pixel, with both-axis flipping. |
| `render_blit_16bit_transparent` | `0x00407A30` | high | Copies nonzero packed 16-bit source pixels and preserves the destination where the source is zero. |
| `render_blit_16bit_color_key` | `0x00407DB0` | high | Copies packed 16-bit pixels except those equal to a caller-supplied color key. |
| `render_blit_16bit_average_transparent` | `0x00408140` | high | Averages each nonzero source pixel with the destination through packed half-color and carry tables. |
| `render_blit_luminance_palette_rgb565` | `0x00408610` | high | Maps every RGB565 source pixel's luminance through one of four 32-entry color ramps. |
| `render_blit_luminance_palette_rgb555` | `0x00408980` | high | Maps every RGB555 source pixel's luminance through one of four 32-entry color ramps. |
| `render_blit_16bit_luminance_palette` | `0x00408CF0` | high | Dispatches luminance-ramp drawing to the optimized, RGB565, or RGB555 implementation. |
| `render_blit_luminance_palette_color_key_rgb565` | `0x00408DC0` | high | Maps non-key RGB565 source pixels through a selected luminance color ramp. |
| `render_blit_luminance_palette_color_key_rgb555` | `0x00409190` | high | Maps non-key RGB555 source pixels through a selected luminance color ramp. |
| `render_blit_16bit_luminance_palette_transparent` | `0x00409560` | high | Dispatches color-keyed luminance-ramp drawing to the optimized or selected 16-bit format implementation. |
| `render_blit_color_blend_rgb565` | `0x00409640` | high | Blends each RGB565 source pixel toward one packed color by a uniform 0..32 weight. |
| `render_blit_color_blend_rgb555` | `0x004099D0` | high | Blends each RGB555 source pixel toward one packed color by a uniform 0..32 weight. |
| `render_blit_16bit_color_blend` | `0x00409D60` | high | Dispatches uniform source-to-color blending to the optimized, RGB565, or RGB555 implementation. |
| `render_blit_color_blend_color_key_rgb565` | `0x00409E40` | high | Blends non-key RGB565 source pixels toward one packed color by a uniform weight. |
| `render_blit_color_blend_color_key_rgb555` | `0x0040A220` | high | Blends non-key RGB555 source pixels toward one packed color by a uniform weight. |
| `render_blit_16bit_color_blend_transparent` | `0x0040A600` | high | Dispatches color-keyed source-to-color blending to the optimized or selected 16-bit format implementation. |
| `render_blit_color_blend_alpha_plane_rgb565` | `0x0040A6F0` | high | Uses a second plane as per-pixel weights while blending RGB565 source pixels toward one color. |
| `render_blit_color_blend_alpha_plane_rgb555` | `0x0040AB00` | high | Uses a second plane as per-pixel weights while blending RGB555 source pixels toward one color. |
| `render_blit_16bit_color_blend_alpha_plane` | `0x0040AF10` | high | Dispatches source-to-color blending controlled by a per-pixel alpha plane. |
| `render_blit_alpha_rgb565` | `0x0040AFF0` | high | Blends every RGB565 source pixel over the destination with one uniform 0..32 weight. |
| `render_blit_alpha_rgb555` | `0x0040B3A0` | high | Blends every RGB555 source pixel over the destination with one uniform 0..32 weight. |
| `render_blit_16bit_alpha` | `0x0040B750` | high | Dispatches uniform source-over-destination alpha blending. |
| `render_blit_alpha_color_key_rgb565` | `0x0040B820` | high | Blends non-key RGB565 source pixels over the destination with one uniform weight. |
| `render_blit_alpha_color_key_rgb555` | `0x0040BC20` | high | Blends non-key RGB555 source pixels over the destination with one uniform weight. |
| `render_blit_16bit_alpha_color_key` | `0x0040C020` | high | Dispatches color-keyed uniform source-over-destination alpha blending. |
| `render_blit_alpha_plane_rgb565` | `0x0040C100` | high | Blends RGB565 source pixels over the destination using a second source plane as per-pixel weights. |
| `render_blit_alpha_plane_rgb555` | `0x0040C520` | high | Blends RGB555 source pixels over the destination using a second source plane as per-pixel weights. |
| `render_blit_16bit_alpha_plane` | `0x0040C940` | high | Dispatches source-over-destination blending controlled by a per-pixel alpha plane. |
| `render_blit_screen_alpha_plane_unflipped_rgb565` | `0x0040CA10` | high | Unflipped RGB565 screen-style composite using a second source plane as independent component alpha values. |
| `render_blit_screen_alpha_plane_unflipped_rgb555` | `0x0040CB40` | high | Unflipped RGB555 screen-style composite using a second source plane as independent component alpha values. |
| `render_blit_screen_alpha_plane_unflipped` | `0x0040CC70` | high | Dispatches the unflipped screen-style alpha-plane loop to its RGB565 or RGB555 implementation. |
| `render_blit_screen_rgb565` | `0x0040CD00` | high | Applies blend mode 0x6D to an RGB565 destination. |
| `render_blit_screen_rgb555` | `0x0040D0D0` | high | Applies blend mode 0x6D to an RGB555 destination. |
| `render_blit_screen_mode` | `0x0040D4A0` | high | Selects the RGB565 or RGB555 screen-style blend used by static render flag 0x80. |
| `render_blit_screen_alpha_plane_rgb565` | `0x0040D560` | high | Applies a screen-style RGB565 composite using a second RGB555-formatted per-component alpha plane. |
| `render_blit_screen_alpha_plane_rgb555` | `0x0040D980` | high | Applies a screen-style RGB555 composite using a second per-component alpha plane. |
| `render_blit_16bit_screen_alpha_plane` | `0x0040DDA0` | high | Dispatches the screen-style composite controlled by a per-component alpha plane. |
| `render_blit_additive_rgb565` | `0x0040DE70` | high | Adds RGB565 source and destination components independently and clamps each to its format maximum. |
| `render_blit_additive_rgb555` | `0x0040E200` | high | Adds RGB555 source and destination components independently and clamps each to 31. |
| `render_blit_16bit_additive` | `0x0040E590` | high | Dispatches saturating additive blending to the optimized, RGB565, or RGB555 implementation. |
| `render_blit_relative_rle_alpha` | `0x0040E650` | high | Draws through row alpha streams located by relative offsets in one packed RLE alpha blob. |
| `render_blit_pointer_rle_alpha` | `0x0040E6B0` | high | Draws through row alpha streams reached through an absolute-pointer row table. |
| `render_blit_rle_alpha_color_key` | `0x0040E710` | high | Draws through RLE alpha rows while preserving destination pixels that match the source color key. |
| `render_blit_dual_rle_alpha_color_key` | `0x0040E770` | high | Combines two RLE alpha streams while excluding source pixels equal to the supplied color key. |
| `render_blit_rle_alpha_color_key_opacity` | `0x0040E7F0` | high | Combines an RLE alpha stream with a global opacity and a source color key. |
| `render_blend_rgb565_with_color` | `0x0040E860` | high | Linearly blends one RGB565 pixel toward another packed color with a 0..32 weight. |
| `render_blend_rgb555_with_color` | `0x0040E900` | high | Linearly blends one RGB555 pixel toward another packed color with a 0..32 weight. |
| `render_screen_pixel_rgb565_with_rgb555_alpha` | `0x0040E9A0` | high | Composites one RGB565 source over a destination using independent five-bit alpha components from an RGB555-formatted plane. |
| `render_screen_pixel_rgb555` | `0x0040EAE0` | high | Combines one RGB555 source and destination pixel with the screen-style component formula. |
| `render_screen_pixel_rgb565` | `0x0040EC20` | high | Combines one RGB565 source and destination pixel with the screen-style component formula. |
| `render_add_pixels_rgb565_saturating` | `0x0040ED60` | high | Adds two RGB565 pixels component by component and clamps red and blue to 31 and green to 63. |
| `render_add_pixels_rgb555_saturating` | `0x0040EE10` | high | Adds two RGB555 pixels component by component and clamps every component to 31. |
| `render_select_mmx_pixel_masks` | `0x0040EEC0` | high | Selects the packed MMX channel and carry masks used by the optimized RGB565 or RGB555 software-blit loops. |
| `render_blit_relative_rle_alpha_mmx` | `0x0040EF60` | high | MMX implementation of packed relative-offset RLE alpha drawing. |
| `render_blit_relative_rle_alpha_rgb565_mmx` | `0x0040F370` | high | RGB565 MMX loop for packed relative-offset RLE alpha rows. |
| `render_blit_relative_rle_alpha_rgb555_mmx` | `0x0040F760` | high | RGB555 MMX loop for packed relative-offset RLE alpha rows. |
| `render_blit_relative_rle_alpha_legacy_dispatch` | `0x0040FB50` | medium | Unreferenced legacy dispatcher whose two pixel-format branches both currently select the RGB565 relative-RLE MMX loop. |
| `render_blit_alpha_plane_mmx` | `0x0040FBE0` | high | MMX implementation of source-over-destination blending controlled by an alpha plane. |
| `render_blit_screen_rgb565_mmx` | `0x0040FE30` | high | RGB565 MMX loop for the screen-style source and destination composite. |
| `render_blit_screen_rgb555_mmx` | `0x004100C0` | high | RGB555 MMX loop for the screen-style source and destination composite. |
| `render_blit_screen_mmx` | `0x00410350` | high | Dispatches the MMX screen-style composite to the active RGB565 or RGB555 pixel format. |
| `render_blit_screen_alpha_plane_rgb565_mmx` | `0x004103C0` | high | RGB565 MMX loop for screen-style compositing controlled by a per-component alpha plane. |
| `render_blit_screen_alpha_plane_rgb555_mmx` | `0x00410670` | high | RGB555 MMX loop for screen-style compositing controlled by a per-component alpha plane. |
| `render_blit_screen_alpha_plane_mmx` | `0x00410920` | high | MMX implementation of the screen-style composite controlled by a per-component alpha plane. |
| `render_blit_alpha_mmx` | `0x004109A0` | high | MMX implementation of uniform source-over-destination alpha blending. |
| `render_blit_alpha_color_key_mmx` | `0x00410BD0` | high | MMX implementation of color-keyed uniform source-over-destination alpha blending. |
| `render_blit_color_blend_alpha_plane_mmx` | `0x00410E50` | high | MMX implementation of source-to-color blending controlled by a per-pixel alpha plane. |
| `render_blit_color_blend_mmx` | `0x004110C0` | high | MMX implementation of uniform source-to-color blending. |
| `render_blit_color_blend_color_key_mmx` | `0x00411310` | high | MMX implementation of color-keyed source-to-color blending. |
| `render_blit_additive_rgb565_mmx` | `0x004115B0` | high | RGB565 MMX loop for saturating additive source and destination blending. |
| `render_blit_additive_rgb555_mmx` | `0x00411780` | high | RGB555 MMX loop for saturating additive source and destination blending. |
| `render_blit_additive_mmx` | `0x00411950` | high | MMX implementation of saturating additive packed-pixel blending. |
| `render_blit_pointer_rle_alpha_mmx` | `0x004119C0` | high | MMX implementation of absolute-pointer-table RLE alpha drawing. |
| `render_blit_rle_alpha_color_key_mmx` | `0x00411DC0` | high | MMX implementation of color-keyed RLE alpha drawing. |
| `render_blit_rle_alpha_color_key_opacity_mmx` | `0x004121E0` | high | MMX implementation combining RLE alpha, a source color key, and global opacity. |
| `render_blit_dual_rle_alpha_color_key_mmx` | `0x00412660` | high | MMX implementation combining two RLE alpha streams with source color-key exclusion. |
| `render_blit_scale_channels_rgb565_mmx` | `0x00412CC0` | high | Unreferenced RGB565 MMX loop that scales red, green, and blue independently with three caller-supplied factors. |
| `render_blit_scale_channels_rgb555_mmx` | `0x00412FF0` | high | Unreferenced RGB555 MMX loop that scales red, green, and blue independently with three caller-supplied factors. |
| `render_blit_luminance_palette_nonzero_ramp_rgb565_mmx` | `0x00413320` | high | RGB565 MMX luminance-palette branch for caller-selected nonzero ramp indexes. |
| `render_blit_luminance_palette_nonzero_ramp_rgb555_mmx` | `0x00413580` | high | RGB555 MMX luminance-palette branch for caller-selected nonzero ramp indexes. |
| `render_blit_luminance_palette_ramp0_rgb565_mmx` | `0x004137E0` | high | RGB565 MMX luminance-palette branch specialized for ramp zero. |
| `render_blit_luminance_palette_ramp0_rgb555_mmx` | `0x004139B0` | high | RGB555 MMX luminance-palette branch specialized for ramp zero. |
| `render_blit_luminance_palette_mmx` | `0x00413B80` | high | MMX implementation of luminance-ramp color mapping. |
| `render_blit_luminance_palette_color_key_nonzero_ramp_rgb565_mmx` | `0x00413C50` | high | Color-keyed RGB565 MMX luminance-palette branch for caller-selected nonzero ramp indexes. |
| `render_blit_luminance_palette_color_key_nonzero_ramp_rgb555_mmx` | `0x00413F10` | high | Color-keyed RGB555 MMX luminance-palette branch for caller-selected nonzero ramp indexes. |
| `render_blit_luminance_palette_color_key_ramp0_rgb565_mmx` | `0x004141D0` | high | Color-keyed RGB565 MMX luminance-palette branch specialized for ramp zero. |
| `render_blit_luminance_palette_color_key_ramp0_rgb555_mmx` | `0x00414400` | high | Color-keyed RGB555 MMX luminance-palette branch specialized for ramp zero. |
| `render_blit_luminance_palette_color_key_mmx` | `0x00414630` | high | MMX implementation of color-keyed luminance-ramp mapping. |
| `render_bink_open_clip` | `0x0042E2D0` | high | Calls BinkOpen, configures playback, and registers the frame timer. |
| `render_bink_present_frame` | `0x0042E440` | high | Uses BinkWait, BinkDoFrame, BinkCopyToBuffer, and BinkNextFrame. |
| `render_get_video_system` | `0x0042E7E0` | high | Returns the VideoSystem singleton. |
| `render_get_human_image_library` | `0x0043FD60` | high | Returns the RTTI-backed HumanImageLib singleton. |
| `render_dibitmap_ctor` | `0x00448F90` | high | Constructs the exact RTTI DIBitmap as a top-down 16-bit DIB section and retains its dimensions and pixel pointer. |
| `render_dibitmap_dtor` | `0x00449150` | high | Deletes the owned DIB handle and clears the DIBitmap pixel state. |
| `render_dibitmap_get_handle` | `0x00449190` | high | Returns the DIBitmap GDI bitmap handle. |
| `render_dibitmap_get_pixels` | `0x004491B0` | high | Returns the DIBitmap pixel pointer. |
| `render_dibitmap_get_width` | `0x004491D0` | high | Returns the DIBitmap width. |
| `render_dibitmap_get_height` | `0x004491F0` | high | Returns the DIBitmap height. |
| `render_dibitmap_get_row_stride_pixels` | `0x00449210` | high | Returns the DIBitmap row stride measured in 16-bit pixels. |
| `render_dibitmap_load_archive_image` | `0x00449230` | high | Loads an archive image and sends its encoded bytes through the DIBitmap decoder. |
| `render_dibitmap_decode_image` | `0x004492A0` | high | Decodes image bytes to RGB555 and copies bounded aligned rows into a newly allocated DIBitmap. |
| `render_dibitmap_scalar_deleting_dtor` | `0x00449480` | high | Runs the DIBitmap destructor and conditionally frees the complete object. |
| `render_direct_draw_ctor` | `0x004494B0` | high | Constructs the RTTI-backed DirectDraw wrapper. |
| `render_direct_draw_dtor` | `0x00449550` | high | Runs DirectDraw wrapper cleanup during deletion. |
| `render_direct_draw_initialize` | `0x004495D0` | high | Creates DirectDraw, selects cooperative and display modes, and creates presentation surfaces. |
| `render_direct_draw_shutdown` | `0x00449CB0` | high | Releases the clipper and surfaces, restores display mode, and releases DirectDraw. |
| `render_direct_draw_create_offscreen_surface` | `0x00449D80` | high | Creates an offscreen DirectDraw surface with the requested dimensions and client-selected caps. |
| `render_direct_draw_release_surface` | `0x00449E40` | high | Releases a retained DirectDraw surface pointer when present. |
| `render_direct_draw_enter_fullscreen_mode` | `0x00449E60` | high | Enters exclusive DirectDraw mode, sets the retained display dimensions and bit depth, and restores surfaces. |
| `render_direct_draw_leave_fullscreen_mode` | `0x00449F30` | high | Restores the display mode and returns DirectDraw to the normal cooperative level. |
| `render_direct_draw_flip` | `0x00449FA0` | high | Flips the attached DirectDraw backbuffer with DDFLIP_WAIT so the call may block until the operation can complete. |
| `render_direct_draw_present_canvas` | `0x00449FD0` | high | Copies a Canvas to the DirectDraw presentation surface and recovers a lost surface. |
| `render_direct_draw_blt_canvas_to_primary` | `0x0044A260` | high | Uses DirectDraw BltFast to copy a surface-backed Canvas to the primary surface. |
| `render_direct_draw_blt_primary_to_canvas` | `0x0044A320` | high | Uses DirectDraw Blt to copy the primary surface into a surface-backed Canvas. |
| `render_direct_draw_scalar_deleting_dtor` | `0x0044A3E0` | high | Runs the DirectDraw wrapper destructor and conditionally frees the complete object. |
| `render_direct_draw_singleton_register` | `0x0044A410` | high | Registers the DirectDraw wrapper singleton instance. |
| `render_direct_draw_singleton_unregister` | `0x0044A450` | high | Unregisters the DirectDraw wrapper singleton instance. |
| `render_canvas_ctor` | `0x0044A490` | high | Constructs the RTTI-backed Canvas object. |
| `render_canvas_dtor` | `0x0044A710` | high | Releases Canvas backing, scanline offsets, alpha-mask rows, and other owned drawing state. |
| `render_canvas_is_initialized` | `0x0044A9A0` | high | Returns whether the Canvas has initialized backing state. |
| `render_canvas_is_drawable` | `0x0044A9E0` | high | Recursively checks a subcanvas parent or tests whether the Canvas has drawable backing. |
| `render_canvas_attach_surface` | `0x0044AA30` | high | Attaches a Canvas to a DirectDraw surface. |
| `render_canvas_create_memory` | `0x0044AB80` | high | Allocates a 16-bit memory canvas with width aligned to four pixels. |
| `render_canvas_create_subcanvas` | `0x0044AD50` | high | Creates a mode-2 subcanvas over a parent rectangle and inherits its backing surface and dimensions. |
| `render_canvas_initialize_point_target` | `0x0044AFF0` | high | Reinitializes the Canvas as a mode-1 point target with the supplied coordinates. |
| `render_canvas_release_backing` | `0x0044B050` | high | Releases active DirectDraw or heap-backed storage and resets the Canvas backing mode. |
| `render_canvas_release` | `0x0044B0D0` | high | Releases the current Canvas storage. |
| `render_canvas_begin` | `0x0044B160` | high | Begins pixel access and locks a wrapped surface when needed. |
| `render_canvas_end` | `0x0044B1B0` | high | Ends pixel access and unlocks a wrapped surface when needed. |
| `render_canvas_set_draw_rgb` | `0x0044B210` | high | Packs an RGB triplet into the client 16-bit format and installs it as the primary draw color. |
| `render_canvas_set_secondary_rgb` | `0x0044B240` | high | Packs an RGB triplet and installs it as the secondary Canvas color. |
| `render_canvas_set_draw_color` | `0x0044B270` | high | Replaces the primary 16-bit draw color and returns its previous value. |
| `render_canvas_set_secondary_color` | `0x0044B2A0` | high | Replaces the secondary 16-bit Canvas color and returns its previous value. |
| `render_canvas_set_draw_palette_color` | `0x0044B2D0` | high | Resolves a client palette index and installs it as the primary draw color. |
| `render_canvas_set_secondary_palette_color` | `0x0044B300` | high | Resolves a client palette index and installs it as the secondary Canvas color. |
| `render_canvas_set_text_position_wrapper` | `0x0044B330` | high | Thin wrapper around the Canvas text-position setter. |
| `render_canvas_set_text_position` | `0x0044B350` | high | Stores the x and y position consumed by subsequent Canvas text drawing. |
| `render_canvas_map_rect_to_absolute_clip` | `0x0044B370` | high | Intersects a local rectangle with Canvas clipping and maps it to absolute backing coordinates. |
| `render_canvas_get_absolute_clip_rect` | `0x0044B420` | high | Builds the absolute clip rectangle by recursively intersecting a subcanvas with its parent. |
| `render_canvas_set_clip_region` | `0x0044B640` | high | Copies a rectangle wrapper into Canvas clipping, or resets clipping to the Canvas bounds. |
| `render_canvas_set_clip_rect` | `0x0044B670` | high | Sets Canvas clipping from a raw rectangle, defaulting to the Canvas bounds. |
| `render_canvas_get_clip_region` | `0x0044B6D0` | high | Copies the Canvas clip region into the caller's rectangle wrapper. |
| `render_canvas_lock_pixels` | `0x0044B6F0` | high | Locks Canvas backing when needed and returns its pixel pointer and row pitch. |
| `render_canvas_unlock_pixels` | `0x0044B730` | high | Unlocks a previously locked Canvas backing. |
| `render_canvas_resolve_backing` | `0x0044B750` | high | Walks a subcanvas parent chain, accumulates offsets, and inherits the owning surface. |
| `render_canvas_lock_backing` | `0x0044B820` | high | Locks heap or DirectDraw backing and caches its pixel pointer and pitch. |
| `render_canvas_unlock_backing` | `0x0044B960` | high | Unlocks DirectDraw backing, restoring a lost surface and retrying when required. |
| `render_canvas_copy_indexed_image` | `0x0044B9D0` | high | Copies a palette-indexed image into 16-bit Canvas pixels through the client RGB packer. |
| `render_canvas_get_bounds_ptr` | `0x0044BBC0` | high | Returns a pointer to the Canvas bounds rectangle. |
| `render_canvas_get_bounds` | `0x0044BBE0` | high | Copies the Canvas bounds rectangle to caller storage. |
| `render_color_table_resolve_entry` | `0x0044CEA0` | high | Lazily resolves one six-color entry, using palette-index fallbacks for built-in entries. |
| `render_canvas_set_flip_flags` | `0x0044CF60` | high | Stores the Canvas vertical and horizontal image-flip flags. |
| `render_canvas_get_flip_flags` | `0x0044CF90` | high | Returns the Canvas vertical and horizontal flip flags used by image blitting. |
| `render_canvas_set_color_key` | `0x0044CFC0` | high | Applies a 16-bit transparency key to DirectDraw backing or records it for heap backing. |
| `render_canvas_set_color_key_directdraw_tail` | `0x0044D03E` | high | Compiler-split internal success tail of the DirectDraw color-key setter with no independent callers. |
| `render_canvas_get_color_key` | `0x0044D070` | high | Returns the Canvas 16-bit transparency color key. |
| `render_canvas_get_scanline_offset` | `0x0044D090` | high | Returns a phased scanline offset under the configured clamp-or-wrap mode. |
| `render_canvas_get_scanline_offsets` | `0x0044D140` | high | Returns the scanline-offset array and writes its element count. |
| `render_canvas_set_scanline_offset` | `0x0044D170` | high | Stores one scanline offset when the requested index is in range. |
| `render_canvas_set_scanline_offset_phase` | `0x0044D1B0` | high | Sets the phase added when looking up scanline offsets. |
| `render_canvas_get_scanline_offset_raw` | `0x0044D1D0` | high | Returns one unphased scanline-offset entry, or zero when out of range. |
| `render_canvas_get_scanline_offset_mode` | `0x0044D210` | high | Returns the scanline-offset addressing mode used for clamped or wrapped lookup. |
| `render_canvas_rotate_scanline_offsets` | `0x0044D230` | high | Rotates the scanline-offset array by a signed amount with optional caller scratch storage. |
| `render_canvas_clear_scanline_offsets` | `0x0044D460` | high | Frees the Canvas scanline-offset array and clears its count. |
| `render_canvas_configure_scanline_offsets` | `0x0044D4B0` | high | Clears and allocates a scanline-offset array with the requested count and addressing mode. |
| `render_canvas_set_alpha_mask_rows` | `0x0044D540` | high | Copies a per-row alpha-mask pointer array and records its row count and mode. |
| `render_canvas_clear_alpha_mask_rows` | `0x0044D610` | high | Frees the Canvas alpha-mask row array and clears its count. |
| `render_canvas_set_alpha_mask_parameters` | `0x0044D660` | high | Stores four byte-sized alpha-mask parameters consumed by software blitting. |
| `render_canvas_get_alpha_mask_rows` | `0x0044D6A0` | high | Returns the per-row alpha-mask array and writes its row count and mode. |
| `render_canvas_get_alpha_mask_parameters` | `0x0044D6E0` | high | Returns four byte-sized alpha-mask parameters consumed by software blitting. |
| `render_write_canvas_jpeg` | `0x0044D730` | high | Locks one canvas and sends its RGB16 pixels to the shared JFIF writer. |
| `render_canvas_scalar_deleting_dtor` | `0x0044D7F0` | high | Runs the Canvas destructor and conditionally frees the complete object. |
| `render_get_direct_draw` | `0x0044D820` | high | Returns the DirectDraw wrapper singleton. |
| `render_get_palette_manager` | `0x0044D830` | high | Returns the RTTI-backed PaletteMan singleton. |
| `render_canvas_blit_pixels_software` | `0x0044D860` | high | Runs the software Canvas blit with clipping, scanline offsets, flips, color key, and optional alpha masks. |
| `render_blit_image` | `0x0044DE30` | high | Draws a decoded Image with copy, blend, alpha, and special plane modes. |
| `render_blit_pixmap` | `0x0044FB80` | high | Draws an indexed PixMap with transparent zero pixels and several software blend modes. |
| `render_blit_pixel_buffer` | `0x004513D0` | high | Blits a raw pixel buffer through the format-selected software dispatch with clipping, modes, and optional flips. |
| `render_blit_canvas` | `0x00451E40` | high | Copies or blends one Canvas into another. |
| `render_canvas_blit_mask` | `0x004526C0` | high | Draws a one-bit bitmap mask into a 16-bit Canvas using the current foreground, background, and blend mode. |
| `render_canvas_scroll_rect` | `0x00452D20` | high | Scrolls a clipped Canvas rectangle in place and accumulates the newly exposed area into the caller region. |
| `render_canvas_tile_pixmap` | `0x00453860` | high | Temporarily clips a Canvas, tiles a pixmap across the target rectangle, and restores the previous clip. |
| `render_blit_indexed_pixmap_palette` | `0x00453A80` | high | Draws an indexed pixmap through its selected palette with transparency and optional horizontal reversal. |
| `render_blit_pixmap_with_palette_mappings` | `0x00453E60` | high | Draws indexed monster pixels while replacing configured source-index ranges through ordered palette-family and palette-selector mappings. |
| `render_canvas_blend_nonzero_with_draw_color` | `0x00454540` | high | Blends each nonzero pixel in a clipped rectangle with the Canvas primary draw color. |
| `render_canvas_blend_nonzero_with_color` | `0x00454570` | high | Blends each nonzero pixel in a clipped rectangle with an explicit 16-bit color. |
| `render_canvas_blend_rect` | `0x00454730` | high | Blends a clipped rectangle toward a color using a uniform weight from 0 through 32. |
| `render_average_pixels` | `0x004548B0` | high | Combines two 16-bit pixels with the fixed component-average lookup path. |
| `render_clip_blit_rects` | `0x004548F0` | high | Clips source and destination rectangles together and adjusts their origins for horizontal or vertical flips. |
| `render_canvas_set_pixel_draw_color` | `0x00454BA0` | high | Writes the Canvas primary draw color to one clipped pixel. |
| `render_canvas_set_pixel_color` | `0x00454BD0` | high | Writes an explicit 16-bit color to one clipped Canvas pixel. |
| `render_canvas_set_pixel_rgb` | `0x00454C80` | high | Packs an RGB triplet and writes it to one clipped Canvas pixel. |
| `render_canvas_draw_line` | `0x00454D40` | high | Draws a clipped line between two points using the Canvas primary draw color. |
| `render_canvas_draw_line_relative` | `0x004550E0` | high | Draws from the current Canvas position by a relative delta and advances the position. |
| `render_canvas_draw_line_to` | `0x00455160` | high | Draws from the current Canvas position to an absolute point and stores the new position. |
| `render_canvas_draw_horizontal_span_draw_color` | `0x004551C0` | high | Draws a horizontal span from the current position with the Canvas primary draw color. |
| `render_canvas_draw_horizontal_span` | `0x004551F0` | high | Draws a colored horizontal span under the Canvas copy, transparency, blend, and dither modes. |
| `render_canvas_fill_diamond_palette` | `0x004554D0` | high | Fills a clipped diamond marker with a palette-resolved color and optional dither mode. |
| `render_canvas_set_pixel_palette_color` | `0x00455710` | high | Resolves a palette index and writes it to one clipped Canvas pixel. |
| `render_measure_fixed_width_text` | `0x004558F0` | high | Returns the six-pixel-cell width for a supplied byte count. |
| `render_canvas_draw_glyph` | `0x00455910` | high | Resolves one 16-bit byte-code key through FontImageLib, blits its one-bit mask, and advances the Canvas cursor. |
| `render_canvas_draw_text` | `0x00455A30` | high | Splits an ANSI byte string with IsDBCSLeadByte, builds one LFT glyph mask per key, and draws it to the software Canvas. |
| `render_canvas_draw_wrapped_fixed_text` | `0x00455D50` | high | Draws DBCS-aware fixed-cell text using six-pixel columns and twelve-pixel line steps. |
| `render_canvas_draw_rect_outline` | `0x00456000` | high | Draws the clipped outline of a rectangle and preserves the prior Canvas drawing position. |
| `render_canvas_fill_rect_draw_color` | `0x004561D0` | high | Fills a clipped rectangle with the Canvas primary draw color and preserves the prior position. |
| `render_canvas_clear_rect` | `0x00456370` | high | Clears a clipped Canvas rectangle to pixel value zero. |
| `render_canvas_toggle_rect_colors` | `0x004564D0` | high | Toggles each pixel in a clipped rectangle between the primary and secondary Canvas colors. |
| `render_canvas_clear` | `0x00456690` | high | Clears the complete Canvas through the clipped rectangle clear path. |
| `render_get_font_image_library` | `0x004566B0` | high | Returns the RTTI-backed FontImageLib singleton used by the active text renderer. |
| `render_effect_image_session_ctor` | `0x004575B0` | high | Opens the available EFA or EPF variant for one effect image session. |
| `render_effect_image_session_dtor` | `0x00457D50` | high | Destroys an EffectImageSession, releases loaded frame records, and frees its user-pointer array. |
| `render_effect_image_session_get_total_duration` | `0x00457DC0` | high | Sums the duration field across every loaded effect-image frame record. |
| `render_effect_image_session_get_effect_id` | `0x00457E20` | high | Returns the effect identifier retained by an EffectImageSession. |
| `render_effect_image_session_get_frame_count` | `0x00457E40` | high | Returns the number of loaded frame records in an EffectImageSession. |
| `render_effect_image_session_add_user` | `0x00457E60` | high | Adds an effect user pointer when absent and updates the session activity time. |
| `render_effect_image_session_remove_user` | `0x00457F10` | high | Removes an effect user pointer by swapping down the last entry. |
| `render_effect_image_session_get_user_count` | `0x00457FB0` | high | Returns the number of active users retained by an EffectImageSession. |
| `render_get_effect_frame_image` | `0x00457FD0` | high | Lazily decodes and caches one requested effect frame image. |
| `render_effect_image_session_get_frame_info` | `0x00458630` | high | Returns one loaded frame rectangle, two numeric properties, and a low-bit flag. |
| `render_effect_image_session_get_frame_image` | `0x004586D0` | high | Returns one loaded frame image pointer and writes its duration. |
| `render_effect_image_pool_ctor` | `0x00458720` | high | Constructs EffectImagePool, loads its frame table, allocates session slots, and schedules 30-second cleanup. |
| `render_effect_image_pool_dtor` | `0x00458860` | high | Clears EffectImagePool sessions, releases the frame table, and tears down its timer base. |
| `render_effect_image_pool_clear` | `0x00458900` | high | Destroys every retained EffectImageSession and frees the effect-ID pointer array. |
| `render_effect_image_pool_get_frame` | `0x004589C0` | high | Creates one EffectImageSession on the first request for an effect ID, retains it, and asks it for the selected frame. |
| `render_effect_image_pool_remove_user` | `0x00458AA0` | high | Removes a user pointer from one existing effect-image session. |
| `render_effect_image_pool_prune_inactive` | `0x00458B00` | high | Deletes effect-image sessions with no retained activity for more than 30 seconds. |
| `render_effect_image_pool_timer_tick` | `0x00458BE0` | high | Prunes inactive effect-image sessions and requeues the cleanup timer. |
| `render_effect_image_pool_resolve_frame_index` | `0x00458C20` | high | Resolves an animation frame index from effect metadata, session state, and the requested frame. |
| `render_effect_image_pool_get_frame_info` | `0x00458CF0` | high | Returns rectangle and flag metadata for one loaded effect frame. |
| `render_effect_image_pool_get_frame_image` | `0x00458D50` | high | Returns one loaded effect frame image pointer and writes its duration. |
| `render_effect_image_pool_get_total_duration` | `0x00458DA0` | high | Returns the total duration retained for one loaded effect-image session. |
| `render_effect_frame_table_ctor` | `0x00458DF0` | high | Constructs the exact RTTI EffectFrameTable and loads effect-frame metadata. |
| `render_effect_frame_table_dtor` | `0x00458E50` | high | Frees EffectFrameTable-owned buffers and runs the LObject base destructor. |
| `render_effect_frame_table_lookup` | `0x00459210` | high | Looks up one byte by effect identifier and frame index in the EffectFrameTable. |
| `render_effect_frame_record_init` | `0x00459240` | high | Initializes an effect-frame record's owned pointers and duration to zero. |
| `render_effect_frame_record_dtor` | `0x00459270` | high | Releases the owned image object and auxiliary allocation in an effect-frame record. |
| `render_effect_image_session_scalar_deleting_dtor` | `0x004592E0` | high | Runs the EffectImageSession destructor and conditionally frees the complete object. |
| `render_effect_frame_record_array_deleting_dtor` | `0x00459310` | high | Destroys one effect-frame record or an allocated array of 0x2C-byte records. |
| `render_effect_image_pool_scalar_deleting_dtor` | `0x00459380` | high | Runs the EffectImagePool destructor and conditionally frees the complete object. |
| `render_effect_frame_table_scalar_deleting_dtor` | `0x004593B0` | high | Runs the EffectFrameTable destructor and conditionally frees the complete object. |
| `render_effect_image_pool_singleton_register` | `0x004593E0` | high | Registers the complete EffectImagePool from its TimerHandler secondary-base pointer. |
| `render_effect_image_pool_singleton_unregister` | `0x00459420` | high | Clears the EffectImagePool singleton when the adjusted TimerHandler owner matches. |
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
| `render_map_rgb565_luminance_palette` | `0x00481980` | high | Computes five-bit luminance from RGB565 and resolves it through one of four 32-entry packed-color ramps. |
| `render_map_rgb555_luminance_palette` | `0x00481A10` | high | Computes five-bit luminance from RGB555 and resolves it through one of four 32-entry packed-color ramps. |
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
| `render_screen_tree_frame` | `0x00554040` | high | Walks the dirty root screen tree and presents only when a dirty entry or forced redraw marks the root for output. |
| `render_screen_timer_tick` | `0x00554270` | high | Runs the root ScreenPane redraw check and requeues timer ID 0 from the current time using the compiled 10 ms interval. |
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
| `render_damage_effect_image_ctor` | `0x005BE6A0` | high | Constructs exact RTTI World::DamageEffectImage and generates 26 five-by-27 meter stages in one 130-by-27 canvas using palette indexes 0x28, 0x97, and 0x89. |
| `render_damage_effect_image_get_frame` | `0x005BE8C0` | high | Clamps a requested stage to 0 through 25 and selects its five-by-27 slice from the generated damage-meter canvas. |
| `render_create_damage_effect_image` | `0x005BE950` | high | Allocates and constructs the 0x124-byte exact RTTI World::CDamageEffectImage object used by the damage-effect image cache. |
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
| `render_world_tile_marker` | `0x005D3DD0` | high | Draws a small symmetric diamond marker at one projected map coordinate before the world-object queues. |
| `render_world_frame` | `0x005D3F70` | high | Draws ground, map backgrounds, and sorted world objects for one world frame. |
| `render_replay_layer_zero_and_self` | `0x005D4360` | high | After the ordinary world frame, draws the separate layer-zero queue and replays the recorded self entry; the normal non-blinded state supplies the selector that makes living sprites use blend mode 3. |
| `render_ground_layer` | `0x005D6A50` | high | Updates and draws the cached visible ground-tile layer. |
| `render_set_ground_bank` | `0x005D7410` | high | Stores the active ground-bank selector and clears the cached ground layer. |
| `render_ground_tile` | `0x005D7690` | high | Copies one decoded isometric tile diamond into the ground cache canvas. |
| `render_world_damage_object` | `0x005DC5A0` | high | Draws the selected generated damage-meter frame at its target-relative world position. |
| `render_effect_object` | `0x005DD380` | high | Draws a world effect frame with its selected software blend mode. |
| `render_update_effect_frame` | `0x005DD470` | high | Advances a world effect through its Effect.tbl frame sequence. |
| `render_item_object_get_bounds` | `0x005DE5A0` | high | Returns the item's draw rectangle and its fixed -16 to +16 tile-relative bounds through WorldObject_Item primary-vtable slot 0x14. |
| `render_item_object` | `0x005DE620` | high | Draws a ground item and computes mode 3 for a nonzero fade selector, although the original final body blit reloads the ordinary object mode instead of consuming that local result. |
| `render_copy_human_appearance_record` | `0x005DEF70` | high | Rearranges the parser-friendly SDrawHumanObjects appearance fields into the stable 0x30-byte HumanAppearanceRecord used by world objects and image sessions. |
| `render_living_object` | `0x005DF950` | high | Draws a living sprite with normal, highlighted, or transparent state. |
| `render_human_apply_appearance` | `0x005E0070` | high | Copies the packet-owned appearance record and forwards it to the live human object. |
| `render_human_apply_appearance_record` | `0x005E00C0` | high | Copies HumanAppearanceRecord to WorldObject_Human +0xA4, derives nonblocking and translucent state, creates the 0x918-byte HumanObjectImageSession, and refreshes direction and motion. |
| `render_monster_apply_appearance` | `0x005E0370` | high | Resolves the untagged monster sprite, creates MonsterObjectImageSession, applies Direction and up to four palette selectors, and refreshes motion. |
| `render_static_object_ctor` | `0x005E42F0` | high | Stores the static tile ID, side, image cache, SOTP render flags, and draw state. |
| `render_static_object` | `0x005E47E0` | high | Draws a fixed world object with its SOTP-selected software blend mode. |
| `render_world_apply_view_layout` | `0x005EE950` | high | Applies a six-value GUI MAP rectangle and view center to WorldPane, resets view-dependent state, invalidates lighting, and schedules a redraw. |
| `render_select_human_part_sprite` | `0x005FD8D0` | high | Selects the sprite ID for each of 21 human body and equipment categories; an overcoat suppresses ordinary pants, armor, and arms, but the body-form selector does not independently suppress equipment. |
| `render_format_human_part_filename` | `0x005FDA90` | high | Builds gendered human-part EPF filenames; body resource 5 resolves through MM005 or WM005 motion files. |
| `render_format_human_part_from_appearance` | `0x005FDC50` | high | Selects the current category's sprite ID from HumanAppearanceRecord and formats its motion-specific resource name. |
| `render_load_human_part_frame` | `0x005FDC90` | high | Resolves one human part resource, selects its direction-group frame, and attaches the applicable asset or appearance palette. |
| `render_build_human_frame_layers` | `0x005FE3A0` | high | Chooses the direction and body-dependent back-to-front category table and builds the current human-part frame descriptors. |
| `render_draw_human_part` | `0x005FED60` | high | Draws one selected human-part frame into the temporary composite with direction-dependent horizontal mirroring. |
| `render_draw_human_frame_layers` | `0x005FEE70` | high | Walks the selected 21-entry category order and draws every present part into the human composite. |
| `render_human_part_apply_direction` | `0x005FEF70` | high | Applies the direction-group frame offset and mirror state to one human part. |
| `render_human_direction_frame_group` | `0x005FF000` | high | Maps left and up to stored frame group 0 and down and right to stored frame group 1. |
| `render_human_direction_is_mirrored` | `0x005FF020` | high | Returns true for right and up so those directions mirror the paired stored human view. |
| `render_human_frame_apply_direction` | `0x005FF550` | high | Applies the current direction selection to a cached human-frame descriptor. |
| `render_human_walk_sequence_ctor` | `0x005FFCD0` | high | Builds a four-step or eight-step human walk interpolation sequence from fixed pixel, frame, and per-step delay tables. |
| `render_human_stand_motion_data_ctor` | `0x006000D0` | high | Constructs standing-motion data and resolves up to 21 body and equipment sprite parts from HumanAppearanceRecord. |
| `render_human_stand_build_frame` | `0x00600150` | high | Builds one standing human frame from the initialized part resources and current direction. |
| `render_human_stand_initialize_parts` | `0x006002F0` | high | Initializes categories 0 through 20 for every human body, including Ghost, Jester, Head, and Blank forms; zero selectors omit individual resources. |
| `render_create_human_stand_motion_data` | `0x00600670` | high | Allocates the initial standing-motion data for a human image session. |
| `render_monster_image_session_ctor` | `0x006017C0` | high | Constructs the 0xE4-byte RTTI MonsterObjectImageSession, including resource pointers, frame and animation state, and four 0x10-byte palette mappings. |
| `render_monster_apply_palette_selectors` | `0x00601A20` | high | Copies at most four resource-defined 16-byte palette mappings, replaces their selector fields from packet bytes, and enables mapped monster rendering. |
| `render_monster_select_motion_sequence` | `0x00601DD0` | high | Accepts motion IDs 0x01, 0x83, 0x84, and 0x85, selects one of three cached monster motion resources, and leaves the caller's duration unchanged. |
| `render_human_image_session_ctor` | `0x00602240` | high | Constructs the 0x918-byte RTTI-backed HumanObjectImageSession with HumanAppearanceRecord, a 21-part frame cache, 21 0x50-byte render states, and animation state. |
| `render_human_image_session_draw` | `0x006023E0` | high | Draws the image session's current cached human layers into the caller's composite canvas. |
| `render_human_image_session_advance_frame` | `0x006026D0` | high | Advances the active human motion and rebuilds direction-dependent frame state when needed. |
| `render_human_image_session_cache_frame_layers` | `0x00602940` | high | Caches the current motion's ordered human-part descriptors for the final draw. |
| `render_human_select_motion_sequence` | `0x00602A40` | high | Selects fixed, table-driven, or appearance-dependent human body motions; normal table motions replace the caller duration with 500, 1000, or 1500 ms. |
| `render_human_select_walk_sequence` | `0x00602CA0` | high | Selects the remote-human, local coarse, or local smooth walk sequence; ScrollLevel chooses four 114 ms steps or eight 57 ms steps for WorldObject_User. |
| `render_merge_light_mask_max` | `0x006036B0` | high | Merges a rectangular 8-bit light image into the viewport mask by retaining the greater value at each pixel. |

## Audio

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `audio_bgm_player_ctor` | `0x004056C0` | high | Constructs the RTTI-backed BGMPlayer, installs Miles file callbacks, and keeps one stream handle. |
| `audio_bgm_player_dtor` | `0x004057A0` | high | Stops the active music path and unregisters the BGMPlayer singleton. |
| `audio_bgm_initialize` | `0x00405810` | high | Trivial BGMPlayer initialization hook called by SoundManager immediately after construction; reports success. |
| `audio_bgm_shutdown` | `0x00405830` | high | Cancels fade timers, pauses and closes the stream, and clears its handle. |
| `audio_bgm_play_path` | `0x00405880` | high | Queues one path for the BGM transition state machine. |
| `audio_bgm_queue_track` | `0x004058B0` | high | Saves a pending music path and starts the fade timer. |
| `audio_bgm_queue_stop` | `0x004058F0` | high | Queues an empty path so the current music fades out and closes. |
| `audio_bgm_get_target_volume` | `0x00405920` | high | Returns the one-byte BGM target volume. |
| `audio_bgm_set_target_volume` | `0x00405940` | high | Changes the one-byte BGM target and schedules a fade tick when needed. |
| `audio_bgm_is_unmuted` | `0x00405980` | high | Returns the BGMPlayer output-enabled byte cleared by mute and restored by unmute. |
| `audio_bgm_mute` | `0x004059A0` | high | Mutes the Miles stream output without replacing the stored target volume. |
| `audio_bgm_unmute` | `0x004059D0` | high | Restores stream output from the current fade volume. |
| `audio_bgm_file_open` | `0x00405A00` | high | Rewrites the logical .mp3 extension to .mus and opens the loose music file. |
| `audio_bgm_file_close` | `0x00405AB0` | high | Closes a BGM file handle for the Miles callback set. |
| `audio_bgm_file_seek` | `0x00405AD0` | high | Implements seek and position queries for the Miles BGM file callbacks. |
| `audio_bgm_file_read` | `0x00405B40` | high | Reads bytes for the Miles BGM file callbacks. |
| `audio_bgm_timer_callback` | `0x00405B80` | high | Advances timer ID 0 and schedules another BGM fade tick after 200 ms while needed. |
| `audio_bgm_transition_tick` | `0x00405BC0` | high | Fades the old stream to zero, replaces it, and fades the new stream toward the target. |
| `audio_bgm_schedule_tick` | `0x00405E20` | high | Schedules a 200 ms BGM transition timer through the shared event system. |
| `audio_bgm_player_scalar_deleting_dtor` | `0x00405E60` | high | Runs the BGMPlayer destructor and conditionally frees the complete object. |
| `audio_bgm_register_singleton` | `0x00405E90` | high | Registers the complete BGMPlayer pointer from its Singleton secondary-base subobject. |
| `audio_bgm_unregister_singleton` | `0x00405ED0` | high | Clears the BGMPlayer singleton pointer when the registered instance is destroyed. |
| `audio_get_miles_driver` | `0x00405F10` | high | Returns the shared Miles digital driver handle used by BGM, sound effects, and video audio. |
| `audio_is_miles_driver_open` | `0x0042E730` | high | Returns whether the Miles audio driver pointer is present. |
| `audio_has_sound_manager` | `0x004316C0` | high | Reports whether the global sound-manager singleton exists. |
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
| `file_album_header_clear` | `0x00402B50` | high | Clears the complete 0x40-byte album.dat header used before an empty album is initialized. |
| `file_album_record_clear_serialized_fields` | `0x00402B70` | high | Clears the 0x60-byte serialized portion of one album record without touching its two runtime buffer pointers. |
| `file_album_record_ctor` | `0x00402B90` | high | Clears both runtime buffer pointers and initializes the 0x60-byte serialized portion of one 0x68-byte album record. |
| `file_album_record_dtor` | `0x00402BC0` | high | Releases one album record's retained compressed payload and inflated pixel buffer. |
| `file_album_record_copy_assign` | `0x00402C10` | high | Releases the destination buffers, deep-copies an active source record's compressed payload, inflates its pixels, and converts for the active renderer when required. |
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
| `file_album_record_vector_deleting_dtor` | `0x00403E20` | high | Implements the MSVC scalar/vector deleting-destructor wrapper for one record or a count-prefixed array of 0x68-byte album records. |
| `file_bulletin_bang_find_or_append_user_record` | `0x00428070` | high | Finds a fixed-width user record or appends a zeroed record in the open bang-list file. |
| `file_bulletin_bang_open_list` | `0x004285E0` | high | Opens banglist&lt;character&gt;.txt for update, creating it when absent. |
| `file_hpf_compressor_ctor` | `0x00431730` | high | Constructs exact RTTI Compressor and initializes its owned HPF decode buffer. |
| `file_hpf_compressor_dtor` | `0x004317B0` | high | Releases the Compressor-owned HPF decode buffer. |
| `file_hpf_clear_decode_result` | `0x00431840` | high | Clears and frees the current Compressor decode result. |
| `file_hpf_decode_strict_allocating` | `0x00431860` | high | Allocates an input-size-times-ten output buffer, requires HPF magic 0xFF02AA55, and decodes through symbol 256. |
| `file_hpf_decode` | `0x004319B0` | high | Checks magic 0xFF02AA55, decodes symbols through an adaptive tree, and accepts raw input when magic is absent. |
| `file_hpf_tree_initialize` | `0x00431B80` | high | Builds the complete initial tree for byte symbols and the 256 terminator. |
| `file_hpf_decode_symbol` | `0x00431C40` | high | Reads bits least-significant bit first and walks the active HPF tree to a symbol leaf. |
| `file_hpf_rotate_tree` | `0x00431D20` | high | Applies the parent and sibling rotations used after every decoded HPF symbol. |
| `file_hpf_compressor_scalar_deleting_dtor` | `0x00431E20` | high | Compiler scalar-deleting destructor for exact RTTI Compressor. |
| `file_hpf_compressor_singleton_register` | `0x00431E50` | high | Registers the Compressor singleton. |
| `file_hpf_compressor_singleton_unregister` | `0x00431E90` | high | Clears the Compressor singleton when the supplied instance owns it. |
| `file_color_table_use_stream_input` | `0x0044CBE0` | high | Selects a CRT stream as color-table parser input and clears memory-input state. |
| `file_color_table_use_memory_input` | `0x0044CC00` | high | Selects a bounded memory buffer as color-table parser input and resets its cursor. |
| `file_color_table_read_byte` | `0x0044CC30` | high | Reads one byte from active stream or memory input, returning -1 at end of input. |
| `file_color_table_read_decimal` | `0x0044CCA0` | high | Skips non-digits and parses the next unsigned decimal integer from color-table input. |
| `file_load_color_table` | `0x0044CD50` | medium | Loads color.tbl records and packs six RGB triples per record for the renderer. |
| `file_open_efa` | `0x00456F30` | high | Opens an EFA resource and returns its u32 frame count from header +0x04 and u32 frame interval from header +0x08. |
| `file_load_efa_frame` | `0x00456FA0` | high | Finds an EFA archive entry and decodes the requested frame into caller-provided image metadata. |
| `file_decode_efa_frame` | `0x00457030` | high | Inflates one zlib payload from a 0x40-byte EFA frame record and builds an Image view. |
| `file_load_effect_frame_table` | `0x00458ED0` | high | Parses Effect.tbl decimal frame sequences into per-effect tables. |
| `file_archive_xor_words` | `0x00471DC0` | high | XORs a buffer in 32-bit words for the extended DAT header and index path. |
| `file_archive_open` | `0x00471E00` | high | Opens resource or loose DAT input and maps either the legacy index or the extended chunked index. |
| `file_archive_find_entry` | `0x00472470` | high | Looks up a named entry in an opened archive. |
| `file_archive_get_entry_data` | `0x00472900` | high | Returns the mapped data pointer for an archive entry. |
| `file_get_main_archive` | `0x00472C70` | high | Lazily constructs and returns the archive object opened as Legend.dat with DarkAges.dat fallback during startup. |
| `file_load_variant_color_table` | `0x0047DEB0` | medium | Loads one numbered color table family used by renderable assets. |
| `file_hea_build_row_views` | `0x00487380` | high | Clips a mask-canvas rectangle and builds one run pointer per pixel scanline; it scans horizontal band checkpoints but client 7.41 always uses band 0's row-offset table. |
| `file_hea_open` | `0x004875B0` | high | Maps the HEA header, band array, row offsets, and packed run stream. |
| `file_hea_project_map_position` | `0x004876D0` | high | Projects two map axes into the padded HEA mask canvas with 28-pixel horizontal and 14-pixel vertical steps, using header screen width and height as margins. |
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
| `file_load_ground_attribute_table` | `0x0058B8C0` | high | Loads structured ground attributes from gndattr.tbl in the active asset archive. |
| `file_parse_ground_attribute_table` | `0x0058B930` | high | Parses the structured set_attr records and applies each attribute set to its listed tile IDs and inclusive ranges. |
| `file_apply_ground_attribute_record` | `0x0058B9B0` | high | Interns one parsed attribute set and assigns it to each ground tile ID covered by the record's apply_to list. |
| `file_intern_ground_attribute_set` | `0x0058BA80` | high | Converts ATTR_gnd_paint height 1 and 2 into separate flags while retaining larger heights as color-and-depth paint records. |
| `file_read_dbcs_line` | `0x00592680` | high | Reads until LF, EOF, or the caller-supplied byte count, tracks DBCS lead-byte state so an LF-valued trail byte does not end the line, then appends NUL. |
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
| `map_can_move_direction` | `0x005EFFE0` | high | Checks bounds and the saved appearance action lock, lets privilege levels 1 and 2 bypass the remaining dynamic-object and direction-specific SOTP collision checks, and otherwise applies CreatureType behavior and SOTP masks. |
| `map_has_special_movement_permission` | `0x005F0980` | high | Grants permission for any nonzero SStatus privilege; otherwise scans the 89 retained skill names for localized message slot 0x77. |
| `map_try_move_local_player` | `0x005F09E0` | high | Applies the special-state privilege-or-skill permission check, then the saved appearance action lock, dynamic occupants, and direction-specific SOTP collision before selecting the local walk sequence and sending CMove. |
| `map_apply_weather_mode` | `0x005F26C0` | high | Creates Snow for mode 1, performs no local setup for project-named Rain mode 2, and enables black ambient plus object light masks for Darkness mode 3. |
| `map_finish_transfer` | `0x005F2DE0` | high | Destroys MapLoadingPane, advances the WorldPane map generation, and either applies prepared map storage immediately or schedules the alternate completion path. |
| `map_interface_apply_world_layout` | `0x005F9B20` | high | MapInterface virtual wrapper that adjusts the interface pointer to its containing WorldPane_Impl and calls render_world_apply_view_layout. |
| `file_load_static_tile_pixmap` | `0x005FD500` | high | Opens and decodes one base or alternate static HPF resource into a pixmap view. |
| `file_open_static_tile` | `0x005FD700` | high | Opens stsNNNNN.hpf in alternate mode and falls back to stcNNNNN.hpf when missing. |
| `file_format_static_tile_path` | `0x005FD850` | high | Formats stcNNNNN.hpf for base art or stsNNNNN.hpf for alternate art. |
| `file_zlib_uncompress` | `0x006043B0` | high | Bundled zlib 1.1.3 uncompress entry shared by assets and network-managed data. |

## Crypto

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `crypto_md5_init` | `0x00401000` | high | Initializes the four standard MD5 chaining words and clears the 64-bit bit count. |
| `crypto_md5_update` | `0x00401040` | high | Updates the MD5 bit count, fills the pending 64-byte block, and transforms every complete input block. |
| `crypto_md5_final` | `0x00401150` | high | Pads to byte 56 modulo 64, appends the original little-endian bit count, emits the 16-byte digest, and clears the context. |
| `crypto_md5_digest` | `0x00401200` | high | Performs init, update, and final to hash one caller-supplied byte span into a 16-byte MD5 digest. |
| `crypto_md5_transform` | `0x00401250` | high | Runs the standard 64-step MD5 compression function over one 64-byte block and adds the result to the chaining state. |
| `crypto_md5_encode_words_le` | `0x004020B0` | high | Serializes 32-bit words into little-endian bytes for the MD5 digest and bit-count paths. |
| `crypto_md5_decode_words_le` | `0x00402150` | high | Decodes little-endian bytes into 32-bit words for the MD5 compression block. |
| `crypto_md5_hex_string` | `0x004C7D80` | high | Hashes a NUL-terminated string and returns lowercase MD5 hexadecimal text. |
| `crypto_md5_bytes` | `0x004C7E30` | high | Hashes an explicit byte span and retains the raw MD5 digest. |

## Uncertain

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `maybe_command_dispatcher_noop` | `0x0042F410` | low | Empty CommandDispatcher virtual method; the exact interface role is not yet established. |
| `maybe_command_dispatcher_return_argument` | `0x0042F420` | low | CommandDispatcher virtual method that returns its second argument unchanged; the exact interface role is not yet established. |
| `maybe_net_load_endpoint_from_command_file` | `0x00433B50` | medium | Unreferenced parser that treats command-line tail text as a filename and loads a host or IPv4 address plus port into Config. |
| `maybe_app_configure_distribution_mode_12` | `0x00436A10` | medium | Dormant mode 12 handler with no matching marker return; sets connection flags without installing an endpoint. |
| `maybe_ui_manufacture_dialog_ctor_from_body` | `0x004C1AD0` | medium | Duplicates the lmanu.txt construction path and applies a decoded opcode-first body, but no live static caller was recovered. |
| `maybe_ui_manufacture_dialog_apply_manual_body` | `0x004C2990` | medium | Applies RecipeCount or Recipe from a decoded opcode-first body for the duplicate raw-body pane path. |

## Other

| Function | Static address | Confidence | Role |
| --- | --- | --- | --- |
| `point_queue_ctor` | `0x00404A20` | high | Constructs exact RTTI PointQueue as a 400-entry circular buffer of two-word points with head and tail at zero. |
| `point_queue_dtor` | `0x00404A60` | high | Restores the exact RTTI PointQueue vtable and runs the LObject base destructor. |
| `point_queue_push` | `0x00404AF0` | high | Appends one two-word point unless advancing the tail would collide with the head; one of 400 slots is reserved to distinguish full from empty. |
| `point_queue_pop_front` | `0x00404B70` | high | Copies and removes the oldest queued point, wrapping the head at the fixed capacity. |
| `point_queue_is_empty` | `0x00404BE0` | high | Returns true when the circular queue head and tail indexes are equal. |
| `point_queue_pop_back` | `0x00404C30` | high | Moves the tail backward with wraparound and returns the newest queued point. |
| `point_queue_copy_assign` | `0x00404CA0` | high | Copies capacity, head, tail, and every fixed two-word point slot from another PointQueue. |
| `point_queue_scalar_deleting_dtor` | `0x00404D00` | high | Runs the PointQueue destructor and conditionally frees the complete object. |
| `batch_session_ctor` | `0x00404D30` | high | Constructs exact RTTI BatchSession as a TimerHandler with an empty linked job queue and no active job. |
| `batch_session_dtor` | `0x00404DA0` | high | Restores the BatchSession vtable, destroys its queued-job list, releases the sentinel node, and runs the TimerHandler destructor. |
| `batch_session_cancel_all` | `0x00404E30` | high | Invokes each queued BatchJob's virtual cleanup method and erases every queue node. |
| `batch_session_start_if_idle` | `0x00404EC0` | high | Starts the next queued job only when BatchSession does not already have an active job. |
| `batch_session_timer_callback` | `0x00404EF0` | high | Handles timer ID 0 by starting the next queued BatchJob and rejects other timer IDs. |
| `batch_session_enqueue_job` | `0x00404F20` | high | Appends one BatchJob pointer to the session's linked queue. |
| `batch_session_remove_job` | `0x00404F80` | high | Finds a queued job by pointer identity, invokes its virtual cleanup method, and erases its node. |
| `batch_session_start_next_job` | `0x00405020` | high | Pops queued jobs until one enabled job begins; disabled jobs are cleaned up, and an empty queue clears the active flag. |
| `batch_job_ctor` | `0x004050E0` | high | Constructs exact RTTI BatchJob and enables it for a future BatchSession begin call. |
| `batch_job_dtor` | `0x00405100` | high | Restores the exact RTTI BatchJob vtable. |
| `batch_job_begin` | `0x00405120` | high | Rejects a disabled job; otherwise records its BatchSession and queue token, invokes the pure virtual execute method, and reports success. |
| `batch_job_complete` | `0x00405170` | high | Schedules timer ID 0 on the live owning BatchSession and invokes the job's virtual cleanup method. |
| `batch_job_is_enabled` | `0x004051C0` | high | Returns the BatchJob enabled byte at object offset 0x0C. |
| `batch_job_disable` | `0x004051E0` | high | Clears the BatchJob enabled byte so BatchSession skips it when dequeued. |
| `batch_session_scalar_deleting_dtor` | `0x00405200` | high | Runs the BatchSession destructor and conditionally frees the complete object. |
| `batch_job_scalar_deleting_dtor` | `0x00405230` | high | Runs the BatchJob destructor and conditionally frees the complete object. |
| `batch_job_list_ctor` | `0x00405260` | high | Constructs the sentinel-backed linked list used by BatchSession to own queued BatchJob pointers. |
| `batch_job_list_erase_node` | `0x004052C0` | high | Unlinks one BatchJob list node, destroys its stored value, frees the node, and returns the following iterator. |
| `batch_job_list_free_sentinel` | `0x00405360` | high | Clears the BatchJob list and frees its sentinel node. |
| `batch_job_list_clear` | `0x00405390` | high | Walks every BatchJob list node, destroys its stored value, frees it, and restores the empty sentinel links. |
| `batch_job_list_value_dtor` | `0x00405420` | high | Compiler-generated value destructor used while releasing one BatchJob pointer list node. |
| `batch_job_list_allocate_nodes` | `0x00405430` | high | Allocates and links a requested run of default BatchJob list nodes before a supplied position. |
| `batch_job_list_insert_before` | `0x004054A0` | high | Creates one node and links it immediately before the supplied BatchJob list iterator. |
| `batch_job_list_create_node` | `0x00405530` | high | Allocates one BatchJob list node and copy-constructs its stored pointer value with exception cleanup. |
| `batch_job_list_create_node_exception_cleanup` | `0x004055A2` | high | Exception landing pad that frees a newly allocated BatchJob list node when value construction fails. |
| `batch_job_list_copy_value` | `0x004055F0` | high | Compiler-generated copy helper for the pointer value stored in a BatchJob list node. |
| `std_bad_alloc_dtor` | `0x00405630` | high | Restores the std::bad_alloc vtable and runs the std::exception base destructor. |
| `std_bad_alloc_scalar_deleting_dtor` | `0x00405650` | high | Runs the std::bad_alloc destructor and conditionally frees the complete exception object. |
| `std_bad_alloc_copy_ctor` | `0x00405690` | high | Copy-constructs std::bad_alloc through its std::exception base and installs the derived vtable. |
| `black_hole_ctor` | `0x00415910` | high | Constructs exact RTTI BlackHole as an LObject with an empty dynamically grown pointer array. |
| `black_hole_dtor` | `0x00415950` | high | Frees the BlackHole pointer array and runs the LObject base destructor. |
| `black_hole_queue_object` | `0x00415990` | high | Appends one object to BlackHole and clears its Concurrency task stack before deferred destruction. |
| `black_hole_queue_pane` | `0x004159C0` | high | Detaches a Pane, queues its TimerHandler secondary-base pointer in BlackHole, and clears pending tasks. |
| `black_hole_destroy_object` | `0x00415A20` | high | Detaches and immediately destroys one queued-compatible object through its deleting destructor. |
| `black_hole_destroy_queued_objects` | `0x00415A70` | high | Runs the deleting destructor for every nonnull BlackHole entry and resets the queued count. |
| `black_hole_append` | `0x00415B00` | high | Reserves capacity, appends one pointer, and increments the BlackHole queue count. |
| `black_hole_reserve` | `0x00415B40` | high | Grows the BlackHole pointer array in 1024-entry chunks while preserving existing entries. |
| `black_hole_scalar_deleting_dtor` | `0x00415C40` | high | Runs the BlackHole destructor and conditionally frees the complete object. |
| `com_auto_init_ctor` | `0x00415C70` | high | Constructs the compiler-generated AutoInit helper and calls OleInitialize for the current thread. |
| `com_auto_init_dtor` | `0x00415C90` | high | Runs OleUninitialize from the compiler-generated AutoInit destructor. |
| `com_advise_connection_point` | `0x0041A7A0` | high | Queries IConnectionPointContainer, finds the requested connection point, and advises the supplied event sink. |
| `com_unadvise_connection_point` | `0x0041A860` | high | Queries IConnectionPointContainer, finds the requested connection point, and removes the supplied advisory cookie. |
| `text_thread_acp_to_bstr` | `0x0041AA00` | high | Converts explicit-length or terminated CP_THREAD_ACP bytes into a newly allocated BSTR. |
| `com_variant_clear` | `0x0041AB40` | high | Clears a VARIANT with VariantClear and returns the HRESULT. |
| `com_variant_set_bstr` | `0x0041AB60` | high | Clears a VARIANT, assigns VT_BSTR, allocates the supplied wide string, and raises the client COM error on failure. |
| `com_assign_iweb_browser2` | `0x0041AC10` | high | Queries a supplied COM object for IID_IWebBrowser2, replaces the retained interface pointer, and releases the previous value. |
| `text_remove_ascii_spaces_dbcs_safe` | `0x004274B0` | high | Removes ASCII spaces while preserving DBCS trail bytes. |
| `time_get_utc_date_yyyymmdd` | `0x00427BD0` | high | Returns the current UTC date as year*10000 + month*100 + day. |
| `std_string_vector_insert_copy` | `0x0042A0C0` | high | Appends a string copy and rotates it into the requested insertion position. |
| `std_string_vector_push_back` | `0x0042A260` | high | Grows a string vector when full and copy-constructs one element at its end. |
| `std_string_vector_rotate_inserted_range` | `0x0042A2B0` | high | Rotates a string-vector range after insertion and returns its iterator. |
| `std_string_vector_allocator_dtor_noop` | `0x0042A3A0` | high | No-op destructor for the string vector's stateless allocator. |
| `std_string_vector_grow_by` | `0x0042A3B0` | high | Checks vector length and reserves geometrically grown capacity. |
| `std_string_vector_reserve` | `0x0042A450` | high | Moves strings into larger storage and releases the old buffer. |
| `std_string_vector_destroy_element` | `0x0042A620` | high | Destroys one std::string element during vector cleanup. |
| `std_string_vector_calculate_growth` | `0x0042A690` | high | Returns the larger of requested capacity and 1.5 times old capacity. |
| `std_string_vector_construct_element_copy` | `0x0042A710` | high | Uses the vector allocator to copy-construct one string element. |
| `std_string_vector_allocate_storage` | `0x0042A730` | high | Allocates 0x1C-byte string vector slots and throws on failure. |
| `std_string_placement_copy_ctor` | `0x0042A820` | high | Default-constructs then copy-assigns a string in caller storage. |
| `std_string_vector_rotate_range` | `0x0042A8C0` | high | Rotates a vector range using cycle decomposition and string swaps. |
| `std_string_vector_uninitialized_copy` | `0x0042AA00` | high | Copy-constructs a range of strings into uninitialized vector storage. |
| `std_string_vector_construct_element_move` | `0x0042AAD0` | high | Default-constructs a vector element and move-assigns its source string. |
| `std_string_swap` | `0x0042AB60` | high | Swaps two MSVC std::string small-buffer or heap representations. |
| `std_string_default_ctor` | `0x0042AD40` | high | Constructs an empty MSVC std::string. |
| `std_string_cstr_ctor` | `0x0042ADA0` | high | Constructs an MSVC std::string from a null-terminated byte string. |
| `std_string_dtor` | `0x0042AE30` | high | Destroys an MSVC std::string and releases heap storage when present. |
| `std_string_compare` | `0x0042AE90` | high | Compares two complete MSVC std::string values lexicographically. |
| `std_string_move_assign` | `0x0042AEE0` | high | Move-assigns an MSVC std::string and transfers heap storage when possible. |
| `std_string_compare_ranges` | `0x0042AFA0` | high | Compares selected byte ranges from a string and another buffer. |
| `std_string_reset` | `0x0042B060` | high | Releases heap storage, restores the small buffer, and terminates the string. |
| `std_string_assign_bytes` | `0x0042B110` | high | Assigns a byte buffer while handling overlap and capacity growth. |
| `std_string_assign_substring` | `0x0042B230` | high | Assigns a bounded substring, including the self-assignment case. |
| `std_string_ensure_capacity` | `0x0042B340` | high | Checks length, shrinks to the small buffer, or grows heap capacity. |
| `std_string_erase` | `0x0042B440` | high | Erases a bounded byte range and restores the null terminator. |
| `std_string_reallocate` | `0x0042B530` | high | Chooses grown capacity, preserves a prefix, and releases old storage. |
| `std_string_allocate_buffer` | `0x0042B7C0` | high | Allocates a string byte buffer and throws std::bad_alloc on failure. |
| `std_string_vector_dtor` | `0x0042B830` | high | Destroys string elements, releases vector storage, and clears its pointers. |
| `integrity_crc16_buffer` | `0x0042EEB0` | high | Calculates the table-driven 16-bit integrity checksum over a byte range, starting from zero. |
| `integrity_crc16_update` | `0x0042EF10` | high | Updates the table-driven 16-bit integrity checksum with one byte. |
| `memory_is_executable_address` | `0x0042EF40` | high | Uses VirtualQueryEx on the current process and accepts only committed executable page protections. |
| `integrity_find_executable_page_range` | `0x0042EFB0` | high | Walks pages from the integrity routine's code address and returns the first and last contiguous executable page plus the 0x1000 page size. |
| `integrity_write_executable_page_checksums` | `0x0042F0A0` | high | Writes repeated executable-page address and CRC16 pairs for the contiguous page span to the supplied stream. |
| `integrity_verify_checksum_stream` | `0x0042F140` | high | Reads at most 0x20000 bytes from a stream and validates its address and CRC16 records against live executable pages. |
| `integrity_verify_executable_page_checksums` | `0x0042F1B0` | high | Validates six-byte address and CRC16 records against committed executable pages; malformed trailing bytes are ignored. |
| `command_dispatcher_ctor` | `0x0042F250` | high | Constructs CommandDispatcher, initializes its argument stack and string arena, and creates a default CommandExecutor when none is supplied. |
| `command_dispatcher_dtor` | `0x0042F350` | high | Destroys CommandDispatcher, its string arena, its owned default executor, and its argument storage. |
| `command_dispatcher_execute_named_command` | `0x0042F440` | high | Matches a command name against the supported command table, invokes its argument handler, and clears temporary arguments afterward. |
| `command_dispatcher_handle_set_tile` | `0x0042F800` | high | Pops set_tile arguments, retains defaults for missing values, and forwards them to the configured command target. |
| `command_dispatcher_handle_set_color` | `0x0042F8F0` | high | Pops set_color arguments, retains defaults for missing values, and forwards them to the configured command target. |
| `command_dispatcher_handle_effect` | `0x0042F9E0` | high | Pops effect arguments with type checks and forwards them to the configured command target. |
| `command_dispatcher_handle_motion` | `0x0042FAC0` | high | Pops motion arguments with type checks and forwards them to the configured command target. |
| `command_dispatcher_handle_move` | `0x0042FBA0` | high | Pops move arguments with type checks and forwards them to the configured command target. |
| `command_dispatcher_handle_put_item` | `0x0042FC40` | high | Pops four integer put_item arguments and forwards them to the configured command target. |
| `command_dispatcher_handle_put_monster` | `0x0042FD50` | high | Pops five integer put_monster arguments and forwards them to the configured command target. |
| `command_dispatcher_handle_put_human` | `0x0042FEA0` | high | Pops put_human arguments with type checks and forwards them to the configured command target. |
| `command_dispatcher_handle_human_to_monster` | `0x0042FFC0` | high | Pops human_to_monster arguments with type checks and forwards them to the configured command target. |
| `command_dispatcher_handle_sound` | `0x004300A0` | high | Pops one integer sound ID, forwards it to the command target, and plays the matching sound effect when audio is available. |
| `command_dispatcher_handle_auto_use_skill_noop` | `0x00430100` | high | Accepts the auto_use_skill command without consuming arguments or changing state. |
| `command_dispatcher_handle_aus_noop` | `0x00430110` | high | Accepts the aus alias without consuming arguments or changing state. |
| `command_dispatcher_handle_set_attr_tracker_noop` | `0x00430120` | high | Accepts the set_attr_tracker command without consuming arguments or changing state. |
| `command_dispatcher_handle_sat_noop` | `0x00430130` | high | Accepts the sat alias without consuming arguments or changing state. |
| `command_dispatcher_handle_auto_move_noop` | `0x00430140` | high | Accepts the auto_move command without consuming arguments or changing state. |
| `command_dispatcher_handle_set_merchant_auto_answer_noop` | `0x00430150` | high | Accepts the merchant auto-answer command without consuming arguments or changing state. |
| `command_dispatcher_handle_set_timer_noop` | `0x00430160` | high | Accepts the set_timer command without consuming arguments or changing state. |
| `command_dispatcher_handle_wait_event_noop` | `0x00430170` | high | Accepts the wait_event command without consuming arguments or changing state. |
| `command_dispatcher_handle_message` | `0x00430180` | high | Pops one string, appends it to the game message overlay in white, and adds a newline. |
| `command_dispatcher_handle_auto_use_spell` | `0x004301F0` | high | Pops one integer and forwards it to the CommandExecutor timed auto-use-spell path. |
| `command_dispatcher_handle_set_ground_tile` | `0x00430250` | high | Pops three integer set_gnd_tile arguments and forwards them to the configured command target. |
| `command_dispatcher_handle_set_static_tile` | `0x00430320` | high | Pops four integer set_stc_tile arguments and forwards them to the configured command target. |
| `command_dispatcher_handle_play_minigame` | `0x00430430` | high | Pops one integer minigame selector and launches the minigame through the active root pane. |
| `command_dispatcher_handle_send_fieldmap` | `0x00430490` | high | Pops three integer map fields and sends the corresponding 0x3F client packet. |
| `command_dispatcher_handle_show` | `0x00430560` | high | Pops a string and integer selector and forwards them to the configured command target. |
| `command_dispatcher_push_integer` | `0x00430600` | high | Pushes a tagged integer onto the fixed 1024-entry command argument stack. |
| `command_dispatcher_push_string` | `0x00430630` | high | Copies a string into the dispatcher arena and pushes a tagged string argument. |
| `command_dispatcher_copy_string_to_arena` | `0x00430680` | high | Grows the command string arena when needed and copies one terminated string into it. |
| `command_dispatcher_push_argument` | `0x004307A0` | high | Pushes one already-tagged command argument when the 1024-entry stack has capacity. |
| `command_argument_copy` | `0x004307F0` | high | Copies a tagged command argument value. |
| `command_dispatcher_pop_argument` | `0x00430830` | high | Pops the newest command argument or reports an empty argument stack. |
| `command_dispatcher_clear_arguments` | `0x00430880` | high | Clears the argument stack and rewinds the temporary string arena. |
| `command_executor_ctor` | `0x004308B0` | high | Constructs CommandExecutor and registers its 500 ms and 2000 ms timers. |
| `command_executor_dtor` | `0x00430940` | high | Unregisters CommandExecutor timers and destroys its TimerHandler base. |
| `command_executor_timer1_tick_noop` | `0x004309C0` | high | Receives the repeating 500 ms executor timer without changing command state. |
| `command_executor_timer_callback` | `0x004309D0` | high | Routes executor timers, requeues timers 1 and 4, accepts timer 2, and rejects timer 3. |
| `command_executor_message` | `0x00430A50` | high | Displays a local command message through the active UI message path. |
| `command_executor_schedule_auto_use_spell` | `0x00430B40` | high | Schedules or clears timer 3 using the selector multiplied by 1000 ms. |
| `command_executor_set_tile_noop` | `0x00430C20` | high | Default CommandExecutor set_tile target; intentionally does nothing. |
| `command_executor_set_color_noop` | `0x00430C30` | high | Default CommandExecutor set_color target; intentionally does nothing. |
| `command_executor_effect_noop` | `0x00430C40` | high | Default CommandExecutor effect target; intentionally does nothing. |
| `command_executor_motion_noop` | `0x00430C50` | high | Default CommandExecutor motion target; intentionally does nothing. |
| `command_executor_move_noop` | `0x00430C60` | high | Default CommandExecutor move target; intentionally does nothing. |
| `command_executor_put_item_noop` | `0x00430C70` | high | Default CommandExecutor put_item target; intentionally does nothing. |
| `command_executor_put_monster_noop` | `0x00430C80` | high | Default CommandExecutor put_monster target; intentionally does nothing. |
| `command_executor_put_human_noop` | `0x00430C90` | high | Default CommandExecutor put_human target; intentionally does nothing. |
| `command_executor_human_to_monster_noop` | `0x00430CA0` | high | Default CommandExecutor human_to_monster target; intentionally does nothing. |
| `command_executor_play_sound` | `0x00430CB0` | high | Plays a local sound through the active sound manager. |
| `command_executor_set_ground_tile_noop` | `0x00430CE0` | high | Default CommandExecutor set_gnd_tile target; intentionally does nothing. |
| `command_executor_set_static_tile_noop` | `0x00430CF0` | high | Default CommandExecutor set_stc_tile target; intentionally does nothing. |
| `command_executor_play_minigame` | `0x00430D00` | high | Launches the selected minigame through the active root pane. |
| `command_executor_send_fieldmap` | `0x00430D30` | high | Builds and sends the field-map client command from three integer fields. |
| `command_executor_show_noop` | `0x00430E20` | high | Default CommandExecutor show target; intentionally does nothing. |
| `command_parse_and_execute_line` | `0x004311E0` | high | Tokenizes one bounded command line, pushes arguments in reverse order, dispatches by name, and clears temporaries. |
| `command_is_bare_token_character` | `0x00431540` | high | Accepts ASCII letters, digits, and underscore in an unquoted command token. |
| `command_dispatcher_scalar_deleting_dtor` | `0x004315A0` | high | Compiler scalar-deleting destructor for CommandDispatcher. |
| `command_executor_scalar_deleting_dtor` | `0x004315D0` | high | Compiler scalar-deleting destructor for CommandExecutor. |
| `command_dispatcher_singleton_register` | `0x00431630` | high | Registers the CommandDispatcher singleton. |
| `command_dispatcher_singleton_unregister` | `0x00431670` | high | Clears the CommandDispatcher singleton when the supplied instance owns it. |
| `command_get_dispatcher` | `0x004316B0` | high | Returns the current CommandDispatcher singleton. |
| `text_format_wide_buffer` | `0x00431FB0` | high | Formats a bounded wide-character string into the caller buffer using the client's shared varargs helper. |
| `text_copy_nth_space_token_wide` | `0x00436A50` | high | Copies one zero-based, space-delimited token from wide text into a bounded caller buffer. |
| `com_get_bstr_result` | `0x00436F80` | high | Retrieves a BSTR result from a legacy endpoint COM service and wraps it in client storage. |
| `com_bstr_ref_create_from_ansi` | `0x004370A0` | high | Converts ANSI text into an owned BSTR reference wrapper. |
| `com_bstr_ref_release_and_clear` | `0x00437150` | high | Releases an owned BSTR reference and clears the wrapper. |
| `com_bstr_ref_get_ansi` | `0x00437180` | high | Converts the wrapped BSTR to the client's cached ANSI representation. |
| `com_bstr_storage_ctor` | `0x004371E0` | high | Constructs the client's reference-counted BSTR storage object. |
| `com_bstr_storage_release` | `0x00437250` | high | Releases one reference to the BSTR storage object. |
| `com_bstr_storage_destroy` | `0x004372A0` | high | Destroys BSTR storage and frees the underlying COM string. |
| `com_invoke_bstr_input_method` | `0x00437300` | high | Invokes a legacy COM method with one BSTR input argument. |
| `com_invoke_bstr_output_method` | `0x004373A0` | high | Invokes a legacy COM method that returns a BSTR. |
| `com_invoke_int_output_method` | `0x00437490` | high | Invokes a legacy COM method that returns an integer. |
| `com_release_interface` | `0x00437510` | high | Calls Release on a non-null COM interface pointer and clears the caller slot. |
| `com_create_thrunet_service_by_progid` | `0x00437540` | high | Creates the legacy Thrunet endpoint service from its registered ProgID. |
| `com_create_excitegame_service` | `0x00437790` | high | Creates and initializes the legacy ExciteGame endpoint COM service. |
| `com_create_thrunet_service` | `0x00437860` | high | Creates and initializes the legacy Thrunet endpoint COM service. |
| `exception_context_dumper_dtor` | `0x00437D20` | high | Destroys the StackWalker owned by exact RTTI ContextDumper. |
| `exception_context_dumper_scalar_deleting_dtor` | `0x00437E30` | high | Compiler scalar-deleting destructor for exact RTTI ContextDumper. |
| `metadata_denied_lookup_dtor` | `0x0043FDC0` | high | Destroys one DeniedItemList category lookup by clearing all rule records and its outer container. |
| `metadata_denied_lookup_contains` | `0x0043FE20` | high | Wraps the supplied text as a client string and queries one category lookup by rule key and numeric value. |
| `metadata_denied_lookup_add_rule` | `0x0043FEE0` | high | Builds a denial-rule record from numeric and word token text and inserts it under the parsed rule key. |
| `metadata_denied_rule_parse_numeric_tokens` | `0x0043FFB0` | high | Extracts consecutive decimal sequences from text and inserts each parsed number into the rule's numeric container. |
| `metadata_denied_rule_parse_word_tokens` | `0x00440100` | high | Splits space-delimited text, strips a trailing carriage return, and inserts each word into the rule's string container. |
| `metadata_denied_rule_record_list_dtor` | `0x00440300` | high | Destroys every owned denial-rule record in a list and then destroys the list storage. |
| `metadata_denied_lookup_clear` | `0x004403C0` | high | Destroys every rule-record list in a category lookup. |
| `metadata_denied_lookup_insert_record` | `0x00440440` | high | Finds or creates a rule-key bucket, inserts the supplied rule record, and reports whether the key remains present. |
| `metadata_denied_rule_record_list_contains` | `0x004405F0` | high | Scans a rule-record list and reports whether any record's numeric container contains the requested value. |
| `metadata_denied_lookup_contains_record` | `0x00440700` | high | Finds the requested rule-key bucket and queries its rule records for the supplied numeric value. |
| `metadata_denied_item_list_ctor` | `0x004407C0` | high | Constructs exact RTTI class DeniedItemList, creates three empty lookup containers, and starts metadata subscription. |
| `metadata_denied_item_list_dtor` | `0x00440900` | high | Destroys the Item, Skill, and Spell denial lookups and the DeniedItemList TimerHandler base. |
| `metadata_denied_item_list_contains` | `0x00440A30` | high | Selects Item, Skill, or Spell lookup index 0..2 and queries it with the supplied rule fields. |
| `metadata_denied_item_list_subscribe` | `0x00440AA0` | high | Registers BItems, BSkills, and BSpells with MetaTableManager and retries after 1000 ms when the manager is unavailable. |
| `metadata_denied_item_list_apply_table` | `0x00440B20` | high | Replaces the current denial lists and routes metadata rows tagged Item, Skill, or Spell into their lookup containers. |
| `metadata_denied_item_list_handle_event` | `0x00440E70` | high | Applies an available denial metadata table or retries the table subscriptions. |
| `metadata_denied_rule_record_dtor` | `0x00440F20` | high | Destroys both containers owned by one parsed denial-rule record. |
| `metadata_denied_item_list_scalar_deleting_dtor` | `0x00440FF0` | high | Compiler scalar-deleting destructor for exact RTTI DeniedItemList. |
| `metadata_denied_numeric_set_ctor` | `0x00441020` | high | Constructs the numeric-token red-black set and initializes its header sentinel. |
| `metadata_denied_numeric_set_dtor` | `0x00441050` | high | Erases the numeric-token set, then frees its header sentinel. |
| `metadata_denied_numeric_set_find` | `0x004410F0` | high | Finds an exact signed numeric token by lower-bound search and equality check. |
| `metadata_denied_word_set_ctor` | `0x00441190` | high | Constructs the word-token red-black set and initializes its header sentinel. |
| `metadata_denied_word_set_dtor` | `0x004411C0` | high | Erases the word-token set, then frees its header sentinel. |
| `metadata_denied_word_set_find` | `0x00441260` | high | Finds an exact word token using the client string-range comparator. |
| `metadata_denied_rule_map_ctor` | `0x00441340` | high | Constructs the denied-rule key map and initializes its header sentinel. |
| `metadata_denied_rule_map_dtor` | `0x00441370` | high | Erases the denied-rule key map, then frees its header sentinel. |
| `metadata_denied_rule_map_find` | `0x00441410` | high | Finds an exact signed rule key by lower-bound search and equality check. |
| `metadata_denied_rule_record_list_storage_dtor` | `0x004414B0` | high | Destroys the owned doubly-linked rule-record list nodes and header storage. |
| `metadata_denied_numeric_set_erase_range` | `0x00441600` | high | Erases a numeric-set iterator range, using a whole-tree fast path when the complete range is selected. |
| `metadata_denied_numeric_set_lower_bound` | `0x004416E0` | high | Returns the first numeric-token set node whose signed key is not less than the requested value. |
| `metadata_denied_numeric_set_initialize` | `0x00441750` | high | Allocates and initializes the numeric-set red-black tree header sentinel. |
| `metadata_denied_word_set_erase_range` | `0x004417D0` | high | Erases a word-set iterator range, using a whole-tree fast path when the complete range is selected. |
| `metadata_denied_word_set_lower_bound` | `0x004418B0` | high | Returns the first word-token set node not ordered before the requested string. |
| `metadata_denied_word_set_initialize` | `0x00441950` | high | Allocates and initializes the word-set red-black tree header sentinel. |
| `metadata_denied_rule_map_erase_range` | `0x004419D0` | high | Erases a denied-rule map iterator range, using a whole-tree fast path for the complete map. |
| `metadata_denied_rule_map_lower_bound` | `0x00441AB0` | high | Returns the first denied-rule map node whose signed key is not less than the requested key. |
| `metadata_denied_rule_map_initialize` | `0x00441B20` | high | Allocates and initializes the denied-rule map red-black tree header sentinel. |
| `metadata_denied_rule_record_list_ctor` | `0x00441BA0` | high | Constructs the denied-rule record list and initializes its sentinel node. |
| `metadata_denied_numeric_set_iterator_ctor` | `0x00441C00` | high | Initializes a numeric-token set iterator wrapper from a tree node pointer. |
| `metadata_denied_word_set_iterator_ctor` | `0x00441C20` | high | Initializes a word-token set iterator wrapper from a tree node pointer. |
| `metadata_denied_rule_map_iterator_ctor` | `0x00441C40` | high | Initializes a denied-rule map iterator wrapper from a tree node pointer. |
| `metadata_denied_rule_map_iterator_next` | `0x00441C60` | high | Advances a denied-rule map iterator to its in-order successor. |
| `metadata_denied_numeric_set_erase` | `0x00441D10` | high | Erases one numeric-token set node and restores red-black tree invariants; rejects an invalid iterator. |
| `metadata_denied_numeric_set_clear` | `0x004421F0` | high | Destroys every numeric-token tree node, resets the header links, and sets the element count to zero. |
| `metadata_denied_word_set_erase` | `0x00442250` | high | Erases one word-token set node and restores red-black tree invariants; rejects an invalid iterator. |
| `metadata_denied_word_set_clear` | `0x00442730` | high | Destroys every word-token tree node, resets the header links, and sets the element count to zero. |
| `metadata_denied_rule_map_erase` | `0x00442790` | high | Erases one denied-rule map node and restores red-black tree invariants; rejects an invalid iterator. |
| `metadata_denied_rule_map_clear` | `0x00442C70` | high | Destroys every denied-rule map node, resets the header links, and sets the element count to zero. |
| `metadata_denied_numeric_set_destroy_subtree` | `0x00442CD0` | high | Recursively destroys a numeric-token set subtree and frees each 0x14-byte tree node. |
| `metadata_denied_numeric_set_rotate_left` | `0x00442D40` | high | Performs a left rotation around one numeric-token red-black tree node. |
| `metadata_denied_numeric_set_rotate_right` | `0x00442DF0` | high | Performs a right rotation around one numeric-token red-black tree node. |
| `metadata_denied_word_set_destroy_subtree` | `0x00442EA0` | high | Recursively destroys a word-token set subtree, destroys each stored string, and frees each tree node. |
| `metadata_denied_word_set_rotate_left` | `0x00442F10` | high | Performs a left rotation around one word-token red-black tree node. |
| `metadata_denied_word_set_rotate_right` | `0x00442FC0` | high | Performs a right rotation around one word-token red-black tree node. |
| `metadata_denied_rule_map_destroy_subtree` | `0x00443070` | high | Recursively destroys a denied-rule map subtree, destroys each mapped value, and frees each tree node. |
| `metadata_denied_rule_map_rotate_left` | `0x004430E0` | high | Performs a left rotation around one denied-rule red-black tree node. |
| `metadata_denied_rule_map_rotate_right` | `0x00443190` | high | Performs a right rotation around one denied-rule red-black tree node. |
| `metadata_denied_numeric_set_iterator_next` | `0x00443240` | high | Advances a numeric-token set iterator to its in-order successor. |
| `metadata_denied_word_set_iterator_next` | `0x004432F0` | high | Advances a word-token set iterator to its in-order successor. |
| `metadata_denied_numeric_set_allocate_nodes` | `0x00443470` | high | Allocates one or more 0x14-byte numeric-token tree nodes and throws std::bad_alloc on overflow or failure. |
| `metadata_denied_word_set_allocate_nodes` | `0x004434E0` | high | Allocates one or more 0x2c-byte word-token tree nodes and throws std::bad_alloc on overflow or failure. |
| `metadata_denied_rule_map_value_destroy` | `0x00443550` | high | Template destruction wrapper used when a denied-rule map value must be discarded; delegates to the value destructor. |
| `metadata_denied_rule_map_allocate_nodes` | `0x00443570` | high | Allocates one or more 0x20-byte denied-rule map nodes and throws std::bad_alloc on overflow or failure. |
| `metadata_denied_rule_record_list_allocate_nodes` | `0x004435E0` | high | Allocates one or more 0x0c-byte denied-rule record list nodes and throws std::bad_alloc on overflow or failure. |
| `metadata_denied_numeric_set_insert_unique` | `0x00443650` | high | Searches for a numeric token and inserts it only when an equivalent signed value is absent. |
| `metadata_denied_word_set_insert_unique` | `0x004438A0` | high | Searches for a word token and inserts it only when an equivalent string is absent. |
| `metadata_denied_rule_map_insert_unique` | `0x00443B00` | high | Searches for a denied-rule key and inserts the key/value record only when the key is absent. |
| `metadata_denied_numeric_set_insert_node` | `0x00443D50` | high | Allocates, links, and rebalances a numeric-token set node at the selected insertion position. |
| `metadata_denied_word_set_insert_node` | `0x00444030` | high | Links a prepared word-token node at the selected position and restores red-black tree invariants. |
| `metadata_denied_rule_map_insert_node` | `0x00444310` | high | Links a prepared denied-rule map node at the selected position and restores red-black tree invariants. |
| `metadata_denied_numeric_set_iterator_prev` | `0x004445F0` | high | Moves a numeric-token set iterator to its in-order predecessor. |
| `metadata_denied_word_set_iterator_prev` | `0x004446B0` | high | Moves a word-token set iterator to its in-order predecessor. |
| `metadata_denied_rule_map_iterator_prev` | `0x00444770` | high | Moves a denied-rule map iterator to its in-order predecessor. |
| `metadata_denied_numeric_set_create_node` | `0x00444830` | high | Allocates a numeric-token tree node and copy-constructs its stored integer value. |
| `metadata_denied_word_set_create_node` | `0x004448D0` | high | Allocates a word-token tree node and copy-constructs its stored string value. |
| `metadata_denied_rule_map_create_node` | `0x00444970` | high | Allocates a denied-rule map node and copy-constructs its key and record list value. |
| `metadata_denied_rule_map_value_dtor` | `0x00444A10` | high | Destroys the record list stored in one denied-rule map value and releases its list header. |
| `metadata_denied_numeric_set_allocate_node` | `0x00444A90` | high | Allocates one numeric-token tree node and initializes its links and red-black tree flags. |
| `metadata_denied_word_set_allocate_node` | `0x00444AE0` | high | Allocates one word-token tree node and initializes its links and red-black tree flags. |
| `metadata_denied_rule_map_allocate_node` | `0x00444B30` | high | Allocates one denied-rule map node and initializes its links and red-black tree flags. |
| `metadata_denied_numeric_value_copy` | `0x00444BA0` | high | Copy-constructs the signed integer stored in a numeric-token tree node. |
| `metadata_denied_rule_map_value_copy` | `0x00444BE0` | high | Copy-constructs a denied-rule map key together with its owned rule-record list. |
| `metadata_denied_rule_record_list_insert_before` | `0x00444C60` | high | Creates and links one rule-record pointer node before the selected list position. |
| `metadata_denied_rule_record_list_create_node` | `0x00444CF0` | high | Allocates one rule-record list node, sets its neighboring links, and copy-constructs the stored record pointer. |
| `metadata_denied_rule_record_pointer_copy` | `0x00444DB0` | high | Copy-constructs the rule-record pointer stored in a list node. |
| `metadata_denied_rule_record_list_copy_ctor` | `0x00444DF0` | high | Constructs a rule-record list and appends a copy of each source pointer node. |
| `metadata_denied_rule_record_list_copy_range` | `0x00444F30` | high | Copies a source iterator range into a denied-rule record list before the selected position. |
| `metadata_denied_rule_record_list_insert_copy_before` | `0x00445030` | high | Creates and links a copied rule-record pointer node before the selected position during list copy construction. |
| `metadata_denied_rule_record_list_erase` | `0x004450C0` | high | Unlinks and frees one rule-record pointer list node, decrements the count, and returns the following iterator. |
| `metadata_denied_rule_record_list_create_copy_node` | `0x00445160` | high | Allocates a rule-record pointer list node, sets its neighboring links, and copy-constructs the stored pointer. |
| `metadata_denied_rule_record_pointer_copy_ctor` | `0x00445220` | high | Copy-constructs the rule-record pointer stored in a copied list node. |
| `text_count_trailing_and_total_spaces` | `0x0044CA70` | high | Counts trailing spaces and total spaces in a fixed-length span for Canvas text layout. |
| `text_rotate_leading_spaces_to_end` | `0x0044CB10` | high | Moves leading spaces to the end of a fixed-length text span while preserving its length. |
| `lobject_dtor_wrapper` | `0x0044D840` | high | Thin wrapper that invokes the recovered LObject destructor. |
| `rect_intersect_or_empty` | `0x00454A70` | high | Computes a nonempty rectangle intersection or writes the shared empty rectangle and returns false. |
| `text_truncate_with_ellipsis_dbcs` | `0x00455740` | high | Truncates a mutable byte string to a six-pixel-cell width, preserves DBCS pairs, and appends three dots. |
| `text_find_last_nonspace_index` | `0x00455880` | high | Returns the last byte index that is not a space, tab, or carriage return. |
| `light_list_ctor` | `0x004AE8D0` | high | Constructs the RTTI LightList singleton and starts loading its cached Light metadata. |
| `light_list_load_metadata` | `0x004AEA80` | high | Requests the Light metadata table when available or schedules a one-second retry. |
| `light_list_find_map_time_entry` | `0x004AEAD0` | high | Finds an inclusive map and time-range entry and returns ambient RGB, intensity, and whether HEA use is permitted. |
| `lobject_ctor` | `0x004B4480` | high | Installs the LObject vtable and writes live-cookie bytes 62 6F 73 79 ("bosy") at +0x04. |
| `lobject_dtor` | `0x004B44B0` | high | Restores the LObject vtable and clears the live cookie at +0x04 to zero. |
| `lobject_is_live` | `0x004B4550` | high | Returns true only when LObject +0x04 equals 0x79736F62; event_dispatch_immediate uses it before dispatch. |
| `metadata_parse_event_record` | `0x0055D6E0` | high | Parses one sequential start-to-end SEvent record and its title, id, qual, sum, result, sub, and reward groups. |
| `metadata_event_requirements_met` | `0x0055E370` | high | Checks an event progression mask, class mask, and every prerequisite legend key against local user state. |
| `metadata_parse_spell_skill_constraint` | `0x0055F890` | high | Parses the first six values of one SClass ability record into display and requirement fields. |
| `metadata_spell_skill_requirements_met` | `0x005600B0` | high | Checks character level, ability and master flags, ability level, attributes, and two named learned-ability prerequisites. |
| `crc16_buffer` | `0x00568870` | high | Applies the custom CRC16 update to a byte buffer starting from zero. |
| `startup_run_pending_patcher` | `0x0057A330` | high | Before normal startup, requires both Patch/Info and Patch/Script to relaunch Patcher2.exe; otherwise deletes both markers and continues. |
| `user_info_load_family_list` | `0x00592560` | high | Clears twenty 40-byte UserInfo family slots, then loads up to twenty lines from the per-character Familylist.cfg file. |
| `user_info_save_family_list` | `0x00592730` | high | Writes all twenty 40-byte UserInfo family slots as lines in the per-character Familylist.cfg file. |
| `user_info_load_friend_list` | `0x00592800` | high | Clears twenty 40-byte UserInfo friend slots, then loads up to twenty lines from the per-character Friendlist.cfg file. |
| `user_info_save_friend_list` | `0x00592920` | high | Writes all twenty 40-byte UserInfo friend slots as lines in the per-character Friendlist.cfg file. |
| `crc16_update` | `0x005B8F30` | high | Updates the custom CRC16 with table[crc high byte] XOR crc shifted left XOR input byte. |
| `world_direction_to_delta` | `0x005BE580` | high | Maps directions 0 through 3 to up, right, down, and left coordinate deltas; values above 3 have no defined result. |
| `world_step_coordinates` | `0x005BE600` | high | Applies the direction delta to a coordinate pair used by local movement and collision checks. |
| `world_object_list_create` | `0x005C7700` | high | Allocates the 0x68-byte WorldObjectList, constructs width times height 0x60-byte cells, and installs it at WorldPane +0x194. |
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
| `world_show_damage_effect` | `0x005CCD40` | high | Resolves the target object, removes its existing type-7 overlay, constructs exact RTTI WorldObject_Damage, and starts the replacement at the requested stage for 2000 ms. |
| `ground_attribute_table_get` | `0x005CFA70` | high | Returns the interned gndattr.tbl entry for one ground tile ID, extending the indexed table in 1024-entry blocks when needed. |
| `world_object_ctor` | `0x005DB3F0` | high | Constructs the 0x7C-byte common WorldObject prefix, including identity, render offsets, tile coordinates, attached panes, object lighting, and ground-paint state. |
| `world_object_set_ground_paint` | `0x005DB6D0` | high | Replaces the WorldObject ground-paint record and publishes a change only when its flag, color, alpha, or depth fields differ. |
| `world_object_set_name_pane` | `0x005DBA80` | high | Replaces the reference-counted WorldObject_Name_Pane pointer at common WorldObject offset +0x58. |
| `world_object_query_ground_attributes` | `0x005DBE80` | high | Broadcasts object query selector 5 so WorldControllerPane can return the gndattr.tbl entry for the object's current ground tile. |
| `world_damage_object_ctor` | `0x005DC1A0` | high | Constructs exact RTTI WorldObject_Damage and initializes its timer generation, stage, and image state. |
| `world_damage_object_start` | `0x005DC350` | high | Selects a meter stage, stores current time plus duration minus 100 ms, and schedules timer ID 1 for the full supplied duration. |
| `world_damage_object_get_bounds` | `0x005DC4B0` | high | Returns the target-relative bounds of the selected five-by-27 damage-meter frame. |
| `world_damage_object_handle_timer` | `0x005DC6A0` | high | Handles timer ID 1 and removes the overlay through the normal world-object path only when the callback generation still matches. |
| `world_effect_start_animation` | `0x005DD1C0` | high | Registers an ordinary world effect with the image pool, prefers the resource's nonzero frame interval over the packet fallback, and schedules its frame timer. |
| `world_object_effect_ctor` | `0x005DD620` | high | Constructs the exact RTTI WorldObject_ObjectEffect with an Effect.tbl resource index, fallback frame interval, and owning object's facing direction. |
| `world_static_effect_ctor` | `0x005DD6D0` | high | Constructs the exact RTTI WorldObject_StaticEffect and retains its tile Y and X coordinates. |
| `world_human_object_ctor` | `0x005DDFC0` | high | Constructs exact RTTI WorldObject_Human, installs the Human vtables, selects draw layer 7, and clears ground-tile state byte +0x1ED. |
| `world_human_start_motion` | `0x005DE110` | high | Suppresses ordinary living-object motion starts while the gndattr.tbl height-1 state is active; otherwise delegates to world_living_start_motion. |
| `world_human_set_ground_tile_state` | `0x005DE150` | high | Caches the gndattr.tbl height-1 marker at WorldObject_Human +0x1ED and selects or clears a cloned human image-session snapshot when it changes. |
| `world_human_refresh_ground_tile_state` | `0x005DE1E0` | high | Queries current ground attributes, updates the Human height-1 state, and refreshes direction, motion, and ground paint after a position change. |
| `world_item_object_ctor` | `0x005DE280` | high | Constructs the 0xB8-byte RTTI WorldObject_Item and retains entity ID, Y, X, untagged sprite, resource context, and dye color. |
| `world_item_refresh_ground_paint` | `0x005DE820` | high | Applies ordinary gndattr paint, but substitutes bytes 39 AE EF 80 and depth 100 when the tile's height-1 marker is set. |
| `world_item_handle_pointer_event` | `0x005DE8F0` | high | Arms WorldObject_Item +0xB5 on a pointer press inside its interaction rectangle, then consumes and clears that state on release or cancel. |
| `world_living_object_ctor` | `0x005DF230` | high | Extends the 0x7C-byte WorldObject base with image sessions, a composite Canvas, name and direction state, and four 0x14-byte timed motion slots through +0x1E3. |
| `world_human_get_active_image_session` | `0x005DFD80` | high | Returns the cloned ground-tile image session at Human +0x94 when present, otherwise the normal image session at +0x90. |
| `world_human_set_ground_image_session` | `0x005DFE40` | high | Replaces the reference-counted ground-tile image session at WorldObject_Human +0x94. |
| `world_human_clear_ground_image_session` | `0x005DFED0` | high | Clears and releases the cloned ground-tile image session at WorldObject_Human +0x94. |
| `world_living_object_refresh_motion` | `0x005E0550` | medium | Clears one live motion flag, invokes the object's motion refresh virtual, and reapplies its current facing; SMove direction 4 uses this when positions already agree. |
| `world_living_start_move` | `0x005E0590` | high | Updates a living object's direction and destination, starts its image-session movement sequence, and publishes the movement event. |
| `world_living_start_move_animation` | `0x005E0610` | high | Starts the current image session's movement sequence and passes the local ScrollLevel boolean to its class-specific selector. |
| `world_living_start_motion` | `0x005E0750` | high | Stores the facing direction, asks the current image session to select a body motion, and schedules its timer using the selector's final duration in milliseconds. |
| `world_living_object_set_direction` | `0x005E0880` | high | When facing changes, invokes the living-object transition hook, stores direction at +0x192, and refreshes the directional motion or image state. |
| `world_living_update_motion_slot` | `0x005E10B0` | high | Creates or updates one of four 0x14-byte motion slots and stores zero or current tick plus duration as its expiry time. |
| `world_living_adjust_render_offset_for_direction` | `0x005E16C0` | high | Applies direction-table deltas to the signed WorldObject render-displacement pair at +0x38 and +0x3C. |
| `world_living_set_render_offset` | `0x005E1770` | high | Replaces the signed render-displacement pair at WorldObject +0x38 and +0x3C independently of tile Y and X. |
| `world_living_handle_timer_event` | `0x005E1800` | high | For motion timer 0x02000001, advances the living animation only when the scheduled generation matches the current motion, so an older timer cannot interrupt a newer motion. |
| `world_living_refresh_ground_paint` | `0x005E2340` | high | Queries current gndattr color and depth fields and updates the living object's ground-paint record. |
| `world_monster_object_ctor` | `0x005E2630` | high | Constructs the 0x1F0-byte RTTI WorldObject_Monster, retains creature_type at +0x1EC, and selects a type-dependent common collision level. |
| `world_moving_effect_ctor` | `0x005E2770` | high | Constructs the exact RTTI WorldObject_MovingEffect and builds its client-timed path between source and target world positions. |
| `world_moving_effect_start` | `0x005E3710` | high | Schedules a moving effect's path timer using the step interval computed from client effect data. |
| `world_static_set_tile_id` | `0x005E4900` | high | Writes the WorldObject_Static live tile ID, reloads its static image and bounds, and invalidates the object for drawing. |
| `world_static_handle_state_transition_message` | `0x005E4A30` | high | Handles scheduled message 0x01000001 by advancing the static state transition. |
| `world_static_transition_to_pair_column_1` | `0x005E4B20` | high | Finds the live tile ID in the 66-row pair table and starts a transition toward column 1. |
| `world_static_transition_to_pair_column_0` | `0x005E4BD0` | high | Finds the live tile ID in the 66-row pair table and starts a transition toward column 0. |
| `world_static_advance_state_transition` | `0x005E4C80` | high | Moves the pair column toward its requested endpoint, applies that tile ID, and reschedules after 150 ms only if another step remains. |
| `world_user_start_move` | `0x005E4FC0` | high | Refreshes WorldObject_User appearance state, then starts the common living-object move with the supplied ScrollLevel flag. |
| `world_object_list_ctor` | `0x005E5290` | high | Constructs the 0x68-byte object list, its ordered entity-ID tree and secondary indexes, and width times height spatial cells of 0x60 bytes each. |
| `world_object_list_insert` | `0x005E5D40` | high | Inserts an object into its 0x60-byte coordinate cell and the ordered entity-ID index, then marks WorldObject +0x48 inserted. |
| `world_object_list_find_by_id` | `0x005E73B0` | high | Searches the ordered ID tree beginning at WorldObjectList +0x1C and returns the reference-counted object pointer from node +0x10. |
| `world_set_view_position` | `0x005EEC70` | high | Publishes a Y, X world-view position and optionally rebuilds the visible world and camera state around it. |
| `world_get_self_user_object` | `0x005EEDB0` | high | Looks up the saved self object ID and RTTI-casts the result to WorldObject_User. |
| `world_update_map_lighting` | `0x005EF360` | high | Scales the stored SChangeHour time step, resolves the current map's Light metadata, updates ambient color and intensity, and conditionally loads its HEA mask. |
| `world_get_static_tile_id_from_object` | `0x005EFEC0` | high | Requires WorldObject_Static and returns its current live tile ID for the movement collision path. |
| `session_world_user_func_ctor` | `0x005FC5F0` | high | Constructs exact RTTI class WorldUserFunc, embeds exact RTTI UserInfo at +0x15C8C, and clears its fixed inventory, spell, and skill arrays; the allocation site requests 0x167D0 bytes. |
| `session_find_first_empty_inventory_slot` | `0x005FC900` | high | Returns the first absent inventory record in slots 1 through 60, or 0 when every slot is occupied. |
| `session_store_inventory_entry` | `0x005FCBB0` | high | Stores one compact 0x106-byte inventory record at WorldUserFunc + 0x1092 + (slot - 1) * 0x106. |
| `session_clear_inventory_entry` | `0x005FCC10` | high | Clears an inventory record's present flag, sprite, and name[0] without overwriting its dye byte or remaining name bytes. |
| `session_store_spell_entry` | `0x005FCC50` | high | Stores one 0x206-byte spell record at WorldUserFunc + 0x4DFA + (slot - 1) * 0x206. |
| `session_clear_spell_entry` | `0x005FCCD0` | high | Clears a spell record's present flag, argument type, name[0], and prompt[0] without overwriting the icon or remaining string bytes. |
| `session_store_skill_entry` | `0x005FCD20` | high | Stores one 0x104-byte skill record at WorldUserFunc + 0x10210 + (slot - 1) * 0x104. |
| `session_clear_skill_entry` | `0x005FCD80` | high | Clears a skill record's present flag and name[0] without overwriting its icon or remaining name bytes. |
| `session_rebuild_group_member_cache` | `0x005FCDC0` | high | Parses SSelfLook group_members lines with DBCS-aware scanning into 0x41-byte records at WorldUserFunc +4 and stores the count at +0x1044. |
| `session_update_from_status_packet` | `0x005FCFD0` | high | Copies present SStatus privilege, core stats, vitals, total experience, gold, weight, and retained unknown bytes into WorldUserFunc. |
| `session_add_inventory_from_packet` | `0x005FD1C0` | high | Accepts SAddInventory slots 1 through 60 and stores sprite, dye color, and name in the compact WorldUserFunc record. |
| `session_remove_inventory_from_packet` | `0x005FD220` | high | Accepts SRemoveInventory slots 1 through 60 and logically clears the matching WorldUserFunc record. |
| `session_add_spell_from_packet` | `0x005FD260` | high | Accepts SAddSpell slots 1 through 89 and argument types 1 through 8 before updating WorldUserFunc spell storage. |
| `session_remove_spell_from_packet` | `0x005FD2E0` | high | Accepts SRemoveSpell slots 1 through 89 before clearing the matching WorldUserFunc spell record. |
| `session_add_skill_from_packet` | `0x005FD320` | high | Accepts SAddSkill slots 1 through 89 before storing the icon and name in WorldUserFunc. |
| `session_remove_skill_from_packet` | `0x005FD370` | high | Accepts SRemoveSkill slots 1 through 89 before clearing the matching WorldUserFunc skill record. |
| `session_update_from_user_appearance_packet` | `0x005FD3B0` | high | Stores user ID, cached facing, raw guild value, character class, final unknown byte, and action state &amp; 0x7F; bit 0 locks movement and actions, while wire bit 0x80 suppresses the other field updates. |
| `session_update_from_self_look_packet` | `0x005FD450` | high | Caches widened SSelfLook show_master_metadata, show_ability_metadata, and character_class at +0x15C74 through +0x15C7C, then rebuilds the fixed group-member records from group_members. |
| `crc32_update` | `0x00604530` | high | Standard reflected IEEE CRC32 update with initial and final inversion. |
| `crt_time` | `0x00622873` | high | Reads the current Windows FILETIME and converts it to Unix-epoch seconds; CLogin passes the result to crt_srand. |
| `crt_srand` | `0x006275DE` | high | Stores the seed used by the client runtime random-number state. |
| `crt_rand` | `0x006275F0` | high | Implements the Microsoft runtime linear-congruential update and returns a 15-bit value. |
