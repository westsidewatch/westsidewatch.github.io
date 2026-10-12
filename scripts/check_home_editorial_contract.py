#!/usr/bin/env python3
"""Static first-screen regression contract. Does not replace browser screenshots."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "layouts/partials/watch-home.html").read_text()
css = (ROOT / "static/css/westside-home-hero-composition.css").read_text()
base = (ROOT / "layouts/_default/baseof.html").read_text()

def check(ok, msg):
    if not ok:
        raise SystemExit("FAIL: " + msg)
    print("PASS:", msg)

check('data-ws-designable="home-brand"' in html, "home brand is registered as designable")
check(html.count('data-ws-designable="home-brand"') == 2, "masthead and intro are the only art-directed zones")
check('sites-home-slogan-zh' in html and 'sites-home-scripture' in html, "bilingual slogan and scripture are independently addressable")
check('Romans 13:12' in html, "scripture reference preserved")
check('sites-home-nav' in html and 'sites-home-entry' in html, "functional navigation preserved")
check('westside-home-hero-composition.css' in base, "single homepage composition stylesheet is loaded")
check('home-composition-r3' in base, "composition CSS cache version refreshed")
check('sites-home-film{z-index:0;pointer-events:none}' in css, "film stays visible within hero stacking context")
check('sites-home-nav{z-index:5}' in css and 'sites-home-entry{z-index:5}' in css, "functional controls stay above film")
check('@media(max-width:900px)' in css and '@media(max-width:520px)' in css, "tablet and phone layouts exist")
check('@media(prefers-reduced-motion:reduce)' in css, "reduced-motion support exists")
check(not re.search(r'(?:scaleX|scaleY)\s*\(', css), "font geometry is not stretched")
