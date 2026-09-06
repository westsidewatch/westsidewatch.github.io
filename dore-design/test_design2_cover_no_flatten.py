#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'design2_multiwrite_cover.py').read_text()
assert "'type':'image'" not in s
for nid in ('mwc-frame','mwc-kicker','mwc-title','mwc-subtitle','mwc-rule','mwc-note'):assert nid in s
print('PASS cover remains structured and editable')
