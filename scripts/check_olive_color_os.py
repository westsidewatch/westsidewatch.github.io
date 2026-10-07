#!/usr/bin/env python3
from pathlib import Path
import re, sys
p=Path("layouts/olive/surface-carrier.html")
s=p.read_text(encoding="utf-8")
forbidden=[
 r"#181816\b",r"#272720\b",r"#d7cfaa\b",r"#8e876b\b",r"#cebd74\b",
 r"rgba\(16,16,14,",r"rgba\(20,20,18,"
]
hits=[pat for pat in forbidden if re.search(pat,s,re.I)]
if hits:
 print("Olive Color OS guard failed: local black/gold palette literals:",", ".join(hits))
 sys.exit(1)
if 'data-ws-color-family="sermon"' not in s:
 print("Olive Color OS guard failed: sermon family binding missing")
 sys.exit(1)
print("Olive Color OS guard: PASS")
