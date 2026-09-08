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

### Task 4: evidence atlas, generated references, and search

Task 3 was committed as `4ee34a9` before this work began. The [function reference](../docs/appendix/functions.md) now connects a behavioral explanation to a particular function, its evidence, and the source export. The existing function groups become twelve focused reference chapters. The original hub URL and all twelve group anchors remain valid.

The generator preserves 5,379 source records as 5,263 distinct name/address entries in the starting working tree. Previously, repeated identities could silently replace an earlier evidence statement. Each entry now retains every source statement and links to the exact YAML record. Seven existing name/address disagreements remain visible, including both candidate records. These are unresolved identity warnings, not inferred aliases or new Binary Ninja findings. Incompatible metadata for the same identity fails generation before any output is written.

The existing YAML exports remain the evidence source. Generated Markdown includes and the browser lookup payload live under `generated/function-reference/`, outside the authored book. The generator checks the existing schema and target fingerprint, required fields, duplicate keys, address bounds, and supplied RVAs. It adds no evidence schema or confidence scale. Its `--check` mode is read-only. The [script guide](../scripts/README.md) documents regeneration, validation, and the limits of these checks.

Readers can search every exported function by full or partial name, static hexadecimal address, or explicit `rva:` query. Results retain conflicting identities and link directly to individual entries. The lookup payload is loaded with the reference hub, not every chapter. The full subsystem references remain usable without JavaScript. Metadata and packet-transform explanations now link to specific evidence entries; the same anchor scheme is available to other chapters as they are revised.

The general search includes the behavioral chapters, packet pages, other appendices, and reference hub. Only the twelve generated function tables are excluded. A link beside general search carries its query into the complete function lookup, so a name or address absent from prose remains discoverable. This exclusion was enabled only after verifying complete lookup coverage.

Search measurements used the official mdBook `0.5.4` build and the same source snapshot:

| Variant | General index bytes | Gzip bytes | Median local initialization |
| --- | ---: | ---: | ---: |
| Task 3, single function appendix | 13,195,636 | 1,598,270 | 94.6 ms |
| Split tables, all evidence still indexed | 13,907,453 | 1,656,749 | 99.0 ms |
| Split tables, complete separate function lookup | 8,232,550 | 1,212,907 | 58.6 ms |

The final general index is about 38% smaller, or 24% smaller after gzip, and no longer produces mdBook's large-index warning. Initialization is the median of nine local Node.js 24 runs executing the generated index and calling `elasticlunr.Index.load`; it excludes network transfer and rendering and is not a browser startup guarantee. The separate lookup payload is 1,031,890 bytes, or 116,500 bytes after gzip. Exhaustive checks found the correct entry for all 15,789 name, static-address, and RVA queries.

Representative general-search results preserve the first destinations for walking, music fade, NPC conversations, `SScreenMenu`, `CPursuit`, and `net_encrypt_client_packet`. The first result for “packet encryption” now reaches transport behavior instead of the function table. An address present only in the exports moves to the exact lookup, with the search handoff verified in the browser.

Relative repository links remain relative in Markdown. An HTML preprocessor resolves tracked targets outside the book to the configured repository reference when publishing. This repairs the fifteen repository-only links identified in Tasks 2 and 3 and supports the generated source-record links. The rendered-link checker validates pages, anchors, redirects, assets, tracked source targets, and source line bounds against the checkout. It does not contact GitHub or prove that an uncommitted source line exists on the remote branch.

Validation against the starting working tree:

- All 18 tests pass: eleven Python tests for generation, source links, and rendered checks; seven JavaScript tests for lookup behavior. CI runs the same suites, both freshness checks, the pinned build, and rendered-link validation.
- All 288 navigation entries are current and appear once. The build passes; 14,785 rendered links and assets resolve without failures.
- All original chapter heading anchors survive. All 137 packet pages, both packet indexes, and all 40 analysis-export files remain byte-identical. Both pre-existing manual-action entries remain in the reference.
- Browser checks cover general search to exact lookup to the evidence entry, conflicting identities, static addresses, explicit RVAs, empty results, Escape clearing, light and dark themes, and a 360 px viewport. Evidence tables become readable cards on phones. Focused result regions scroll without triggering chapter navigation. No browser errors were observed.
- An isolated checkout using only committed exports independently passes all tests, freshness checks, the pinned build, and 14,783 rendered-link checks. It contains 5,261 identities from 5,377 records. This confirms that Task 4 does not require the owner's unrelated `manual-actions.yaml` additions.
- Whitespace checks pass. No source export, client binary, or analysis database was modified, and no site was published.

