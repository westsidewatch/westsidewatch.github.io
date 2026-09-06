#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ROLL-ACTION').read_text().strip()=='rollout'
print('PASS rollout action final')
