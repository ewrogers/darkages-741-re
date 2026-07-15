# Analysis exports

This directory is reserved for deterministic Binary Ninja exports such as user symbols, function metadata, types, and comments.

The first export must define and document its schema, identify the exact target fingerprint, and include a tested importer and exporter under `binaryninja/scripts/`. Do not copy legacy exports here without revalidation.
