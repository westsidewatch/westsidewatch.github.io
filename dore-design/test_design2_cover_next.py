#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-NEXT').read_text().strip()=='a2a-production-rollout'
print('PASS next action rollout')
