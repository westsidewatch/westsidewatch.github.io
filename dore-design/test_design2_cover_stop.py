#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-STOP').read_text().strip()=='stop'
print('PASS source stop marker')
