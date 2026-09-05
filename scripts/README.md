# Repository scripts

These scripts build generated parts of the book. They do not require Binary Ninja.

```text
python3 scripts/build_book_summary.py
python3 scripts/build_book_summary.py --check
python3 scripts/build_function_reference.py
```

- `build_book_summary.py` rebuilds mdBook navigation and both packet indexes. Packet titles and transform labels come from their pages. It rejects missing, unlisted, or duplicate navigation entries; `--check` reports stale generated content without writing.
- `build_function_reference.py` rebuilds the grouped function appendix from YAML exports.

Binary Ninja import, export, and analysis scripts remain under `binaryninja/scripts/`.
