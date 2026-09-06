#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ROLL-ONLY').read_text().strip()=='rollout-only'
print('PASS rollout-only')
