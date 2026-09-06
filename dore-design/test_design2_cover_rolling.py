#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ROLLING').read_text().strip()=='ready'
print('PASS cover ready to roll')
