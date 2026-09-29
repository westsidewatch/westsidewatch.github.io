#!/usr/bin/env python3
"""Westside Watch hard brand gate: no large black/near-black UI backgrounds."""
import re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EXT={'.css','.html','.htm','.scss'}
SKIP={'.git','node_modules','vendor','public','resources'}
# Black/near-black literals historically used as generic full-section backgrounds.
DARK_HEX=re.compile(r'(?i)#(?:000(?:000)?|0[0-9a-f]{5}|1[0-9a-f]{5}|2[0-9a-f]{5})\b')
BG=re.compile(r'(?i)(?:background|background-color)\s*:\s*([^;}{]+)')
violations=[]
for p in ROOT.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in EXT or any(x in SKIP for x in p.parts): continue
    text=p.read_text(errors='ignore')
    for m in BG.finditer(text):
        value=m.group(1)
        if DARK_HEX.search(value) or re.search(r'(?i)\b(?:black|rgb\(\s*(?:0|[0-3]?\d)\s*,\s*(?:0|[0-3]?\d)\s*,\s*(?:0|[0-3]?\d)\s*\))\b',value):
            line=text.count('\n',0,m.start())+1
            # Explicit narrowly-scoped media/rendering surfaces may opt out only with adjacent authority marker.
            before=text[max(0,m.start()-180):m.start()]
            if 'brand-dark-exception:' in before: continue
            violations.append(f'{p.relative_to(ROOT)}:{line}: {m.group(0).strip()}')
if violations:
    print('WESTSIDE_WATCH_NO_FULL_BLACK_BACKGROUND=FAIL')
    print('\n'.join(violations[:200]))
    print('Rule: black/near-black cannot be used as a generic UI background. A narrowly scoped media/rendering surface requires an adjacent brand-dark-exception: reason.')
    sys.exit(1)
print('WESTSIDE_WATCH_NO_FULL_BLACK_BACKGROUND=PASS')
