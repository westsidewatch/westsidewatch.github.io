#!/usr/bin/env python3
from pathlib import Path
import re

ROOTS = (Path("content"),)
SUFFIXES = {".md", ".html"}
PATTERN = re.compile(r"(?m)^([ \t]*)_build([ \t]*:)")

changed = []
for root in ROOTS:
    if not root.exists():
        continue
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        updated = PATTERN.sub(r"\1build\2", text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path))

if changed:
    print("Normalized deprecated _build front matter:")
    print("\n".join(changed))

leftovers = []
for root in ROOTS:
    if not root.exists():
        continue
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUFFIXES:
            if PATTERN.search(path.read_text(encoding="utf-8")):
                leftovers.append(str(path))

if leftovers:
    raise SystemExit(
        "Deprecated _build remains in Hugo content tree: " + ", ".join(leftovers)
    )
