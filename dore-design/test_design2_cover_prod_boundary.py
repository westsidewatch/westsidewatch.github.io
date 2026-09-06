#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-PROD-BOUNDARY').read_text().strip()=='mac'
print('PASS final production boundary')