The working reference intentionally reflects the owner's two uncommitted manual-action records. When committing Task 4 separately from those records, regenerate the staged artifacts against committed exports in an isolated checkout; retain the working-tree reference and source edits. The independent validation above exercised that exact source state.

Task 4 is complete. Tasks 5 and 6 remain pending. Full contributor guidance and the earthy spellbook theme retain their separate scopes.

### Task 5: contributor handbook and repository guidance

Task 4 was committed as `294faa2` before this work began. The [contributor handbook](../CONTRIBUTING.md) now provides the entry for prose, diagrams, binary findings, packets, formats, and tooling. It connects each contribution to its source files, regeneration step, automated checks, and human review. Contributors can improve explanations without installing Binary Ninja or obtaining private client data.

The [authoring guide](../contributing/authoring.md) owns voice, reading depth, worked examples, and diagrams. The [research policy](../contributing/research-policy.md) owns evidence and subsystem requirements. [Analysis policy](README.md) remains the home for export requirements. `AGENTS.md` now routes to those mandatory instructions in seventeen lines while retaining the core source-of-truth, preservation, privacy, patch-authorization, and completion requirements. `CLAUDE.md` continues to route through `AGENTS.md`.

The book's methodology now explains the reader's evidence model and links to contributor guidance. Its former authoring anchors remain valid. Contributor guides stay outside `docs/` and outside the reader's chapter sequence. The historical audit remains a record of completed work, not the source of current policy.

#### Rule-preservation checklist

Every section of the former `AGENTS.md` was mapped before replacing it. Twenty-three sections retain their substantive text verbatim in the destinations below. The remaining three received the explicit checks listed after the table.

