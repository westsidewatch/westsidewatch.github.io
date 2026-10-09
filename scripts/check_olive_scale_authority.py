#!/usr/bin/env python3
"""Olive Mountain poster scale authority regression gate (stdlib only)."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "olive/index.html"
JS = ROOT / "olive/olive.js"
DOC = ROOT / "docs/OLIVE_MOUNTAIN_DESIGN_ENGINEERING.md"
errors = []
html = PAGE.read_text(encoding="utf-8")
js = JS.read_text(encoding="utf-8")
css = html.split("<style>", 1)[1].split("</style>", 1)[0] if "<style>" in html else ""

def require(condition, message):
    if not condition:
        errors.append(message)

require('container-type:inline-size' in css, "poster container query authority missing")
require('aspect-ratio:3/4' in css, "approved poster 3:4 ratio missing")
require('font-size:var(--poster-size)' in css, "English type is not poster-relative")
require('font-optical-sizing:none' in css, "poster optical size lock missing")
require('font-synthesis:none' in css, "font synthesis lock missing")
require('prefers-reduced-motion:reduce' in css, "reduced motion missing")
require('dore-editorial-cover' in js, "editorial cover rendering missing")
require('editorialOrder' in js, "approved speaker order missing")
require('huang-shuhua' in css and 'jerry-lai' in css, "approved foreground occlusion missing")
require(DOC.exists(), "engineering memo missing")
# Disallow known accidental glyph distortions on poster typography.
for pattern in (r'\.olive-speaker-english\s*\{[^}]*scaleX\(', r'\.olive-speaker-english\s*\{[^}]*scaleY\('):
    require(not re.search(pattern, css, re.S), "nonuniform glyph scaling detected")
# Keep the existing content/URL authority untouched in this phase.
require('id="olive-speakers"' in html and 'id="olive-series"' in html, "speaker/series anchors missing")
if errors:
    for error in errors:
        print("FAIL:", error)
    sys.exit(1)
print("PASS: Olive Mountain poster scale authority checks (12 assertions)")
