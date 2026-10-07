#!/usr/bin/env python3
"""Prevent reintroduction of the retired black+gold theme.

Legacy debt is baselined so this gate can land without pretending old files are
already migrated. Every PR is checked against main: it may remove legacy debt,
but may not add a new black/gold pairing or a theme alias.
"""
from pathlib import Path
import re, subprocess, sys

EXTS={".css",".html",".htm",".scss",".sass",".js",".jsx",".ts",".tsx",".md"}
GOLD=re.compile(r"(?i)(#(?:CEBD74|A2872A|B79838|D2BC69|D7CFAA|8E876B)\b|rgba?\(\s*206\s*,\s*189\s*,\s*116)")
DARK=re.compile(r"(?i)(#(?:000000|000|10100E|181816|20201C|252525|272720)\b|rgba?\(\s*(?:0|16|20|24|37|39)\s*,\s*(?:0|16|20|24|37|39)\s*,\s*(?:0|14|18|24|37|32))")
ALIAS=re.compile(r"(?i)(--(?:sites-)?gold\b|black.?gold|dark.?gold|night.?gold)")

def risky(text):
    return bool(ALIAS.search(text) or (GOLD.search(text) and DARK.search(text)))

def base_text(path):
    try:
        return subprocess.run(["git","show",f"origin/main:{path}"],capture_output=True,text=True,check=True).stdout
    except Exception:
        return ""

bad=[]
for root in ("layouts","assets","static","content"):
    p=Path(root)
    if not p.exists(): continue
    for file in p.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in EXTS: continue
        rel=file.as_posix()
        try: now=file.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        if risky(now) and not risky(base_text(rel)):
            bad.append(rel)

if bad:
    print("BLACK+GOLD GLOBAL BAN: FAIL — new retired-palette debt")
    for rel in bad: print(rel)
    sys.exit(1)
print("BLACK+GOLD GLOBAL BAN: PASS — no new retired-palette debt")
