#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'static'/'dore-design'/'dore-design-observer.js'

def main():
    if not P.exists(): print('FAIL: observer missing'); return 1
    s=P.read_text()
    required=(
      "schema: 'dore.design-observation-evidence.v1'",
      "getComputedStyle(el)", "getBoundingClientRect()", "querySelectorAll",
      "method:['dom','css','computed-style','render']",
      "mayPromoteCanonical:false", "requiresBeautifulGate:true",
      "historicalAuthority:false", "inferredRationale: []"
    )
    missing=[x for x in required if x not in s]
    forbidden=('mayPromoteCanonical:true','requiresBeautifulGate:false','historicalAuthority:true')
    bad=[x for x in forbidden if x in s]
    if missing or bad:
        for x in missing: print('FAIL missing:',x)
        for x in bad: print('FAIL forbidden:',x)
        return 1
    print('PASS: runtime DOM/CSS/computed-style/render observer emits evidence without authority escalation.')
    return 0
if __name__=='__main__': sys.exit(main())
