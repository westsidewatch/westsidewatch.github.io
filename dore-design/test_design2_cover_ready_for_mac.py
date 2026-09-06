#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-READY-FOR-MAC').read_text().strip()=='ready-for-mac'
print('PASS cover ready for Mac')
