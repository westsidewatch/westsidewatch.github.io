#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-PROD-HANDOFF').read_text().strip()=='handoff'
print('PASS final production handoff')
