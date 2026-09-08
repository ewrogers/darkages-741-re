#!/usr/bin/env python3
"""Publish relative links to tracked repository files outside the book.

Run after mdBook's include preprocessor. Source Markdown stays useful in a clone;
published evidence links use the same repository/ref as the configured edit URL.
"""

import json
from html import unescape
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote, unquote, urlsplit


def repository_base(config: dict) -> str:
    template = config["output"]["html"]["edit-url-template"]
    suffix = "/" + config["book"]["src"].strip("/") + "/{path}"
    if "/edit/" not in template or not template.endswith(suffix):
        raise ValueError("edit-url-template must identify the repository ref and book source")
    return template[:-len(suffix)].replace("/edit/", "/blob/", 1) + "/"


def rewrite(content: str, chapter: Path, docs: Path, root: Path, tracked: set[str], base: str) -> str:
    def target(url: str) -> str:
        parsed = urlsplit(unescape(url))
        if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
            return url
        path = (chapter.parent / unquote(parsed.path)).resolve()
        if path.is_relative_to(docs):
            return url
        if not path.is_relative_to(root):
            raise ValueError(f"{chapter.name}: link escapes repository: {url}")
        relative = path.relative_to(root).as_posix()
        if relative not in tracked or not path.is_file():
            raise ValueError(f"{chapter.name}: outside-book link is not a tracked file: {url}")
        return urlsplit(base + quote(relative))._replace(query=parsed.query, fragment=parsed.fragment).geturl()

    return map_markdown_links(content, target)


def markdown_lines(content: str):
    """Yield source lines and whether they are outside fenced/indented examples."""
    fence = None
    for line in content.splitlines(keepends=True):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if marker:
            run = marker[1]
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            yield line, False
        else:
            yield line, not fence and not line.startswith(("    ", "\t"))


def map_markdown_links(content: str, target) -> str:
    """Visit the Markdown/reference/HTML destinations used by repository guides.

    This deliberately shares the publisher's scanner, rather than treating every
    path-looking string in examples as a link.
    """
    # Restrict rewriting to actual link destinations. Fenced and inline code are
    # left alone so examples of repository paths remain literal examples.
    inline = re.compile(r'(`+)(.*?)(\1)|(?P<link>!?\[[^\]\n]*\]\()(?P<url>[^\s)]+)(?P<end>\))|(?P<attr>\bhref=["\x27])(?P<htmlurl>[^"\x27]+)(?P<quote>["\x27])')
    reference = re.compile(r'^( {0,3}\[[^\]]+\]:\s*)(\S+)(.*)$')

    def replace(match: re.Match) -> str:
        if match.group("link"):
            return match.group("link") + target(match.group("url")) + match.group("end")
        if match.group("attr"):
            return match.group("attr") + target(match.group("htmlurl")) + match.group("quote")
        return match.group(0)

    output = []
    for line, prose in markdown_lines(content):
        if not prose:
            output.append(line)
            continue
        ref = reference.match(line.rstrip("\n"))
        if ref:
            output.append(ref[1] + target(ref[2]) + ref[3] + ("\n" if line.endswith("\n") else ""))
        else:
            output.append(inline.sub(replace, line))
    return "".join(output)


def markdown_links(content: str) -> list[str]:
    links = []

    def collect(url):
        links.append(unescape(url))
        return url

    map_markdown_links(content, collect)
    return links


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "supports":
        raise SystemExit(0 if len(sys.argv) > 2 and sys.argv[2] == "html" else 1)
    context, book = json.load(sys.stdin)
    root = Path(context["root"]).resolve()
    docs = (root / context["config"]["book"]["src"]).resolve()
    files = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    tracked = set(files)
    base = repository_base(context["config"])

    def walk(items: list) -> None:
        for item in items:
            chapter = item.get("Chapter") if isinstance(item, dict) else None
            if chapter:
                source = chapter.get("source_path") or chapter.get("path")
                if source:
                    chapter["content"] = rewrite(chapter["content"], docs / source, docs, root, tracked, base)
                walk(chapter["sub_items"])

    walk(book["items"])
    json.dump(book, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError) as error:
        print(f"Repository links: {error}", file=sys.stderr)
        raise SystemExit(1) from error
