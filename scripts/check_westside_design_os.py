#!/usr/bin/env python3
from pathlib import Path
import json,sys,re

root=Path(__file__).resolve().parents[1]
required=[
 root/"design-system/tokens/westside.tokens.json",
 root/"design-system/scopes.json",
 root/"static/css/westside-design-os.css",
 root/"static/css/westside-design-tokens.css",
]
missing=[str(p.relative_to(root)) for p in required if not p.exists()]
if missing:
 print("Design OS guard failed: missing",", ".join(missing));sys.exit(1)

scopes=json.loads((root/"design-system/scopes.json").read_text())["scopes"]
if "global" not in scopes or "tool" not in scopes:
 print("Design OS guard failed: global/tool scopes missing");sys.exit(1)

base=(root/"layouts/_default/baseof.html").read_text()
if 'css/westside-design-os.css' not in base or 'data-ws-scope=' not in base:
 print("Design OS guard failed: Hugo runtime is not bound to Design OS");sys.exit(1)
if 'css/typography-sitewide.css" | relURL' in base or 'css/westside-color-authority.css" | relURL' in base:
 print("Design OS guard failed: legacy authorities loaded beside Design OS");sys.exit(1)

runtime=(root/"static/css/westside-design-os.css").read_text()
for legacy in ["/* Visual type-scale normalization", "/* === Color Operating System"]:
 if legacy not in runtime:
  print("Design OS guard failed: migrated visual declarations missing",legacy);sys.exit(1)

import subprocess
# The retired black/gold palette is a Design OS invariant, not a separate CI gate.
palette_guard=subprocess.run([sys.executable,str(root/"scripts/check_black_gold_global_ban.py")],cwd=root)
if palette_guard.returncode: sys.exit(palette_guard.returncode)
result=subprocess.run([sys.executable,str(root/"scripts/build_westside_design_os.py"),"--check"],cwd=root)
if result.returncode: sys.exit(result.returncode)
if '/css/westside-design-tokens.css' not in runtime:
 print("Design OS guard failed: generated token runtime is not loaded");sys.exit(1)
# Chinese reading must have exactly one family authority: the generated OS.
tokens=json.loads((root/"design-system/tokens/westside.tokens.json").read_text())
if tokens["font"]["reading-zh"]["$value"] != tokens["font"]["display-zh"]["$value"]:
 print("Design OS guard failed: reading font disagrees with approved Chinese family");sys.exit(1)
for rel in ("static/css/westside-design-os.css",
            "static/css/typography-sitewide.css",
            "assets/css/typography-system.css"):
 legacy_text=(root/rel).read_text()
 if re.search(r"--ws-type-(?:reading|display)-zh\s*:",legacy_text):
  print("Design OS guard failed: duplicated Chinese font authority:",rel);sys.exit(1)
if "font-family: var(--ws-type-reading-zh)" not in (root/"assets/css/main.css").read_text():
 print("Design OS guard failed: article prose bypasses reading role");sys.exit(1)
# English paragraphs should inherit their article's chosen reading font rather
# than being forced to the Chinese body family, including in bilingual issues.
type_guard=(root/"static/css/westside-typography-enforcement.css").read_text()
if "font-family:var(--ws-type-reading-zh);" not in type_guard or ":not(:lang(en))" not in type_guard:
 print("Design OS guard failed: English longform overrides Chinese reading role");sys.exit(1)
# The editorial roles must come from generated tokens, never another global
# scale in section CSS; primary=900, secondary=200, Bodoni display=400.
expected_roles=(
 "editorial-hero-en","editorial-hero-zh","editorial-chapter-en",
 "editorial-chapter-zh","editorial-article-en","editorial-article-zh",
 "editorial-feature-en","editorial-feature-zh","editorial-subhead-zh",
 "editorial-standfirst-zh","editorial-byline-zh","editorial-contents-zh")
generated=(root/"static/css/westside-design-tokens.css").read_text()
if any(("--ws-type-scale-"+role+":") not in generated for role in expected_roles):
 print("Design OS guard failed: missing generated editorial scale roles");sys.exit(1)
if "for name, item in tokens.get(\"typeScale\", {})" not in (root/"scripts/build_westside_design_os.py").read_text():
 print("Design OS guard failed: editorial type scale not generated from tokens");sys.exit(1)
if not all(marker in runtime for marker in (".ws-editorial-hero-zh",".ws-editorial-feature-zh",'data-ws-editorial-hierarchy="primary"')):
 print("Design OS guard failed: editorial 900/200 type grammar missing");sys.exit(1)
print("Westside Design OS guard: PASS")
