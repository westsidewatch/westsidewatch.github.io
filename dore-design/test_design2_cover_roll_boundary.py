#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ROLL-BOUNDARY').read_text().strip()=='mac-result-required'
print('PASS Mac result required')
