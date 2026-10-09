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
hugo = (ROOT / "layouts/olive/surface-carrier.html").read_text(encoding="utf-8")
journey = (ROOT / "static/js/olive-journey.js").read_text(encoding="utf-8")
rail = (ROOT / "static/js/olive-editorial-rail.js").read_text(encoding="utf-8")
manifest = (ROOT / "static/dore-design/runtime/olive-editorial-covers.v1.json").read_text(encoding="utf-8")
require('data-pawson-play' in hugo, "approved Pawson hero missing")
require('olive-editorial-rail.js' in hugo and 'olive-journey.js' in hugo, "single journey not wired")
require(all(x in journey for x in ('The Speakers', 'The Sermons', 'The Archive')), "journey layers missing")
require('olive-editorial-covers.v1.json' in rail, "approved poster source missing")
require(manifest.count('"speaker":') == 12, "expected twelve editorial poster assets")
config = (ROOT / "hugo.toml").read_text(encoding="utf-8")
olive_mount = config.split('source = "olive"', 1)[1].split('[[module.mounts]]', 1)[0] if 'source = "olive"' in config else ''
require('excludeFiles = ["index.html"]' in olive_mount, "static Olive homepage still conflicts with Hugo homepage")
require('layout: "surface-carrier"' in (ROOT / "content/olive/_index.md").read_text(encoding="utf-8"), "canonical Olive Hugo route missing")
require('/olive/#olive-series' not in journey, "obsolete standalone series anchor still linked")
require("'/olive/?person='" not in hugo, "Hugo homepage still routes speakers to removed query page")
require("'/olive/'+slug+'/'" in hugo, "canonical speaker routes missing")
require("poster.style.backgroundSize='contain'" in hugo, 'preview images must not crop')
require("poster.style.backgroundSize='cover'" not in hugo, 'video thumbnail must not crop')
require("poster.style.backgroundRepeat='no-repeat'" in hugo, 'fallback poster must not tile')
require('data-feature-next' in hugo and 'data-feature-prev' in hugo and 'maxresdefault.jpg' in hugo and 'hqdefault.jpg' in hugo, 'video thumbnail navigation missing')
require('const featured=[' in hugo and 'featured[index]' in hugo, 'video and preview must share selection')
require("selectFeatured(index-1)" in hugo and "selectFeatured(index+1)" in hugo, 'bidirectional feature navigation missing')
require("event.key==='ArrowRight'" in hugo and "event.key==='ArrowLeft'" in hugo, 'keyboard navigation missing')
require('data-feature-source' in hugo and "source.href='https://www.youtube.com/watch?v='+item.id" in hugo, 'video-specific external playback fallback missing')
if errors:
    for error in errors:
        print("FAIL:", error)
    sys.exit(1)
print("PASS: Olive Mountain poster scale authority checks (20 assertions)")
