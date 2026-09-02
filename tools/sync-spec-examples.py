#!/usr/bin/env python3
"""Regenerate the specification's worked examples from the sample package.

Clause 29.2 quotes afds-manifest.json verbatim.
Clause 30.3 quotes afds-inventory.json with the records array abridged to the
two records the clause discusses, every other field reproduced as it stands.

Both clauses claim in their own prose that they are generated rather than
transcribed. This script is what makes that claim true. Run it after any
change to the sample package, then run --check in CI.

Usage, from anywhere:
    python3 tools/sync-spec-examples.py            # rewrite the clauses
    python3 tools/sync-spec-examples.py --check    # exit 1 if they have drifted
"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SPEC = REPO / "docs" / "AFDS-SPECIFICATION.md"
MANIFEST = REPO / "afds-sample" / "afds-manifest.json"
INVENTORY = REPO / "afds-sample" / "afds-inventory.json"

# The two records clause 30.3 shows, in the order it shows them.
ABRIDGED_PATHS = ["afds-manifest.json", "tokens/core.tokens.json"]

NUMBER_WORDS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
    6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
    11: "eleven", 12: "twelve",
}


def fenced_block(payload: str) -> str:
    return "```json\n" + payload.rstrip("\n") + "\n```"


def replace_block(text: str, clause: str, payload: str) -> str:
    """Replace the first ```json fence inside the named clause."""
    start = re.search(rf"^#### {re.escape(clause)}\b.*$", text, re.M)
    if not start:
        sys.exit(f"clause {clause} not found in {SPEC.name}")
    # Bound the search to this clause: stop at the next ### or #### heading.
    nxt = re.search(r"^#{3,4} \d", text[start.end():], re.M)
    end = start.end() + (nxt.start() if nxt else len(text) - start.end())
    segment = text[start.end():end]
    fence = re.search(r"```json\n.*?\n```", segment, re.S)
    if not fence:
        sys.exit(f"no json fence inside clause {clause}")
    new_segment = segment[:fence.start()] + fenced_block(payload) + segment[fence.end():]
    return text[:start.end()] + new_segment + text[end:]


def build_payloads():
    manifest_text = MANIFEST.read_text()
    manifest = json.loads(manifest_text)

    inventory = json.loads(INVENTORY.read_text())
    by_path = {r["path"]: r for r in inventory["records"]}
    missing = [p for p in ABRIDGED_PATHS if p not in by_path]
    if missing:
        sys.exit(f"clause 30.3 wants records that are not in the inventory: {missing}")
    abridged = dict(inventory)
    abridged["records"] = [by_path[p] for p in ABRIDGED_PATHS]

    # The manifest is quoted verbatim: use its own bytes, not a re-dump, so
    # that the clause reproduces the file including its formatting.
    return manifest_text.rstrip("\n"), json.dumps(abridged, indent=2), manifest, inventory


def sync_prose_counts(text: str, manifest: dict) -> str:
    """Keep prose counts that describe the example in step with it."""
    n = len(manifest["documentation"]["sources"])
    word = NUMBER_WORDS.get(n, str(n))
    text, hits = re.subn(
        r"(including the )\w+( in `documentation\.sources`)",
        rf"\g<1>{word}\g<2>",
        text,
    )
    if hits != 1:
        sys.exit(f"expected 1 documentation.sources count sentence, found {hits}")
    return text


def main() -> int:
    check = "--check" in sys.argv
    original = SPEC.read_text()
    manifest_payload, inventory_payload, manifest, inventory = build_payloads()

    updated = replace_block(original, "29.2", manifest_payload)
    updated = replace_block(updated, "30.3", inventory_payload)
    updated = sync_prose_counts(updated, manifest)

    if check:
        if updated != original:
            print("DRIFT: clause 29.2 or 30.3 no longer matches the sample package.")
            print("Run: python3 sync-spec-examples.py")
            return 1
        print("clauses 29.2 and 30.3 match the sample package")
        return 0

    if updated == original:
        print("no change: clauses 29.2 and 30.3 already match the sample package")
    else:
        SPEC.write_text(updated)
        print("rewrote clauses 29.2 and 30.3 from the sample package")

    m_bytes = MANIFEST.read_bytes()
    print(f"  manifest      {len(m_bytes)} bytes, {len(manifest['documentation']['sources'])} documentation sources")
    print(f"  inventory     {len(inventory['records'])} records, entryCount {inventory['entryCount']}")
    print(f"  abridged to   {', '.join(ABRIDGED_PATHS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
