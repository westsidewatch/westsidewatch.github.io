#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-HALT').read_text().strip()=='halt'
print('PASS source halt')
