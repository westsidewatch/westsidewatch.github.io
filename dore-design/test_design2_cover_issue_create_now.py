#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ISSUE-CREATE-NOW').read_text().strip()=='now'
print('PASS issue create now')
