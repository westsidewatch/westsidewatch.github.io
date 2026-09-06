#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-CUTOVER').read_text().strip()=='cutover'
print('PASS rollout cutover')
