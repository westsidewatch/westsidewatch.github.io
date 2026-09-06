#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ISSUE-BOUNDARY').read_text().strip()=='issue-now'
print('PASS final A2A boundary')
