#!/usr/bin/env python3
"""Build function-reference includes and exact lookup from the existing exports.

Only the repository's flat scalar target header and top-level function records
are read. Unsupported syntax fails explicitly; this is not a general YAML reader.
Binary Ninja and third-party packages are not required.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import html
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IMAGE_BASE = 0x00400000
TARGET = {
    "architecture": "x86", "file": "Darkages.exe", "image_base": "0x00400000",
    "reported_version": "741", "size": "3112960",
    "sha256": "054a5d6adc56099c6bfd9d2a58675aff62dc788b63209a3d906492f5b89e96c6",
}
GAME_LOOP_NAMES = {"app_run_message_loop", "app_window_proc", "event_dispatcher_tick"}
GROUPS = {
    "application": "Application lifecycle and configuration", "game-loop": "Game loop",
    "events": "Events", "input": "Input", "ui": "UI", "network": "Network",
    "rendering": "Rendering", "audio": "Audio", "maps-and-files": "Maps and files",
    "crypto": "Crypto", "uncertain": "Uncertain", "other": "Other",
}
REQUIRED = {"name", "address", "confidence", "evidence"}
OPTIONAL = {"rva", "prototype", "end_address"}


@dataclass(frozen=True)
class Record:
    fields: dict[str, str]
    source: str
    line: int

    @property
    def location(self) -> str:
        return f"{self.source}:{self.line}"


def scalar(text: str) -> str:
    value = text.strip()
    if value.startswith('"'):
        return str(json.loads(value))
    if value.startswith("'"):
        if not value.endswith("'"):
            raise ValueError("unterminated quoted scalar")
        return value[1:-1].replace("''", "'")
    if value in {"|", ">"} or value.startswith(("[", "{", "&", "*", "!")):
        raise ValueError(f"unsupported scalar syntax: {value}")
    return value


def hex_value(value: str) -> int:
    if not re.fullmatch(r"0[xX][0-9a-fA-F]{1,8}", value):
        raise ValueError(f"invalid 32-bit hexadecimal value: {value!r}")
    return int(value, 16)


def read_functions(path: Path) -> list[Record]:
    records: list[Record] = []
    target: dict[str, str] = {}
    version, section = "", ""
    sections = set()
    current: dict[str, str] | None = None
    start_line = 0
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            if not line.startswith(" "):
                if current is not None:
                    records.append(Record(current, path.name, start_line))
                    current = None
                key, _, value = line.partition(":")
                if key in sections:
                    raise ValueError(f"duplicate top-level field: {key}")
                sections.add(key)
                section = key
                if key == "schema_version":
                    version = scalar(value)
                if key == "functions" and value.strip() not in {"", "[]"}:
                    raise ValueError("functions must be a top-level list")
                continue
            if section == "target":
                field = re.fullmatch(r"  ([a-z_][a-z_0-9]*):\s*(.*)", line)
                if not field or field[1] in target:
                    raise ValueError("unsupported or duplicate target field")
                target[field[1]] = scalar(field[2])
            elif section == "functions":
                field = re.fullmatch(r"(  - |    )([a-z_]+):\s*(.*)", line)
                if not field:
                    raise ValueError("unsupported function field syntax")
                if field[1] == "  - ":
                    if current is not None:
                        records.append(Record(current, path.name, start_line))
                    current, start_line = {}, number
                if current is None or field[2] in current:
                    raise ValueError("orphan or duplicate function field")
                current[field[2]] = scalar(field[3])
        except (ValueError, TypeError) as error:
            raise ValueError(f"{path.name}:{number}: {error}") from error
    if current is not None:
        records.append(Record(current, path.name, start_line))
    if version != "1" or target != TARGET:
        raise ValueError(f"{path.name}: unsupported schema or mismatched target fingerprint")
    for record in records:
        fields = record.fields
        if not REQUIRED <= fields.keys() or any(not fields[key] for key in REQUIRED):
            raise ValueError(f"{record.location}: missing required function fields")
        if fields.keys() - REQUIRED - OPTIONAL:
            raise ValueError(f"{record.location}: unsupported function fields: {fields.keys() - REQUIRED - OPTIONAL}")
        if not re.fullmatch(r"[a-z_][a-z_0-9]*", fields["name"]):
            raise ValueError(f"{record.location}: invalid project name {fields['name']!r}")
        address = hex_value(fields["address"])
        if address < IMAGE_BASE:
            raise ValueError(f"{record.location}: address precedes preferred image base")
        for key in {"address", "rva", "end_address"} & fields.keys():
            fields[key] = f"0x{hex_value(fields[key]):08X}"
        if fields.get("rva") and hex_value(fields["rva"]) != address - IMAGE_BASE:
            raise ValueError(f"{record.location}: RVA does not match static address")
        if fields.get("end_address") and hex_value(fields["end_address"]) <= address:
            raise ValueError(f"{record.location}: invalid end address")
    return records


def group_for(name: str) -> str:
    if name in GAME_LOOP_NAMES:
        return "game-loop"
    for prefix, group in [
        ("app_", "application"), ("event_", "events"), ("input_", "input"),
        ("ui_", "ui"), ("net_", "network"), ("render_", "rendering"),
        ("audio_", "audio"), ("map_", "maps-and-files"), ("file_", "maps-and-files"),
        ("crypto_", "crypto"), ("maybe_", "uncertain"),
    ]:
        if name.startswith(prefix):
            return group
    return "other"


def anchor(name: str, address: str) -> str:
    return f"fn-{name}-{int(address, 16):08x}"


def cell(value: str) -> str:
    return html.escape(value, quote=False).replace("|", "&#124;").replace("\n", " ")


def collect(exports: Path) -> tuple[dict, list[tuple[str, list[tuple[str, str]]]]]:
    identities: dict[tuple[str, str], list[Record]] = defaultdict(list)
    paths = sorted(exports.glob("*.yaml"))
    if not paths:
        raise ValueError(f"no YAML exports in {exports}")
    for path in paths:
        for record in read_functions(path):
            identities[(record.fields["name"], record.fields["address"])].append(record)
    for key, records in identities.items():
        for field in OPTIONAL | {"confidence"}:
            values = {record.fields[field] for record in records if record.fields.get(field)}
            if len(values) > 1:
                locations = ", ".join(f"{r.location}={r.fields.get(field)!r}" for r in records)
                raise ValueError(f"conflicting {field} for {key}: {locations}")
    names: dict[str, list] = defaultdict(list)
    addresses: dict[str, list] = defaultdict(list)
    for key in sorted(identities):
        names[key[0]].append(key)
        addresses[key[1]].append(key)
    conflicts = [
        (f"One name, multiple addresses: `{name}`", keys)
        for name, keys in sorted(names.items()) if len(keys) > 1
    ] + [
        (f"One address, multiple names: `{address}`", keys)
        for address, keys in sorted(addresses.items()) if len(keys) > 1
    ]
    return dict(identities), conflicts


def render(exports: Path) -> dict[str, str]:
    identities, conflicts = collect(exports)
    conflict_keys = {key for _, keys in conflicts for key in keys}
    grouped = {group: [] for group in GROUPS}
    for key in identities:
        grouped[group_for(key[0])].append(key)
    outputs: dict[str, str] = {}
    lookup = []
    for group, keys in grouped.items():
        lines = [
            "<!-- Generated by scripts/build_function_reference.py; edit the YAML sources. -->",
            "", f"{len(keys):,} name/address entries. Static addresses use preferred image base `0x00400000`.",
            "", "Every export record is retained, including complementary evidence for the same identity. "
            "The linked YAML record contains any signature, function range, and deeper provenance. "
            "An identity warning records disagreement between exports; it does not establish an alias or a corrected name.",
            "", '<div class="function-reference">', "",
            "| Function | Static address | Confidence | Evidence and source |",
            "| --- | --- | --- | --- |",
        ]
        for name, address in sorted(keys, key=lambda k: (int(k[1], 16), k[0])):
            records = identities[(name, address)]
            is_conflict = (name, address) in conflict_keys
            function = f'<a id="{anchor(name, address)}"></a>`{name}`'
            if is_conflict:
                function += ' ([identity warning](../functions.md#identity-warnings))'
            evidence = "<br><br>".join(
                f"{cell(record.fields['evidence'])} "
                f"([{record.source}:{record.line}](../../../analysis/exports/{record.source}#L{record.line}))"
                for record in records
            )
            lines.append(f"| {function} | `{address}` | {cell(records[0].fields['confidence'])} | {evidence} |")
            lookup.append({
                "name": name, "address": address, "rva": f"0x{int(address, 16) - IMAGE_BASE:08X}",
                "url": f"functions/{group}.html#{anchor(name, address)}",
                "group": GROUPS[group], "conflict": is_conflict,
            })
        lines.extend(["", "</div>"])
        outputs[f"{group}.md"] = "\n".join(lines) + "\n"
    overview = [
        "<!-- Generated by scripts/build_function_reference.py; edit the YAML sources. -->", "",
        f"The reference retains **{len(identities):,} name/address entries** from "
        f"**{sum(map(len, identities.values())):,} export records**. All entries target the fingerprint below.", "",
        "| Group | Entries |", "| --- | ---: |",
    ]
    for group, label in GROUPS.items():
        old_anchor = label.lower().replace(" ", "-")
        overview.append(f'| <a id="{old_anchor}"></a>[{label}](functions/{group}.md) | {len(grouped[group]):,} |')
    outputs["overview.md"] = "\n".join(overview) + "\n"
    warnings = [
        "<!-- Generated by scripts/build_function_reference.py; edit the YAML sources. -->", "",
        "These exports disagree about identity. Keep both records until a focused Binary Ninja check resolves the difference. "
        "Repeated addresses are not automatically aliases, and repeated names are not automatically the same function.", "",
    ]
    for label, keys in conflicts:
        warnings += [f"- {label}."]
        for name, address in keys:
            sources = ", ".join(
                f"[{record.source}:{record.line}](../../analysis/exports/{record.source}#L{record.line})"
                for record in identities[(name, address)]
            )
            warnings.append(f"  - [`{name}` at `{address}`](functions/{group_for(name)}.md#{anchor(name, address)}): {sources}.")
    if not conflicts:
        warnings.append("No name/address identity disagreements were found.")
    outputs["identity-warnings.md"] = "\n".join(warnings) + "\n"
    # This derived browser payload is not a new analysis-export schema.
    payload = {"functions": sorted(lookup, key=lambda row: (row["name"], row["address"]))}
    outputs["index.json"] = json.dumps(payload, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c") + "\n"
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report stale output without writing")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args()
    destination = args.root / "generated" / "function-reference"
    try:
        outputs = render(args.root / "analysis" / "exports")
        stale = [name for name, text in outputs.items() if not (destination / name).exists() or (destination / name).read_text(encoding="utf-8") != text]
        extra = sorted(p.name for p in destination.glob("*") if p.is_file() and p.name not in outputs)
        if extra:
            raise ValueError(f"unexpected generated files; review before removing: {', '.join(extra)}")
        if args.check:
            for name in stale:
                print(f"stale: generated/function-reference/{name}")
            if stale:
                raise SystemExit(1)
            print("Function references and exact lookup are current; source metadata checks pass.")
        else:
            destination.mkdir(parents=True, exist_ok=True)
            for name in stale:
                (destination / name).write_text(outputs[name], encoding="utf-8")
            print(f"Updated {len(stale)} function-reference files.")
        _, conflicts = collect(args.root / "analysis" / "exports")
        if conflicts:
            print(f"{len(conflicts)} unresolved identity groups retained in the visible identity warnings.")
    except ValueError as error:
        print(f"Function reference: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
