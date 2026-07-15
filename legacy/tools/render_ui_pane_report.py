#!/usr/bin/env python3

from pathlib import Path
import argparse
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ida" / "exports" / "ui-pane-classes.yaml"
OUTPUT = ROOT / "docs" / "ui" / "pane-classes.md"


def code(value):
    return f"`{str(value).replace('|', '\\|').replace('`', '\\`')}`"


def render_layouts(item):
    layouts = item.get("layouts", [])
    if not layouts:
        return "unknown"
    values = []
    for layout in layouts:
        values.append(f"{layout['archive']}:{layout['entry']}")
    return "<br>".join(code(value) for value in values)


def render_context(item):
    parts = []
    if item.get("category"):
        parts.append(item["category"])
    for role, function in item.get("functions", {}).items():
        parts.append(f"{role}: {function['name']} at {function['address']}")
    if item.get("notes"):
        parts.append(item["notes"])
    if not parts:
        return "RTTI name only"
    return "<br>".join(part.replace("|", "\\|") for part in parts)


def render(data):
    classes = data["classes"]
    concrete = [item for item in classes if item["kind"] == "concrete"]
    templates = [item for item in classes if item["kind"] != "concrete"]
    contextual = [
        item for item in classes
        if item.get("layouts") or item.get("functions") or item.get("notes")
    ]

    lines = [
        "# UI pane class catalog",
        "",
        "The version-741 executable retains Microsoft Visual C++ RTTI names for much of its UI hierarchy. This gives us the company\'s class names even when function symbols are absent.",
        "",
        "The machine-readable source is `ida/exports/ui-pane-classes.yaml`. Addresses are static virtual addresses of RTTI type-name strings, not object instances or vtables.",
        "",
        "## Scope",
        "",
        f"- RTTI records containing `Pane`: `{len(classes)}`",
        f"- Concrete class records: `{len(concrete)}`",
        f"- Template and singleton wrapper records: `{len(templates)}`",
        f"- Records with recovered layout or usage context: `{len(contextual)}`",
        "",
        "The wrapper records are useful. A `Singleton<T>` record is evidence that the engine manages one shared instance of `T`, but it is not a second pane implementation.",
        "",
        "Layout associations are listed only when the local executable references that archive entry from the construction path, or when the class and layout relationship is otherwise direct. See [declarative layout files](layout-files.md) for the format and archive inventory.",
        "",
        "## Classes",
        "",
        "| Internal class | RTTI address | Kind | Layout archive entry | Recovered context |",
        "|---|---:|---|---|---|",
    ]

    for item in classes:
        kind = "class" if item["kind"] == "concrete" else "wrapper"
        lines.append(
            f"| {code(item['name'])} | {code(item['address'])} | {kind} | "
            f"{render_layouts(item)} | {render_context(item)} |"
        )

    lines.extend([
        "",
        "## Updating the export",
        "",
        "With the matching executable available locally, run:",
        "",
        "```powershell",
        "python tools/export_ui_pane_classes.py C:\\path\\to\\Darkages.exe",
        "python tools/render_ui_pane_report.py",
        "```",
        "",
        "The exporter verifies the executable hash and preserves curated context fields already present in the YAML. Do not commit the executable or extracted game assets.",
        "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the committed report does not match the YAML export",
    )
    args = parser.parse_args()

    data = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))
    names = [item["name"] for item in data["classes"]]
    if names != sorted(names, key=str.lower):
        print("UI pane class export must be sorted by name.")
        return 1
    expected = render(data)

    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            print("UI pane report is stale. Run tools/render_ui_pane_report.py.")
            return 1
        print(f"UI pane report is current for {len(data['classes'])} records.")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(data['classes'])} records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
