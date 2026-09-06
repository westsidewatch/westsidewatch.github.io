#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ROLL-START').read_text().strip()=='start'
print('PASS rollout start')
