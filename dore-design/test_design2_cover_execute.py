#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-EXECUTE').read_text().strip()=='execute'
print('PASS execute marker')
