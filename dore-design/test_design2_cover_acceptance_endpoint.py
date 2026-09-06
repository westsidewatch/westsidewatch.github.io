#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R/'design2_cover_acceptance.py').read_text();app=(R/'app_visual_v2.py').read_text()
for token in ('structured_nodes','revisioned','dore.design.cover-acceptance.v1'):assert token in s
assert '/api/design2/multiwrite-cover/acceptance' in app
print('PASS cover acceptance endpoint contract')
