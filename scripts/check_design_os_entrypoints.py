#!/usr/bin/env python3
"""Guard every standalone public HTML entry against bypassing Westside Design OS."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = ("/vendor/", "/node_modules/", "/fixtures/", "/test/", "/tests/")
paths = [ROOT / "cinema" / "index.html", *sorted((ROOT / "static").rglob("*.html"))]
errors = []
for p in paths:
    if not p.exists():
        continue
    rel = "/" + p.relative_to(ROOT).as_posix()
    if any(x in rel for x in EXCLUDE):
        continue
    html = p.read_text(encoding="utf-8")
    if not re.search(r'<html\b', html, re.I):
        continue
    if not re.search(r'<link\b[^>]*href=["\'][^"\']*westside-design-os\.css', html, re.I):
        errors.append(f"{rel}: missing Design OS stylesheet")
    if not re.search(r'<body\b[^>]*\bdata-ws-scope=', html, re.I):
        errors.append(f"{rel}: missing data-ws-scope")
for e in errors:
    print("DESIGN OS ENTRYPOINT FAIL:", e)
print(f"Checked {len(paths)} standalone HTML files; {len(errors)} violations")
sys.exit(bool(errors))
