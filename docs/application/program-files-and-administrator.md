# Program Files and administrator mode

Dark Ages does not need administrator rights for its normal registry settings. The problem is where it stores files and how it starts its patcher.

The client treats its installation directory as both a program folder and a save-data folder. That worked on older, loosely protected installations. A normal process cannot write there when the game is under `Program Files`.

Running the whole client as administrator hides these problems, but it gives old game and network code far more access than it needs.

## The short answer

Two choices in this client cause the trouble:

1. `app_set_working_directory_from_executable` changes the process working directory to the folder containing `Darkages.exe`.
2. Most mutable paths are relative, so settings, character files, crash reports, and patch handoff files are written under that folder.

`C:\Dark Ages` works when its folder permissions allow the current user to write. `C:\Program Files\Dark Ages` does not because `Program Files` is meant for installed program files that ordinary users can read but cannot change.

Microsoft has enforced this model since Windows Vista. It is not a new Windows 10 or Windows 11 rule. See [User Account Control for game developers](https://learn.microsoft.com/en-us/windows/win32/dxtecharts/user-account-control-for-game-developers).

## What the client writes

The exact set depends on the action being performed.

| Action | Relative output |
| --- | --- |
| Missing or rejected installation settings | `Darkages.cfg` |
| Changing client-owned options | `Darkages.cfg` |
| Entering or leaving a character | Character directory and its `.cfg` files |
| Editing a profile | Character `profile.txt` |
| Editing spell or skill lines | Character file plus `tmp.cfg` |
| Unhandled crash | `LCrash.nfo` |
| Starting an update | `Patch/Info` |
| Recovering an incomplete update | Delete `Patch/Info` and `Patch/Script` |

These writes do not all happen during every launch. For example, `app_config_ctor` saves `Darkages.cfg` during startup only when `app_load_config_file` fails. Later option changes call `app_save_config` again.

The common problem is that every relative path begins under the executable directory.

## Why VirtualStore does not help

`Darkages.exe` is a 32-bit application, but it is not treated as an unmarked legacy program. Its embedded manifest says:

```xml
<requestedExecutionLevel level="asInvoker" uiAccess="false">
```

`asInvoker` is the correct level for the game itself. It means the game uses the same normal user rights as its launcher.

The same manifest entry also disables Windows file and registry virtualization. Windows therefore does not redirect failed `Program Files` writes into the user's `VirtualStore`. It returns an access error instead. Microsoft documents this behavior under [application manifests](https://learn.microsoft.com/en-us/windows/win32/sbscs/application-manifests).

Removing the manifest to bring back VirtualStore would not be a good fix. It would split files between the real installation and a hidden per-user copy. The patcher and the game could then see different versions.

## The patcher creates the administrator message

The update path explains where the community advice came from.

When the server sends the update form of `SVersionCheck`, `app_write_patch_info_and_launch_patcher` does this:

```text
create Patch directory
write Patch/Info
start Patcher2.exe with CreateProcessA
exit Darkages.exe
```

Failure has two visible forms:

- If `Patch/Info` cannot be created, the client shows `Cannot access file` and exits.
- If `CreateProcessA` cannot start the patcher, the client tells the player to run the Dark Ages shortcut as administrator.

The matching `Patcher2.exe` requests `highestAvailable` in its own manifest. For a user in the Administrators group, Windows treats that like an administrator request.

The non-elevated game starts it with `CreateProcessA`. That function cannot show a UAC prompt for a child that needs a higher level. Windows rejects the call with `ERROR_ELEVATION_REQUIRED`. Microsoft describes this exact rule in its [UAC game guidance](https://learn.microsoft.com/en-us/windows/win32/dxtecharts/user-account-control-for-game-developers#uac-implications-with-createprocess).

The client catches the failure, but its only recovery message is to elevate the whole game.

The `Patcher2.exe` manifest was checked in the matching private installation:

```text
Size: 802,816 bytes
SHA-256: C119ECF8CD5ACCB4A575156D00EC00867F230B5A27EF4385DF714D88A467F632
requestedExecutionLevel: highestAvailable
```

The patcher's internal update flow remains supporting evidence rather than part of the version 741 client analysis.

## The registry is not the blocker

`app_winmain` stores `DisplayMode` under:

```text
HKEY_CURRENT_USER\Software\KRU\Dark Ages
```

That is per-user state and does not need administrator rights.

The default endpoint setup also tries to keep old installation IDs under two `HKEY_CLASSES_ROOT` keys. It asks for broad registry access, which can fail for a normal user. That failure does not stop startup. The client substitutes a fixed value, derives an in-memory ID, and continues.

No registry failure in these paths produces the administrator message. The message belongs to the failed `Patcher2.exe` launch.

## Why it may seem newer than it is

The protected-folder rule and UAC process levels began with Windows Vista. The exact client and patcher manifests also declare their intended levels explicitly.

The earlier experience could have differed for several reasons:

- an older client or patcher had a different manifest;
- the old installer granted users write access to the game folder;
- the game was installed outside `Program Files`;
- an older shortcut or launcher was already elevated;
- no update was pending, so the patcher path was not reached;
- an unmarked older executable received VirtualStore compatibility.

Those are possible explanations, not confirmed history. Proving which one changed requires the older installer and executable that showed the different behavior.

## Safe fix for the unchanged client

Install the complete client in a per-user program directory, for example:

```text
%LOCALAPPDATA%\Programs\Dark Ages
```

Then run `Darkages.exe` normally.

This preserves the client's assumption that program files and writable data share one directory. It also lets the old patch handoff work without giving the game administrator rights.

`C:\Dark Ages` works for the same reason when its access rules allow the player to write. A per-user directory is clearer and does not make a machine-wide folder writable.

Do not grant all users write access to a game directory under `Program Files`. An unprivileged process could replace game code or a DLL that is later loaded by an elevated patcher or client.

## Proper Program Files design

A modern installation should separate program files from user data:

```text
Program Files
  Dark Ages binaries and read-only assets

LocalAppData
  Darkages.cfg
  character directories
  profiles
  crash reports
  downloaded patch handoff
```

The game should remain `asInvoker`. Only a small updater helper should request elevation when it is ready to replace files under `Program Files`.

```c
void start_game(void)
{
    data_root = get_local_app_data_path("Dark Ages");
    load_assets_from(install_root);
    load_user_files_from(data_root);
}

void apply_update(void)
{
    download_and_verify_update(data_root);
    shell_execute_as_admin(updater_path, verified_update_path);
}
```

Microsoft recommends keeping the main application at normal user rights and separating elevated work into a helper. See [Running with administrator privileges](https://learn.microsoft.com/en-us/windows/win32/secbp/running-with-administrator-privileges).

The helper should accept only a verified update description, reject paths outside the installation root, replace only expected files, and exit. The game should never stay elevated during normal play.

## Why one launch patch is not enough

Replacing the `CreateProcessA` call with `ShellExecuteA("runas")` would let Windows show a UAC prompt for `Patcher2.exe`. It would not solve the complete problem:

- the game must create `Patch/Info` before that call;
- configuration and character files would still be under `Program Files`;
- crash-report and temporary-file writes would still fail.

A complete runtime extension would need to redirect every mutable path or move the whole working installation into a per-user directory. For the unchanged client, a per-user installation is the smaller and safer solution.

## Security reason not to elevate the game

The client contains old code that can try to create `%SystemRoot%\System32\Mscfg.dll` after a server message. As a normal user, that write is blocked. Running the whole client as administrator gives that network-driven path permission to modify a system directory.

This is another reason to keep normal play at `asInvoker` and elevate only a narrow, short-lived updater.

Addresses and evidence for the named client functions are kept in the [function reference](../appendix/functions.md).
