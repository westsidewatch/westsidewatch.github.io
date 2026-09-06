#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-PROD-ROLL-NEXT').read_text().strip()=='next'
print('PASS production rollout next marker')
