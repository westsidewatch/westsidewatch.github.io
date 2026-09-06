#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ROLLING-NOW').read_text().strip()=='roll'
print('PASS immediate rollout')
