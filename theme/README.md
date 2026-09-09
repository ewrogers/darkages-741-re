# Grimoire presentation

The book uses mdBook with a neutral paper and brown grimoire palette. Parchment combines pale paper with brown ink and a muted brown binding. Lamplight uses warm charcoal reading surfaces, cream text, and subdued brass links. Technical language, exact data, and reading routes remain independent of the decoration. This directory contains the maintained presentation sources; generated HTML stays outside the source tree.

## Ownership

- [book.toml](../book.toml) selects the assets and default theme. Keep mdBook's chapter navigation, search, theme storage, copy buttons, and print renderer.
- [grimoire.css](grimoire.css) owns palette, typography, binding, local outline, responsive spacing, focus, and print overrides. It loads after the existing diagram and function-reference styles.
- [grimoire.js](grimoire.js) adds the home link, skip link, local heading outline, and keyboard access to overflowing code and tables. Heading IDs and source text stay unchanged. The combined print page skips these additions.
- [bookplate.svg](../docs/assets/ornaments/bookplate.svg) is original decorative artwork. It conveys no technical information. Fonts and assets are local; the theme requires no CDN, framework, or game art.
- [diagrams.js](diagrams.js) and [function-lookup.js](function-lookup.js) retain their existing controls. Follow the [authoring guide](../contributing/authoring.md) for figures and technical examples.

Parchment uses mdBook's `light` preference; Lamplight uses `navy`. The existing `rust`, `coal`, and `ayu` IDs remain as palette aliases so saved preferences and native menu keyboard handling still work. Auto follows the operating-system preference. Do not remove native theme buttons without revisiting mdBook's cached menu logic.

Keep backgrounds behind prose and code plain. Use serif type for headings and monospace for exact data. Ornament belongs on the binding and chapter openings. Do not rename technical concepts to fit the theme. Keep normal text and syntax-token contrast at least 4.5:1, including visited links, tables, muted captions, and theme aliases. No ambient animation is needed; respect reduced motion.

## Validate a presentation change

Run the [common checks](../CONTRIBUTING.md#run-the-checks), then inspect the built book in a browser:

1. Check Parchment and Lamplight, a saved alias, and Auto. Check the front page, a long chapter, a packet schema, a figure, and the exact function lookup.
2. Inspect a wide desktop, a 375 px phone, and 200% zoom. Verify reflow, readable text, sidebar access, and local outlines without page-wide horizontal scrolling. If the browser cannot set native zoom, record an equivalent narrow CSS viewport as a reflow check and state that native zoom remains unverified.
3. Use Tab and Enter for skip, theme, outline, search, and copy controls. Scroll wide code and tables with arrow keys, then Tab out. Arrow keys inside a scroll region must not change chapters. Check copied text against the displayed source.
4. Follow general search into exact lookup, a function permalink, and its evidence source. Check the edit link against the actual repository path.
5. Inspect print output with search open. Remove navigation and decoration, keep technical content, and allow long examples to wrap across pages. Check real print pagination when a print-capable browser is available; a screen proof of print styles does not establish pagination.

At 1500 px and wider, local contents occupy the right margin. Smaller screens use a native collapsible outline after the introduction. Only overflowing code and tables join the tab order. Without the enhancement script, the source content and native mdBook navigation remain available.
