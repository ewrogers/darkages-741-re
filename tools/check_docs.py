#!/usr/bin/env python3

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SUMMARY = DOCS / "SUMMARY.md"

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SUMMARY_LINK = re.compile(r"^\s*-?\s*\[[^\]]+\]\(([^)]+\.md)\)\s*$")
PACKET_NAME = re.compile(r"^(\d{3})-0x([0-9a-f]{2})-[a-z0-9-]+\.md$")

ALLOWED_FENCES = {
    "",
    "c",
    "cpp",
    "json",
    "powershell",
    "sh",
    "shell",
    "text",
    "toml",
    "yaml",
}


def is_emoji(character):
    value = ord(character)
    return (
        0x1F300 <= value <= 0x1FAFF
        or 0x2600 <= value <= 0x27BF
    )


def relative_name(path):
    return path.relative_to(ROOT).as_posix()


def check_style(path, text, errors):
    if chr(0x2013) in text or chr(0x2014) in text:
        errors.append(f"{relative_name(path)}: contains an en or em dash")

    if any(is_emoji(character) for character in text):
        errors.append(f"{relative_name(path)}: contains an emoji")

    inside_fence = False
    opening_line = 0
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.startswith("```"):
            continue

        if inside_fence:
            inside_fence = False
            continue

        language = line[3:].strip().split(",", 1)[0]
        if language not in ALLOWED_FENCES:
            errors.append(
                f"{relative_name(path)}:{line_number}: "
                f"unsupported code fence language {language!r}"
            )
        inside_fence = True
        opening_line = line_number

    if inside_fence:
        errors.append(
            f"{relative_name(path)}:{opening_line}: unclosed code fence"
        )


def check_links(path, text, errors):
    for match in MARKDOWN_LINK.finditer(text):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]

        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if target.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", target):
            errors.append(
                f"{relative_name(path)}: local link must be relative: {target}"
            )
            continue

        file_part = target.split("#", 1)[0]
        if not file_part:
            continue

        resolved = (path.parent / file_part).resolve()
        if not resolved.exists():
            errors.append(
                f"{relative_name(path)}: broken local link: {target}"
            )


def check_summary(errors):
    if not SUMMARY.exists():
        errors.append("docs/SUMMARY.md: missing mdBook table of contents")
        return

    included = set()
    for line in SUMMARY.read_text(encoding="utf-8").splitlines():
        match = SUMMARY_LINK.match(line)
        if match:
            included.add(Path(match.group(1)).as_posix())

    expected = {
        path.relative_to(DOCS).as_posix()
        for path in DOCS.rglob("*.md")
        if path != SUMMARY
    }

    for path in sorted(expected - included):
        errors.append(f"docs/SUMMARY.md: chapter is missing: {path}")
    for path in sorted(included - expected):
        errors.append(f"docs/SUMMARY.md: chapter does not exist: {path}")


def check_packet_files(errors):
    combined_index = (DOCS / "network" / "README.md").read_text(
        encoding="utf-8"
    )
    for direction in ("client", "server"):
        packet_dir = DOCS / "network" / direction
        direction_index = (packet_dir / "README.md").read_text(
            encoding="utf-8"
        )
        for path in sorted(packet_dir.glob("*.md")):
            if path.name == "README.md":
                continue

            match = PACKET_NAME.match(path.name)
            if not match:
                errors.append(
                    f"{relative_name(path)}: invalid packet filename"
                )
                continue

            decimal_text, hex_text = match.groups()
            if int(decimal_text) != int(hex_text, 16):
                errors.append(
                    f"{relative_name(path)}: decimal and hex opcodes differ"
                )

            lines = path.read_text(encoding="utf-8").splitlines()
            expected = f"# {decimal_text} / 0x{hex_text}:"
            if not lines or not lines[0].lower().startswith(expected):
                errors.append(
                    f"{relative_name(path)}: heading must start with {expected}"
                )

            if path.name not in direction_index:
                errors.append(
                    f"{relative_name(path)}: missing from direction index"
                )
            if f"{direction}/{path.name}" not in combined_index:
                errors.append(
                    f"{relative_name(path)}: missing from combined index"
                )


def main():
    errors = []
    files = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "CLAUDE.md",
        ROOT / "ida" / "README.md",
        *sorted(DOCS.rglob("*.md")),
        *sorted(DOCS.rglob("*.c")),
        *sorted(DOCS.rglob("*.h")),
    ]

    for path in files:
        text = path.read_text(encoding="utf-8")
        check_style(path, text, errors)
        if path.suffix == ".md":
            check_links(path, text, errors)

    if list(ROOT.rglob("*.cs")):
        errors.append("C# files remain; protocol references should use C or C++")

    check_summary(errors)
    check_packet_files(errors)

    if errors:
        for error in errors:
            print(error)
        return 1

    print(f"Documentation checks passed for {len(files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
