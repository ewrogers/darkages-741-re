# Contributor handbook

Help a reader understand one part of the client, implement its exact behavior, and find the evidence behind it. Start with an existing topic and carry the change through its explanation, reference, and checks.

Reading and editing the book do not require the private client or Binary Ninja. New claims about client behavior require the matching binary and the research workflow below.

## Choose a contribution

| You want to | Start here | Carry the change through |
| --- | --- | --- |
| Clarify prose or improve a diagram | [Authoring guide](contributing/authoring.md) | Existing explanation, exact reference, and [reader review](#review-the-result) |
| Research or correct client behavior | [Local analysis setup](docs/getting-started.md) and [research policy](contributing/research-policy.md) | Binary Ninja evidence, export, and matching chapter |
| Add or revise a packet | [Packet requirements](contributing/research-policy.md#packet-documentation) | Direction-specific page, owners, paired messages, and regenerated indexes |
| Document an asset reader or writer | [Format requirements](contributing/research-policy.md#file-format-documentation) | One format page, sample validation, and evidence; keep renderer behavior separate |
| Change navigation, generation, or presentation | [Tool contracts](scripts/README.md) | Authored inputs, generated output, compatibility links, and rendered checks |

The [authoring guide](contributing/authoring.md) owns writing conventions. The [research policy](contributing/research-policy.md) owns evidence and subsystem requirements. [Analysis policy](analysis/README.md) owns export requirements. Follow the applicable rules through the whole change; the book's [methodology](docs/methodology.md) explains to readers what those rules mean for the findings.

## Prepare a documentation checkout

Run commands from the repository root. For documentation checks, install Python 3.12 or newer, Node.js with `node --test` support, and mdBook `0.5.4`, matching [CI](.github/workflows/docs.yml). The documentation scripts use the Python standard library and Node's built-in test runner. They do not need Binary Ninja, PyYAML, or a package install in this repository.

If you use Cargo, the pinned mdBook can be installed with:

```sh
cargo install mdbook --version 0.5.4 --locked
```

Check the starting state before editing:

```sh
git status --short
python3 scripts/check_docs.py
```

The check command verifies generated output, runs the tests, builds in a temporary directory, and checks rendered links. It does not regenerate files or publish the book. Use `--mdbook /path/to/mdbook` to select a separate executable without replacing your normal installation. A version mismatch stops with the required version.

For new binary research, continue with [Getting started](docs/getting-started.md). That page owns the matching-client check, Binary Ninja license requirements, plugin setup, and first read-only MCP request. Keep the analysis workspace [private](binaryninja/README.md).

## Choose the existing home

Search the book and exports for the topic and established names before adding a page. A new route should link to the canonical explanation. Add focused documentation directories only when direct Binary Ninja evidence justifies them. Extend an existing page instead of creating a competing source of truth.

| Location | Responsibility |
| --- | --- |
| [Book entry](docs/README.md) and [navigation](docs/SUMMARY.md) | Reader routes and the generated chapter sequence |
| [Setup](docs/getting-started.md) and [methodology](docs/methodology.md) | Local analysis setup and the reader's evidence model |
| `docs/application/` | Startup, configuration, lifecycle, and the game loop |
| `docs/systems/` | Events, input, UI panes, and other focused game systems |
| `docs/rendering/` | Renderer lifecycle, pane drawing, world layers, sprites, effects, and blending |
| `docs/audio/` | Audio lifecycle, music, sound effects, volume, fades, and MIDI status |
| `docs/file-formats/` | One developer-facing page per confirmed asset or data format |
| `docs/network/` | Connection, transport, transforms, and separate packet directions |
| `docs/appendix/` | Addresses, runtime patches, layouts, inheritance, and large lookup tables |
| `analysis/` | Research/export policy and dated audit history, including [this revamp's audit](analysis/editorial-audit.md) |
| `analysis/exports/` | Deterministic symbols, functions, types, comments, and other verified evidence |
| `generated/function-reference/` | Generated presentation of those exports; edit the source records |
| `binaryninja/scripts/` | Binary Ninja import, export, and reusable analysis scripts |
| `scripts/` | Documentation generation and validation without Binary Ninja |
| `docs/assets/diagrams/` and `theme/` | Editable figures and the shared presentation behavior |
| `CONTRIBUTING.md` and `contributing/` | Contributor workflow and maintained authoring/research guidance |
| `client/` and `binaryninja/workspace/` | Ignored private client installation and local `.bndb` files |
| `legacy/` | Archived leads; leave the archive unchanged |

## Improve an explanation

1. Read the existing page, its exact reference, and the [authoring guide](contributing/authoring.md). Identify the reader's question and the conditions the explanation must preserve.
2. Lead with the visible result, then the owners and flow. Put exact fields, bounds, ordering, timing, and exceptions where an implementer needs them. Link to proof without opening with addresses.
3. Use the existing [worked explanations](contributing/authoring.md#voice-and-worked-explanations) to choose a useful example or figure. Keep uncertainty beside the claim, and label invented teaching values.
4. If moving material, transfer every unique detail before removing the duplicate. Preserve the page URL and incoming heading anchors. Keep the figure, prose, and exact reference consistent.
5. Run the checks and [review both reading paths](#review-the-result). Describe the change as editorial unless new behavior was verified.

If existing sources disagree, preserve the disagreement and state what remains unresolved. Improving prose does not authorize selecting a new address, renaming a function, or promoting a tentative field to a confirmed one.

## Research or correct a finding

Follow the [investigation workflow](contributing/research-policy.md#reverse-engineering-workflow) and the relevant subsystem requirements. Confirm the target, search existing conclusions, trace the behavior, and check important control flow and data against lower-level views. High-level intermediate language (HLIL) is a convenient reconstruction; medium-level and low-level intermediate language (MLIL and LLIL), or disassembly, help check the details it hides.

Record durable names, types, and evidence comments in Binary Ninja using user APIs. Use the [existing export formats](analysis/exports/README.md) and checked-in synchronization scripts; their Binary Ninja and PyYAML requirements are separate from documentation tooling. Preserve unknowns and contradictory evidence. Update the matching chapter and exact reference in the same change.

A reverse-engineering task is complete when the local behavior is explained from Binary Ninja evidence, useful user symbols or comments are updated, durable analysis is exported when supported, documentation is synchronized, uncertainty is visible, and basic validation has passed.

Do not patch executable bytes as a side effect of research. [Patch authorization and launcher requirements](contributing/research-policy.md#runtime-patch-documentation) apply separately from normal naming, typing, and commenting.

## Regenerate only what changed

| Source change | Update |
| --- | --- |
| New chapter or changed navigation | Add its route in `scripts/build_book_summary.py`, then run `python3 scripts/build_book_summary.py` |
| Packet title, opcode, or transform metadata | Edit the packet page, then run `python3 scripts/build_book_summary.py` to update both direction indexes and the sidebar |
| Exported function records | Run `python3 scripts/build_function_reference.py` and inspect the resulting reference changes |
| Figure or theme assets | Update the source asset and referring page; no function-reference regeneration is needed |

The generators' `--check` modes report stale files without rewriting them. The combined check command uses those modes. Regenerate deliberately and review the diff; never repair a generated table by editing its rows.

Function generation rejects incompatible metadata for the same name/address identity. Existing names at multiple addresses, or addresses with multiple names, remain visible warnings with all candidates retained. Resolve those only through focused evidence work. See the [function-reference contract](scripts/README.md#function-reference-and-search).

New repository files linked from the book must be known to Git before building, because the publishing preprocessor rejects untracked targets. During review, `git add -N -- path/to/new-file.md` makes a new path visible without staging its contents. Do not use that step to expose a private file.

## Run the checks

```sh
python3 scripts/check_docs.py
git diff --check
```

Local work and documentation CI use the same command. It fails on stale navigation or function references, invalid packet metadata, incompatible function metadata, failed tests/builds, and broken rendered pages, anchors, redirects, assets, contributor-guide links, or repository evidence targets. The link check uses the checkout; it does not fetch external websites or revalidate the binary.

To retain a local preview in the ignored build directory:

```sh
python3 scripts/check_docs.py --book-dir book
python3 -m http.server 8000 --directory book
```

Open `http://localhost:8000/`. You can also pass an absolute temporary directory to `--book-dir`. Build output never belongs in `docs/` or `generated/`. CI uses `--book-dir book` for its upload artifact; local validation does not deploy it.

| A check fails because | Next action |
| --- | --- |
| Generated content is stale | Run the matching generator, inspect its diff, then check again |
| A chapter is missing or unlisted | Fix its source path and the navigation definition before regenerating |
| A source target or heading is missing | Repair the link or preserve the former anchor; use a tracked, shareable evidence source |
| Function metadata conflicts | Compare the source records; retain uncertainty rather than selecting a winner for the build |
| mdBook has the wrong version | Select the pinned executable with `--mdbook` |

## Review the result

Follow the [novice and implementer review](contributing/authoring.md#review-two-reading-paths). The novice should understand the result and each owner without interpreting addresses. The implementer should recover exact conditions and reach the supporting evidence.

For changed figures or presentation, inspect desktop and narrow screens, keyboard navigation, light and dark themes, and print. Check units, labels, arrow direction, alternative text, and the explanation without the image. Structural checks cannot decide whether the writing is clear or a claim is established.

Report what changed, the evidence or existing reference used, which checks and reader journeys passed, and what remains uncertain. Keep audit history as history; maintain the current rule in its guide instead of requiring contributors to reconstruct it from an old audit.

Review the intended commit as well as the working tree. If unrelated export edits remain, generated references can be correct locally but stale in a clean checkout. Validate a separate checkout with only the intended source changes and regenerate its artifacts from those sources. Preserve the owner's source edits and corresponding working references; do not include unrelated analysis just to satisfy a freshness check.

## Repository hygiene

- Preserve unrelated user changes.
- Do not commit anything under `client/` or `binaryninja/workspace/`.
- Do not commit `.bndb` files, original binaries, game archives, credentials, character data, or unsanitized captures.
- Small sanitized fixtures are acceptable when necessary to reproduce a parser or test. Add ignored binary fixtures deliberately with `git add -f` only after review.
- Keep generated files and tool output out of the documentation tree.
- Use relative Markdown links inside the repository.
- Do not commit or push unless the user asks.
