# Declarative UI layout files

The active version-741 layouts are text entries in `setoa.dat`. They describe named controls, rectangles, images, values, and colors. The parser does not accept callback names, scripts, parent references, anchors, or layout expressions.

## Active underscore namespace

`setoa.dat` contains 732 entries. Of those, 199 begin with `_`, including 46 `_n*.txt` layout files and their associated EPF or SPF artwork. The executable directly references the `_n*.txt` set.

The same archive also retains older `l*.txt` layouts such as `llogin.txt`, `lcreate.txt`, and `lmain.txt`. No version-741 code reference was found for those old names. The strongest local interpretation is that the underscore `_n` namespace is the active newer UI set and the `l*.txt` files are legacy archive residue. The exact original meaning of `n` is not proven.

`national.dat` also contains underscore-prefixed resources, mostly SPF artwork plus `_tcoord.txt` and `_tncoord.txt`. Those are a separate resource namespace and should not be assumed to use the GUI layout grammar.

## Grammar

`ui_layout_parse_control_block` at `0x4A81F0` accepts exactly these tags:

| Tag | Value | Repeats |
|---|---|---:|
| `<CONTROL>` | Begins one control definition | no |
| `<NAME>` | Quoted lookup name | no |
| `<TYPE>` | Integer control category | no |
| `<RECT>` | Four integers: left, top, right, bottom | no |
| `<IMAGE>` | Quoted archive entry name followed by a frame number | yes |
| `<VALUE>` | Integer preset or control value | yes |
| `<COLOR>` | Integer color value | yes |
| `<ENDCONTROL>` | Ends the definition | no |

An era-appropriate representation is:

```c
struct ui_layout_image {
    char archive_entry[256];
    int frame;
};

struct ui_control_definition {
    char name[128];
    int type;
    int left;
    int top;
    int right;
    int bottom;
    ui_layout_image images[3];
    int image_count;
    int values[16];
    int value_count;
    int colors[16];
    int color_count;
};
```

The array sizes above are descriptive, not recovered object bounds. The client uses its own dynamic containers.

A reduced example based on the login layout is:

```text
<CONTROL>
  <NAME> "OK"
  <TYPE> 7
  <RECT> 28 130 90 150
  <IMAGE> "menubtn.epf" 0
          "menubtn.epf" 1
<ENDCONTROL>
```

Repeated `IMAGE` lines provide visual states. A filename beginning with `-` is treated as no image. The shipped layouts use `-DUMMY-` for this purpose.

## Parse and cache flow

`ui_layout_load_from_archive` at `0x482340` performs this sequence:

```c
layout *load_layout(const char *entry_name, fastfile *archive)
{
    layout *result;
    fastfile_entry *entry;
    parser input;
    control_definition control;

    if (archive == 0)
        archive = default_ui_archive();

    result = layout_cache_lookup(entry_name, archive);
    if (result != 0)
        return result;

    entry = fastfile_open_entry(archive, entry_name);
    if (entry == 0)
        throw_invalid_gui_data(entry_name);

    parser_from_memory(&input, entry->data, entry->size);
    result = new_layout("temp");

    while (parse_control_block(&input, &control))
        layout_add_control(result, &control);

    fastfile_close_entry(entry);
    layout_cache_store(entry_name, archive, result);
    return result;
}
```

Relevant functions:

| Function | Address | Role |
|---|---:|---|
| `ui_layout_cache_lookup` | `0x481CE0` | Finds a parsed layout by archive and entry name |
| `ui_layout_cache_store` | `0x481E60` | Stores a parsed layout |
| `ui_layout_select_control` | `0x482140` | Selects a definition by `<NAME>` and throws if absent |
| `ui_layout_get_control_rect` | `0x482630` | Copies the selected rectangle |
| `ui_layout_get_image_entry` | `0x4826E0` | Reads one indexed image and frame |
| `ui_layout_get_value_entry` | `0x482870` | Reads one indexed value |
| `ui_layout_build_image_button_spec` | `0x4828E0` | Resolves a preset or up to three explicit images |
| `ui_layout_create_image_button` | `0x4832E0` | Constructs an `ImageButtonControlPane` |

## Observed TYPE values

Across all 130 text layouts in `setoa.dat`, the parser sees 1,245 control definitions:

| TYPE | Count | Current interpretation |
|---:|---:|---|
| `0` | 120 | Root or container definition in confirmed active layouts |
| `3` | 112 | Older standard control definition, often paired with `VALUE` |
| `5` | 15 | Specialized control category, exact factory mapping not yet confirmed |
| `6` | 11 | Specialized control category, exact factory mapping not yet confirmed |
| `7` | 987 | Named geometry or image definition used heavily by the active `_n` layouts |

