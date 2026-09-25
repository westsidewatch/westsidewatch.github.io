#!/usr/bin/env python3
import importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'scripts'/'design_generation_gateway.py'
spec=importlib.util.spec_from_file_location('gateway',P); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
required={'westside-watch','journal','dawn-library','living-water','one','cinema','chidi','neser','game','publication','pond-bottom'}
known=set(g.consumers())
errors=[]
if not required.issubset(known): errors.append('missing consumers: '+','.join(sorted(required-known)))
for consumer in sorted(required):
    try:
        out=g.prepare(consumer,'domus-ponti',subject='site-wide acceptance',exploration=False)
        if out.get('status')!='READY_FOR_GENERATOR': errors.append(consumer+': not ready')
        if out.get('resolution',{}).get('grammar_id')!='domus-ponti': errors.append(consumer+': wrong grammar')
        if 'domus-ponti-250' not in out.get('resolution',{}).get('visual_evidence',[]): errors.append(consumer+': evidence not resolved')
        if 'architectural construction' not in out.get('generator_prompt',''): errors.append(consumer+': canonical grammar absent')
    except Exception as e: errors.append(consumer+': '+str(e))
try:
    g.prepare('unregistered-consumer','domus-ponti')
    errors.append('unregistered consumer was accepted')
except ValueError: pass
if errors:
    [print('FAIL:',x) for x in errors]; sys.exit(1)
print('PASS: all registered site consumers resolve generation through canonical Doré authority.')
