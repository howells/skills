#!/usr/bin/env python3
"""Materialise shared reference files into the skills that consume them.

`shared/` holds the single source of truth. Each skill still ships a real file
in its own `references/` directory, because `npx skills` installs one skill at a
time and a skill must stand alone once installed. This script writes those
copies; `check-skills.py` fails if one has drifted from its source.

Edit the file in `shared/`, then run this. Never edit a generated copy.

  python3 scripts/sync-shared.py          # write the copies
  python3 scripts/sync-shared.py --check  # report drift, write nothing
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "shared"
MANIFEST = SHARED / "manifest.json"

HEADER = (
    "<!-- generated from shared/{source} by scripts/sync-shared.py."
    " Edit the source, not this copy. -->\n"
)


def rendered(source: str) -> str:
    body = (SHARED / source).read_text()
    return HEADER.format(source=source) + body


def entries() -> list[tuple[str, str]]:
    manifest = json.loads(MANIFEST.read_text())
    pairs = []
    for source, destinations in manifest.items():
        if not (SHARED / source).is_file():
            raise SystemExit(f"missing shared source: shared/{source}")
        for destination in destinations:
            pairs.append((source, destination))
    return pairs


def main() -> int:
    check = "--check" in sys.argv
    drifted = []
    written = 0

    for source, destination in entries():
        target = ROOT / destination
        want = rendered(source)
        have = target.read_text() if target.is_file() else None
        if have == want:
            continue
        if check:
            drifted.append((destination, source, have is None))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(want)
        written += 1
        print(f"wrote {destination}")

    if check:
        for destination, source, missing in drifted:
            state = "missing" if missing else "differs from"
            print(f"ERROR {destination} {state} shared/{source}")
        if drifted:
            print(f"{len(drifted)} generated copies out of date. Run: python3 scripts/sync-shared.py")
            return 1
        print(f"{len(entries())} generated copies match their sources")
        return 0

    print(f"{written} written, {len(entries()) - written} already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