`TYPE` is not enough to determine the final C++ class. Active layouts frequently use type 7 for buttons, text fields, labels, and specialized panes. The owning constructor decides which concrete class to instantiate for a control name.

## Archive entry catalog

These underscore-prefixed layout entries are present in `setoa.dat`. A code address means the executable directly references the entry from that function.

| Archive entry | Confirmed or likely role | Direct code use |
|---|---|---:|
| `_nagree.txt` | Account agreement | `ui_agreement_dialog_ctor` at `0x402430` |
| `_narlist.txt` | Article list | not yet traced |
| `_narti.txt` | Article view | not yet traced |
| `_nartin.txt` | Article input | not yet traced |
| `_nbdlist.txt` | Bulletin list | `ui_bulletin_dialog_ctor` at `0x41D8B0` |
| `_nbk_l.txt` | Large book view | not yet traced |
| `_nbk_s.txt` | Small book view | not yet traced |
| `_nbworld.txt` | Bulletin world view | no literal code reference found |
| `_ncreate.txt` | Character creation | `ui_create_user_dialog_ctor` at `0x43C370` |
| `_nexch.txt` | Exchange dialog | `0x469560` |
| `_nfriend.txt` | Friend list | `0x5435F0` |
| `_ngcdlg0.txt` | Game-club dialog variant 0 | `0x510B70` |
| `_ngcdlg1.txt` | Game-club dialog variant 1 | `0x511400` |
| `_ngcmain.txt` | Game-club main pane | `0x512A80` |
| `_nhotkem.txt` | Hot-key element layout | not yet traced |
| `_nhotkey.txt` | Hot-key configuration | `ui_hot_key_pane_ctor` at `0x488320` |
| `_nload.txt` | Loading pane | `0x496FE0` |
| `_nloadm.txt` | Loading pane variant | `0x55CC50`, `0x5914B0` |
| `_nlogin.txt` | Login dialog | `ui_login_dialog_ctor` at `0x4BA180` |
| `_nmacro.txt` | Macro configuration | `0x5413B0` |
| `_nmaill.txt` | Mail list | `0x422EE0` |
| `_nmailr.txt` | Mail reader | `0x424E00` |
| `_nmails.txt` | Mail sender | `0x426080` |
| `_nmoney.txt` | Money input dialog | not yet class-mapped |
| `_noptdlg.txt` | Options dialog | `0x53FF30`, `0x5A6B30` |
| `_npw.txt` | Password change | `ui_change_password_dialog_ctor` at `0x4BB2A0` |
| `_npw2.txt` | Password dialog variant | `0x4BC220` |
| `_nsett.txt` | Settings pane | `0x542370` |
| `_nstart.txt` | Startup main menu | `ui_main_menu_pane_ctor` at `0x4B6C70` |
| `_nstatur.txt` | Status sublayout | not yet traced |
| `_nstatus.txt` | User status and profile layouts | `0x4BE9A0`, `0x4C0850`, `0x59E7B0`, `0x59F320` |
| `_nsvr.txt` | Server selection | `0x5586F0`, `0x559650` |
| `_nui.txt` | Root in-game new UI geometry | `ui_build_main_layout_geometry` at `0x5AA880` |
| `_nui_al.txt` | Album pane | `ui_nui_album_pane_ctor` at `0x5B2A70` |
| `_nui_alb.txt` | Album sublayout | not yet traced |
| `_nui_dr.txt` | Legend pane | `ui_nui_legend_pane_ctor` at `0x5B7AA0` |
| `_nui_eq.txt` | Intro and equipment pane | `ui_nui_intro_pane_ctor` at `0x5B59F0` |
| `_nui_eqa.txt` | Intro and equipment auxiliary layout | `ui_nui_intro_pane_ctor` at `0x5B59F0` |
| `_nui_ev.txt` | Event pane | `ui_nui_event_pane_ctor` at `0x5B3EE0` |
| `_nui_eve.txt` | Event detail dialog | `ui_event_info_dialog_ctor` at `0x5AF460` |
| `_nui_fm.txt` | Family pane | `ui_nui_family_pane_ctor` at `0x5B4FB0` |
| `_nui_pi.txt` | Portrait text input | `ui_portrait_text_input_dialog_ctor` at `0x5B11A0` |
| `_nui_sk.txt` | Skill and spell pane | `ui_nui_skill_spell_pane_ctor` at `0x5B80C0` |
| `_nui_ske.txt` | Skill or spell detail dialog | `ui_skill_spell_info_dialog_ctor` at `0x5AE090` |
| `_nui_ski.txt` | Skill list item sublayout | `0x5B3930` |
| `_nusers.txt` | User list | `0x55B2B0` |

Several names above are behavioral readings of archive filenames. The class links in the [pane catalog](pane-classes.md) are stricter and only record relationships confirmed through RTTI, vtables, and constructor references.
