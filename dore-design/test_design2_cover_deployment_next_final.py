#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-DEPLOYMENT-NEXT-FINAL').read_text().strip()=='a2a-rollout'
print('PASS deployment next final marker')
