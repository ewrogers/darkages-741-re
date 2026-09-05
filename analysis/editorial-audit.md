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
