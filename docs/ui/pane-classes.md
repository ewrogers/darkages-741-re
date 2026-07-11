# UI pane class catalog

The version-741 executable retains Microsoft Visual C++ RTTI names for much of its UI hierarchy. This gives us the company's class names even when function symbols are absent.

The machine-readable source is `ida/exports/ui-pane-classes.yaml`. Addresses are static virtual addresses of RTTI type-name strings, not object instances or vtables.

## Scope

- RTTI records containing `Pane`: `302`
- Concrete class records: `263`
- Template and singleton wrapper records: `39`
- Records with recovered layout or usage context: `23`

The wrapper records are useful. A `Singleton<T>` record is evidence that the engine manages one shared instance of `T`, but it is not a second pane implementation.

Layout associations are listed only when the local executable references that archive entry from the construction path, or when the class and layout relationship is otherwise direct. See [declarative layout files](layout-files.md) for the format and archive inventory.

## Classes

| Internal class | RTTI address | Kind | Layout archive entry | Recovered context |
|---|---:|---|---|---|
| `_EventListPane` | `0x6d2c2c` | class | unknown | RTTI name only |
| `_temp_::GroupAlertPane` | `0x6d39c8` | class | unknown | RTTI name only |
| `AddToBlockListenInputPane` | `0x6cc5a8` | class | unknown | RTTI name only |
| `AgreementDialogPane` | `0x6c4048` | class | `setoa.dat:_nagree.txt` | account agreement dialog<br>constructor: ui_agreement_dialog_ctor at 0x402430 |
| `AlbumInfoPane` | `0x6cb3c4` | class | unknown | RTTI name only |
| `AlbumPicDialogPane` | `0x6d2bcc` | class | unknown | RTTI name only |
| `AlbumViewPane` | `0x6cb3e0` | class | unknown | RTTI name only |
| `AlertPane` | `0x6c4724` | class | unknown | RTTI name only |
| `AlphaScreenPane` | `0x6c4138` | class | unknown | RTTI name only |
| `AlphaScreenPaneSegmented` | `0x6c4158` | class | unknown | RTTI name only |
| `AnimationPane` | `0x6c4180` | class | unknown | RTTI name only |
| `ArgsLineInputPane` | `0x6c7580` | class | unknown | RTTI name only |
| `ArgumentedTextMenuPane` | `0x6ca130` | class | unknown | RTTI name only |
| `ArticleListPane` | `0x6c46c8` | class | unknown | RTTI name only |
| `BkStoryPane` | `0x6c42c4` | class | unknown | RTTI name only |
| `BlockListenInputPane` | `0x6cc534` | class | unknown | RTTI name only |
| `BoardListPane` | `0x6c4654` | class | unknown | RTTI name only |
| `BrowserControlPane` | `0x6c43a0` | class | unknown | RTTI name only |
| `BrowserDialogPane` | `0x6c4334` | class | unknown | RTTI name only |
| `BtmButtonsPane_A` | `0x6c45a0` | class | unknown | RTTI name only |
| `BulletinDialogPane` | `0x6c4610` | class | `setoa.dat:_nbdlist.txt` | bulletin board dialog<br>constructor: ui_bulletin_dialog_ctor at 0x41d8b0 |
| `ButtonControlPane` | `0x6c58e4` | class | unknown | RTTI name only |
| `ButtonGroupViewPane` | `0x6cb0b4` | class | unknown | RTTI name only |
| `ChangePasswordDialogPane` | `0x6c9c78` | class | `setoa.dat:_npw.txt` | password change dialog<br>constructor: ui_change_password_dialog_ctor at 0x4bb2a0 |
| `CharInputPane` | `0x6cc558` | class | unknown | RTTI name only |
| `ChatInputPane` | `0x6cc4d8` | class | unknown | public say and shout text input<br>constructor: chat_input_pane_ctor at 0x54fca0<br>submit: chat_input_send_say at 0x54fd90 |
| `ChattingPane` | `0x6c4a2c` | class | unknown | RTTI name only |
| `ChattingPane2` | `0x6d2964` | class | unknown | RTTI name only |
| `ChattingPaneInterface` | `0x6d28dc` | class | unknown | RTTI name only |
| `CIPane` | `0x6c4a64` | class | unknown | RTTI name only |
| `ClockPane` | `0x6c4aa4` | class | unknown | RTTI name only |
| `CommandLineInputPane` | `0x6c5584` | class | unknown | RTTI name only |
| `ControlPane` | `0x6c43c4` | class | unknown | RTTI name only |
| `CreateUserDialogPane` | `0x6c5af8` | class | `setoa.dat:_ncreate.txt` | character creation dialog<br>constructor: ui_create_user_dialog_ctor at 0x43c370 |
| `DeleteFromBlockListenInputPane` | `0x6cc5d0` | class | unknown | RTTI name only |
| `DescPane` | `0x6c7648` | class | unknown | RTTI name only |
| `DialogPane` | `0x6c406c` | class | unknown | RTTI name only |
| `DraggedInvItemPane` | `0x6c7440` | class | unknown | RTTI name only |
| `DraggedMapItemPane` | `0x6c7480` | class | unknown | RTTI name only |
| `DraggedPane` | `0x6c5d34` | class | unknown | RTTI name only |
| `DraggedPicPane` | `0x6cb3fc` | class | unknown | RTTI name only |
| `DraggedSkillInvItemPane` | `0x6c74c4` | class | unknown | RTTI name only |
| `DraggedSpellInvItemPane` | `0x6c750c` | class | unknown | RTTI name only |
| `DraggedWorldItemPane` | `0x6d3750` | class | unknown | RTTI name only |
| `DropGoldDialogPane` | `0x6c73f8` | class | unknown | RTTI name only |
| `EditablePaperPane` | `0x6cbeec` | class | unknown | RTTI name only |
| `EmoticonSelectPane_A` | `0x6c5de4` | class | unknown | RTTI name only |
| `EmployeeDialogPane` | `0x6c5e68` | class | unknown | RTTI name only |
| `EmployeeItemPropertyDialogPane` | `0x6c5e08` | class | unknown | RTTI name only |
| `EmployeeQuantityInputDialogPane` | `0x6c5e38` | class | unknown | RTTI name only |
| `EquipPane` | `0x6c5ebc` | class | unknown | RTTI name only |
| `EventInfoDialogPane` | `0x6d2b20` | class | `setoa.dat:_nui_eve.txt` | event detail dialog<br>constructor: ui_event_info_dialog_ctor at 0x5af460 |
| `EventInfoPane` | `0x6cb2e4` | class | unknown | RTTI name only |
| `EventListPane` | `0x6cb31c` | class | unknown | RTTI name only |
| `EventViewPane` | `0x6cb300` | class | unknown | RTTI name only |
| `ExchangeItemListPane` | `0x6c63bc` | class | unknown | RTTI name only |
| `ExGroupViewPane` | `0x6cb180` | class | unknown | RTTI name only |
| `ExtraStatusInfoPane` | `0x6d1b08` | class | unknown | RTTI name only |
| `FamilyListDialogPane` | `0x6c690c` | class | unknown | RTTI name only |
| `FieldMapBalloonPane` | `0x6c6934` | class | unknown | RTTI name only |
| `FieldMapPane` | `0x6c6958` | class | unknown | RTTI name only |
| `FieldMapPointPane` | `0x6c6974` | class | unknown | RTTI name only |
| `FindFarmpet::FindFarmpetPane` | `0x6ca674` | class | unknown | RTTI name only |
| `FishingDialogPane` | `0x6c6a90` | class | unknown | RTTI name only |
| `FishingGetPane` | `0x6c6a70` | class | unknown | RTTI name only |
| `FishingImpactPane` | `0x6c6a50` | class | unknown | RTTI name only |
| `GameMessagePane` | `0x6c6b10` | class | unknown | upper-left colored message overlay<br>constructor: chat_game_message_pane_ctor at 0x47c2a0<br>append_rgb: chat_game_message_pane_append_rgb at 0x47c5c0 |
| `GiveGoldDialogPane` | `0x6c741c` | class | unknown | RTTI name only |
| `GroupAdDialogPane` | `0x6cb144` | class | unknown | RTTI name only |
| `GroupAdInfoDialogPane` | `0x6cb1a0` | class | unknown | RTTI name only |
| `GroupAdPane` | `0x6cb164` | class | unknown | RTTI name only |
| `GroupListPane` | `0x6cb128` | class | unknown | RTTI name only |
| `GroupViewPane` | `0x6c5efc` | class | unknown | RTTI name only |
| `GUIBackPane` | `0x6d270c` | class | unknown | RTTI name only |
| `GUIBackPane::_BtmButtonsPane` | `0x6d2754` | class | unknown | RTTI name only |
| `GUIBackPane::_EmoticonSelectPane` | `0x6d27ac` | class | unknown | RTTI name only |
| `GUIBackPane::_ShowUsersPane` | `0x6d2780` | class | unknown | RTTI name only |
| `GUIBackPane::_SpelledViewPane` | `0x6d27dc` | class | unknown | RTTI name only |
| `GUIBackPane_Interface` | `0x6d26bc` | class | unknown | RTTI name only |
| `GUIInfoPane` | `0x6cb4d8` | class | unknown | RTTI name only |
| `GUIOptionPane` | `0x6d28c0` | class | unknown | RTTI name only |
| `HelpInfoPane` | `0x6cb49c` | class | unknown | RTTI name only |
| `HotKeyPane` | `0x6c6d50` | class | `setoa.dat:_nhotkey.txt` | hot-key configuration<br>constructor: ui_hot_key_pane_ctor at 0x488320 |
| `HumanImageControlPane` | `0x6c6d6c` | class | unknown | RTTI name only |
| `ImageButtonControlPane` | `0x6c5950` | class | unknown | RTTI name only |
| `ImageButtonExControlPane` | `0x6c5978` | class | unknown | RTTI name only |
| `ImageControlPane` | `0x6c5a80` | class | unknown | RTTI name only |
| `ImageFieldMapPointPane` | `0x6c69b8` | class | unknown | RTTI name only |
| `ImagePane` | `0x6c708c` | class | unknown | RTTI name only |
| `IMECandidatePane` | `0x6c71e8` | class | unknown | RTTI name only |
| `InputBirthdateDialogPane` | `0x6c9ca0` | class | unknown | RTTI name only |
| `InventoryNumberShortcutPane` | `0x6d2690` | class | unknown | RTTI name only |
| `InventoryPane_A` | `0x6c7278` | class | unknown | RTTI name only |
| `InventorySelectButtonsPane` | `0x6d2874` | class | unknown | RTTI name only |
| `InvItemPane` | `0x6c73dc` | class | unknown | RTTI name only |
| `ItemBuyAlertPane` | `0x6ca1cc` | class | unknown | RTTI name only |
| `ItemDragPane` | `0x6d3734` | class | unknown | RTTI name only |
| `ItemImageControlPane` | `0x6ca450` | class | unknown | RTTI name only |
| `ItemInventoryPane` | `0x6d2980` | class | unknown | RTTI name only |
| `ItemListPane` | `0x6c9fdc` | class | unknown | RTTI name only |
| `ItemListPane_New` | `0x6c9fbc` | class | unknown | RTTI name only |
| `ItemPane` | `0x6c73c4` | class | unknown | RTTI name only |
| `ItemShop::IconInvControlPane` | `0x6c7688` | class | unknown | RTTI name only |
| `ItemShop::SBGetAlertPane` | `0x6c76b4` | class | unknown | RTTI name only |
| `ItemShop::ShopDialogPane` | `0x6c7748` | class | unknown | RTTI name only |
| `ItemShop::ShoppingBagDialogPane` | `0x6c76dc` | class | unknown | RTTI name only |
| `KeyboardInfoPane` | `0x6cb4b8` | class | unknown | RTTI name only |
| `LayeredTabImagePane` | `0x6d1bd8` | class | unknown | RTTI name only |
| `LayeredTabPane` | `0x6cb1ec` | class | unknown | RTTI name only |
| `LegendDialogPane` | `0x6c49a4` | class | unknown | RTTI name only |
| `LegendInfoPane` | `0x6cb234` | class | unknown | RTTI name only |
| `LegendListPane` | `0x6c4984` | class | unknown | RTTI name only |
| `LineInputPane` | `0x6c55a8` | class | unknown | RTTI name only |
| `ListPane` | `0x6c4670` | class | unknown | RTTI name only |
| `LoadUsersPane` | `0x6d1154` | class | unknown | RTTI name only |
| `LoginDialogPane` | `0x6c9c58` | class | `setoa.dat:_nlogin.txt` | login dialog<br>constructor: ui_login_dialog_ctor at 0x4ba180<br>control_action: ui_login_dialog_handle_control_action at 0x4ba8c0<br>key_event: ui_login_dialog_handle_key_event at 0x4ba810<br>Child attachment order maps OK to action ID 0 and Cancel to action ID 1. |
| `LogoPane` | `0x6c99c4` | class | unknown | RTTI name only |
| `LogoShowPane` | `0x6c9c08` | class | unknown | RTTI name only |
| `MailListPane` | `0x6c47d0` | class | unknown | RTTI name only |
| `MainMenuPane` | `0x6c9c3c` | class | `setoa.dat:_nstart.txt` | startup main menu<br>constructor: ui_main_menu_pane_ctor at 0x4b6c70 |
| `ManufactureDialogPane` | `0x6c9cd8` | class | unknown | RTTI name only |
| `MapItem_Pane` | `0x6c7464` | class | unknown | RTTI name only |
| `MapLoadingPane` | `0x6d2fa0` | class | unknown | RTTI name only |
| `MerchantDialogPane` | `0x6ca03c` | class | unknown | RTTI name only |
| `MFGSAlertPane` | `0x6ca5f4` | class | unknown | RTTI name only |
| `MiniGame::AbstractGameControlPane` | `0x6ca888` | class | unknown | RTTI name only |
| `MiniGame::BrowserGameControlPane` | `0x6cb024` | class | unknown | RTTI name only |
| `MiniGame::GameDialogPane` | `0x6cb054` | class | unknown | RTTI name only |
| `MonsterImageControlPane` | `0x6ca428` | class | unknown | RTTI name only |
| `MonsterInfoPane` | `0x6cb41c` | class | unknown | RTTI name only |
| `MonsterListPane` | `0x6cb43c` | class | unknown | RTTI name only |
| `MyItemListPane` | `0x6c63fc` | class | unknown | RTTI name only |
| `NewChatting2Pane` | `0x6d2944` | class | unknown | RTTI name only |
| `NewChattingPane` | `0x6d2924` | class | unknown | RTTI name only |
| `NewChattingPane_Tpl` | `0x6d2900` | class | unknown | RTTI name only |
| `NewExtraStatusInfoPane` | `0x6d284c` | class | unknown | RTTI name only |
| `NewInventoryPane<SkillInvItemPane>` | `0x6c72bc` | wrapper | unknown | RTTI name only |
| `NewInventoryPane<SpellInvItemPane>` | `0x6c7318` | wrapper | unknown | RTTI name only |
| `NewLegendDialogPane` | `0x6c4a08` | class | unknown | RTTI name only |
| `NewPatchPane` | `0x6cb4f4` | class | unknown | RTTI name only |
| `NewSkillInventoryPane` | `0x6c7298` | class | unknown | RTTI name only |
| `NewSpellInventoryPane` | `0x6c72f4` | class | unknown | RTTI name only |
| `NewStatusInfoPane` | `0x6d282c` | class | unknown | RTTI name only |
| `NewSystemMessagePane` | `0x6d29f0` | class | unknown | RTTI name only |
| `NewSystemMessageTextPane` | `0x6d29c8` | class | unknown | RTTI name only |
| `NewWorldMapInfoPane` | `0x6cb478` | class | unknown | RTTI name only |
| `NexonClubAuthAlertPane` | `0x6cb510` | class | unknown | RTTI name only |
| `NoNexonClubIDWarningPane` | `0x6c5b50` | class | unknown | RTTI name only |
| `NPCIllustPane` | `0x6cb5a8` | class | unknown | RTTI name only |
| `NPCListMenuPane` | `0x6cb700` | class | unknown | RTTI name only |
| `NPCTilePane` | `0x6cb5c4` | class | unknown | RTTI name only |
| `nui_AlbumPane` | `0x6d2bf0` | class | `setoa.dat:_nui_al.txt` | new-UI album pane<br>constructor: ui_nui_album_pane_ctor at 0x5b2a70 |
| `nui_ElemListPane` | `0x6d2c0c` | class | unknown | RTTI name only |
| `nui_EventPane` | `0x6d2c4c` | class | unknown | RTTI name only |
| `nui_EventPaneImpl` | `0x6d2c68` | class | `setoa.dat:_nui_ev.txt` | new-UI event pane implementation<br>constructor: ui_nui_event_pane_ctor at 0x5b3ee0 |
| `nui_FamilyPane` | `0x6d2c88` | class | `setoa.dat:_nui_fm.txt` | new-UI family pane<br>constructor: ui_nui_family_pane_ctor at 0x5b4fb0 |
| `nui_IntroPane` | `0x6d2ca8` | class | `setoa.dat:_nui_eq.txt`<br>`setoa.dat:_nui_eqa.txt` | new-UI character overview and equipment pane<br>constructor: ui_nui_intro_pane_ctor at 0x5b59f0 |
| `nui_LegendPane` | `0x6d2cc4` | class | `setoa.dat:_nui_dr.txt` | new-UI legend pane<br>constructor: ui_nui_legend_pane_ctor at 0x5b7aa0 |
| `nui_SkillSpellPane` | `0x6d2d08` | class | `setoa.dat:_nui_sk.txt` | new-UI skill and spell pane<br>constructor: ui_nui_skill_spell_pane_ctor at 0x5b80c0 |
| `NumberArgsSpellInputPane` | `0x6c7558` | class | unknown | RTTI name only |
| `NumLineInputPane` | `0x6d1d3c` | class | unknown | RTTI name only |
| `OptionPane` | `0x6cbc94` | class | unknown | RTTI name only |
| `Pane` | `0x6c4088` | class | unknown | RTTI name only |
| `PopupMenuPane` | `0x6cc178` | class | unknown | world object context menu<br>constructor: ui_popup_menu_pane_ctor at 0x54c010<br>open_for_object: input_open_object_popup_menu at 0x54bdb0 |
| `PortraitControlPane` | `0x6c49c4` | class | unknown | RTTI name only |
| `PortraitTextInputDialogPane` | `0x6d2b44` | class | `setoa.dat:_nui_pi.txt` | portrait text input dialog<br>constructor: ui_portrait_text_input_dialog_ctor at 0x5b11a0 |
| `ProgressBarControlPane` | `0x6c58bc` | class | unknown | RTTI name only |
| `ProgressBarControlPaneEx` | `0x6c5a58` | class | unknown | RTTI name only |
| `Puzzle::BalloonPane` | `0x6ca9e4` | class | unknown | RTTI name only |
| `Puzzle::GameControlPane` | `0x6ca860` | class | unknown | RTTI name only |
| `Puzzle::HelpPane` | `0x6ca984` | class | unknown | RTTI name only |
| `Puzzle::ImageCutPane` | `0x6caa08` | class | unknown | RTTI name only |
| `Puzzle::LevelPane` | `0x6ca9c4` | class | unknown | RTTI name only |
| `Puzzle::PlayPane` | `0x6ca8d8` | class | unknown | RTTI name only |
| `Puzzle::PuzzlePane` | `0x6caa4c` | class | unknown | RTTI name only |
| `Puzzle::PuzzlePane::Tile` | `0x6caa6c` | class | unknown | RTTI name only |
| `Puzzle::RankingPane` | `0x6ca91c` | class | unknown | RTTI name only |
| `Puzzle::ResultPane` | `0x6ca940` | class | unknown | RTTI name only |
| `Puzzle::SendResultPane` | `0x6ca960` | class | unknown | RTTI name only |
| `Puzzle::SettingPane` | `0x6ca8f8` | class | unknown | RTTI name only |
| `Puzzle::TilePane` | `0x6caa2c` | class | unknown | RTTI name only |
| `Puzzle::TimePane` | `0x6ca9a4` | class | unknown | RTTI name only |
| `Puzzle::TitlePane` | `0x6ca8b8` | class | unknown | RTTI name only |
| `QuantityInputDialogPane` | `0x6cc1dc` | class | unknown | RTTI name only |
| `RadioGroupControlPane` | `0x6c59a0` | class | unknown | RTTI name only |
| `ReconnectDialogPane` | `0x6cc35c` | class | unknown | RTTI name only |
| `RopeSkipping::CountdownPane` | `0x6cacc0` | class | unknown | RTTI name only |
| `RopeSkipping::GameControlPane` | `0x6cac18` | class | unknown | RTTI name only |
| `RopeSkipping::GameoverPane` | `0x6cacec` | class | unknown | RTTI name only |
| `RopeSkipping::GradePane` | `0x6cac98` | class | unknown | RTTI name only |
| `RopeSkipping::HelpPane` | `0x6cadb4` | class | unknown | RTTI name only |
| `RopeSkipping::PlayPane` | `0x6cad40` | class | unknown | RTTI name only |
| `RopeSkipping::RankingPane` | `0x6cad8c` | class | unknown | RTTI name only |
| `RopeSkipping::ResultPane` | `0x6cad64` | class | unknown | RTTI name only |
| `RopeSkipping::SkipCountPane` | `0x6cac6c` | class | unknown | RTTI name only |
| `RopeSkipping::TitlePane` | `0x6cac44` | class | unknown | RTTI name only |
| `ScorePane` | `0x6cc600` | class | unknown | score text overlay and SMessage type 18 target<br>constructor: ui_score_pane_ctor at 0x551260<br>append_rgb: ui_score_pane_append_rgb at 0x5516c0 |
| `ScreenPane` | `0x6d104c` | class | unknown | RTTI name only |
| `ScrollableControlPane` | `0x6c59c4` | class | unknown | RTTI name only |
| `ScrollablePane` | `0x6c4688` | class | unknown | RTTI name only |
| `ScrollPane` | `0x6d1088` | class | unknown | RTTI name only |
| `ServerSelectDialogPane` | `0x6d10a4` | class | unknown | RTTI name only |
| `SessionLayeredTabPane` | `0x6cb1c8` | class | unknown | RTTI name only |
| `ShowUsersListPane` | `0x6d10cc` | class | unknown | RTTI name only |
| `ShowUsersPane` | `0x6d10ec` | class | unknown | RTTI name only |
| `ShowUsersPane_A` | `0x6d1108` | class | unknown | RTTI name only |
| `Singleton<AgreementDialogPane>` | `0x6c40e8` | wrapper | unknown | RTTI name only |
| `Singleton<BlockListenInputPane>` | `0x6cc574` | wrapper | unknown | RTTI name only |
| `Singleton<BrowserControlPane>` | `0x6c43e0` | wrapper | unknown | RTTI name only |
| `Singleton<BrowserDialogPane>` | `0x6c4354` | wrapper | unknown | RTTI name only |
| `Singleton<ButtonGroupViewPane>` | `0x6cb0d8` | wrapper | unknown | RTTI name only |
| `Singleton<CIPane>` | `0x6c4a7c` | wrapper | unknown | RTTI name only |
| `Singleton<ClockPane>` | `0x6c4abc` | wrapper | unknown | RTTI name only |
| `Singleton<CreateUserDialogPane>` | `0x6c5b1c` | wrapper | unknown | RTTI name only |
| `Singleton<DescPane>` | `0x6c7660` | wrapper | unknown | RTTI name only |
| `Singleton<EmployeeDialogPane>` | `0x6c5e8c` | wrapper | unknown | RTTI name only |
| `Singleton<EquipPane>` | `0x6c5ed4` | wrapper | unknown | RTTI name only |
| `Singleton<ExtraStatusInfoPane>` | `0x6d1b2c` | wrapper | unknown | RTTI name only |
| `Singleton<GameMessagePane>` | `0x6c6b30` | wrapper | unknown | RTTI name only |
| `Singleton<GUIBackPane>` | `0x6d2728` | wrapper | unknown | RTTI name only |
| `Singleton<IMECandidatePane>` | `0x6c7208` | wrapper | unknown | RTTI name only |
| `Singleton<ItemShop::ShopDialogPane>` | `0x6c7770` | wrapper | unknown | RTTI name only |
| `Singleton<ItemShop::ShoppingBagDialogPane>` | `0x6c770c` | wrapper | unknown | RTTI name only |
| `Singleton<LoadUsersPane>` | `0x6d1170` | wrapper | unknown | RTTI name only |
| `Singleton<LogoPane>` | `0x6c99dc` | wrapper | unknown | RTTI name only |
| `Singleton<ManufactureDialogPane>` | `0x6c9cfc` | wrapper | unknown | RTTI name only |
| `Singleton<MapLoadingPane>` | `0x6d2fc0` | wrapper | unknown | RTTI name only |
| `Singleton<NexonClubAuthAlertPane>` | `0x6cb538` | wrapper | unknown | RTTI name only |
| `Singleton<PopupMenuPane>` | `0x6cc194` | wrapper | unknown | RTTI name only |
| `Singleton<ScorePane>` | `0x6cc618` | wrapper | unknown | RTTI name only |
| `Singleton<ShowUsersPane>` | `0x6d1128` | wrapper | unknown | RTTI name only |
| `Singleton<SpellDelayControlPane>` | `0x6c75c4` | wrapper | unknown | RTTI name only |
| `Singleton<StatusInfoPane>` | `0x6d1adc` | wrapper | unknown | RTTI name only |
| `Singleton<TerminalPane2>` | `0x6d1c18` | wrapper | unknown | RTTI name only |
| `Singleton<ToolTipPane>` | `0x6d1dd0` | wrapper | unknown | RTTI name only |
| `Singleton<TownMapPane>` | `0x6d1e18` | wrapper | unknown | RTTI name only |
| `Singleton<UnitelPane>` | `0x6c5878` | wrapper | unknown | RTTI name only |
| `Singleton<UserInfoPane_ForOthers>` | `0x6d2b98` | wrapper | unknown | RTTI name only |
| `Singleton<UserInfoPane_ForUser>` | `0x6d2ac4` | wrapper | unknown | RTTI name only |
| `Singleton<UserLookPane>` | `0x6c5f34` | wrapper | unknown | RTTI name only |
| `Singleton<WorldPane>` | `0x6d393c` | wrapper | unknown | RTTI name only |
| `Singleton<WorldPane_Impl>` | `0x6d3a48` | wrapper | unknown | RTTI name only |
| `SkillInvItemPane` | `0x6c74a4` | class | unknown | RTTI name only |
| `SkillSpellInfoDialogPane` | `0x6d2af8` | class | `setoa.dat:_nui_ske.txt` | skill or spell detail dialog<br>constructor: ui_skill_spell_info_dialog_ctor at 0x5ae090 |
| `SkillSpellInventoryPane` | `0x6d29a0` | class | unknown | RTTI name only |
| `SkillSpellListPane` | `0x6d2ce4` | class | unknown | RTTI name only |
| `SnowParticle_::SnowParticlePane` | `0x6d305c` | class | unknown | RTTI name only |
| `SpellDelayControlPane` | `0x6c75a0` | class | unknown | RTTI name only |
| `SpelledViewPane_A` | `0x6d1910` | class | unknown | RTTI name only |
| `SpellInvItemPane` | `0x6c74ec` | class | unknown | RTTI name only |
| `SpellSkillInfoPane` | `0x6cb254` | class | unknown | RTTI name only |
| `SpellSkillPropertyPane` | `0x6cb2bc` | class | unknown | RTTI name only |
| `SpellSkillViewPane` | `0x6cb298` | class | unknown | RTTI name only |
| `StackNiye::GameControlPane` | `0x6caecc` | class | unknown | RTTI name only |
| `StackNiye::PlayPane` | `0x6caef4` | class | unknown | RTTI name only |
| `StaffPane` | `0x6c42e0` | class | unknown | RTTI name only |
| `StaticTextControlPane` | `0x6c5a0c` | class | unknown | RTTI name only |
| `StaticTextControlPane2` | `0x6c5a30` | class | unknown | RTTI name only |
| `StatusInfoPane` | `0x6d1abc` | class | unknown | RTTI name only |
| `StringListPane` | `0x6c48ac` | class | unknown | RTTI name only |
| `StringSpellInputPane` | `0x6c7534` | class | unknown | RTTI name only |
| `SystemButtonsPane` | `0x6d28a0` | class | unknown | RTTI name only |
| `TabButtonPane` | `0x6cb10c` | class | unknown | RTTI name only |
| `TabPane<LayeredImage>` | `0x6cb20c` | wrapper | unknown | RTTI name only |
| `TaskListPane` | `0x6ca0cc` | class | unknown | RTTI name only |
| `TellInputPane` | `0x6cc518` | class | unknown | private tell or whisper text input<br>submit: chat_tell_input_send at 0x550590 |
| `TellReceiverInputPane` | `0x6cc4f4` | class | unknown | RTTI name only |
| `TerminalPane2` | `0x6d1bfc` | class | unknown | RTTI name only |
| `TextBoxPane` | `0x6d1d04` | class | unknown | RTTI name only |
| `TextButtonControlPane` | `0x6c5904` | class | unknown | RTTI name only |
| `TextButtonExControlPane` | `0x6c5928` | class | unknown | RTTI name only |
| `TextEditControlPane` | `0x6c59e8` | class | unknown | RTTI name only |
| `TextEditPane` | `0x6c4a48` | class | unknown | RTTI name only |
| `TextFieldMapPointPane` | `0x6c6994` | class | unknown | RTTI name only |
| `TextLinePane` | `0x6d1d20` | class | unknown | RTTI name only |
| `ToolTipPane` | `0x6d1db4` | class | unknown | RTTI name only |
| `TownInfoPane` | `0x6cb45c` | class | unknown | RTTI name only |
| `TownMapPane` | `0x6d1dfc` | class | unknown | RTTI name only |
| `UnitelPane` | `0x6c585c` | class | unknown | RTTI name only |
| `UrlAlertPane` | `0x6d1ea0` | class | unknown | RTTI name only |
| `UserConfirmPane` | `0x6d1ebc` | class | unknown | RTTI name only |
| `UserInfoPane` | `0x6d2a84` | class | unknown | RTTI name only |
| `UserInfoPane_ForOthers` | `0x6d2b70` | class | unknown | RTTI name only |
| `UserInfoPane_ForUser` | `0x6d2aa0` | class | unknown | RTTI name only |
| `UserInfoTabPane` | `0x6d2a64` | class | unknown | RTTI name only |
| `UserLookPane` | `0x6c5f18` | class | unknown | RTTI name only |
| `UserShapeControlPane` | `0x6ca2c0` | class | unknown | RTTI name only |
| `VirusAlertPane` | `0x6cc39c` | class | unknown | RTTI name only |
| `WindowMessageDialogPane` | `0x6c5bfc` | class | unknown | SMessage look and message popup<br>constructor: ui_window_message_dialog_ctor at 0x4488c0 |
| `World::BalloonPane` | `0x6d325c` | class | unknown | object-attached speech balloon<br>constructor: chat_world_balloon_pane_ctor at 0x5c4f00 |
| `WorldControllerPane` | `0x6d327c` | class | unknown | RTTI name only |
| `WorldMapImagePane` | `0x6cb380` | class | unknown | RTTI name only |
| `WorldMapInfo_DA_Pane` | `0x6cb3a0` | class | unknown | RTTI name only |
| `WorldMapInfo_Normal_Pane` | `0x6cb358` | class | unknown | RTTI name only |
| `WorldMapInfoPane` | `0x6cb338` | class | unknown | RTTI name only |
| `WorldMinimapPane_Impl` | `0x6d3544` | class | unknown | RTTI name only |
| `WorldObject_Name_Pane` | `0x6d383c` | class | unknown | RTTI name only |
| `WorldPane` | `0x6d38f8` | class | unknown | RTTI name only |
| `WorldPane_Impl` | `0x6d3a28` | class | unknown | RTTI name only |
| `WorldPane_MiscPacketProcessor` | `0x6d3910` | class | unknown | RTTI name only |
| `WorldPane_user_object_message` | `0x6d3408` | class | unknown | RTTI name only |
| `YesNoAlertPane` | `0x6c5bdc` | class | unknown | RTTI name only |

## Updating the export

With the matching executable available locally, run:

```powershell
python tools/export_ui_pane_classes.py C:\path\to\Darkages.exe
python tools/render_ui_pane_report.py
```

The exporter verifies the executable hash and preserves curated context fields already present in the YAML. Do not commit the executable or extracted game assets.
