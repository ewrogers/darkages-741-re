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

This is a restructuring of documented findings. No new client behavior is inferred from the presentation change. Existing page URLs and heading anchors remain the compatibility surface; no new book pages or export schemas are introduced. Tasks 2 through 6 were pending after this step.

Task 1 is complete for this first reading path and the NPC example. Validation compared the edited book with a snapshot of the starting working tree:

- Navigation and packet indexes remain current; all 276 chapter entries are listed once.
- The local mdBook build passes with the existing large-search-index warning.
- All original rendered heading anchors survive on the edited pages.
- All original behavior tables remain intact. Code and layout blocks remain verbatim except the corrected dispatch diagram and duplicate layouts consolidated into the existing appendix. All five NPC code blocks and nine tables remain byte-identical.
- Across 3,676 rendered link checks, no new missing targets or fragments were introduced.
- All analysis exports and the pre-existing function-reference edits remain unchanged from the starting working tree.
- Independent editorial review and whitespace checks pass. No executable, analysis database, commit, or published site was changed.

The baseline local build also has 32 unavailable link targets, including repository-only evidence links and `README.html` paths. Tasks 2 and 4 should resolve these against the intended published URLs after local and CI mdBook versions are aligned. This task preserves those existing links rather than claiming that the entire published link surface has passed validation.

### Task 2: reader routes and section guides

Task 1 was committed as `b7bbad3` before this work began. Task 2 adds purpose-based routes to the existing book entry, seven section guides, and two packet indexes. The guides still cover every topic; no parallel tutorial tree or new book page was introduced.

| Area | Change |
| --- | --- |
| Book and repository entry | Separate reading from research setup; offer starting points for a client turn, NPC conversation, asset reader, and exact reference. |
| Section guides | Put reader questions before the complete topic inventory. Link explanations to their existing exact references instead of duplicating their contents. |
| Network guide and packet indexes | Keep screen-menu and pursuit pairs separate, preserve both directions, and provide direct opcode-index anchors. |
| Sidebar | Group client behavior, lookup material, and research workflow. Put setup and methodology after the behavior and reference chapters. |
| Published guide links | Keep ten `README.html` aliases for guide chapters published as `index.html`; preserve heading fragments through the generated redirects. |
| Site configuration | Align the site, repository, and edit-link slug with the existing Git remote and repository README: `darkages-741-re`. |

Validation used the official mdBook `0.5.4` release, matching CI, in a temporary workspace:

- Navigation regeneration is idempotent, and all 276 chapters remain listed exactly once.
- Six explicit content-link journeys reach their destination in two or three links: one client turn, an NPC screen menu, a pursuit conversation, EPF rendering, function lookup, and event layout lookup. These checks use content links rather than incidental sidebar reachability.
- The build passes with the existing large-search-index warning. Across 3,753 rendered link checks, no new missing targets or fragments were introduced.
- All existing guide heading anchors, coverage/status tables, packet indexes, and raw-event provenance survive. All 137 individual packet pages remain byte-identical to the starting working tree.
- The guide aliases resolve 17 formerly missing targets. The remaining 15 links point to repository-only analysis or script files outside the published book; their publication path remains for Task 4.
- Independent reader review, Python syntax, and whitespace checks pass. Existing analysis exports and the pre-existing function-reference edits remain unchanged.

Task 2 is complete. Tasks 3 through 6 remain pending. No site was published and no system-wide mdBook installation was changed.

### Task 3: voice, worked explanations, and diagrams

Task 2 was committed as `bcb9aad` before this work began. Task 3 establishes the craft in four representative explanations and records reusable [voice and figure conventions](../docs/methodology.md#voice-and-worked-explanations). This is an editorial treatment of existing findings, not a new verification of binary behavior or a rewrite of every chapter.

| Example | What the explanation makes visible |
| --- | --- |
| Local walking | Four versus eight samples share a nominal 456 ms step. The timeline aligns sample boundaries, repeated poses, and the final hold; exact displacements and remote timing stay in the original tables. |
| Music replacement | The old stream reaches silence before the new stream starts. The ordered flow stays separate from the nonlinear volume rule and 200 ms callback cadence. |
| Pursuit reply | Packet direction, client response-pending state, and server ownership of the next conversation step. Previous, Close, and conditional speech remain explicit in the surrounding reference. |
| Packet body notation | An explicitly invented seven-byte example connects field order, big-endian integers, and byte-counted text to the original schema. It makes no real opcode assignment. |

The four figures are editable, self-contained SVG source under `docs/assets/diagrams/`, using plain parchment, brown ink, and monospace identifiers and exact values. Each has alternative text, an SVG title and description, a caption, and a full-size source link. Prose and exact tables remain usable without the image. Existing short ASCII flows remain where they already explain their relationship.

The small `theme/diagrams.css` and `theme/diagrams.js` additions serve these figures only. Narrow screens get a scrolling hint and a focusable scroll region. The script prevents mdBook's chapter shortcuts from consuming Left and Right inside that region, preserving native scrolling and normal Tab navigation. Broader visual identity, typography, and navigation styling remain for Task 6.

Validation against the starting working tree:

- The official mdBook `0.5.4` build passes, and all 276 navigation entries remain current. The existing search-index warning remains, at roughly 13.2 MB.
- All chapter heading anchors, existing behavior tables, and packet schemas survive. The redundant music ASCII flow is the only removed fenced block; its sequence is retained in prose and SVG.
- All 137 packet pages, 40 analysis exports, and pre-existing function-reference edits remain unchanged.
- Across 3,766 rendered link checks, no new failures were introduced. The same 15 repository-only targets remain for Task 4. All eight image placements resolve, including the four in the combined print book.
- All four SVGs render without clipped labels. The walking coordinates and timing labels match the documented intervals, and the invented byte strip encodes the stated values. The lowest text contrast is 5.27:1; labels and lines carry meaning independently of color.
- Browser checks cover desktop presentation, light and dark themes, and every figure at a 360 px viewport. Figures scroll inside the page without widening it. Left and Right scroll a focused figure, Tab leaves it, and chapter shortcuts still work outside it. Print asset paths and print CSS were checked; printer pagination was not visually verified.
- Independent technical/editorial review, JavaScript syntax, and whitespace checks pass.

Task 3 is complete for these worked examples and conventions. Tasks 4 through 6 remain pending. No client binary or analysis database was changed, and no site was published.
