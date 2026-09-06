#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-NEXT-ROLL').read_text().strip()=='roll'
print('PASS next rollout final')
