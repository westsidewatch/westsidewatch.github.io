#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-A2A-NOW-FINAL').read_text().strip()=='now'
print('PASS final A2A now')
