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
for legacy in ["/css/typography-sitewide.css","/css/westside-color-authority.css"]:
 if legacy not in runtime:
  print("Design OS guard failed: compatibility runtime missing",legacy);sys.exit(1)

import subprocess
result=subprocess.run([sys.executable,str(root/"scripts/build_westside_design_os.py"),"--check"],cwd=root)
if result.returncode: sys.exit(result.returncode)
if '/css/westside-design-tokens.css' not in runtime:
 print("Design OS guard failed: generated token runtime is not loaded");sys.exit(1)
print("Westside Design OS guard: PASS")
