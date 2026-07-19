# UI layout registry

This registry maps confirmed text layouts in `setoa.dat` to the pane classes that load them. Class names come from Microsoft C++ RTTI at the loading call site. The control count comes from the matching local archive.

An unresolved row means the asset exists but no matching filename reference was found in the client. It does not prove that the file is unused because a name could still be built at runtime.

| Layout file | Controls | Loading pane class or classes |
| --- | ---: | --- |
| `_nagree.txt` | 5 | `AgreementDialogPane` |
| `_narlist.txt` | 9 | `ArticleListDialog` |
| `_narti.txt` | 11 | `ArticleDialog` |
| `_nartin.txt` | 6 | `NewArticleDialog` |
| `_nbdlist.txt` | 4 | `BoardListDialog` |
| `_nbk_l.txt` | 47 | `GUIBackPane` |
| `_nbk_s.txt` | 49 | `GUIBackPane` |
| `_nbworld.txt` | 17 | Unresolved |
| `_ncreate.txt` | 19 | `CreateUserDialogPane` |
| `_nexch.txt` | 10 | `ExchangeDialog` |
| `_nfriend.txt` | 6 | `FriendListDialog` |
| `_ngcdlg0.txt` | 5 | `GroupListPane` |
| `_ngcdlg1.txt` | 15 | `GroupAdDialogPane` |
| `_ngcmain.txt` | 6 | `ExGroupViewPane` |
| `_nhotkem.txt` | 3 | `HotKeyPane` |
| `_nhotkey.txt` | 16 | `HotKeyPane` |
| `_nload.txt` | 4 | `LoadUsersPane`, `TransferServerProgress` |
| `_nloadm.txt` | 4 | `MapLoadingPane` |
| `_nlogin.txt` | 5 | `LoginDialogPane` |
| `_nmacro.txt` | 5 | `MacroDialog` |
| `_nmaill.txt` | 8 | `MailListDialog` |
| `_nmailr.txt` | 12 | `MailDialog` |
| `_nmails.txt` | 7 | `NewMailDialog` |
| `_nmoney.txt` | 5 | `DropGoldDialogPane`, `GiveGoldDialogPane` |
| `_noptdlg.txt` | 9 | `OptionPane`, `GUIOptionPane` |
| `_npw.txt` | 7 | `ChangePasswordDialogPane` |
| `_npw2.txt` | 4 | `InputBirthdateDialogPane` |
| `_nsett.txt` | 7 | `GameSettingDialog` |
| `_nstart.txt` | 10 | `MainMenuPane` |
| `_nstatur.txt` | 17 | `GUIBackPane` |
| `_nstatus.txt` | 28 | `GUIBackPane` |
| `_nsvr.txt` | 8 | `ServerSelectDialogPane` |
| `_nui.txt` | 10 | `UserInfoPane` |
| `_nui_al.txt` | 8 | `nui_AlbumPane` |
| `_nui_alb.txt` | 6 | `AlbumPicDialogPane` |
| `_nui_dr.txt` | 3 | `nui_LegendPane` |
| `_nui_eq.txt` | 39 | `nui_IntroPane` |
| `_nui_eqa.txt` | 33 | `nui_IntroPane` |
| `_nui_ev.txt` | 5 | `nui_EventPaneImpl` |
| `_nui_eve.txt` | 7 | `EventInfoDialogPane` |
| `_nui_fm.txt` | 13 | `nui_FamilyPane` |
| `_nui_pi.txt` | 4 | `PortraitTextInputDialogPane` |
| `_nui_sk.txt` | 3 | `nui_SkillSpellPane` |
| `_nui_ske.txt` | 12 | `SkillSpellInfoDialogPane` |
| `_nui_ski.txt` | 5 | `nui_ElemListPane` |
| `_nusers.txt` | 9 | `ShowUsersPane_A` |
| `lnpcd.txt` | 13 | `NPCMessageDialog` |
| `lnpcd2.txt` | 9 | `NPCMenuDialog` |
| `lnpcd3.txt` | 18 | `NPCServerItemMenuDialog` |
| `lnpcd4.txt` | 6 | `NPC_Pursuit_TextInputMenuDialog` |
| `lnpcnid.txt` | 10 | `NPC_Pursuit_NexonIdDialog` |
| `lpopup.txt` | 5 | `PopupMenuPane` |

The full pane inheritance inventory remains in [Pane types and inheritance](pane-types.md). See [UI layout files](../systems/ui-layouts.md) for the text grammar and callback model.
