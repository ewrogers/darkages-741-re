# Getting Started

The repository keeps the private client, the local Binary Ninja database, and the reviewable project record separate. This protects original game data while allowing contributors to share evidence and repeat useful analysis.

## License requirement

Binary Ninja Free does not support plugins. Using `binary_ninja_mcp` requires a paid Binary Ninja edition with plugin support. A Non-Commercial/Personal license can run the plugin through the Binary Ninja GUI. Commercial and Ultimate licenses also support headless plugin execution.

The MCP plugin also requires Python 3.12 or newer.

## Local files

Create this local layout:

```text
client/
  Darkages.exe
  ...complete private client installation...
binaryninja/
  workspace/
    Darkages.exe.bndb
```

Both `client/` and `binaryninja/workspace/` are ignored as complete directories. Do not force-add their contents.

On macOS or Linux, verify the executable with:

```shell
shasum -a 256 client/Darkages.exe
```

On Windows PowerShell, use:

```powershell
Get-FileHash .\client\Darkages.exe -Algorithm SHA256
```

The result must be:

```text
054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
```

The file size must be `3,112,960` bytes.

## Binary Ninja workspace

1. Open `client/Darkages.exe` in Binary Ninja.
2. Allow initial analysis to finish.
3. Save the analysis database as `binaryninja/workspace/Darkages.exe.bndb`.
4. Install `binary_ninja_mcp` through the Plugin Manager or its documented manual process.
5. Click the MCP plugin button in the lower-left corner of the Binary Ninja GUI.
6. Configure the local MCP client using the plugin's generated or manual configuration.
7. Verify access with a read-only query for the entry point, imports, or one function.

Keep the GUI open when using a Non-Commercial/Personal license. Do not commit absolute plugin paths or local MCP configuration.

## Codex configuration

The Binary Ninja plugin listens on `localhost:9009`. Register its recommended stdio bridge in the user-level Codex configuration:

```shell
codex mcp add binary-ninja-mcp -- npx -y binary-ninja-mcp --host localhost --port 9009
```

Verify the stored entry with:

```shell
codex mcp get binary-ninja-mcp --json
```

Restart Codex after adding or changing the entry. Keep Binary Ninja open with the target loaded and the MCP plugin enabled before starting an analysis task.

## What to commit

Commit new findings to the book under `docs/`. Commit stable machine-readable names, types, comments, and function facts under `analysis/exports/`. Commit the scripts that produce and consume those exports under `binaryninja/scripts/`.

Do not commit the `.bndb`. It is useful local state, but it is binary, contains analysis history, and is unsuitable as the shared source of truth.
