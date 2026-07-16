#!/usr/bin/env python3
"""Build the Markdown function reference from deterministic YAML exports.

The parser intentionally reads only the simple top-level `functions` lists used by
this repository. It avoids requiring Binary Ninja or a third-party YAML package.
"""

from __future__ import annotations

import ast
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "analysis" / "exports"
OUTPUT = ROOT / "docs" / "appendix" / "functions.md"

GAME_LOOP_NAMES = {
    "app_run_message_loop",
    "app_window_proc",
    "event_dispatcher_tick",
}

GROUPS = [
    "Application lifecycle and configuration",
    "Game loop",
    "Events",
    "Input",
    "UI",
    "Network",
    "Rendering",
    "Maps and files",
    "Crypto",
    "Uncertain",
    "Other",
]


def scalar(text: str) -> str:
    value = text.strip()
    if not value:
        return ""
    if value[0] in "'\"" and value[-1] == value[0]:
        return str(ast.literal_eval(value))
    return value


def read_functions(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    inside = False

    for line in path.read_text(encoding="utf-8").splitlines():
        if line == "functions:":
            inside = True
            continue
        if inside and line and not line.startswith(" "):
            break
        if not inside:
            continue

        start = re.match(r"^  - ([a-z_]+):\s*(.*)$", line)
        field = re.match(r"^    ([a-z_]+):\s*(.*)$", line)
        if start:
            if current:
                rows.append(current)
            current = {start.group(1): scalar(start.group(2))}
        elif field and current is not None:
            current[field.group(1)] = scalar(field.group(2))

    if current:
        rows.append(current)
    return rows


def group_for(name: str) -> str:
    if name in GAME_LOOP_NAMES:
        return "Game loop"
    if name.startswith("app_"):
        return "Application lifecycle and configuration"
    if name.startswith("event_"):
        return "Events"
    if name.startswith("input_"):
        return "Input"
    if name.startswith("ui_"):
        return "UI"
    if name.startswith("net_"):
        return "Network"
    if name.startswith("render_"):
        return "Rendering"
    if name.startswith(("map_", "file_")):
        return "Maps and files"
    if name.startswith("crypto_"):
        return "Crypto"
    if name.startswith("maybe_"):
        return "Uncertain"
    return "Other"


def short_role(evidence: str) -> str:
    role = evidence.split(". ", 1)[0].rstrip(".")
    role = html.escape(role, quote=False)
    return role.replace("|", "\\|").replace("\n", " ") + "."


def main() -> None:
    unique: dict[tuple[str, str], dict[str, str]] = {}
    for path in sorted(EXPORTS.glob("*.yaml")):
        for row in read_functions(path):
            if row.get("name") and row.get("address"):
                unique[(row["name"], row["address"])] = row

    grouped: dict[str, list[dict[str, str]]] = {name: [] for name in GROUPS}
    for row in unique.values():
        grouped[group_for(row["name"])].append(row)

    lines = [
        "# Function reference",
        "",
        "This appendix is the address book for functions named in the main text. "
        "Static addresses assume preferred image base `0x00400000`. At runtime, "
        "use the loaded module base and the matching RVA.",
        "",
        "Roles are short summaries from the checked-in Binary Ninja YAML exports. "
        "Those exports remain the source for full evidence and provenance.",
    ]

    for group in GROUPS:
        rows = sorted(grouped[group], key=lambda row: (int(row["address"], 16), row["name"]))
        if not rows:
            continue
        lines.extend([
            "",
            f"## {group}",
            "",
            "| Function | Static address | Confidence | Role |",
            "| --- | --- | --- | --- |",
        ])
        for row in rows:
            lines.append(
                f"| `{row['name']}` | `{row['address']}` | "
                f"{row.get('confidence', 'unknown')} | {short_role(row.get('evidence', ''))} |"
            )

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} with {len(unique)} functions")


if __name__ == "__main__":
    main()
