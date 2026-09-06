#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-A2A-ISSUE-NOW').read_text().strip()=='now'
print('PASS A2A issue now')
