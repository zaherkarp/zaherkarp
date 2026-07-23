#!/usr/bin/env python3
"""Marker-integrity lint for the profile README.

Ported from zaherkarp.github.io/scripts/lint_markers.py. The generated regions
that build_readme.py splices into must stay paired and intact, so a stray hand
edit cannot corrupt the file or make the generator silently do nothing.

Checks per file:
  STRUCTURE  no orphan end, no nested/overlapping opens, no crossed close,
             no unterminated start.
  PRESENCE   every required pair appears as a completed start/end.

Exit 1 on any failure (hard gate; wired into .github/workflows/lint.yml).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# file (repo-relative) -> marker names build_readme.py injects into.
PAIR_MARKERS: dict[str, list[str]] = {
    "README.md": ["title", "stack", "writing", "research"],
}

MARK_RE = re.compile(r"^\s*<!--\s*([a-z0-9-]+):(start|end)\s*-->\s*$")


def check_file(rel: str, names: list[str]) -> list[str]:
    path = ROOT / rel
    if not path.exists():
        return [f"{rel}: file not found"]
    errs: list[str] = []
    open_name: str | None = None
    seen: set[str] = set()
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = MARK_RE.match(line)
        if not m:
            continue
        name, kind = m.group(1), m.group(2)
        if kind == "start":
            if open_name is not None:
                errs.append(
                    f"{rel}:{lineno}: '{name}:start' opens while "
                    f"'{open_name}:start' is still open (nested/unterminated)"
                )
            open_name = name
        else:  # end
            if open_name is None:
                errs.append(f"{rel}:{lineno}: '{name}:end' with no open start (orphan)")
            elif open_name != name:
                errs.append(
                    f"{rel}:{lineno}: '{name}:end' closes the wrong region "
                    f"(expected '{open_name}:end')"
                )
                open_name = None
            else:
                seen.add(name)
                open_name = None
    if open_name is not None:
        errs.append(f"{rel}: '{open_name}:start' is never closed (unterminated)")
    for want in names:
        if want not in seen:
            errs.append(
                f"{rel}: required marker pair '{want}:start'/'{want}:end' "
                f"is missing or malformed"
            )
    return errs


def main() -> None:
    errs: list[str] = []
    for rel, names in PAIR_MARKERS.items():
        errs += check_file(rel, names)
    if errs:
        print("lint_markers: FAIL", file=sys.stderr)
        for e in errs:
            print("  " + e, file=sys.stderr)
        sys.exit(1)
    print("lint_markers: ok")


if __name__ == "__main__":
    main()
