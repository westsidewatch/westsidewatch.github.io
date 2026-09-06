#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-HANDOFF').read_text().strip()=='rollout'
print('PASS final rollout handoff')
