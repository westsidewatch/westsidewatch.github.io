#!/usr/bin/env python3
"""Hard gate: Atlas runtime prompts must be grounded in exact image observations.

The legacy manually authored fingerprint registry may remain temporarily as a
regression corpus, but no production prompt path may load or consume it.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ATLAS=ROOT/'static/dore-design/italian-editorial-atlas.html'
COMPILER=ROOT/'static/dore-design/italian-editorial-prompt-compiler.v1.js'
OBS=ROOT/'static/dore-design/italian-editorial-grounded-observations.v0.json'
LEGACY=ROOT/'static/dore-design/italian-editorial-visual-fingerprints.v1.json'

atlas=ATLAS.read_text(encoding='utf-8')
compiler=COMPILER.read_text(encoding='utf-8')
obs=json.loads(OBS.read_text(encoding='utf-8'))
errors=[]

# Runtime dependency cutover.
for forbidden in ['italian-editorial-visual-fingerprints.v1.json','fingerprintDb','fp.dimensions']:
    if forbidden in atlas: errors.append('atlas runtime still references '+forbidden)
    if forbidden in compiler: errors.append('compiler runtime still references '+forbidden)

for required in ['italian-editorial-grounded-observations.v0.json','selectedEvidenceIds','observationDb']:
    if required not in atlas: errors.append('atlas grounded runtime missing '+required)
for required in ['selectedEvidenceIds','observationDb','exact selected historical image','Grounded observations']:
    if required.lower() not in compiler.lower(): errors.append('compiler grounded authority missing '+required)

# Exact evidence identity is mandatory; token-wide evidence lookup is forbidden.
if 'filter(x=>(x.tokens||[]).includes(token)' in compiler:
    errors.append('shared-token evidence resolution remains in compiler')
if 'chosen.set(t.key,ev.id)' not in atlas:
    errors.append('picker does not bind grammar selection to exact evidence id')

# Grounded records must themselves carry image-inspection provenance.
items=obs.get('items') or []
if not items: errors.append('grounded observation corpus empty')
for item in items:
    eid=(item.get('evidence') or {}).get('id') or '<unknown>'
    if item.get('authority')!='historical-image-observation': errors.append(eid+': wrong observation authority')
    if (item.get('provenance') or {}).get('imageInspected') is not True: errors.append(eid+': imageInspected provenance missing')
    if item.get('canonicalDoréLearning') is not False: errors.append(eid+': observation self-promoted to canon')

# Legacy file is explicitly permitted only as non-runtime regression evidence.
legacy_state='absent'
if LEGACY.exists():
    legacy_state='regression-only'
    legacy=json.loads(LEGACY.read_text(encoding='utf-8'))
    if not legacy.get('items'): errors.append('legacy registry exists but cannot serve even as regression corpus')

if errors:
    print('PROMPT_AUTHORITY_CUTOVER=FAIL')
    for error in errors: print('-',error)
    raise SystemExit(1)
print('PROMPT_AUTHORITY_CUTOVER=PASS')
print('RUNTIME_PROMPT_AUTHORITY=historical-image-observation')
print('EXACT_EVIDENCE_IDENTITY=REQUIRED')
print('MANUAL_FINGERPRINT_RUNTIME_AUTHORITY=NONE')
print('LEGACY_FINGERPRINT_STATE='+legacy_state)
print('CANON_PROMOTION=SEPARATE')
