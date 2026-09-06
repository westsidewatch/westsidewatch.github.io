#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ROLL-READY').read_text().strip()=='yes'
print('PASS final rollout readiness')
