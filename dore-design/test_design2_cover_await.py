#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-AWAIT-ROLL').read_text().strip()=='await'
print('PASS await rollout')
