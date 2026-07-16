#!/usr/bin/env python3
"""Export the x86 MSVC RTTI hierarchy for every Pane-derived class."""

from __future__ import annotations

import argparse
import hashlib
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TARGET_SIZE = 3_112_960
TARGET_SHA256 = "054a5d6adc56099c6bfd9d2a58675aff62dc788b63209a3d906492f5b89e96c6"


@dataclass(frozen=True)
class Section:
    name: str
    virtual_address: int
    virtual_size: int
    file_offset: int
    file_size: int


class PEImage:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = path.read_bytes()
        pe_offset = self.u32_file(0x3C)
        if self.data[pe_offset : pe_offset + 4] != b"PE\0\0":
            raise ValueError("not a PE image")

        file_header = pe_offset + 4
        machine, section_count = struct.unpack_from("<HH", self.data, file_header)
        optional_size = struct.unpack_from("<H", self.data, file_header + 16)[0]
        optional = file_header + 20
        if machine != 0x14C or self.u16_file(optional) != 0x10B:
            raise ValueError("expected a 32-bit x86 PE image")
        self.image_base = self.u32_file(optional + 28)

        self.sections: list[Section] = []
        section_table = optional + optional_size
        for index in range(section_count):
            offset = section_table + index * 40
            raw_name = self.data[offset : offset + 8].split(b"\0", 1)[0]
            virtual_size, virtual_address, file_size, file_offset = struct.unpack_from(
                "<IIII", self.data, offset + 8
            )
            self.sections.append(
                Section(
                    raw_name.decode("ascii", errors="replace"),
                    virtual_address,
                    virtual_size,
                    file_offset,
                    file_size,
                )
            )

    def u16_file(self, offset: int) -> int:
        return struct.unpack_from("<H", self.data, offset)[0]

    def u32_file(self, offset: int) -> int:
        return struct.unpack_from("<I", self.data, offset)[0]

    def va_to_file(self, address: int) -> int | None:
        rva = address - self.image_base
        for section in self.sections:
            span = max(section.virtual_size, section.file_size)
            if section.virtual_address <= rva < section.virtual_address + span:
                delta = rva - section.virtual_address
                if delta < section.file_size:
                    return section.file_offset + delta
                return None
        return None

    def u32_va(self, address: int) -> int:
        offset = self.va_to_file(address)
        if offset is None:
            raise ValueError(f"unmapped VA 0x{address:08X}")
        return self.u32_file(offset)

    def cstring_va(self, address: int, limit: int = 512) -> str:
        offset = self.va_to_file(address)
        if offset is None:
            raise ValueError(f"unmapped VA 0x{address:08X}")
        end = self.data.find(b"\0", offset, min(len(self.data), offset + limit))
        if end < 0:
            raise ValueError(f"unterminated string at 0x{address:08X}")
        return self.data[offset:end].decode("ascii", errors="replace")


@dataclass(frozen=True)
class BaseDescriptor:
    name: str
    decorated_name: str
    contained_bases: int
    member_displacement: int
    vbtable_displacement: int
    vbase_displacement: int
    attributes: int


@dataclass
class ClassRecord:
    name: str
    decorated_name: str
    direct_bases: list[str]
    all_bases: list[str]
    complete_object_locators: set[int]


def demangle_type(decorated: str) -> str:
    if not (decorated.startswith(".?AV") or decorated.startswith(".?AU")):
        return decorated
    if decorated[4:].startswith("?$"):
        encoded = decorated[6:]
        if "@" in encoded:
            template_name, argument = encoded.split("@", 1)
            if argument[:1] in {"U", "V"} and argument.endswith("@@@@"):
                argument_parts = [
                    part for part in argument[1:-4].split("@") if part
                ]
                if argument_parts:
                    argument_name = "::".join(reversed(argument_parts))
                    return f"{template_name}<{argument_name}>"
    body = decorated[4:]
    if body.endswith("@@"):
        body = body[:-2]
    parts = [part for part in body.split("@") if part]
    if not parts:
        return decorated
    if any(part.startswith("?$") for part in parts):
        return decorated
    return "::".join(reversed(parts))


