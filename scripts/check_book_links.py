#!/usr/bin/env python3
"""Check rendered local targets, fragments, assets, and repository evidence links.

Repository URLs are checked against local tracked source files, not the network.
The combined print page is checked for images but not ambiguous duplicate headings.
"""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
import tomllib
from urllib.parse import unquote, urlsplit

from book_repository_links import repository_base

ROOT = Path(__file__).resolve().parents[1]


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
    tracked = set(subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0"))
    pages = {path.resolve(): Page(path) for path in book.rglob("*.html")}
    if not pages:
        return 0, [f"No HTML pages in {book}"]
    checked, errors, source_lines = 0, [], {}
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
                if relative not in tracked or not target.is_file() or not target.is_relative_to(root):
                    failure = "missing tracked repository file"
                elif parsed.fragment.startswith("L"):
                    match = re.fullmatch(r"L(\d+)(?:-L(\d+))?", parsed.fragment)
                    if target not in source_lines:
                        source_lines[target] = len(target.read_text().splitlines())
                    if not match or not 1 <= int(match[1]) <= int(match[2] or match[1]) <= source_lines[target]:
                        failure = "invalid source line target"
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
    print(f"Checked {checked:,} rendered links and assets; {len(errors)} failures.")
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
