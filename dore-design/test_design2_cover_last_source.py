#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-LAST-SOURCE').read_text().strip()=='rollout-next'
print('PASS source phase terminated')
