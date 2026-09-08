# Repository scripts

These scripts build generated parts of the book. They do not require Binary Ninja.

For local book builds, use mdBook `0.5.4`, matching the version pinned in `.github/workflows/docs.yml`.

```text
python3 scripts/build_book_summary.py
python3 scripts/build_book_summary.py --check
python3 scripts/build_function_reference.py
```

- `build_book_summary.py` rebuilds mdBook navigation and both packet indexes. Packet titles and transform labels come from their pages. It rejects missing, unlisted, or duplicate navigation entries; `--check` reports stale generated content without writing.
- `build_function_reference.py` rebuilds the grouped function appendix from YAML exports.

Binary Ninja import, export, and analysis scripts remain under `binaryninja/scripts/`.

The navigation places client behavior first, lookup material second, and the research setup and methodology last. Section guides provide reading routes into those same pages. Keep each chapter listed once and preserve existing packet direction and opcode ordering.

`book.toml` retains `README.html` redirects for the guide chapters published as `index.html`. Check both URL spellings, including heading fragments, when changing a guide or its links.
