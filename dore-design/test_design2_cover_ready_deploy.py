#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-READY-DEPLOY').read_text().strip()=='ready'
print('PASS ready deploy final')
