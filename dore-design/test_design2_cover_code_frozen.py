#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-CODE-FROZEN').read_text().strip()=='frozen'
print('PASS code frozen final')
