#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent

def load(name):
 p=HERE/f'{name}.py'; s=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

m=load('design_generation_a2a')
r=m.execute({'operation':'resolve','grammar_id':'domus-ponti','subject':'A2A acceptance specimen','consumer':'chatgpt-a2a'})
assert r['ok'] and r['status']=='completed'
p=r['generation_package']
assert p['grammar_id']=='domus-ponti'
assert 'domus-ponti-250' in p['visual_evidence']
assert 'architectural construction' in r['generator_prompt']

v=m.execute({'operation':'verify','generation_package':p,'observations':{'grammar_fidelity':True,'evidence_fidelity':True,'subject_fidelity':True,'forbidden_artifacts_absent':True}})
assert v['ok'] and v['verified'] is True and v['truth_state']=='verified-specimen'

bad=m.execute({'operation':'verify','generation_package':p,'observations':{'grammar_fidelity':False,'evidence_fidelity':True,'subject_fidelity':True,'forbidden_artifacts_absent':True},'corrections':['restore canonical grammar']})
assert bad['ok'] and bad['verified'] is False and bad['status']=='revision_required'
print('PASS: A2A design.generation resolve -> generator package -> verify loop')
