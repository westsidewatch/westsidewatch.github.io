#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-CANDIDATE').read_text().strip()=='candidate'
print('PASS final candidate')
