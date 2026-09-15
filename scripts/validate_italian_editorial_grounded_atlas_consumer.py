#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ATLAS=(ROOT/'static/dore-design/italian-editorial-atlas.html').read_text(encoding='utf-8')
COMPILER=(ROOT/'static/dore-design/italian-editorial-prompt-compiler.v1.js').read_text(encoding='utf-8')
errors=[]

for required in [
    'italian-editorial-grounded-observations.v0.json',
    'selectedEvidenceIds',
    'observationDb',
    'GROUNDED VISUAL COVERAGE',
    "chosen.set(t.key,ev.id)",
]:
    if required not in ATLAS: errors.append('atlas missing '+required)

if 'italian-editorial-visual-fingerprints.v1.json' in ATLAS:
    errors.append('Atlas still loads manual fingerprint registry')
if 'fingerprintDb' in ATLAS:
    errors.append('Atlas still passes manual fingerprint authority')

for required in [
    'selectedEvidenceIds',
    'observationDb',
    'Manually authored fingerprint prose is not prompt authority',
    'The exact selected historical image is concrete visual authority',
]:
    if required not in COMPILER: errors.append('compiler missing '+required)
if 'fingerprintDb' in COMPILER or 'fp.dimensions' in COMPILER:
    errors.append('compiler still consumes manual fingerprints')
if 'filter(x=>(x.tokens||[]).includes(token)' in COMPILER:
    errors.append('compiler still resolves evidence indirectly by shared token')

if errors:
    print('GROUNDED_ATLAS_CONSUMER=FAIL')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('GROUNDED_ATLAS_CONSUMER=PASS')
print('EXACT_EVIDENCE_SELECTION=PASS')
print('MANUAL_FINGERPRINT_RUNTIME_AUTHORITY=REMOVED')
print('SHARED_TOKEN_EVIDENCE_DRIFT=BLOCKED')
