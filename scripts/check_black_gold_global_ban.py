#!/usr/bin/env python3
"""Repository-wide ban on dominant dark+gold theme literals.

This is deliberately source-level and global. Color Authority owns gold-family
and dark-family anchors; product/page code may consume semantic tokens, but may
not locally recreate the retired black/dark + gold theme.
"""
from pathlib import Path
import re, sys

ROOTS=("layouts","assets","static","content")
EXTS={".css",".html",".htm",".scss",".sass",".js",".jsx",".ts",".tsx",".md"}
EXEMPT=set()
# Gold-family literals are authority-only inputs; product/page code may not recreate a theme from them.
GOLD=re.compile(r"(?i)(#(?:CEBD74|A2872A|B79838|D2BC69|D7CFAA|8E876B)\b|rgba?\(\s*206\s*,\s*189\s*,\s*116)")
# Dark literals used by the retired black/night treatment. Semantic Color OS
# tokens are allowed; arbitrary local dark paint paired with gold is not.
DARK=re.compile(r"(?i)(#(?:000000|000|10100E|181816|20201C|252525|272720)\b|rgba?\(\s*(?:0|16|20|24|37|39)\s*,\s*(?:0|16|20|24|37|39)\s*,\s*(?:0|14|18|24|37|32))")

violations=[]
alias=re.compile(r"(?i)(--(?:sites-)?gold\b|black.?gold|dark.?gold|night.?gold)")
for root in ROOTS:
 p=Path(root)
 if not p.exists(): continue
 for f in p.rglob("*"):
  if not f.is_file() or f.suffix.lower() not in EXTS: continue
  rel=f.as_posix()
  if rel in EXEMPT: continue
  try: s=f.read_text(encoding="utf-8")
  except UnicodeDecodeError: continue
  # Any non-authority source that locally declares both families recreates the deleted palette.
  # The authority file itself is also scanned: legacy theme aliases/compatibility names are forbidden.
  if alias.search(s) and rel != "scripts/check_black_gold_global_ban.py":
   violations.append((rel,["forbidden theme alias"],["forbidden theme alias"]))
  elif GOLD.search(s) and DARK.search(s):
   gl=[i for i,l in enumerate(s.splitlines(),1) if GOLD.search(l)]
   dl=[i for i,l in enumerate(s.splitlines(),1) if DARK.search(l)]
   violations.append((rel,gl[:8],dl[:8]))

if violations:
 print("BLACK+GOLD GLOBAL BAN: FAIL")
 for rel,g,d in violations:
  print(f"{rel}: gold lines {g}; dark lines {d}")
 print("Use Westside Color OS semantic roles instead of local dark/gold literals.")
 sys.exit(1)
print("BLACK+GOLD GLOBAL BAN: PASS")
