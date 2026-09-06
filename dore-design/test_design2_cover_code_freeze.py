#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-CODE-FREEZE').read_text().strip()=='frozen-for-rollout'
print('PASS cover frozen for rollout')
