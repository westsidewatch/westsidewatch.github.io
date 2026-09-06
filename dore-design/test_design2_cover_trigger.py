#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-TRIGGER').read_text().strip()=='trigger'
print('PASS rollout trigger')
