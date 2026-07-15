# Analysis exports

This directory contains deterministic Binary Ninja exports such as user symbols, function metadata, types, comments, and runtime patch records.

[`startup.yaml`](startup.yaml) establishes schema version `1`. [`network.yaml`](network.yaml) uses the same schema for command-line and initial-connection analysis. Each manifest records the exact target fingerprint, focused user analysis, evidence notes, and any related ASLR-safe runtime patch RVAs. Lists are sorted by address. Addresses and byte strings use uppercase hexadecimal text so reviews do not depend on YAML number handling.

Use [`sync_user_analysis.py`](../../binaryninja/scripts/sync_user_analysis.py) from Binary Ninja's Python console to import or refresh its tracked names and comments. The script requires [PyYAML](https://pyyaml.org/). Pass `client/Darkages.exe` as `binary_path` so the script fails before changing analysis when the private input does not match.

Do not copy legacy exports here without revalidation.
