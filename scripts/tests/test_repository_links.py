"""Check the source-to-published-link interface used by mdBook 0.5."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from book_repository_links import repository_base, rewrite
from check_book_links import audit, audit_guides, markdown_anchors, repository_target_error


class RepositoryLinkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.docs = self.root / "docs"
        self.docs.mkdir()
        self.source = self.root / "analysis/exports/evidence.yaml"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("schema_version: 1\n")
        self.tracked = {"analysis/exports/evidence.yaml"}
        self.base = "https://github.com/example/client/blob/main/"

    def convert(self, content):
        return rewrite(content, self.docs / "chapter.md", self.docs, self.root, self.tracked, self.base)

    def test_relative_evidence_links_keep_query_and_fragment(self):
        source = "[Evidence](../analysis/exports/evidence.yaml?plain=1#L2)"
        self.assertEqual("[Evidence](" + self.base + "analysis/exports/evidence.yaml?plain=1#L2)", self.convert(source))
        self.assertEqual("[Inside](chapter.md#one)", self.convert("[Inside](chapter.md#one)"))
        self.assertEqual("[External](https://example.com/x)", self.convert("[External](https://example.com/x)"))

    def test_code_is_literal_but_reference_definitions_and_html_links_publish(self):
        link = "[Evidence](../analysis/exports/evidence.yaml)"
        source = f"`{link}`\n```md\n{link}\n```\n    {link}\n"
        self.assertEqual(source, self.convert(source))
        self.assertIn(self.base, self.convert("[evidence]: ../analysis/exports/evidence.yaml\n"))
        self.assertIn(self.base, self.convert('<a href="../analysis/exports/evidence.yaml#L1">Source</a>'))

    def test_private_missing_and_outside_repository_paths_fail(self):
        for path in ["../client/Darkages.exe", "../analysis/missing.yaml", "../../outside.txt"]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.convert(f"[Source]({path})")

    def test_preprocessor_protocol_and_edit_ref(self):
        config = {"book": {"src": "docs"}, "output": {"html": {
            "edit-url-template": "https://github.com/example/client/edit/review/docs/{path}",
        }}}
        self.assertEqual("https://github.com/example/client/blob/review/", repository_base(config))
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "add", "analysis/exports/evidence.yaml"], cwd=self.root, check=True)
        chapter = {"Chapter": {"name": "Chapter", "source_path": "chapter.md", "path": "chapter.md", "content": "[Source](../analysis/exports/evidence.yaml#L1)", "sub_items": []}}
        payload = [{"root": str(self.root), "config": config}, {"items": [chapter]}]
        result = subprocess.run([sys.executable, str(SCRIPTS / "book_repository_links.py")], input=json.dumps(payload), capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("/blob/review/analysis/exports/evidence.yaml#L1", json.loads(result.stdout)["items"][0]["Chapter"]["content"])

    def test_rendered_audit_checks_alias_fragments_assets_and_source_lines(self):
        (self.root / "book.toml").write_text('[book]\nsrc="docs"\n[output.html]\nsite-url="/book/"\nedit-url-template="https://github.com/example/client/edit/main/docs/{path}"\n')
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "add", "analysis/exports/evidence.yaml"], cwd=self.root, check=True)
        book = self.root / "book"
        book.mkdir()
        (book / "guide.html").write_text('<h1 id="heading">Guide</h1>')
        (book / "alias.html").write_text('<meta http-equiv="refresh" content="0; URL=guide.html"><script>url.hash = window.location.hash;</script>')
        index = book / "index.html"
        index.write_text(f'<a href="/book/alias.html#heading">Alias</a><a href="{self.base}analysis/exports/evidence.yaml#L1">Source</a>')
        self.assertEqual([], audit(book, self.root)[1])
        index.write_text(f'<a href="guide.html#absent">Missing heading</a><img src="missing.svg"><a href="{self.base}analysis/exports/evidence.yaml#L9">Wrong source line</a>')
        errors = audit(book, self.root)[1]
        self.assertEqual(3, len(errors))
        self.assertTrue(any("missing heading" in error for error in errors))
        self.assertTrue(any("invalid source line" in error for error in errors))

    def test_guide_paths_must_be_existing_tracked_repository_files(self):
        guide = self.root / "CONTRIBUTING.md"
        guide.write_text("# Contributing\n[Evidence](analysis/exports/evidence.yaml#L1)\n")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "add", "CONTRIBUTING.md", "analysis/exports/evidence.yaml"], cwd=self.root, check=True)
        self.assertEqual((1, []), audit_guides(self.root))
        (self.root / "private.md").write_text("# Untracked\n")
        guide.write_text("[Missing](missing.md)\n[Private](private.md)\n[Escape](../outside.md)\n[Absolute](/CONTRIBUTING.md)\n")
        checked, errors = audit_guides(self.root)
        self.assertEqual(4, checked)
        self.assertEqual(4, len(errors))
        self.assertTrue(any("must be relative" in error for error in errors))
        self.assertTrue(all("CONTRIBUTING.md:" in error for error in errors))

    def test_guide_fragments_include_headings_explicit_ids_and_duplicate_suffixes(self):
        guide = self.root / "README.md"
        guide.write_text("# Start\n## Source *and* `data`\n## Source *and* `data`\n"
                         "Setext title\n------------\n<a id=\"stable\"></a><a name=\"legacy\"></a>\n"
                         "[First](#source-and-data) [Second](#source-and-data-1)\n"
                         "[Setext](#setext-title) [Explicit](#stable) [Legacy](#legacy)\n")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "add", "README.md"], cwd=self.root, check=True)
        self.assertEqual((5, []), audit_guides(self.root))
        guide.write_text(guide.read_text() + "[Absent](#missing) [Wrong duplicate](#source-and-data-2)\n")
        self.assertEqual(2, len(audit_guides(self.root)[1]))

    def test_code_examples_cannot_create_links_or_anchor_targets(self):
        source = ("# Guide\n`[Inline](missing-inline.md)`\n``[Nested `code`](missing-nested.md)``\n"
                  "```md\n[Example](missing-fenced.md)\n## Fake heading\n<a id=\"fake-id\"></a>\n```\n"
                  "~~~md\n[Example](missing-tilde.md)\n~~~\n"
                  "    [Indented](missing-indented.md)\n"
                  "`<a id=\"inline-id\"></a>`\n"
                  "[Remote](https://example.invalid/missing#fragment)\n")
        (self.root / "AGENTS.md").write_text(source)
        (self.root / "contributing").mkdir()
        (self.root / "contributing/review.md").write_text("[Guide](../AGENTS.md#guide)\n")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "add", "AGENTS.md", "contributing/review.md"], cwd=self.root, check=True)
        self.assertEqual((1, []), audit_guides(self.root))
        self.assertEqual({"guide"}, markdown_anchors(source))
        (self.root / "contributing/review.md").write_text("[guide]: ../AGENTS.md#fake-heading\n<a href=\"../AGENTS.md#fake-id\">Fake</a>\n")
        self.assertEqual(2, len(audit_guides(self.root)[1]))

    def test_rendered_repository_markdown_fragments_and_source_guides_are_audited(self):
        (self.root / "book.toml").write_text('[book]\nsrc="docs"\n[output.html]\nedit-url-template="https://github.com/example/client/edit/main/docs/{path}"\n')
        (self.root / "CONTRIBUTING.md").write_text("# Contributing\n## Review the result\n<a id=\"stable\"></a>\n")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "add", "CONTRIBUTING.md"], cwd=self.root, check=True)
        book = self.root / "book"
        book.mkdir()
        index = book / "index.html"
        index.write_text(f'<a href="{self.base}CONTRIBUTING.md#review-the-result">Heading</a><a href="{self.base}CONTRIBUTING.md#stable">Anchor</a>')
        self.assertEqual((2, []), audit(book, self.root))
        index.write_text(f'<a href="{self.base}CONTRIBUTING.md#missing">Bad heading</a>')
        (self.root / "CONTRIBUTING.md").write_text("# Contributing\n[Missing](missing.md)\n")
        checked, errors = audit(book, self.root)
        self.assertEqual(2, checked)
        self.assertEqual(2, len(errors))
        self.assertTrue(any("missing repository Markdown heading" in error for error in errors))
        self.assertTrue(any(error.startswith("CONTRIBUTING.md:") for error in errors))

    def test_many_source_line_links_read_each_evidence_file_once(self):
        cache = {}
        with patch.object(Path, "read_text", return_value="first\nsecond\n") as read:
            for fragment in ("L1", "L2", "L1-L2"):
                self.assertIsNone(repository_target_error(self.source, fragment, self.root, self.tracked, cache))
            read.assert_called_once()


if __name__ == "__main__":
    unittest.main()
