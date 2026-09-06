#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-LOCK').read_text().strip()=='locked'
print('PASS cover source locked')
