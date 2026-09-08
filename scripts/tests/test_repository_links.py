"""Check the source-to-published-link interface used by mdBook 0.5."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from book_repository_links import repository_base, rewrite
from check_book_links import audit


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


if __name__ == "__main__":
    unittest.main()
