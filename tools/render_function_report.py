#!/usr/bin/env python3

from pathlib import Path
import argparse
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ida" / "exports" / "functions.yaml"
OUTPUT = ROOT / "docs" / "functions" / "README.md"


def markdown_code(value):
    if value is None or value == "":
        return "unknown"
    return f"`{value.replace('|', '\\|').replace('`', '\\`')}`"


def render(data):
    functions = sorted(data["functions"], key=lambda item: item["name"])
    known_signatures = sum(1 for item in functions if item["signature"])
    target = data["target"]
    export = data["export"]

    lines = [
        "# Friendly function index",
        "",
        "This report preserves useful IDA names without committing the binary database. It is generated from `ida/exports/functions.yaml` and sorted by function name.",
        "",
        "## Scope",
        "",
        f"- Target: `{target['file']}` reporting version `{target['reported_version']}`",
        f"- Preferred image base: `{target['preferred_image_base']}`",
        f"- Friendly functions exported: `{len(functions)}`",
        f"- Functions with an IDA-inferred signature: `{known_signatures}`",
        f"- Functions still using an unknown signature: `{len(functions) - known_signatures}`",
        f"- Total functions in the IDA database at export time: `{export['total_database_functions']}`",
        "",
        "The report includes friendly subsystem names such as `net_`, `ui_`, `render_`, `audio_`, and `config_`. Generic `sub_...` functions, imports, compiler helpers, and library symbols are excluded until they receive a project name.",
        "",
        "## Reading the report",
        "",
        "Addresses are static virtual addresses from the IDA database. If the module is relocated at runtime, subtract the preferred image base and add the actual module base.",
        "",
        "Signatures come from IDA type information. They are useful working assumptions, not recovered source declarations. `unknown` means IDA does not currently have a useful prototype. Verify important calling conventions and arguments against callers, stack cleanup, register use, and disassembly before relying on them.",
        "",
        "A function name records the current project interpretation. Names beginning with `maybe_` are intentionally provisional.",
        "",
        "## Contributing function discoveries",
        "",
        "When you identify or improve a function:",
        "",
        "1. Rename and comment it in IDA using the repository [agent conventions](https://github.com/ewrogers/darkages-re-741/blob/main/AGENTS.md).",
        "2. Add or update its entry in `ida/exports/functions.yaml`.",
        "3. Preserve the static address and function size.",
        "4. Export the IDA prototype when useful. Use `null` when the signature is not known.",
        "5. Run `python tools/render_function_report.py`.",
        "6. Update any focused subsystem or packet documentation affected by the discovery.",
        "7. Run `python tools/check_docs.py` and `mdbook build`.",
        "",
        "Keep the YAML function list sorted by `name`. New subsystem prefixes are welcome when they are clear and consistently applied.",
        "",
        "## Functions",
        "",
        "| Function | Address | Size | IDA-inferred signature |",
        "|---|---:|---:|---|",
    ]

    for function in functions:
        lines.append(
            f"| `{function['name']}` | `{function['address']}` | "
            f"`{function['size']}` | {markdown_code(function['signature'])} |"
        )

    lines.append("")
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
    names = [item["name"] for item in data["functions"]]
    if names != sorted(names):
        print("Function export must be sorted by name.")
        return 1
    if len(names) != len(set(names)):
        print("Function export contains a duplicate name.")
        return 1
    expected = render(data)

    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            print("Function report is stale. Run tools/render_function_report.py.")
            return 1
        print(f"Function report is current for {len(data['functions'])} functions.")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(data['functions'])} functions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