def find_type_descriptors(image: PEImage) -> dict[int, tuple[str, str]]:
    descriptors: dict[int, tuple[str, str]] = {}
    for section in image.sections:
        begin = section.file_offset
        end = begin + section.file_size
        cursor = begin
        while cursor < end:
            positions = [
                position
                for position in (
                    image.data.find(b".?AV", cursor, end),
                    image.data.find(b".?AU", cursor, end),
                )
                if position >= 0
            ]
            if not positions:
                break
            name_offset = min(positions)
            descriptor_offset = name_offset - 8
            if descriptor_offset >= begin:
                rva = section.virtual_address + descriptor_offset - begin
                address = image.image_base + rva
                decorated = image.cstring_va(address + 8)
                descriptors[address] = (demangle_type(decorated), decorated)
            cursor = name_offset + 4
    return descriptors


def read_hierarchy(
    image: PEImage,
    hierarchy_address: int,
    types: dict[int, tuple[str, str]],
) -> list[BaseDescriptor] | None:
    try:
        signature = image.u32_va(hierarchy_address)
        attributes = image.u32_va(hierarchy_address + 4)
        count = image.u32_va(hierarchy_address + 8)
        array_address = image.u32_va(hierarchy_address + 12)
    except ValueError:
        return None
    if signature != 0 or attributes > 7 or not 1 <= count <= 512:
        return None

    descriptors: list[BaseDescriptor] = []
    try:
        for index in range(count):
            descriptor_address = image.u32_va(array_address + index * 4)
            type_address = image.u32_va(descriptor_address)
            if type_address not in types:
                return None
            contained = image.u32_va(descriptor_address + 4)
            mdisp, pdisp, vdisp = struct.unpack(
                "<iii",
                image.data[
                    image.va_to_file(descriptor_address + 8) :
                    image.va_to_file(descriptor_address + 8) + 12
                ],
            )
            base_attributes = image.u32_va(descriptor_address + 20)
            name, decorated = types[type_address]
            descriptors.append(
                BaseDescriptor(
                    name,
                    decorated,
                    contained,
                    mdisp,
                    pdisp,
                    vdisp,
                    base_attributes,
                )
            )
    except (TypeError, ValueError, struct.error):
        return None
    return descriptors


def direct_bases(descriptors: list[BaseDescriptor]) -> list[str]:
    result: list[str] = []
    index = 1
    while index < len(descriptors):
        descriptor = descriptors[index]
        result.append(descriptor.name)
        index += 1 + descriptor.contained_bases
    return result


