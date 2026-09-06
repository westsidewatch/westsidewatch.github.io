#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ROLL-PENDING').read_text().strip()=='pending'
print('PASS rollout pending Mac')
