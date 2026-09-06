#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-A2A-CREATE').read_text().strip()=='create'
print('PASS A2A create issue boundary')
