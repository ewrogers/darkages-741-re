# Book editorial audit

The book's underlying voice was already consistent: short explanations, named client functions, and explicit uncertainty. The main drift was in page openings, packet terminology, navigation, and the boundary between explanations and lookup material.

## Scope

The audit covered the structure and conventions of all 277 Markdown book pages, with focused prose review and edits across chapter introductions, overviews, packet references, and misplaced lookup sections. It refined 135 book pages. This was an editorial audit, not a fresh Binary Ninja verification of every technical conclusion.

## Findings and changes

| Finding | Refinement |
| --- | --- |
| 53 packet pages opened with metadata | Moved their purpose statements before the table and retained old section anchors |
| Transform labels mixed modes with key names | Standardized pages, indexes, and explanations on `raw`, `static`, and `derived` |
| Placeholder introductions repeated packet names | Replaced them with established behavior or explicit limits where behavior remains unknown |
| Generic constructor proof interrupted packet explanations | Moved 13 constructor paragraphs into closing name-evidence sections |
| Body headings varied without a semantic difference | Standardized 12 plaintext-body headings; retained special labels for common, partial, and observed bodies |
| Overviews became uneven or incomplete | Expanded section guides, linked the motion-effect table, and clarified the distinction between compiled behavior and proposed extensions |
| Navigation lagged behind the book | Added Map loading and cache, preserved CPU affinity in the generator, and gave Game loop its own reading step |
| Addresses and hook details remained in main chapters | Used existing function/export references and moved unique call sites and the optional help-button hook into matching appendices |
| Two cross-references were stale | Repaired the map-control filename and effect-timing anchor |

## Keeping it consistent

The [methodology](../docs/methodology.md#writing-a-consistent-page) records the page conventions. The [navigation generator](../scripts/README.md) now derives both packet indexes from page titles and transform metadata. Its `--check` mode rejects stale output and missing, duplicate, or unlisted pages. Documentation CI runs that check.

## Validation and limits

- mdBook builds successfully; its only warning is the roughly 13 MB search index.
- All 1,525 checked local Markdown links resolve, including rendered heading targets.
- All 137 packet pages retain their original fenced code blocks.
- All 39 YAML analysis exports remain unchanged from the starting working tree.
- Generator regeneration and rejection paths, Python syntax, and whitespace checks pass.
- Existing work in progress was preserved. No executable or analysis database was changed, and nothing was committed.

External URLs and the underlying technical findings were not revalidated. Specialized packet, file-format, and patch pages retain structures appropriate to their content rather than sharing one rigid template.

## Documentation revamp sequence

The project owner accepted the architecture review on 2026-09-08 and requested implementation in this order:

1. Give each topic deliberate reading depth.
2. Turn section guides into useful starting points.
3. Make explanations and diagrams a coherent craft.
4. Make the evidence atlas precise and findable.
5. Give contributors one place to learn the craft.
6. Give the book an old-spellbook identity.

The visual direction should favor brown wood, leather, parchment, and earth tones. Keep technical content readable and use monospace for code, packet layouts, addresses, and exact values. Ornament belongs around the reading surface. Begin with an mdBook theme; evaluate a platform change against demonstrated authoring, search, or usability limitations.

### Task 1: reading depth

The first implementation covers the Game loop, Events, and UI foundations, plus NPC dialogs as the larger mixed-purpose example. The [methodology](../docs/methodology.md#reading-depth) records the progression for subsequent topics.

| Page | Change |
| --- | --- |
| Game loop | Put owner responsibilities and the main-thread rule before detailed pacing, background behavior, and clock experiments. |
| Event system | Explain immediate versus queued delivery before storage; correct the flow diagram so immediate dispatch does not appear to wait for a tick. Keep timer and pointer behavior ahead of runtime representation. |
| UI and panes | Explain the distinct trees, independent pane states, controls, and drawing before concrete screens and storage details. |
| NPC dialogs | Keep live entry, pane composition, and round trips together; place exact selection rules and native invocation later, followed by explicitly dormant families. |
| Pane and event layouts | Consolidate the event representation and dialog fields in the existing appendix, retaining the unique decoded-server payload and drag-bound fields from main text. |

This is a restructuring of documented findings. No new client behavior is inferred from the presentation change. Existing page URLs and heading anchors remain the compatibility surface; no new book pages or export schemas are introduced. The other five tasks remain pending.

Task 1 is complete for this first reading path and the NPC example. Validation compared the edited book with a snapshot of the starting working tree:

- Navigation and packet indexes remain current; all 276 chapter entries are listed once.
- The local mdBook build passes with the existing large-search-index warning.
- All original rendered heading anchors survive on the edited pages.
- All original behavior tables remain intact. Code and layout blocks remain verbatim except the corrected dispatch diagram and duplicate layouts consolidated into the existing appendix. All five NPC code blocks and nine tables remain byte-identical.
- Across 3,676 rendered link checks, no new missing targets or fragments were introduced.
- All analysis exports and the pre-existing function-reference edits remain unchanged from the starting working tree.
- Independent editorial review and whitespace checks pass. No executable, analysis database, commit, or published site was changed.

The baseline local build also has 32 unavailable link targets, including repository-only evidence links and `README.html` paths. Tasks 2 and 4 should resolve these against the intended published URLs after local and CI mdBook versions are aligned. This task preserves those existing links rather than claiming that the entire published link surface has passed validation.
