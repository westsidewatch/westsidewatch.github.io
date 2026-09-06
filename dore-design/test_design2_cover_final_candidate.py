#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-FINAL-CANDIDATE').read_text().strip()=='final-candidate'
print('PASS final production candidate')
