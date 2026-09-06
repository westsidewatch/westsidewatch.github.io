#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-PRODUCTION-CANDIDATE').read_text().strip()=='production-candidate'
print('PASS production candidate')
