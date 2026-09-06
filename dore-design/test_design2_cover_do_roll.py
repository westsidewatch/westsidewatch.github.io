#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-DO-ROLL').read_text().strip()=='do'
print('PASS do rollout')
