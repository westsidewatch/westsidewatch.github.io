#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-CUT').read_text().strip()=='cut'
print('PASS source cut')
