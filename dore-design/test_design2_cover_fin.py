#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-FIN').read_text().strip()=='fin'
print('PASS source fin')
