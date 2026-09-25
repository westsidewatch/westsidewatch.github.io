#!/usr/bin/env python3
import importlib.util
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'scripts'/'resolve_design_generation_prompt.py'
spec=importlib.util.spec_from_file_location('resolver',P); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

checks=[]
def ok(name, cond):
    checks.append((name,bool(cond)))

try:
    r=m.resolve('domus-ponti', subject='test subject', consumer='resolver-regression')
    ok('resolves known grammar', r['grammar_id']=='domus-ponti')
    ok('carries canonical authority', 'italian-editorial-grammars.v1.json' in ' '.join(x or '' for x in r['authority_sources']))
    ok('carries visual evidence', 'domus-ponti-250' in r['visual_evidence'])
    ok('injects subject without replacing grammar', 'test subject' in r['canonical_prompt'] and 'architectural construction' in r['canonical_prompt'])
    ok('formal truth state', r['truth_state']=='canonical-resolved')
except Exception as e:
    print('FAIL: known grammar resolution:',e); sys.exit(1)

try:
    m.resolve('does-not-exist')
    ok('unknown grammar blocks',False)
except ValueError:
    ok('unknown grammar blocks',True)

failed=[n for n,v in checks if not v]
for n,v in checks: print(('PASS: ' if v else 'FAIL: ')+n)
if failed: sys.exit(1)
print('PASS: Doré formal generation resolver contract.')
