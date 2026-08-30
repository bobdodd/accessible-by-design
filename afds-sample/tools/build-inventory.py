# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Bob Dodd
"""Generate and verify afds-inventory.json for an AFDS package source tree.

Usage:
    python3 tools/build-inventory.py build      Regenerate afds-inventory.json.
    python3 tools/build-inventory.py verify     Verify afds-inventory.json.
    python3 tools/build-inventory.py pack PATH  Write a .afds ZIP to PATH.

The inventory records every package entry except itself.
Records are sorted by path so that a rebuild produces a stable, reviewable diff.
Digests are lowercase hexadecimal SHA-256 over the exact bytes of each entry.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
INVENTORY_NAME = "afds-inventory.json"
MANIFEST_NAME = "afds-manifest.json"

# Repository-side helpers that are not part of the distributable package.
EXCLUDED_TOP_LEVEL = {"tools", "README.md"}
EXCLUDED_NAMES = {".DS_Store"}

MEDIA_TYPES = {
    ".json": "application/json",
    ".md": "text/markdown; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
}

# Declared artefact role per package path or path prefix.
ROLES = [
    (MANIFEST_NAME, "canonical"),
    ("tokens/", "canonical"),
    ("components/", None),  # decided by extension below
    ("patterns/", None),
    ("evidence/", "evidence"),
    ("schemas/", "schema"),
    ("adapters/", "adapter"),
    ("stories/", "derived"),
    ("docs/", "documentation"),
    ("LICENSES.md", "documentation"),
]


def media_type_for(path: str) -> str:
    return MEDIA_TYPES.get(Path(path).suffix.lower(), "application/octet-stream")


def role_for(path: str) -> str:
    """Return the declared artefact role for a package-relative path."""
    if path == MANIFEST_NAME:
        return "canonical"
    if path == "LICENSES.md":
        return "documentation"
    if path.startswith(("tokens/", "patterns/")):
        return "canonical"
    if path.startswith("components/"):
        # A machine-readable contract is canonical; its prose companion is documentation.
        return "canonical" if path.endswith(".spec.json") else "documentation"
    if path.startswith("evidence/"):
        return "evidence"
    if path.startswith("schemas/"):
        return "schema"
    if path.startswith("adapters/"):
        # Adapter guidance prose is documentation; generated output is adapter role.
        return "documentation" if path.endswith(".md") else "adapter"
    if path.startswith("stories/"):
        return "derived"
    if path.startswith("docs/"):
        return "documentation"
    return "documentation"


def collect_entries() -> list[str]:
    """Return sorted package-relative paths of every entry except the inventory."""
    entries: list[str] = []
    for dirpath, dirnames, filenames in os.walk(PACKAGE_ROOT):
        rel_dir = Path(dirpath).relative_to(PACKAGE_ROOT)
        top = rel_dir.parts[0] if rel_dir.parts else ""
        if top in EXCLUDED_TOP_LEVEL:
            dirnames[:] = []
            continue
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_TOP_LEVEL and not d.startswith("."))
        for filename in sorted(filenames):
            if filename in EXCLUDED_NAMES or filename == INVENTORY_NAME:
                continue
            rel = (rel_dir / filename).as_posix() if rel_dir.parts else filename
            if rel.split("/", 1)[0] in EXCLUDED_TOP_LEVEL:
                continue
            entries.append(rel)
    return sorted(entries)


def record_for(rel: str) -> dict:
    data = (PACKAGE_ROOT / rel).read_bytes()
    return {
        "path": rel,
        "mediaType": media_type_for(rel),
        "byteLength": len(data),
        "role": role_for(rel),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def build_inventory() -> dict:
    manifest = json.loads((PACKAGE_ROOT / MANIFEST_NAME).read_text(encoding="utf-8"))
    records = [record_for(rel) for rel in collect_entries()]
    return {
        "afdsFormat": "afds-inventory",
        "afdsVersion": manifest.get("afdsVersion", "1.0.0"),
        "packageId": manifest.get("packageId"),
        "packageVersion": manifest.get("packageVersion"),
        "digestAlgorithm": "SHA-256",
        "digestEncoding": "lowercase-hex",
        "excludesSelf": True,
        "entryCount": len(records),
        "description": (
            "Inventory of every entry in this package except this inventory itself. "
            "A consumer must verify every record before relying on package content. "
            "These digests detect transfer changes; they are not a digital signature "
            "and do not identify a signer or prove provenance."
        ),
        "records": records,
    }


def cmd_build() -> int:
    inventory = build_inventory()
    target = PACKAGE_ROOT / INVENTORY_NAME
    target.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"built {INVENTORY_NAME} with {inventory['entryCount']} records")
    for record in inventory["records"]:
        print(f"  {record['sha256'][:16]}...  {record['byteLength']:>7}  {record['role']:<13}  {record['path']}")
    return 0


def cmd_verify() -> int:
    target = PACKAGE_ROOT / INVENTORY_NAME
    if not target.exists():
        print(f"FAIL: {INVENTORY_NAME} is missing", file=sys.stderr)
        return 1

    inventory = json.loads(target.read_text(encoding="utf-8"))
    problems: list[str] = []

    if inventory.get("digestAlgorithm") != "SHA-256":
        problems.append("digestAlgorithm is not SHA-256")
    if inventory.get("excludesSelf") is not True:
        problems.append("excludesSelf is not true")

    recorded = {r["path"]: r for r in inventory.get("records", [])}
    if INVENTORY_NAME in recorded:
        problems.append(f"{INVENTORY_NAME} must not appear in its own records")

    actual = set(collect_entries())
    for missing in sorted(actual - set(recorded)):
        problems.append(f"entry present but not inventoried: {missing}")
    for extra in sorted(set(recorded) - actual):
        problems.append(f"inventoried but not present: {extra}")

    checked = 0
    for rel in sorted(actual & set(recorded)):
        expected = recorded[rel]
        found = record_for(rel)
        for field in ("byteLength", "sha256", "mediaType", "role"):
            if expected.get(field) != found[field]:
                problems.append(f"{rel}: {field} mismatch (inventory {expected.get(field)!r}, actual {found[field]!r})")
        checked += 1

    if inventory.get("entryCount") != len(recorded):
        problems.append(f"entryCount {inventory.get('entryCount')} does not match {len(recorded)} records")

    print(f"inventory: {len(recorded)} records, {checked} entries digest-checked")
    if problems:
        print("VERIFY FAILED")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("VERIFY PASSED: every entry is inventoried, lengths and SHA-256 digests match")
    return 0


def cmd_pack(destination: str) -> int:
    dest = Path(destination).resolve()
    if PACKAGE_ROOT in dest.parents or dest.parent == PACKAGE_ROOT:
        print("FAIL: refusing to write the package inside the source tree", file=sys.stderr)
        return 1
    if cmd_verify() != 0:
        print("FAIL: refusing to pack an unverified source tree", file=sys.stderr)
        return 1
    paths = collect_entries() + [INVENTORY_NAME]
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for rel in sorted(paths):
            archive.write(PACKAGE_ROOT / rel, arcname=rel)
    print(f"packed {len(paths)} entries into {dest}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build, verify, or pack an AFDS package inventory.")
    parser.add_argument("command", choices=["build", "verify", "pack"])
    parser.add_argument("destination", nargs="?", help="Output path for the pack command.")
    args = parser.parse_args()

    if args.command == "build":
        return cmd_build()
    if args.command == "verify":
        return cmd_verify()
    if not args.destination:
        parser.error("pack requires a destination path outside the source tree")
    return cmd_pack(args.destination)


if __name__ == "__main__":
    sys.exit(main())
