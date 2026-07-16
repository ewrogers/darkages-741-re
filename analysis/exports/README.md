# Analysis exports

This directory contains deterministic Binary Ninja exports such as user symbols, function metadata, types, comments, and runtime patch records.

[`startup.yaml`](startup.yaml) establishes schema version `1`. [`network.yaml`](network.yaml) records connection analysis, [`transport.yaml`](transport.yaml) records the shared send, receive, framing, and transform pipeline, [`ui-events.yaml`](ui-events.yaml) records the event, timer, pane-tree, and dialog-control architecture, [`ui-pane-types.yaml`](ui-pane-types.yaml) records every RTTI class whose inheritance reaches `Pane`, and [`packets.yaml`](packets.yaml) adds deterministic direction-specific opcode indexes. All retain the same required manifest fields. Each manifest records the exact target fingerprint and focused evidence. Lists are sorted by address, opcode, or type name. Addresses and byte strings use uppercase hexadecimal text so reviews do not depend on YAML number handling.

Use [`sync_user_analysis.py`](../../binaryninja/scripts/sync_user_analysis.py) from Binary Ninja's Python console to import or refresh tracked names and comments and to normalize packet records. The script requires [PyYAML](https://pyyaml.org/). Pass `client/Darkages.exe` as `binary_path` so the script fails before changing analysis when the private input does not match.

Do not copy legacy exports here without revalidation.
