# Binary Ninja scripts

Place reusable Binary Ninja import, export, validation, and focused analysis scripts here.

Scripts must be cross-platform, must not depend on a hard-coded Binary Ninja installation path, and must not write original client bytes or secrets into committed output. An exporter should be deterministic, and its importer should be tested against a fresh local `.bndb` before the format is treated as stable.

`sync_user_analysis.py` imports and refreshes any schema-version-1 manifest under `analysis/exports/`. Install `requirements.txt` into Binary Ninja's selected Python environment, then run the script from Binary Ninja's Python console:

```python
exec(open("binaryninja/scripts/sync_user_analysis.py").read())
import_manifest(bv, "analysis/exports/startup.yaml", "client/Darkages.exe")
export_manifest(bv, "analysis/exports/startup.yaml", "client/Darkages.exe")
import_manifest(bv, "analysis/exports/network.yaml", "client/Darkages.exe")
export_manifest(bv, "analysis/exports/network.yaml", "client/Darkages.exe")
import_manifest(bv, "analysis/exports/transport.yaml", "client/Darkages.exe")
export_manifest(bv, "analysis/exports/transport.yaml", "client/Darkages.exe")
import_manifest(bv, "analysis/exports/packets.yaml", "client/Darkages.exe")
export_manifest(bv, "analysis/exports/packets.yaml", "client/Darkages.exe")
import_manifest(bv, "analysis/exports/rendering.yaml", "client/Darkages.exe")
export_manifest(bv, "analysis/exports/rendering.yaml", "client/Darkages.exe")
import_manifest(bv, "analysis/exports/audio.yaml", "client/Darkages.exe")
export_manifest(bv, "analysis/exports/audio.yaml", "client/Darkages.exe")
import_manifest(bv, "analysis/exports/file-formats.yaml", "client/Darkages.exe")
export_manifest(bv, "analysis/exports/file-formats.yaml", "client/Darkages.exe")
import_manifest(bv, "analysis/exports/profile-text.yaml", "client/Darkages.exe")
export_manifest(bv, "analysis/exports/profile-text.yaml", "client/Darkages.exe")
import_manifest(bv, "analysis/exports/ui-layouts.yaml", "client/Darkages.exe")
export_manifest(bv, "analysis/exports/ui-layouts.yaml", "client/Darkages.exe")
```

The script updates only addresses already listed in the manifest. Packet records are normalized but do not change the Binary Ninja database. Runtime patch records are documentation for a launcher and are never applied by this script.

`export_pane_rtti.py` independently validates the private executable fingerprint, decodes the 32-bit MSVC RTTI hierarchy, and regenerates the Pane type manifest and appendix:

```text
python binaryninja/scripts/export_pane_rtti.py --binary client/Darkages.exe --yaml analysis/exports/ui-pane-types.yaml --markdown docs/appendix/pane-types.md
```

It reads the client but never writes client bytes.
