#!/usr/bin/env python3

from pathlib import Path
import argparse
import hashlib
import re
import struct
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "ida" / "exports" / "ui-pane-classes.yaml"
TYPE_DESCRIPTOR = re.compile(rb"\.\?AV[ -~]{1,255}\x00")


def read_u16(data, offset):
    return struct.unpack_from("<H", data, offset)[0]


def read_u32(data, offset):
    return struct.unpack_from("<I", data, offset)[0]


def parse_pe(data):
    if data[:2] != b"MZ":
        raise ValueError("input is not a PE file")

    pe_offset = read_u32(data, 0x3C)
    if data[pe_offset:pe_offset + 4] != b"PE\x00\x00":
        raise ValueError("input has no PE signature")

    coff = pe_offset + 4
    section_count = read_u16(data, coff + 2)
    optional_size = read_u16(data, coff + 16)
    optional = coff + 20
    if read_u16(data, optional) != 0x10B:
        raise ValueError("only PE32 images are supported")

    image_base = read_u32(data, optional + 28)
    sections = []
    section_table = optional + optional_size
    for index in range(section_count):
        entry = section_table + index * 40
        name = data[entry:entry + 8].split(b"\x00", 1)[0].decode("ascii")
        virtual_size = read_u32(data, entry + 8)
        virtual_address = read_u32(data, entry + 12)
        raw_size = read_u32(data, entry + 16)
        raw_offset = read_u32(data, entry + 20)
        sections.append({
            "name": name,
            "virtual_size": virtual_size,
            "virtual_address": virtual_address,
            "raw_size": raw_size,
            "raw_offset": raw_offset,
        })
    return image_base, sections


def file_offset_to_va(offset, image_base, sections):
    for section in sections:
        start = section["raw_offset"]
        end = start + section["raw_size"]
        if start <= offset < end:
            return image_base + section["virtual_address"] + offset - start
    return image_base + offset


def decode_scope(encoded):
    parts = [part for part in encoded.split("@") if part]
    return "::".join(reversed(parts))


def readable_name(rtti):
    singleton = re.fullmatch(r"\.\?AV\?\$Singleton@V(.+)@@@@", rtti)
    if singleton:
        return f"Singleton<{decode_scope(singleton.group(1))}>"

    new_inventory = re.fullmatch(
        r"\.\?AV\?\$NewInventoryPane@V(.+)@@@@",
        rtti,
    )
    if new_inventory:
        return f"NewInventoryPane<{decode_scope(new_inventory.group(1))}>"

    tab_pane = re.fullmatch(r"\.\?AV\?\$TabPane@U(.+)@@@@", rtti)
    if tab_pane:
        return f"TabPane<{decode_scope(tab_pane.group(1))}>"

    if rtti.startswith(".?AV") and rtti.endswith("@@"):
        body = rtti[4:-2]
        if not body.startswith("?$"):
            return decode_scope(body)
    return rtti


def load_existing():
    if not OUTPUT.exists():
        return {}
    data = yaml.safe_load(OUTPUT.read_text(encoding="utf-8")) or {}
    return {
        item["rtti"]: item
        for item in data.get("classes", [])
    }


def scan(binary):
    data = binary.read_bytes()
    image_base, sections = parse_pe(data)
    old = load_existing()
    classes = []

    for match in TYPE_DESCRIPTOR.finditer(data):
        rtti = match.group(0)[:-1].decode("ascii")
        if "Pane" not in rtti or not rtti.endswith("@@"):
            continue

        address = file_offset_to_va(match.start(), image_base, sections)
        item = {
            "name": readable_name(rtti),
            "address": f"0x{address:x}",
            "kind": "template_instantiation" if "?$" in rtti else "concrete",
            "rtti": rtti,
        }
        previous = old.get(rtti, {})
        for key, value in previous.items():
            if key not in item:
                item[key] = value
        classes.append(item)

    classes.sort(key=lambda item: (item["name"].lower(), item["address"]))
    return data, image_base, classes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("binary", type=Path, help="path to the version-741 Darkages.exe")
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail unless the checked-in export has the same RTTI records",
    )
    args = parser.parse_args()

    binary = args.binary.resolve()
    data, image_base, classes = scan(binary)
    digest = hashlib.sha256(data).hexdigest().upper()
    expected_digest = "054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6"
    if digest != expected_digest:
        print(f"Unexpected executable SHA-256: {digest}")
        return 1

    document = {
        "schema_version": 1,
        "target": {
            "file": binary.name,
            "reported_version": 741,
            "sha256": digest,
            "preferred_image_base": f"0x{image_base:x}",
        },
        "export": {
            "source": "MSVC RTTI type descriptor strings in the local executable",
            "class_count": len(classes),
        },
        "classes": classes,
    }

    if args.check:
        if not OUTPUT.exists():
            print("UI pane class export is missing.")
            return 1
        current = yaml.safe_load(OUTPUT.read_text(encoding="utf-8"))
        current_records = [
            (item["rtti"], item["address"])
            for item in current.get("classes", [])
        ]
        expected_records = [
            (item["rtti"], item["address"])
            for item in classes
        ]
        if current_records != expected_records:
            print("UI pane RTTI export is stale.")
            return 1
        print(f"UI pane RTTI export is current for {len(classes)} records.")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        yaml.safe_dump(document, sort_keys=False, width=1000),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(classes)} RTTI records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
