# Repository scripts

These scripts build generated parts of the book. They do not require Binary Ninja.

Start with the [contributor handbook](../CONTRIBUTING.md#run-the-checks) for prerequisites, the complete workflow, and reader review. Local checks and CI share this command, using mdBook `0.5.4`:

```text
python3 scripts/check_docs.py
```

## Tool contracts

- `check_docs.py` verifies the pinned mdBook version, runs both freshness checks and both test suites, builds, and validates rendered links. It stops at the first failure and never regenerates source artifacts. The default build is temporary and removed on exit. `--book-dir book` retains an ignored preview; an external destination is also allowed. Other repository destinations are rejected to protect authored sources. `--mdbook` selects a particular executable.
- `build_book_summary.py` rebuilds mdBook navigation and both packet indexes. Packet titles and transform labels come from their pages. It rejects missing, unlisted, or duplicate navigation entries; `--check` reports stale generated content without writing.
- `build_function_reference.py` reads the existing flat function records in YAML exports and writes deterministic includes and lookup data under `generated/function-reference/`. The small chapter entries in `docs/appendix/functions/` include those tables. `--check` detects stale output without writing. Edit the source export instead of a generated table.
- `book_repository_links.py` is an mdBook HTML preprocessor, run after includes. Relative source links inside the repository remain relative in Markdown; links to tracked files outside the book become repository URLs in the published book. The repository and ref come from `edit-url-template`. Missing or untracked outside-book targets fail the build.
- `check_book_links.py` checks the built HTML, heading fragments, guide redirects, image and script assets, and repository evidence targets. It also checks relative links in the contributor and repository guides and Markdown heading/explicit-anchor targets reached from the book. The source scanner follows the repository's Markdown conventions and skips literal code examples; it is not a general Markdown renderer. Source URLs and line numbers are checked against the local checkout, so this check does not require network access. It does not verify external websites or the underlying binary interpretation.

Binary Ninja import, export, and analysis scripts remain under `binaryninja/scripts/`.

The navigation places client behavior first, lookup material second, and the research setup and methodology last. Section guides provide reading routes into those same pages. Keep each chapter listed once and preserve existing packet direction and opcode ordering.

`book.toml` retains `README.html` redirects for the guide chapters published as `index.html`. Check both URL spellings, including heading fragments, when changing a guide or its links.

## Function reference and search

Function collection validates schema version 1, the matching target fingerprint, required fields, static addresses, and supplied RVAs. Duplicate name/address records retain every evidence statement and source line. Incompatible nonempty confidence, signature, range, or RVA fields fail generation before output is written. Names attached to multiple addresses, or addresses attached to multiple names, remain visible as identity warnings; an editorial change must not resolve those disagreements by choosing a winner.

The [function lookup](../docs/appendix/functions.md) covers all name/address entries, including conflicting identities. It calculates RVAs from the preferred image base and preserves subsystem and per-entry links. The general search keeps the lookup entry but omits the generated function-table chapters through mdBook's [per-chapter search configuration](https://rust-lang.github.io/mdBook/format/configuration/renderers.html#outputhtmlsearchchapter). A link beside general search carries the query into the exact lookup. Do not narrow indexing further without preserving discovery and measuring actual search results.

Generated includes are versioned outside `docs/` so freshness is reviewable and `mdbook build` works after a clone. Preview sites, rendered HTML, and measurement output remain outside the source tree. The function generator has no Binary Ninja or third-party Python dependency; Python 3.12 or newer and Node.js are sufficient for these checks.
