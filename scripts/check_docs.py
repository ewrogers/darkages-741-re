#!/usr/bin/env python3
"""Run the same documentation validation locally and in CI, without regeneration."""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
MDBOOK_VERSION = "0.5.4"


def run(label, command):
    print(f"\n{label}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def validate(mdbook, destination):
    run("Check navigation and packet indexes", [sys.executable, "scripts/build_book_summary.py", "--check"])
    run("Check function references", [sys.executable, "scripts/build_function_reference.py", "--check"])
    run("Test generation and repository links", [sys.executable, "-m", "unittest", "discover", "-s", "scripts/tests", "-p", "test_*.py"])
    run("Test exact function lookup", ["node", "--test", "scripts/tests/test_function_lookup.cjs"])
    for script in sorted((ROOT / "theme").glob("*.js")):
        run(f"Check theme syntax: {script.name}", ["node", "--check", str(script)])
    run("Build the book", [mdbook, "build", "--dest-dir", str(destination)])
    run("Check rendered links and assets", [sys.executable, "scripts/check_book_links.py", str(destination)])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mdbook", default="mdbook", help=f"mdBook {MDBOOK_VERSION} executable")
    parser.add_argument("--book-dir", type=Path, help="retain the build in root book/ or an external directory")
    args = parser.parse_args()

    if sys.version_info < (3, 12):
        parser.error("Python 3.12 or newer is required")
    mdbook = shutil.which(args.mdbook)
    if not mdbook:
        parser.error(f"mdBook {MDBOOK_VERSION} was not found; select it with --mdbook")
    mdbook = str(Path(mdbook).resolve())
    if not shutil.which("node"):
        parser.error("Node.js with node --test support is required")

    destination = args.book_dir
    if destination is not None:
        destination = (ROOT / destination).resolve()
        if destination == ROOT or destination in ROOT.parents or (ROOT in destination.parents and destination != ROOT / "book"):
            parser.error("--book-dir must be root book/ or outside the repository, never an authored source directory")

    try:
        version = subprocess.run([mdbook, "--version"], check=True, capture_output=True, text=True).stdout.strip()
        if version != f"mdbook v{MDBOOK_VERSION}":
            parser.error(f"expected mdbook v{MDBOOK_VERSION}; found {version!r}; select the pinned executable with --mdbook")
        if destination is None:
            with tempfile.TemporaryDirectory(prefix="darkages-docs-check-") as temporary:
                validate(mdbook, Path(temporary) / "book")
            print("\nDocumentation checks passed; temporary build removed.")
        else:
            validate(mdbook, destination)
            print(f"\nDocumentation checks passed; preview retained at {destination}")
    except subprocess.CalledProcessError as error:
        print(f"\nDocumentation checks stopped: command exited with status {error.returncode}.", file=sys.stderr)
        return error.returncode
    except OSError as error:
        print(f"\nDocumentation checks stopped: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
