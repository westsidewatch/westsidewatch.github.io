#!/usr/bin/env python3
from pathlib import Path
import json,sys,re

root=Path(__file__).resolve().parents[1]
required=[
 root/"design-system/tokens/westside.tokens.json",
 root/"design-system/scopes.json",
 root/"design-system/realm-visual-materials.json",
 root/"static/css/westside-design-os.css",
 root/"static/css/westside-design-tokens.css",
]
missing=[str(p.relative_to(root)) for p in required if not p.exists()]
if missing:
 print("Design OS guard failed: missing",", ".join(missing));sys.exit(1)

scopes=json.loads((root/"design-system/scopes.json").read_text())["scopes"]
if "global" not in scopes or "tool" not in scopes:
 print("Design OS guard failed: global/tool scopes missing");sys.exit(1)

# The seven-realm material inventory is an OS workchain contract, not a CSS source.
registry=json.loads((root/"design-system/realm-visual-materials.json").read_text())
realms=registry["realms"]
expected=["church","journal","one","olive","dawn-library","cinema","daylight-cafe"]
if [r["scope"] for r in realms]!=expected or [r["id"] for r in realms]!=[f"{n:02}" for n in range(1,8)]:
 print("Design OS guard failed: seven-realm material registry mismatch");sys.exit(1)
for r in realms:
 t=r["texture"]
 status=t["status"]
 needs_selection=status in ("replace_candidate","supplement_candidate","missing_mature_svg")
 mode="establish_master" if needs_selection else "reuse_fixed" if status=="accepted_fixed" else "reuse_existing"
 if t["selectionRequired"]!=needs_selection or t["workchainMode"]!=mode:
  print("Design OS guard failed: material selection/reuse state mismatch",r["scope"]);sys.exit(1)
 if status=="accepted_fixed":
  master=t.get("fixedMaster") or {}
  if not all(master.get(k) for k in ("path","version","source","license","originalSha256","masterSha256","acceptanceEvidence")) or not (root/master.get("path","")).is_file():
   print("Design OS guard failed: fixed master missing asset or provenance",r["scope"]);sys.exit(1)
  import hashlib
  if hashlib.sha256((root/master["path"]).read_bytes()).hexdigest()!=master["masterSha256"]:
   print("Design OS guard failed: fixed master digest changed",r["scope"]);sys.exit(1)
 elif t.get("fixedMaster") is not None:
  print("Design OS guard failed: unaccepted fixed master",r["scope"]);sys.exit(1)
 if r["scope"] not in scopes or r["scripture"]["section"]!=r["id"] or not r["identity"]["sourceRef"] or not r["identity"]["geometry"] or not r["texture"]["territory"]:
  print("Design OS guard failed: incomplete realm material contract",r["scope"]);sys.exit(1)
 if r["texture"]["selectedNewAsset"] is not None and not any(c.get("state")=="verified" and c.get("sha256") and c.get("license") and c.get("nativeSvg") and c.get("assetPath")==r["texture"]["selectedNewAsset"] for c in r["texture"]["candidates"]):
  print("Design OS guard failed: selected material lacks verified provenance",r["scope"]);sys.exit(1)
 if any(c.get("state")=="verified" and not (c.get("sha256") and c.get("license") and c.get("nativeSvg")) for c in r["texture"]["candidates"]):
  print("Design OS guard failed: material falsely verified",r["scope"]);sys.exit(1)
if not (root/registry["scriptureStudio"]["path"]).is_file() or not (root/registry["scriptureStudio"]["model"]).is_file():
 print("Design OS guard failed: Scripture Studio source missing");sys.exit(1)

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
print("Westside Design OS guard: PASS")
