#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-PRODUCTION-NOW').read_text().strip()=='production-now'
print('PASS production now boundary')
