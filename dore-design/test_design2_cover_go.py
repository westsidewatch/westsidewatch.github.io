#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-GO').read_text().strip()=='go'
print('PASS final go')
