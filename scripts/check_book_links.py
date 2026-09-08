#!/usr/bin/env python3
"""Check rendered book links and canonical repository contributor guides.

Repository URLs are checked against local tracked source files, not the network.
The combined print page is checked for images but not ambiguous duplicate headings.
"""

import argparse
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
import tomllib
from urllib.parse import unquote, urlsplit

from book_repository_links import markdown_lines, markdown_links, repository_base

ROOT = Path(__file__).resolve().parents[1]
GUIDES = (
    "README.md", "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md",
    "analysis/README.md", "analysis/exports/README.md",
    "binaryninja/README.md", "scripts/README.md", "theme/README.md",
)


class MarkdownHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])


def markdown_anchors(content: str) -> set[str]:
    """Collect GitHub-style ATX/Setext heading IDs and explicit HTML anchors.

    These cover the repository's Markdown conventions; this is not a renderer
    for arbitrary CommonMark extensions. Literal code cannot define an anchor.
    """
    anchors, used = set(), set()
    html = MarkdownHTML()
    previous = ""
    for line, prose in markdown_lines(content):
        if not prose:
            previous = ""
            continue
        html.feed(re.sub(r'(`+).*?\1', '', line))
        atx = re.match(r'^ {0,3}#{1,6}(?:\s+|$)(.*)', line)
        if atx:
            heading = re.sub(r'\s+#+\s*$', '', atx[1]).strip()
        elif previous.strip() and re.fullmatch(r' {0,3}(?:=+|-+)\s*', line):
            heading = previous.strip()
        else:
            previous = line
            continue
        # Inline code contributes its text. Link labels do too; destinations do
        # not. HTML tags and Markdown decoration do not contribute punctuation.
        heading = re.sub(r'!?\[([^\]]+)\]\([^)]*\)', r'\1', heading)
        heading = unescape(re.sub(r'<[^>]*>', '', heading)).replace('`', '')
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        anchor, suffix = slug, 0
        while anchor in used:
            suffix += 1
            anchor = f"{slug}-{suffix}"
        used.add(anchor)
        anchors.add(anchor)
        previous = ""
    return anchors | html.ids


def tracked_files(root: Path) -> set[str]:
    return set(subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0"))


def repository_target_error(target: Path, fragment: str, root: Path, tracked: set[str], cache: dict):
    if not target.is_relative_to(root) or target.relative_to(root).as_posix() not in tracked or not target.is_file():
        return "missing tracked repository file"
    if not fragment:
        return None
    if target.suffix.lower() == ".md":
        if target not in cache:
            cache[target] = markdown_anchors(target.read_text(encoding="utf-8"))
        if fragment in cache[target]:
            return None
        if not fragment.startswith("L"):
            return "missing repository Markdown heading or anchor"
    if fragment.startswith("L"):
        match = re.fullmatch(r"L(\d+)(?:-L(\d+))?", fragment)
        if not match:
            return "invalid source line target"
        line_key = (target, "lines")
        if line_key not in cache:
            try:
                cache[line_key] = len(target.read_text(encoding="utf-8").splitlines())
            except UnicodeError:
                return "invalid source line target"
        count = cache[line_key]
        if not 1 <= int(match[1]) <= int(match[2] or match[1]) <= count:
            return "invalid source line target"
    return None


def audit_guides(root: Path, tracked: set[str] | None = None, cache: dict | None = None) -> tuple[int, list[str]]:
    """Check existing canonical source guides, independently of an mdBook build."""
    root = root.resolve()
    tracked = tracked_files(root) if tracked is None else tracked
    cache = {} if cache is None else cache
    guides = [root / name for name in GUIDES] + sorted((root / "contributing").glob("*.md"))
    checked, errors = 0, []
    for guide in guides:
        if not guide.is_file():
            continue
        for link in set(markdown_links(guide.read_text(encoding="utf-8"))):
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            checked += 1
            if parsed.path.startswith("/"):
                failure = "repository guide link must be relative"
            else:
                target = (guide.parent / unquote(parsed.path)).resolve() if parsed.path else guide
                failure = repository_target_error(target, unquote(parsed.fragment), root, tracked, cache)
            if failure:
                errors.append(f"{guide.relative_to(root)}: {link}: {failure}")
    return checked, sorted(set(errors))


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.links, self.images, self.assets = set(), [], [], []
        self.redirect = None
        self.source = path.read_text(encoding="utf-8")
        self.feed(self.source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "img" and attrs.get("src"):
            self.images.append(attrs["src"])
        if tag == "script" and attrs.get("src"):
            self.assets.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "stylesheet" and attrs.get("href"):
            self.assets.append(attrs["href"])
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            match = re.search(r"url=(.+)$", attrs.get("content", ""), re.I)
            if match:
                self.redirect = match[1]


def audit(book: Path, root: Path) -> tuple[int, list[str]]:
    book, root = book.resolve(), root.resolve()
    config = tomllib.loads((root / "book.toml").read_text())
    site_path = config["output"]["html"].get("site-url", "/")
    repository = repository_base(config)
    tracked = tracked_files(root)
    pages = {path.resolve(): Page(path) for path in book.rglob("*.html")}
    if not pages:
        return 0, [f"No HTML pages in {book}"]
    cache = {}
    checked, errors = audit_guides(root, tracked, cache)
    for source, page in pages.items():
        links = page.images + page.assets
        if source.name not in {"print.html", "toc.html"}:
            links += page.links
        for link in set(links):
            parsed = urlsplit(link)
            failure = None
            if link.startswith(repository):
                checked += 1
                relative = unquote(urlsplit(link[len(repository):]).path)
                target = (root / relative).resolve()
                failure = repository_target_error(target, unquote(parsed.fragment), root, tracked, cache)
            elif parsed.scheme or parsed.netloc:
                continue
            else:
                checked += 1
                if parsed.path.startswith("/"):
                    target = book / unquote(parsed.path.removeprefix(site_path).lstrip("/"))
                else:
                    target = source.parent / unquote(parsed.path) if parsed.path else source
                target = target.resolve()
                fragment, visited = unquote(parsed.fragment), set()
                while target in pages and pages[target].redirect:
                    if target in visited:
                        failure = "redirect cycle"
                        break
                    visited.add(target)
                    redirect = pages[target]
                    if fragment and "url.hash = window.location.hash" not in redirect.source:
                        failure = "redirect loses heading fragment"
                        break
                    destination = urlsplit(redirect.redirect)
                    target = (target.parent / unquote(destination.path)).resolve()
                    fragment = unquote(destination.fragment) or fragment
                if failure is None:
                    if not target.is_file() or not target.is_relative_to(book):
                        failure = "missing book target"
                    elif fragment and target in pages and fragment not in pages[target].ids:
                        failure = "missing heading or anchor"
            if failure:
                errors.append(f"{source.relative_to(book)}: {link}: {failure}")
    return checked, sorted(set(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book", nargs="?", type=Path, default=ROOT / "book")
    args = parser.parse_args()
    checked, errors = audit(args.book, ROOT)
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Checked {checked:,} book/guide links and assets; {len(errors)} failures.")
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
