#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ONLY-ROLL').read_text().strip()=='only-rollout'
print('PASS only rollout remains')