| Former section | Maintained home | Check |
| --- | --- | --- |
| Project goal | [Research policy](../contributing/research-policy.md#project-goal) | Preserved |
| Clean-slate rule | [Research policy](../contributing/research-policy.md#clean-slate-rule) | Preserved |
| Book audience and voice | [Authoring guide](../contributing/authoring.md#book-audience-and-voice) | Preserved |
| Book organization | [Authoring guide](../contributing/authoring.md#book-organization) | Preserved |
| Book authoring style | [Authoring guide](../contributing/authoring.md#book-authoring-style) | Preserved |
| Code and pseudocode style | [Authoring guide](../contributing/authoring.md#code-and-pseudocode-style) | Packet exception clarified |
| Binary Ninja and MCP setup | [Getting started](../docs/getting-started.md) | Every prerequisite and setup action mapped |
| Repository map | [Handbook](../CONTRIBUTING.md#choose-the-existing-home) | All responsibilities retained; current paths added |
| Reverse-engineering workflow | [Research policy](../contributing/research-policy.md#reverse-engineering-workflow) | Preserved |
| Binary Ninja naming and comments | [Research policy](../contributing/research-policy.md#binary-ninja-naming-and-comments) | Preserved |
| UI and event documentation | [Research policy](../contributing/research-policy.md#ui-and-event-documentation) | Preserved |
| Timing and animation documentation | [Research policy](../contributing/research-policy.md#timing-and-animation-documentation) | Preserved |
| UI layout documentation | [Research policy](../contributing/research-policy.md#ui-layout-documentation) | Preserved |
| Portrait, profile, and formatted text documentation | [Research policy](../contributing/research-policy.md#portrait-profile-and-formatted-text-documentation) | Preserved; proxy rules receive their own heading |
| Rendering and file-format documentation | [Research policy](../contributing/research-policy.md#rendering-and-file-format-documentation) | Preserved |
| Audio documentation | [Research policy](../contributing/research-policy.md#audio-documentation) | Preserved |
| Text encoding and localization | [Research policy](../contributing/research-policy.md#text-encoding-and-localization) | Preserved; patch-authorization paragraph moved to runtime patches |
| Map and rendering documentation | [Research policy](../contributing/research-policy.md#map-and-rendering-documentation) | Preserved |
| Runtime patch documentation | [Research policy](../contributing/research-policy.md#runtime-patch-documentation) | Preserved |
| Version-controlled analysis | [Analysis policy](README.md#durable-function-records) | Preserved |
| Address and evidence requirements | [Research policy](../contributing/research-policy.md#address-and-evidence-requirements) | Preserved |
| Packet documentation | [Research policy](../contributing/research-policy.md#packet-documentation) | Preserved |
| File format documentation | [Research policy](../contributing/research-policy.md#file-format-documentation) | Preserved |
| Source-of-truth rules | [Research policy](../contributing/research-policy.md#source-of-truth-rules) | Preserved |
| Repository hygiene | [Handbook](../CONTRIBUTING.md#repository-hygiene) | Preserved, including the reviewed sanitized-fixture exception |
| Completion standard | [Handbook](../CONTRIBUTING.md#research-or-correct-a-finding) | Preserved |

The pseudocode guidance now explicitly applies C-like structures to runtime memory and fixed file layouts. Packet wire layouts follow the existing field-list rule, resolving the old generic sentence that also suggested C structs for packets. No wire convention changed.

Setup retains the supported analysis platforms, legally obtained matching client, size and hash check, paid plugin-capable license, GUI/headless distinction, Python and MCP prerequisites, local database path, plugin installation and start, first read-only request, and private configuration requirement. The repository map retains every former responsibility and adds the contributor guides, generated references, and presentation sources.

All moved methodology authoring text remains in the authoring guide, with relative links rebased. Its final build-output instruction now points to the common workflow's temporary build and ignored preview directory. This keeps output out of authored sources while matching the existing mdBook build directory. Existing examples, schemas, figures, timing values, and evidence were not changed.

#### One validation and review workflow

`python3 scripts/check_docs.py` runs the same sequence locally and in CI: both generator freshness checks, the Python and JavaScript suites, the pinned mdBook `0.5.4` build, and rendered-link validation. It checks without regeneration, stops at the first failure, and removes its temporary build. An explicit preview destination can be retained; authored repository directories are rejected. The README and script guide point to this command, and contributor-guide changes trigger documentation CI.

The handbook distinguishes structural failures from human review. Incompatible metadata for one function identity fails generation; the seven existing name/address disagreements remain visible warnings. Reviewers follow a novice reading path and an implementer lookup path and check that simplification preserves conditions, exceptions, units, provenance, and uncertainty. The handbook also records how to validate an intended commit when unrelated source edits remain in the working tree.

The link checker now covers the contributor and repository guides outside the book, including relative paths, tracked targets, heading fragments, and explicit anchors. Published book links to repository Markdown receive the same fragment check. The publisher and checker share the existing Markdown destination scanner, so fenced and inline examples remain literal. Heading recognition covers the repository's conventions; external websites and arbitrary Markdown extensions are outside the check. Source-line counts remain cached when thousands of evidence links reach the same export.

Validation:

- All 23 tests pass: sixteen Python tests and seven JavaScript tests. Five new tests exercise broken guide paths and fragments, explicit anchors, code examples, published Markdown targets, and source-line caching.
- The common workflow passes with mdBook `0.5.4`: 14,892 book/guide links and assets checked, including 114 contributor-guide links, with zero failures.
- An isolated checkout containing only the intended Task 5 changes also passes all tests, freshness checks, the pinned build, and 14,890 link/asset checks. Its temporary build is removed after validation. The two-link difference comes from the owner's existing manual-action records, which remain outside the intended commit.
- The runner rejects the installed `0.5.2` executable, a missing executable, and destinations that would overwrite the repository root or authored documentation. A stale generated-file fixture stops before tests or build and remains unmodified. These failure checks ran without changing the user's source files or system installation.
- All 288 reader navigation entries remain current, and the rendered table of contents is unchanged. All old anchors on methodology and setup survive. The browser confirms the old reading-depth link reaches the contributor handoff, links use the configured repository reference, and the page fits a 360 px viewport. No browser errors were observed.
- The prose-review route reaches the authoring guide and existing worked examples without private tooling. The research route reaches the target check, subsystem requirements, durable exports, exact reference, and shared checks. No client-behavior chapter, packet page, packet index, figure, or export changed; all 40 export files match the starting snapshot.
- Whitespace and independent link-tool review pass. No client binary or analysis database was changed, nothing was pushed or published, and the owner's unrelated source and generated-reference edits remain intact.

Task 5 is complete and committed as `b97c8f6`.

### Task 6: earthy grimoire presentation

The reader-facing title is now **The Dark Ages Grimoire**. The existing homepage heading and technical chapter names remain intact. Parchment provides warm paper and brown ink; Lamplight provides a dark brown reading surface. Both use a brown binding, quiet gold accents, serif headings, readable body text, and monospaced exact data. The original bookplate is decorative SVG; there is no game art, remote font service, or ambient animation.

mdBook remains the publishing engine. Its chapter navigation, search, saved theme preferences, copy controls, and print renderer remain in use. The older theme IDs are retained as palette aliases. A small enhancement script adds the book-home link, skip navigation, an outline based on existing headings, and keyboard access to wide code and tables. At wide desktop sizes the outline occupies the right margin; smaller screens use a native collapsible control after the introduction. The native sidebar outline remains a fallback when the enhancement is unavailable. The combined print page skips these additions.

The print styles use white paper, dark ink, wrapping examples, and no navigation or decoration. Palette selectors also override mdBook's more specific no-JavaScript fallback, which otherwise leaked dark table colors into print. Syntax tokens and visited binding links have explicit readable colors. The common workflow now checks every theme JavaScript file's syntax, and the theme maintenance guide records ownership and the browser review procedure.

The usability pass also corrected the native edit link. In mdBook `0.5.4`, `{path}` already includes the book source directory. Removing the extra `docs/` prevents links such as `docs/docs/README.md`; repository evidence links still resolve under `blob/main/`. Focused tests cover the revised contract and reject unsupported templates.

Validation:

- All 25 tests pass: eighteen Python tests and seven JavaScript tests. Navigation and reference freshness, all theme syntax checks, the pinned mdBook build, and 15,485 book/guide link and asset checks pass.
- An isolated checkout of the intended changes passes the same workflow with 15,483 link and asset checks. The two-link difference belongs to the owner's unrelated manual-action records. All 288 native edit links point to existing repository sources.
- Browser review covers Parchment and Lamplight, the homepage, walking explanation and figure, packet notation, general search, exact lookup, a function permalink, and its evidence citation. Phone layouts fit 375 CSS pixels without page-wide overflow; 640 CSS pixels exercise the reflow expected when a 1280 px view is magnified to 200%. Wide desktop review checks the margin outline and reading measure.
- Tab and Enter operate the skip link, outline, theme choice, and reference links. Arrow keys scroll wide code without changing chapters, and Tab exits the region. Copy activation displays mdBook's success feedback. The browser automation's clipboard bridge returns no text, so an independent clipboard round trip remains unverified.
- A browser proof of the print declarations shows dark text on white, readable tables, wrapped packet schemas, and hidden search/navigation controls. This proof does not establish real printer pagination. Native browser zoom and actual print pagination remain manual release checks; they are not claimed as tested here.
- Palette calculations meet 4.5:1 for normal text, links, muted text, and syntax tokens. Main text contrast is 11.87:1 on Parchment and 11.10:1 on Lamplight; the weakest assigned syntax color is 4.98:1. Reduced-motion rules remove transitions and animation.
- Only the homepage changes among existing reader Markdown files, adding the decorative opening and updating its contributor handoff. Technical chapters, packet pages and indexes, code examples, figures, and all 40 source exports remain unchanged. The owner's source and generated-reference edits remain intact.

Task 6 implementation is ready for review. mdBook supports this design without a platform migration. The final browser-only release checks above remain documented in the theme maintenance guide.
