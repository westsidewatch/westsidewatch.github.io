#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ISSUE-GATE').read_text().strip()=='go'
print('PASS issue gate final')
