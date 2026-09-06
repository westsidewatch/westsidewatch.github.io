#!/usr/bin/env python3
from pathlib import Path
r=Path(__file__).parent
entry=(r/'app_design2.py').read_text();phase=(r/'design2_phase7_http.py').read_text();app=(r/'app_visual_v2.py').read_text()
assert 'design2_phase7_http.install' in entry
assert '/api/design2/production-health' in phase
assert "'version':'2.0-production'" in phase
assert '/api/design2/closeout' in app
print('DESIGN2_PHASE7_CONTRACT_PASS')
