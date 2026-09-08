"""Exercise the generated reference's evidence-preservation and CLI contracts."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import build_function_reference as reference


class FunctionReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.exports = self.root / "analysis/exports"
        self.exports.mkdir(parents=True)

    def export(self, name, rows, target=None):
        lines = ["schema_version: 1", "target:"]
        lines.extend(f"  {key}: {json.dumps(value)}" for key, value in (target or reference.TARGET).items())
        lines.append("functions:")
        for row in rows:
            for index, (key, value) in enumerate(row.items()):
                lines.append(("  - " if index == 0 else "    ") + key + ": " + json.dumps(value))
        (self.exports / name).write_text("\n".join(lines) + "\n")

    def row(self, **fields):
        return dict(name="net_example", address="0x00401234", confidence="high", evidence="First finding.") | fields

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "build_function_reference.py"), "--root", str(self.root), *args], capture_output=True, text=True)

    def test_complementary_evidence_and_optional_fields_survive(self):
        self.export("a.yaml", [self.row(evidence="First | finding <with> details.", prototype="void example(void)")])
        self.export("b.yaml", [self.row(address="0x401234", evidence="A second source preserves another branch.")])
        output = reference.render(self.exports)
        self.assertIn("First &#124; finding &lt;with&gt; details.", output["network.md"])
        self.assertIn("another branch", output["network.md"])
        self.assertIn("a.yaml#L", output["network.md"])
        self.assertIn("b.yaml#L", output["network.md"])
        records, _ = reference.collect(self.exports)
        self.assertEqual(2, len(records[("net_example", "0x00401234")]))
        index = json.loads(output["index.json"])["functions"]
        self.assertEqual(1, len(index))
        self.assertEqual("0x00001234", index[0]["rva"])

    def test_identity_disagreements_are_visible_without_choosing_a_winner(self):
        self.export("a.yaml", [self.row(), self.row(name="net_other")])
        self.export("b.yaml", [self.row(address="0x00402000")])
        output = reference.render(self.exports)
        index = json.loads(output["index.json"])["functions"]
        self.assertEqual(3, len(index))
        self.assertTrue(all(row["conflict"] for row in index))
        self.assertIn("One name, multiple addresses", output["identity-warnings.md"])
        self.assertIn("One address, multiple names", output["identity-warnings.md"])

    def test_incompatible_metadata_fails_before_any_write(self):
        self.export("a.yaml", [self.row()])
        self.assertEqual(0, self.run_cli().returncode)
        before = {p.name: p.read_bytes() for p in (self.root / "generated/function-reference").iterdir()}
        self.export("b.yaml", [self.row(confidence="low")])
        result = self.run_cli()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("conflicting confidence", result.stderr)
        self.assertIn("a.yaml:", result.stderr)
        self.assertIn("b.yaml:", result.stderr)
        self.assertEqual(before, {p.name: p.read_bytes() for p in (self.root / "generated/function-reference").iterdir()})

    def test_target_required_fields_and_rva_are_validated(self):
        for change in [{"rva": "0x00001235"}, {"evidence": ""}, {"address": "bad"}]:
            with self.subTest(change=change):
                self.export("a.yaml", [self.row(**change)])
                with self.assertRaises(ValueError):
                    reference.render(self.exports)
        self.export("a.yaml", [self.row()], target=reference.TARGET | {"sha256": "0" * 64})
        with self.assertRaisesRegex(ValueError, "fingerprint"):
            reference.render(self.exports)

    def test_check_is_read_only_and_regeneration_is_idempotent(self):
        self.export("a.yaml", [self.row()])
        self.assertNotEqual(0, self.run_cli("--check").returncode)
        self.assertFalse((self.root / "generated").exists())
        self.assertEqual(0, self.run_cli().returncode)
        output = self.root / "generated/function-reference/index.json"
        before = (output.read_bytes(), output.stat().st_mtime_ns)
        self.assertEqual(0, self.run_cli("--check").returncode)
        self.assertEqual(0, self.run_cli().returncode)
        self.assertEqual(before, (output.read_bytes(), output.stat().st_mtime_ns))
        self.export("a.yaml", [self.row(), self.row(name="net_new", address="0x00402000")])
        result = self.run_cli("--check")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("stale:", result.stdout)
        self.assertEqual(before, (output.read_bytes(), output.stat().st_mtime_ns))

    def test_duplicate_top_level_fields_fail_instead_of_overwriting(self):
        self.export("a.yaml", [self.row()])
        path = self.exports / "a.yaml"
        original = path.read_text()
        for content in ["schema_version: 999\n" + original, original + "functions: []\n"]:
            with self.subTest(content=content[-25:]):
                path.write_text(content)
                with self.assertRaisesRegex(ValueError, "duplicate top-level"):
                    reference.render(self.exports)


if __name__ == "__main__":
    unittest.main()