def unique(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def collect_classes(image: PEImage) -> dict[str, ClassRecord]:
    types = find_type_descriptors(image)
    records: dict[str, ClassRecord] = {}

    for section in image.sections:
        if section.name not in {".rdata", ".data"}:
            continue
        begin = section.file_offset
        end = begin + section.file_size - 20
        for offset in range(begin, end, 4):
            signature, object_offset, constructor_offset, type_address, hierarchy_address = (
                struct.unpack_from("<IIIII", image.data, offset)
            )
            if (
                signature != 0
                or object_offset > 0x10000
                or constructor_offset > 0x10000
                or type_address not in types
            ):
                continue
            descriptors = read_hierarchy(image, hierarchy_address, types)
            if not descriptors:
                continue
            name, decorated = types[type_address]
            if descriptors[0].decorated_name != decorated:
                continue

            address = image.image_base + section.virtual_address + offset - begin
            bases = direct_bases(descriptors)
            all_bases = unique(descriptor.name for descriptor in descriptors[1:])
            record = records.get(name)
            if record is None:
                records[name] = ClassRecord(
                    name,
                    decorated,
                    bases,
                    all_bases,
                    {address},
                )
            else:
                if record.direct_bases != bases or record.all_bases != all_bases:
                    raise ValueError(f"conflicting RTTI hierarchy for {name}")
                record.complete_object_locators.add(address)
    return records


def pane_lineage(name: str, records: dict[str, ClassRecord]) -> list[str] | None:
    def visit(current: str, path: list[str]) -> list[str] | None:
        if current == "Pane":
            return path + [current]
        if current in path or current not in records:
            return None
        for base in records[current].direct_bases:
            result = visit(base, path + [current])
            if result is not None:
                return result
        return None

    return visit(name, [])


def make_manifest(image: PEImage, records: dict[str, ClassRecord]) -> dict:
    pane_records = []
    for name in sorted(records, key=str.casefold):
        lineage = pane_lineage(name, records)
        if lineage is None:
            continue
        record = records[name]
        pane_records.append(
            {
                "name": name,
                "decorated_name": record.decorated_name,
                "direct_bases": record.direct_bases,
                "pane_lineage": lineage,
                "all_bases": record.all_bases,
                "complete_object_locators": [
                    f"0x{address:08X}"
                    for address in sorted(record.complete_object_locators)
                ],
            }
        )

    return {
        "schema_version": 1,
        "target": {
            "architecture": "x86",
            "file": image.path.name,
            "image_base": f"0x{image.image_base:08X}",
            "reported_version": 741,
            "sha256": hashlib.sha256(image.data).hexdigest(),
            "size": len(image.data),
        },
        "source": {
            "kind": "msvc_x86_rtti",
            "description": (
                "Complete Object Locator, Class Hierarchy Descriptor, "
                "Base Class Array, and Base Class Descriptor records"
            ),
        },
        "pane_type_count": len(pane_records),
        "pane_types": pane_records,
    }


def markdown_name(name: str) -> str:
    escaped = name.replace("|", "\\|")
    return f"`{escaped}`"


def make_markdown(manifest: dict) -> str:
    lines = [
        "# Pane type and inheritance appendix",
        "",
        (
            f"The matching client contains {manifest['pane_type_count']} distinct "
            "RTTI classes whose inheritance reaches `Pane`. The list is "
            "alphabetical and deduplicates secondary vtables for multiple "
            "inheritance."
        ),
        "",
        (
            "Direct bases come from each MSVC Base Class Array. Pane lineage "
            "shows the shortest direct-base path back to `Pane`. `Pane` itself "
            "directly inherits `Canvas` and `TimerHandler`; both reach `LObject`."
        ),
        "",
        "| Type | Direct base class(es) | Pane lineage |",
        "| --- | --- | --- |",
    ]
    for record in manifest["pane_types"]:
        bases = ", ".join(markdown_name(base) for base in record["direct_bases"])
        lineage = " → ".join(markdown_name(item) for item in record["pane_lineage"])
        lines.append(f"| {markdown_name(record['name'])} | {bases} | {lineage} |")
    lines.extend(
        [
            "",
            "## Scope and evidence",
            "",
            (
                "This is a static class inventory, not a list of panes alive at "
                "runtime. Names are exact MSVC RTTI type names. Inheritance is "
                "decoded from RTTI hierarchy records rather than inferred from "
                "a class name, namespace, constructor similarity, or vtable shape."
            ),
            "",
            (
                "The deterministic source manifest is "
                "[`analysis/exports/ui-pane-types.yaml`]"
                "(../../analysis/exports/ui-pane-types.yaml)."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def yaml_quote(value: str) -> str:
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
    )
    return f'"{escaped}"'


def make_yaml(manifest: dict) -> str:
    target = manifest["target"]
    source = manifest["source"]
    lines = [
        f"schema_version: {manifest['schema_version']}",
        "target:",
        f"  architecture: {target['architecture']}",
        f"  file: {target['file']}",
        f"  image_base: {yaml_quote(target['image_base'])}",
        f"  reported_version: {target['reported_version']}",
        f"  sha256: {target['sha256']}",
        f"  size: {target['size']}",
        "source:",
        f"  kind: {source['kind']}",
        f"  description: {yaml_quote(source['description'])}",
        f"pane_type_count: {manifest['pane_type_count']}",
        "pane_types:",
    ]
    for record in manifest["pane_types"]:
        lines.append(f"  - name: {yaml_quote(record['name'])}")
        lines.append(
            f"    decorated_name: {yaml_quote(record['decorated_name'])}"
        )
        lines.append("    direct_bases:")
        if record["direct_bases"]:
            for base in record["direct_bases"]:
                lines.append(f"      - {yaml_quote(base)}")
        else:
            lines[-1] += " []"
        lines.append("    pane_lineage:")
        for item in record["pane_lineage"]:
            lines.append(f"      - {yaml_quote(item)}")
        lines.append("    all_bases:")
        if record["all_bases"]:
            for base in record["all_bases"]:
                lines.append(f"      - {yaml_quote(base)}")
        else:
            lines[-1] += " []"
        lines.append("    complete_object_locators:")
        for address in record["complete_object_locators"]:
            lines.append(f"      - {yaml_quote(address)}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--yaml", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()

    image = PEImage(args.binary)
    digest = hashlib.sha256(image.data).hexdigest()
    if len(image.data) != TARGET_SIZE or digest != TARGET_SHA256:
        raise SystemExit("target fingerprint mismatch")

    manifest = make_manifest(image, collect_classes(image))
    args.yaml.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.yaml.write_text(
        make_yaml(manifest),
        encoding="utf-8",
    )
    args.markdown.write_text(make_markdown(manifest), encoding="utf-8")


if __name__ == "__main__":
    main()
