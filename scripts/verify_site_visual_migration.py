#!/usr/bin/env python3
"""Guard the Site-to-GitHub migration boundary.

The Site contributes presentation only. GitHub main remains authoritative for
navigation, routes, content, and page hierarchy.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

required_visual_assets = (
    "assets/css/brand-shell.css",
    "assets/css/global-navigation.css",
    "assets/css/realm-flow.css",
    "assets/css/second-layer-system.css",
    "assets/css/typography-system.css",
    "assets/css/visual-refinement.css",
    "static/css/brand-surface-overrides.css",
    "static/css/editorial-authority.css",
    "static/css/home-candidate01-authority.css",
    "static/css/church-mersi-motion.css",
    "static/css/sites-second-layer.css",
    "static/css/sites-layer-restoration.css",
    "static/js/typography-system.js",
)

missing = [path for path in required_visual_assets if not (ROOT / path).is_file()]
if missing:
    raise SystemExit("Missing migrated visual assets: " + ", ".join(missing))

base = (ROOT / "layouts/_default/baseof.html").read_text(encoding="utf-8")
for needle in (
    'resources.Get "css/global-navigation.css"',
    'resources.Get "css/second-layer-system.css"',
    'resources.Get "css/typography-system.css"',
    '"js/typography-system.js" | relURL',
    '"css/sites-composition-authority.css" | relURL',
    '"css/sites-layer-restoration.css" | relURL',
):
    if needle not in base:
        raise SystemExit(f"Visual system is not wired into the Hugo shell: {needle}")

header = (ROOT / "layouts/partials/header.html").read_text(encoding="utf-8")
current_routes = (
    '"church/" | relURL',
    '"journal/" | relURL',
    '"one/" | relURL',
    '"olive/" | relURL',
    '"dawn-library/" | relURL',
    '"cinema/" | relURL',
    '"daylight-cafe/" | relURL',
    'href="/dore/search/"',
)
missing_routes = [route for route in current_routes if route not in header]
if missing_routes:
    raise SystemExit("Current main navigation contract changed: " + ", ".join(missing_routes))

print("PASS: Site visual system is present; current GitHub navigation contract remains intact.")

# GitHub Pages serves cinema/index.html directly, bypassing Hugo's asset
# pipeline. Keep its linked visual shell in the static publication layer.
cinema = (ROOT / "cinema/index.html").read_text(encoding="utf-8")
if 'href="cinema-unified.css"' not in cinema:
    raise SystemExit("Static Cinema entry no longer links its unified visual shell.")
if not (ROOT / 'cinema/cinema-unified.css').is_file():
    raise SystemExit("Static Cinema unified visual shell is missing.")

# Motion reduction belongs only to the user's accessibility preference.  A
# static route must not globally silence the Cinema programme.
cinema_shell = (ROOT / "static/css/sites-second-layer.css").read_text(encoding="utf-8")
if "body.sites-cinema *{animation:none!important" in cinema_shell:
    raise SystemExit("Static Cinema shell globally disables programme motion.")
