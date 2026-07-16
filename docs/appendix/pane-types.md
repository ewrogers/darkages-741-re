# Pane type and inheritance appendix

The matching client contains 332 distinct RTTI classes whose inheritance reaches `Pane`. The list is alphabetical and deduplicates secondary vtables for multiple inheritance.

Direct bases come from each MSVC Base Class Array. Pane lineage shows the shortest direct-base path back to `Pane`. `Pane` itself directly inherits `Canvas` and `TimerHandler`; both reach `LObject`.

For the text layout file loaded by each known pane, see the [UI layout registry](ui-layout-registry.md).

| Type | Direct base class(es) | Pane lineage |
| --- | --- | --- |
| `_EventListPane` | `nui_ElemListPane` | `_EventListPane` → `nui_ElemListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `_temp_::GroupAlertPane` | `AlertPane` | `_temp_::GroupAlertPane` → `AlertPane` → `DialogPane` → `Pane` |
| `AddItemDialog` | `DialogPane` | `AddItemDialog` → `DialogPane` → `Pane` |
| `AddItemWithCountDialog` | `DialogPane` | `AddItemWithCountDialog` → `DialogPane` → `Pane` |
| `AddToBlockListenInputPane` | `LineInputPane` | `AddToBlockListenInputPane` → `LineInputPane` → `Pane` |
| `AgreementDialogPane` | `DialogPane`, `Singleton<AgreementDialogPane>` | `AgreementDialogPane` → `DialogPane` → `Pane` |
| `AlbumInfoPane` | `Pane` | `AlbumInfoPane` → `Pane` |
| `AlbumPicDialogPane` | `DialogPane` | `AlbumPicDialogPane` → `DialogPane` → `Pane` |
| `AlbumViewPane` | `ScrollablePane` | `AlbumViewPane` → `ScrollablePane` → `Pane` |
| `AlertPane` | `DialogPane` | `AlertPane` → `DialogPane` → `Pane` |
| `AlphaScreenPane` | `Pane` | `AlphaScreenPane` → `Pane` |
| `AlphaScreenPaneSegmented` | `Pane` | `AlphaScreenPaneSegmented` → `Pane` |
| `AnimationPane` | `Pane` | `AnimationPane` → `Pane` |
| `ArgsLineInputPane` | `LineInputPane` | `ArgsLineInputPane` → `LineInputPane` → `Pane` |
| `ArgumentedTextInputMenuDialog` | `TextInputMenuDialog` | `ArgumentedTextInputMenuDialog` → `TextInputMenuDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `ArgumentedTextMenuDialog` | `TextMenuDialog` | `ArgumentedTextMenuDialog` → `TextMenuDialog` → `TaskListDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `ArgumentedTextMenuDialogEx` | `TextMenuDialogEx` | `ArgumentedTextMenuDialogEx` → `TextMenuDialogEx` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `ArgumentedTextMenuPane` | `TaskListPane` | `ArgumentedTextMenuPane` → `TaskListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `ArticleDialog` | `BulletinDialogPane` | `ArticleDialog` → `BulletinDialogPane` → `DialogPane` → `Pane` |
| `ArticleListDialog` | `BulletinDialogPane` | `ArticleListDialog` → `BulletinDialogPane` → `DialogPane` → `Pane` |
| `ArticleListPane` | `ListPane` | `ArticleListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `BkStoryPane` | `Pane` | `BkStoryPane` → `Pane` |
| `BlockListenInputPane` | `CharInputPane`, `Singleton<BlockListenInputPane>` | `BlockListenInputPane` → `CharInputPane` → `LineInputPane` → `Pane` |
| `BoardListDialog` | `BulletinDialogPane` | `BoardListDialog` → `BulletinDialogPane` → `DialogPane` → `Pane` |
| `BoardListPane` | `ListPane` | `BoardListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `BrowserControlPane` | `ControlPane`, `Singleton<BrowserControlPane>`, `IOleClientSite`, `IOleInPlaceSite`, `DWebBrowserEvents2`, `IDocHostUIHandler`, `IDocHostShowUI` | `BrowserControlPane` → `ControlPane` → `Pane` |
| `BrowserDialogPane` | `DialogPane`, `Singleton<BrowserDialogPane>` | `BrowserDialogPane` → `DialogPane` → `Pane` |
| `BtmButtonsPane_A` | `Pane` | `BtmButtonsPane_A` → `Pane` |
| `BulletinBangNotifyDialog` | `DialogPane` | `BulletinBangNotifyDialog` → `DialogPane` → `Pane` |
| `BulletinDialogPane` | `DialogPane` | `BulletinDialogPane` → `DialogPane` → `Pane` |
| `BulletinSession` | `Pane`, `Singleton<BulletinSession>` | `BulletinSession` → `Pane` |
| `ButtonControlPane` | `ControlPane` | `ButtonControlPane` → `ControlPane` → `Pane` |
| `ButtonGroupViewPane` | `DialogPane`, `Singleton<ButtonGroupViewPane>` | `ButtonGroupViewPane` → `DialogPane` → `Pane` |
| `ChangePasswordDialogPane` | `DialogPane` | `ChangePasswordDialogPane` → `DialogPane` → `Pane` |
| `CharInputPane` | `LineInputPane` | `CharInputPane` → `LineInputPane` → `Pane` |
| `ChatInputPane` | `LineInputPane` | `ChatInputPane` → `LineInputPane` → `Pane` |
| `ChattingPane` | `TextEditPane` | `ChattingPane` → `TextEditPane` → `ScrollablePane` → `Pane` |
| `ChattingPane2` | `ChattingPane` | `ChattingPane2` → `ChattingPane` → `TextEditPane` → `ScrollablePane` → `Pane` |
| `CIPane` | `Pane`, `Singleton<CIPane>` | `CIPane` → `Pane` |
| `ClientItemMenuDialog` | `TaskListDialog` | `ClientItemMenuDialog` → `TaskListDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `ClientSkillMenuDialog` | `TaskListDialog` | `ClientSkillMenuDialog` → `TaskListDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `ClientSpellMenuDialog` | `TaskListDialog` | `ClientSpellMenuDialog` → `TaskListDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `ClockPane` | `Pane`, `Singleton<ClockPane>` | `ClockPane` → `Pane` |
| `CommandLineInputPane` | `LineInputPane` | `CommandLineInputPane` → `LineInputPane` → `Pane` |
| `ConfirmDeleteAlert` | `AlertPane` | `ConfirmDeleteAlert` → `AlertPane` → `DialogPane` → `Pane` |
| `ControlPane` | `Pane` | `ControlPane` → `Pane` |
| `CreateUserDialogPane` | `DialogPane`, `Singleton<CreateUserDialogPane>` | `CreateUserDialogPane` → `DialogPane` → `Pane` |
| `DeleteFromBlockListenInputPane` | `LineInputPane` | `DeleteFromBlockListenInputPane` → `LineInputPane` → `Pane` |
| `DeleteReplyAlert` | `AlertPane`, `Singleton<DeleteReplyAlert>` | `DeleteReplyAlert` → `AlertPane` → `DialogPane` → `Pane` |
| `DescPane` | `Pane`, `Singleton<DescPane>` | `DescPane` → `Pane` |
| `DialogPane` | `Pane` | `DialogPane` → `Pane` |
| `DraggedInvItemPane` | `DraggedPane` | `DraggedInvItemPane` → `DraggedPane` → `Pane` |
| `DraggedMapItemPane` | `DraggedPane` | `DraggedMapItemPane` → `DraggedPane` → `Pane` |
| `DraggedPane` | `Pane` | `DraggedPane` → `Pane` |
| `DraggedPicPane` | `DraggedPane` | `DraggedPicPane` → `DraggedPane` → `Pane` |
| `DraggedSkillInvItemPane` | `DraggedPane` | `DraggedSkillInvItemPane` → `DraggedPane` → `Pane` |
| `DraggedSpellInvItemPane` | `DraggedPane` | `DraggedSpellInvItemPane` → `DraggedPane` → `Pane` |
| `DraggedWorldItemPane` | `DraggedPane` | `DraggedWorldItemPane` → `DraggedPane` → `Pane` |
| `DropGoldDialogPane` | `DialogPane` | `DropGoldDialogPane` → `DialogPane` → `Pane` |
| `EditablePaperPane` | `DialogPane` | `EditablePaperPane` → `DialogPane` → `Pane` |
| `EmoticonSelectPane_A` | `Pane` | `EmoticonSelectPane_A` → `Pane` |
| `EmployeeDialogPane` | `DialogPane`, `Singleton<EmployeeDialogPane>` | `EmployeeDialogPane` → `DialogPane` → `Pane` |
| `EmployeeItemPropertyDialogPane` | `DialogPane` | `EmployeeItemPropertyDialogPane` → `DialogPane` → `Pane` |
| `EmployeeQuantityInputDialogPane` | `DialogPane` | `EmployeeQuantityInputDialogPane` → `DialogPane` → `Pane` |
| `EquipPane` | `DialogPane`, `Singleton<EquipPane>` | `EquipPane` → `DialogPane` → `Pane` |
| `EventInfoDialogPane` | `DialogPane` | `EventInfoDialogPane` → `DialogPane` → `Pane` |
| `EventInfoPane` | `SessionLayeredTabPane` | `EventInfoPane` → `SessionLayeredTabPane` → `LayeredTabPane` → `TabPane<LayeredImage>` → `DialogPane` → `Pane` |
| `EventListPane` | `ListPane` | `EventListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `EventViewPane` | `DialogPane` | `EventViewPane` → `DialogPane` → `Pane` |
| `ExchangeDialog` | `DialogPane` | `ExchangeDialog` → `DialogPane` → `Pane` |
| `ExchangeItemListPane` | `ListPane` | `ExchangeItemListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `ExGroupViewPane` | `Pane` | `ExGroupViewPane` → `Pane` |
| `ExTextButtonControl` | `ButtonControlPane` | `ExTextButtonControl` → `ButtonControlPane` → `ControlPane` → `Pane` |
| `ExtraStatusInfoPane` | `Pane`, `StatusInfo`, `Singleton<ExtraStatusInfoPane>` | `ExtraStatusInfoPane` → `Pane` |
| `FaceMenuDialog` | `MerchantDialogPane` | `FaceMenuDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `FamilyListDialogPane` | `DialogPane` | `FamilyListDialogPane` → `DialogPane` → `Pane` |
| `FieldMapBalloonPane` | `Pane` | `FieldMapBalloonPane` → `Pane` |
| `FieldMapPane` | `Pane` | `FieldMapPane` → `Pane` |
| `FieldMapPointPane` | `Pane` | `FieldMapPointPane` → `Pane` |
| `FindFarmpet::FindFarmpetPane` | `Pane` | `FindFarmpet::FindFarmpetPane` → `Pane` |
| `FishingDialogPane` | `DialogPane` | `FishingDialogPane` → `DialogPane` → `Pane` |
| `FishingGetPane` | `Pane` | `FishingGetPane` → `Pane` |
| `FishingImpactPane` | `Pane` | `FishingImpactPane` → `Pane` |
| `FriendListDialog` | `DialogPane`, `Singleton<FriendListDialog>` | `FriendListDialog` → `DialogPane` → `Pane` |
| `GameMessagePane` | `Pane`, `Singleton<GameMessagePane>` | `GameMessagePane` → `Pane` |
| `GameSettingDialog` | `DialogPane`, `Singleton<GameSettingDialog>` | `GameSettingDialog` → `DialogPane` → `Pane` |
| `GiveGoldDialogPane` | `DialogPane` | `GiveGoldDialogPane` → `DialogPane` → `Pane` |
| `GroupAdDialogPane` | `DialogPane` | `GroupAdDialogPane` → `DialogPane` → `Pane` |
| `GroupAdInfoDialogPane` | `GroupAdDialogPane` | `GroupAdInfoDialogPane` → `GroupAdDialogPane` → `DialogPane` → `Pane` |
| `GroupAdPane` | `GroupAdDialogPane` | `GroupAdPane` → `GroupAdDialogPane` → `DialogPane` → `Pane` |
| `GroupListPane` | `DialogPane` | `GroupListPane` → `DialogPane` → `Pane` |
| `GroupViewPane` | `Pane` | `GroupViewPane` → `Pane` |
| `GUIBackPane` | `Pane`, `GUIBackPane_Interface`, `InventoryControl_Interface`, `Singleton<GUIBackPane>` | `GUIBackPane` → `Pane` |
| `GUIBackPane::_BtmButtonsPane` | `BtmButtonsPane_A` | `GUIBackPane::_BtmButtonsPane` → `BtmButtonsPane_A` → `Pane` |
| `GUIBackPane::_EmoticonSelectPane` | `EmoticonSelectPane_A` | `GUIBackPane::_EmoticonSelectPane` → `EmoticonSelectPane_A` → `Pane` |
| `GUIBackPane::_ShowUsersPane` | `ShowUsersPane_A` | `GUIBackPane::_ShowUsersPane` → `ShowUsersPane_A` → `DialogPane` → `Pane` |
| `GUIBackPane::_SpelledViewPane` | `SpelledViewPane_A` | `GUIBackPane::_SpelledViewPane` → `SpelledViewPane_A` → `Pane` |
| `GUIInfoPane` | `Pane` | `GUIInfoPane` → `Pane` |
| `GUIOptionPane` | `DialogPane` | `GUIOptionPane` → `DialogPane` → `Pane` |
| `HelpDialog` | `DialogPane` | `HelpDialog` → `DialogPane` → `Pane` |
| `HelpInfoPane` | `SessionLayeredTabPane` | `HelpInfoPane` → `SessionLayeredTabPane` → `LayeredTabPane` → `TabPane<LayeredImage>` → `DialogPane` → `Pane` |
| `HotKeyPane` | `Pane` | `HotKeyPane` → `Pane` |
| `HumanImageControlPane` | `ControlPane` | `HumanImageControlPane` → `ControlPane` → `Pane` |
| `ImageButtonControlPane` | `ButtonControlPane` | `ImageButtonControlPane` → `ButtonControlPane` → `ControlPane` → `Pane` |
| `ImageButtonExControlPane` | `ImageButtonControlPane` | `ImageButtonExControlPane` → `ImageButtonControlPane` → `ButtonControlPane` → `ControlPane` → `Pane` |
| `ImageControlPane` | `ControlPane` | `ImageControlPane` → `ControlPane` → `Pane` |
| `ImageFieldMapPointPane` | `FieldMapPointPane` | `ImageFieldMapPointPane` → `FieldMapPointPane` → `Pane` |
| `ImagePane` | `Pane` | `ImagePane` → `Pane` |
| `IMECandidatePane` | `Pane`, `Singleton<IMECandidatePane>` | `IMECandidatePane` → `Pane` |
| `InputBirthdateDialogPane` | `DialogPane` | `InputBirthdateDialogPane` → `DialogPane` → `Pane` |
| `InventoryNumberShortcutPane` | `Pane` | `InventoryNumberShortcutPane` → `Pane` |
| `InventoryPane_A` | `Pane` | `InventoryPane_A` → `Pane` |
| `InventorySelectButtonsPane` | `Pane` | `InventorySelectButtonsPane` → `Pane` |
| `InvItemPane` | `ItemPane` | `InvItemPane` → `ItemPane` → `Pane` |
| `ItemBuyAlertPane` | `AlertPane` | `ItemBuyAlertPane` → `AlertPane` → `DialogPane` → `Pane` |
| `ItemDragPane` | `Pane` | `ItemDragPane` → `Pane` |
| `ItemImageControlPane` | `ControlPane` | `ItemImageControlPane` → `ControlPane` → `Pane` |
| `ItemInventoryPane` | `InventoryPane_A` | `ItemInventoryPane` → `InventoryPane_A` → `Pane` |
| `ItemListPane` | `ListPane` | `ItemListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `ItemListPane_New` | `ItemListPane` | `ItemListPane_New` → `ItemListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `ItemPane` | `Pane` | `ItemPane` → `Pane` |
| `ItemShop::IconInvControlPane` | `ControlPane` | `ItemShop::IconInvControlPane` → `ControlPane` → `Pane` |
| `ItemShop::SBGetAlertPane` | `AlertPane` | `ItemShop::SBGetAlertPane` → `AlertPane` → `DialogPane` → `Pane` |
| `ItemShop::ShopDialogPane` | `DialogPane`, `Singleton<ItemShop::ShopDialogPane>` | `ItemShop::ShopDialogPane` → `DialogPane` → `Pane` |
| `ItemShop::ShoppingBagDialogPane` | `DialogPane`, `Singleton<ItemShop::ShoppingBagDialogPane>` | `ItemShop::ShoppingBagDialogPane` → `DialogPane` → `Pane` |
| `KeyboardInfoPane` | `Pane` | `KeyboardInfoPane` → `Pane` |
| `LayeredTabImagePane` | `ImagePane` | `LayeredTabImagePane` → `ImagePane` → `Pane` |
| `LayeredTabPane` | `TabPane<LayeredImage>` | `LayeredTabPane` → `TabPane<LayeredImage>` → `DialogPane` → `Pane` |
| `LegendDialogPane` | `DialogPane` | `LegendDialogPane` → `DialogPane` → `Pane` |
| `LegendInfoPane` | `SessionLayeredTabPane` | `LegendInfoPane` → `SessionLayeredTabPane` → `LayeredTabPane` → `TabPane<LayeredImage>` → `DialogPane` → `Pane` |
| `LegendListPane` | `ListPane` | `LegendListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `LineInputPane` | `Pane` | `LineInputPane` → `Pane` |
| `ListPane` | `ScrollablePane` | `ListPane` → `ScrollablePane` → `Pane` |
| `LoadUsersPane` | `Pane`, `Singleton<LoadUsersPane>` | `LoadUsersPane` → `Pane` |
| `LoginDialogPane` | `DialogPane` | `LoginDialogPane` → `DialogPane` → `Pane` |
| `LogoPane` | `Pane`, `Singleton<LogoPane>` | `LogoPane` → `Pane` |
| `LogoShowPane` | `Pane` | `LogoShowPane` → `Pane` |
| `MacroDialog` | `DialogPane`, `Singleton<MacroDialog>` | `MacroDialog` → `DialogPane` → `Pane` |
| `MailDeleteReplyAlert` | `AlertPane` | `MailDeleteReplyAlert` → `AlertPane` → `DialogPane` → `Pane` |
| `MailDialog` | `BulletinDialogPane` | `MailDialog` → `BulletinDialogPane` → `DialogPane` → `Pane` |
| `MailListDialog` | `BulletinDialogPane` | `MailListDialog` → `BulletinDialogPane` → `DialogPane` → `Pane` |
| `MailListPane` | `ListPane` | `MailListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `MailTransferReplyAlert` | `AlertPane` | `MailTransferReplyAlert` → `AlertPane` → `DialogPane` → `Pane` |
| `MainMenuPane` | `Pane` | `MainMenuPane` → `Pane` |
| `ManufactureDialogPane` | `DialogPane`, `Singleton<ManufactureDialogPane>` | `ManufactureDialogPane` → `DialogPane` → `Pane` |
| `MapItem_Pane` | `Pane` | `MapItem_Pane` → `Pane` |
| `MapLoadingPane` | `Pane`, `Singleton<MapLoadingPane>` | `MapLoadingPane` → `Pane` |
| `MerchantDialogPane` | `DialogPane` | `MerchantDialogPane` → `DialogPane` → `Pane` |
| `MerchantSession` | `Pane` | `MerchantSession` → `Pane` |
| `MessageDialog` | `MessageDialogBase` | `MessageDialog` → `MessageDialogBase` → `DialogPane` → `Pane` |
| `MessageDialogBase` | `DialogPane` | `MessageDialogBase` → `DialogPane` → `Pane` |
| `MetaTableManager` | `Pane`, `Singleton<MetaTableManager>` | `MetaTableManager` → `Pane` |
| `MFGSAlertPane` | `AlertPane` | `MFGSAlertPane` → `AlertPane` → `DialogPane` → `Pane` |
| `MidiPlayer` | `Pane` | `MidiPlayer` → `Pane` |
| `MiniGame::AbstractGameControlPane` | `ControlPane` | `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `MiniGame::BrowserGameControlPane` | `MiniGame::AbstractGameControlPane` | `MiniGame::BrowserGameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `MiniGame::GameDialogPane` | `DialogPane` | `MiniGame::GameDialogPane` → `DialogPane` → `Pane` |
| `MonsterImageControlPane` | `ControlPane` | `MonsterImageControlPane` → `ControlPane` → `Pane` |
| `MonsterInfoPane` | `DialogPane` | `MonsterInfoPane` → `DialogPane` → `Pane` |
| `MonsterListPane` | `ListPane` | `MonsterListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `MyItemListPane` | `ListPane` | `MyItemListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `NewArticleDialog` | `BulletinDialogPane` | `NewArticleDialog` → `BulletinDialogPane` → `DialogPane` → `Pane` |
| `NewChatting2Pane` | `NewChattingPane_Tpl` | `NewChatting2Pane` → `NewChattingPane_Tpl` → `Pane` |
| `NewChattingPane` | `NewChattingPane_Tpl` | `NewChattingPane` → `NewChattingPane_Tpl` → `Pane` |
| `NewChattingPane_Tpl` | `ChattingPaneInterface`, `Pane` | `NewChattingPane_Tpl` → `Pane` |
| `NewExtraStatusInfoPane` | `ExtraStatusInfoPane`, `StatusInfoInterface` | `NewExtraStatusInfoPane` → `ExtraStatusInfoPane` → `Pane` |
| `NewInventoryPane<SkillInvItemPane>` | `Pane` | `NewInventoryPane<SkillInvItemPane>` → `Pane` |
| `NewInventoryPane<SpellInvItemPane>` | `Pane` | `NewInventoryPane<SpellInvItemPane>` → `Pane` |
| `NewLegendDialogPane` | `DialogPane`, `LegendInterface` | `NewLegendDialogPane` → `DialogPane` → `Pane` |
| `NewMailDialog` | `BulletinDialogPane` | `NewMailDialog` → `BulletinDialogPane` → `DialogPane` → `Pane` |
| `NewPatchPane` | `Pane` | `NewPatchPane` → `Pane` |
| `NewSkillInventoryPane` | `NewInventoryPane<SkillInvItemPane>` | `NewSkillInventoryPane` → `NewInventoryPane<SkillInvItemPane>` → `Pane` |
| `NewSpellInventoryPane` | `NewInventoryPane<SpellInvItemPane>` | `NewSpellInventoryPane` → `NewInventoryPane<SpellInvItemPane>` → `Pane` |
| `NewStatusInfoPane` | `StatusInfoPane`, `StatusInfoInterface` | `NewStatusInfoPane` → `StatusInfoPane` → `Pane` |
| `NewSystemMessagePane` | `Pane` | `NewSystemMessagePane` → `Pane` |
| `NewSystemMessageTextPane` | `TextEditPane` | `NewSystemMessageTextPane` → `TextEditPane` → `ScrollablePane` → `Pane` |
| `NewWorldMapInfoPane` | `SessionLayeredTabPane` | `NewWorldMapInfoPane` → `SessionLayeredTabPane` → `LayeredTabPane` → `TabPane<LayeredImage>` → `DialogPane` → `Pane` |
| `NexonClubAuthAlertPane` | `AlertPane`, `Singleton<NexonClubAuthAlertPane>` | `NexonClubAuthAlertPane` → `AlertPane` → `DialogPane` → `Pane` |
| `NexonclubDialog` | `MessageDialogBase` | `NexonclubDialog` → `MessageDialogBase` → `DialogPane` → `Pane` |
| `NoNexonClubIDWarningPane` | `AlertPane` | `NoNexonClubIDWarningPane` → `AlertPane` → `DialogPane` → `Pane` |
| `NPC_Merchant_MessageDialog` | `NPCMessageDialog` | `NPC_Merchant_MessageDialog` → `NPCMessageDialog` → `DialogPane` → `Pane` |
| `NPC_Pursuit_MessageDialog` | `NPCMessageDialog` | `NPC_Pursuit_MessageDialog` → `NPCMessageDialog` → `DialogPane` → `Pane` |
| `NPC_Pursuit_NexonIdDialog` | `NPCMenuDialog` | `NPC_Pursuit_NexonIdDialog` → `NPCMenuDialog` → `DialogPane` → `Pane` |
| `NPC_Pursuit_TextInputMenuDialog` | `NPCMenuDialog` | `NPC_Pursuit_TextInputMenuDialog` → `NPCMenuDialog` → `DialogPane` → `Pane` |
| `NPCIllustPane` | `Pane` | `NPCIllustPane` → `Pane` |
| `NPCListMenuDialog` | `NPCMenuDialog` | `NPCListMenuDialog` → `NPCMenuDialog` → `DialogPane` → `Pane` |
| `NPCListMenuPane` | `ListPane` | `NPCListMenuPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `NPCMenuDialog` | `DialogPane` | `NPCMenuDialog` → `DialogPane` → `Pane` |
| `NPCMessageDialog` | `DialogPane` | `NPCMessageDialog` → `DialogPane` → `Pane` |
| `NPCServerItemMenuDialog` | `NPCMenuDialog` | `NPCServerItemMenuDialog` → `NPCMenuDialog` → `DialogPane` → `Pane` |
| `NPCSession` | `Pane` | `NPCSession` → `Pane` |
| `NPCTextInputMenuDialog` | `NPCMenuDialog` | `NPCTextInputMenuDialog` → `NPCMenuDialog` → `DialogPane` → `Pane` |
| `NPCTextMenuDialog` | `NPCMenuDialog` | `NPCTextMenuDialog` → `NPCMenuDialog` → `DialogPane` → `Pane` |
| `NPCTilePane` | `Pane` | `NPCTilePane` → `Pane` |
| `nui_AlbumPane` | `DialogPane` | `nui_AlbumPane` → `DialogPane` → `Pane` |
| `nui_ElemListPane` | `ListPane` | `nui_ElemListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `nui_EventPane` | `DialogPane` | `nui_EventPane` → `DialogPane` → `Pane` |
| `nui_EventPaneImpl` | `nui_EventPane` | `nui_EventPaneImpl` → `nui_EventPane` → `DialogPane` → `Pane` |
| `nui_FamilyPane` | `DialogPane` | `nui_FamilyPane` → `DialogPane` → `Pane` |
| `nui_IntroPane` | `DialogPane` | `nui_IntroPane` → `DialogPane` → `Pane` |
| `nui_LegendPane` | `DialogPane`, `LegendInterface` | `nui_LegendPane` → `DialogPane` → `Pane` |
| `nui_SkillSpellPane` | `DialogPane` | `nui_SkillSpellPane` → `DialogPane` → `Pane` |
| `NumberArgsSpellInputPane` | `ArgsLineInputPane` | `NumberArgsSpellInputPane` → `ArgsLineInputPane` → `LineInputPane` → `Pane` |
| `NumLineInputPane` | `LineInputPane` | `NumLineInputPane` → `LineInputPane` → `Pane` |
| `OptionPane` | `DialogPane` | `OptionPane` → `DialogPane` → `Pane` |
| `Pane` | `Canvas`, `TimerHandler` | `Pane` |
| `PopupMenuPane` | `Pane`, `Singleton<PopupMenuPane>` | `PopupMenuPane` → `Pane` |
| `PortraitControlPane` | `ControlPane` | `PortraitControlPane` → `ControlPane` → `Pane` |
| `PortraitTextInputDialogPane` | `DialogPane` | `PortraitTextInputDialogPane` → `DialogPane` → `Pane` |
| `ProgressBarControlPane` | `ControlPane` | `ProgressBarControlPane` → `ControlPane` → `Pane` |
| `ProgressBarControlPaneEx` | `ControlPane` | `ProgressBarControlPaneEx` → `ControlPane` → `Pane` |
| `Puzzle::BalloonPane` | `Pane` | `Puzzle::BalloonPane` → `Pane` |
| `Puzzle::GameControlPane` | `MiniGame::AbstractGameControlPane` | `Puzzle::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `Puzzle::HelpPane` | `Puzzle::GameControlPane` | `Puzzle::HelpPane` → `Puzzle::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `Puzzle::ImageCutPane` | `Pane` | `Puzzle::ImageCutPane` → `Pane` |
| `Puzzle::LevelPane` | `Pane` | `Puzzle::LevelPane` → `Pane` |
| `Puzzle::PlayPane` | `Puzzle::GameControlPane` | `Puzzle::PlayPane` → `Puzzle::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `Puzzle::PuzzlePane` | `Pane` | `Puzzle::PuzzlePane` → `Pane` |
| `Puzzle::PuzzlePane::Tile` | `Puzzle::TilePane` | `Puzzle::PuzzlePane::Tile` → `Puzzle::TilePane` → `Puzzle::ImageCutPane` → `Pane` |
| `Puzzle::RankingPane` | `Puzzle::GameControlPane` | `Puzzle::RankingPane` → `Puzzle::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `Puzzle::ResultPane` | `Puzzle::GameControlPane` | `Puzzle::ResultPane` → `Puzzle::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `Puzzle::SendResultPane` | `Puzzle::GameControlPane` | `Puzzle::SendResultPane` → `Puzzle::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `Puzzle::SettingPane` | `Puzzle::GameControlPane` | `Puzzle::SettingPane` → `Puzzle::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `Puzzle::TilePane` | `Puzzle::ImageCutPane` | `Puzzle::TilePane` → `Puzzle::ImageCutPane` → `Pane` |
| `Puzzle::TimePane` | `Pane` | `Puzzle::TimePane` → `Pane` |
| `Puzzle::TitlePane` | `Puzzle::GameControlPane` | `Puzzle::TitlePane` → `Puzzle::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `QuantityInputDialogPane` | `DialogPane` | `QuantityInputDialogPane` → `DialogPane` → `Pane` |
| `QuestionMessageDialog` | `MessageDialogBase` | `QuestionMessageDialog` → `MessageDialogBase` → `DialogPane` → `Pane` |
| `QuestionMessageFaceDialog` | `MessageDialogBase` | `QuestionMessageFaceDialog` → `MessageDialogBase` → `DialogPane` → `Pane` |
| `RadioGroupControlPane` | `ControlPane` | `RadioGroupControlPane` → `ControlPane` → `Pane` |
| `ReconnectDialogPane` | `AlertPane` | `ReconnectDialogPane` → `AlertPane` → `DialogPane` → `Pane` |
| `RopeSkipping::CountdownPane` | `Pane` | `RopeSkipping::CountdownPane` → `Pane` |
| `RopeSkipping::GameControlPane` | `MiniGame::AbstractGameControlPane` | `RopeSkipping::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `RopeSkipping::GameoverPane` | `Pane` | `RopeSkipping::GameoverPane` → `Pane` |
| `RopeSkipping::GradePane` | `Pane` | `RopeSkipping::GradePane` → `Pane` |
| `RopeSkipping::HelpPane` | `RopeSkipping::GameControlPane` | `RopeSkipping::HelpPane` → `RopeSkipping::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `RopeSkipping::PlayPane` | `RopeSkipping::GameControlPane` | `RopeSkipping::PlayPane` → `RopeSkipping::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `RopeSkipping::RankingPane` | `RopeSkipping::GameControlPane` | `RopeSkipping::RankingPane` → `RopeSkipping::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `RopeSkipping::ResultPane` | `RopeSkipping::GameControlPane` | `RopeSkipping::ResultPane` → `RopeSkipping::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `RopeSkipping::SkipCountPane` | `Pane` | `RopeSkipping::SkipCountPane` → `Pane` |
| `RopeSkipping::TitlePane` | `RopeSkipping::GameControlPane` | `RopeSkipping::TitlePane` → `RopeSkipping::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `SafeQuitAlert` | `AlertPane` | `SafeQuitAlert` → `AlertPane` → `DialogPane` → `Pane` |
| `ScorePane` | `Pane`, `Singleton<ScorePane>` | `ScorePane` → `Pane` |
| `ScreenDimmer` | `Pane` | `ScreenDimmer` → `Pane` |
| `ScreenPane` | `Pane` | `ScreenPane` → `Pane` |
| `ScrollableControlPane` | `ControlPane` | `ScrollableControlPane` → `ControlPane` → `Pane` |
| `ScrollablePane` | `Pane` | `ScrollablePane` → `Pane` |
| `ScrollPane` | `Pane` | `ScrollPane` → `Pane` |
| `ServerItemMenuDialog` | `TaskListDialog` | `ServerItemMenuDialog` → `TaskListDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `ServerItemMenuDialog2` | `TaskListDialog` | `ServerItemMenuDialog2` → `TaskListDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `ServerItemMenuDialog3` | `TaskListDialog` | `ServerItemMenuDialog3` → `TaskListDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `ServerSelectDialogPane` | `DialogPane` | `ServerSelectDialogPane` → `DialogPane` → `Pane` |
| `ServerSkillMenuDialog` | `TaskListDialog` | `ServerSkillMenuDialog` → `TaskListDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `ServerSpellMenuDialog` | `TaskListDialog` | `ServerSpellMenuDialog` → `TaskListDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `SessionLayeredTabPane` | `LayeredTabPane` | `SessionLayeredTabPane` → `LayeredTabPane` → `TabPane<LayeredImage>` → `DialogPane` → `Pane` |
| `ShowUsersListPane` | `ListPane` | `ShowUsersListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `ShowUsersPane` | `ShowUsersPane_A`, `Singleton<ShowUsersPane>` | `ShowUsersPane` → `ShowUsersPane_A` → `DialogPane` → `Pane` |
| `ShowUsersPane_A` | `DialogPane` | `ShowUsersPane_A` → `DialogPane` → `Pane` |
| `SimpleMessageDialog` | `MessageDialog` | `SimpleMessageDialog` → `MessageDialog` → `MessageDialogBase` → `DialogPane` → `Pane` |
| `SimpleQuestionMessageDialog` | `MessageDialogBase` | `SimpleQuestionMessageDialog` → `MessageDialogBase` → `DialogPane` → `Pane` |
| `SimpleTextMessageDialog` | `MessageDialogBase` | `SimpleTextMessageDialog` → `MessageDialogBase` → `DialogPane` → `Pane` |
| `SkillbookDialog` | `DialogPane` | `SkillbookDialog` → `DialogPane` → `Pane` |
| `SkillInvItemPane` | `Pane` | `SkillInvItemPane` → `Pane` |
| `SkillSpellInfoDialogPane` | `DialogPane` | `SkillSpellInfoDialogPane` → `DialogPane` → `Pane` |
| `SkillSpellInventoryPane` | `Pane` | `SkillSpellInventoryPane` → `Pane` |
| `SkillSpellListPane` | `nui_ElemListPane` | `SkillSpellListPane` → `nui_ElemListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `SnowParticle_::SnowParticlePane` | `ImagePane` | `SnowParticle_::SnowParticlePane` → `ImagePane` → `Pane` |
| `SpellbookDialog` | `DialogPane` | `SpellbookDialog` → `DialogPane` → `Pane` |
| `SpellDelayControlPane` | `Pane`, `Singleton<SpellDelayControlPane>` | `SpellDelayControlPane` → `Pane` |
| `SpelledViewPane_A` | `Pane` | `SpelledViewPane_A` → `Pane` |
| `SpellInvItemPane` | `Pane` | `SpellInvItemPane` → `Pane` |
| `SpellSkillInfoPane` | `SessionLayeredTabPane` | `SpellSkillInfoPane` → `SessionLayeredTabPane` → `LayeredTabPane` → `TabPane<LayeredImage>` → `DialogPane` → `Pane` |
| `SpellSkillPropertyPane` | `DialogPane` | `SpellSkillPropertyPane` → `DialogPane` → `Pane` |
| `SpellSkillViewPane` | `Pane` | `SpellSkillViewPane` → `Pane` |
| `StackNiye::GameControlPane` | `MiniGame::AbstractGameControlPane` | `StackNiye::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `StackNiye::PlayPane` | `StackNiye::GameControlPane` | `StackNiye::PlayPane` → `StackNiye::GameControlPane` → `MiniGame::AbstractGameControlPane` → `ControlPane` → `Pane` |
| `StaffPane` | `Pane` | `StaffPane` → `Pane` |
| `StaticTextControlPane` | `TextEditControlPane` | `StaticTextControlPane` → `TextEditControlPane` → `ControlPane` → `Pane` |
| `StaticTextControlPane2` | `TextEditControlPane` | `StaticTextControlPane2` → `TextEditControlPane` → `ControlPane` → `Pane` |
| `StatusInfoPane` | `Pane`, `StatusInfo`, `Singleton<StatusInfoPane>` | `StatusInfoPane` → `Pane` |
| `StringListPane` | `ListPane` | `StringListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `StringSpellInputPane` | `LineInputPane` | `StringSpellInputPane` → `LineInputPane` → `Pane` |
| `SystemButtonsPane` | `Pane` | `SystemButtonsPane` → `Pane` |
| `TabButtonPane` | `Pane` | `TabButtonPane` → `Pane` |
| `TabPane<LayeredImage>` | `DialogPane` | `TabPane<LayeredImage>` → `DialogPane` → `Pane` |
| `TaskListDialog` | `MerchantDialogPane` | `TaskListDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `TaskListPane` | `ListPane` | `TaskListPane` → `ListPane` → `ScrollablePane` → `Pane` |
| `TellInputPane` | `LineInputPane` | `TellInputPane` → `LineInputPane` → `Pane` |
| `TellReceiverInputPane` | `LineInputPane` | `TellReceiverInputPane` → `LineInputPane` → `Pane` |
| `TerminalPane2` | `Pane`, `Singleton<TerminalPane2>` | `TerminalPane2` → `Pane` |
| `TextBoxPane` | `TextEditPane` | `TextBoxPane` → `TextEditPane` → `ScrollablePane` → `Pane` |
| `TextButtonControlPane` | `ButtonControlPane` | `TextButtonControlPane` → `ButtonControlPane` → `ControlPane` → `Pane` |
| `TextButtonExControlPane` | `ButtonControlPane` | `TextButtonExControlPane` → `ButtonControlPane` → `ControlPane` → `Pane` |
| `TextEditControlPane` | `ControlPane` | `TextEditControlPane` → `ControlPane` → `Pane` |
| `TextEditPane` | `ScrollablePane` | `TextEditPane` → `ScrollablePane` → `Pane` |
| `TextFieldMapPointPane` | `FieldMapPointPane` | `TextFieldMapPointPane` → `FieldMapPointPane` → `Pane` |
| `TextInputMenuDialog` | `MerchantDialogPane` | `TextInputMenuDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `TextLinePane` | `TextEditPane` | `TextLinePane` → `TextEditPane` → `ScrollablePane` → `Pane` |
| `TextMenuDialog` | `TaskListDialog` | `TextMenuDialog` → `TaskListDialog` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `TextMenuDialogEx` | `MerchantDialogPane` | `TextMenuDialogEx` → `MerchantDialogPane` → `DialogPane` → `Pane` |
| `TextMessageDialog` | `MessageDialogBase` | `TextMessageDialog` → `MessageDialogBase` → `DialogPane` → `Pane` |
| `ToolTipPane` | `Pane`, `Singleton<ToolTipPane>` | `ToolTipPane` → `Pane` |
| `TownInfoPane` | `DialogPane` | `TownInfoPane` → `DialogPane` → `Pane` |
| `TownMapPane` | `Pane`, `Singleton<TownMapPane>` | `TownMapPane` → `Pane` |
| `TransferReplyAlert` | `AlertPane` | `TransferReplyAlert` → `AlertPane` → `DialogPane` → `Pane` |
| `TransferServerProgress` | `Pane`, `Singleton<TransferServerProgress>` | `TransferServerProgress` → `Pane` |
| `UnitelPane` | `Pane`, `Singleton<UnitelPane>` | `UnitelPane` → `Pane` |
| `UrlAlertPane` | `AlertPane` | `UrlAlertPane` → `AlertPane` → `DialogPane` → `Pane` |
| `UserConfirmPane` | `AlertPane` | `UserConfirmPane` → `AlertPane` → `DialogPane` → `Pane` |
| `UserInfoPane` | `Pane` | `UserInfoPane` → `Pane` |
| `UserInfoPane_ForOthers` | `UserInfoPane`, `Singleton<UserInfoPane_ForOthers>` | `UserInfoPane_ForOthers` → `UserInfoPane` → `Pane` |
| `UserInfoPane_ForUser` | `UserInfoPane`, `Singleton<UserInfoPane_ForUser>` | `UserInfoPane_ForUser` → `UserInfoPane` → `Pane` |
| `UserInfoTabPane` | `Pane` | `UserInfoTabPane` → `Pane` |
| `UserLookPane` | `DialogPane`, `Singleton<UserLookPane>` | `UserLookPane` → `DialogPane` → `Pane` |
| `UserShapeControlPane` | `ControlPane` | `UserShapeControlPane` → `ControlPane` → `Pane` |
| `VirusAlertPane` | `AlertPane` | `VirusAlertPane` → `AlertPane` → `DialogPane` → `Pane` |
| `WindowMessageDialogPane` | `DialogPane` | `WindowMessageDialogPane` → `DialogPane` → `Pane` |
| `World::BalloonPane` | `Pane`, `zz::_RefCnt` | `World::BalloonPane` → `Pane` |
| `WorldBackFixedImage` | `WorldBackImage` | `WorldBackFixedImage` → `WorldBackImage` → `Pane` |
| `WorldBackGradation` | `WorldBackImage` | `WorldBackGradation` → `WorldBackImage` → `Pane` |
| `WorldBackImage` | `Pane` | `WorldBackImage` → `Pane` |
| `WorldBackPattern` | `WorldBackImage` | `WorldBackPattern` → `WorldBackImage` → `Pane` |
| `WorldControllerPane` | `Pane` | `WorldControllerPane` → `Pane` |
| `WorldMapImagePane` | `Pane` | `WorldMapImagePane` → `Pane` |
| `WorldMapInfo_DA_Pane` | `WorldMapInfoPane` | `WorldMapInfo_DA_Pane` → `WorldMapInfoPane` → `Pane` |
| `WorldMapInfo_Normal_Pane` | `WorldMapInfoPane` | `WorldMapInfo_Normal_Pane` → `WorldMapInfoPane` → `Pane` |
| `WorldMapInfoPane` | `Pane` | `WorldMapInfoPane` → `Pane` |
| `WorldMinimapPane_Impl` | `Pane`, `WorldMinimapInterface` | `WorldMinimapPane_Impl` → `Pane` |
| `WorldObject_Name_Pane` | `Pane`, `zz::_RefCnt` | `WorldObject_Name_Pane` → `Pane` |
| `WorldPane` | `WorldControllerPane`, `WorldPane_MiscPacketProcessor`, `Singleton<WorldPane>` | `WorldPane` → `WorldControllerPane` → `Pane` |
| `WorldPane_Impl` | `WorldPane`, `MapInterface`, `MapUserInterface`, `Singleton<WorldPane_Impl>` | `WorldPane_Impl` → `WorldPane` → `WorldControllerPane` → `Pane` |
| `YesNoAlertPane` | `AlertPane` | `YesNoAlertPane` → `AlertPane` → `DialogPane` → `Pane` |

## Scope and evidence

This is a static class inventory, not a list of panes alive at runtime. Names are exact MSVC RTTI type names. Inheritance is decoded from RTTI hierarchy records rather than inferred from a class name, namespace, constructor similarity, or vtable shape.

The deterministic source manifest is [`analysis/exports/ui-pane-types.yaml`](../../analysis/exports/ui-pane-types.yaml).
