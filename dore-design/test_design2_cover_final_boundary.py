#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-FINAL-BOUNDARY').read_text().strip()=='deploy-only'
print('PASS final source deploy boundary')
