#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-READY-PROD').read_text().strip()=='ready-prod'
print('PASS production rollout ready')
