#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-PUSH').read_text().strip()=='production-gate'
print('PASS production gate push')
