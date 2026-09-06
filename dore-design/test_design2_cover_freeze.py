#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-FREEZE').read_text().strip()=='freeze'
print('PASS source freeze')
