#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ISSUE-ONLY').read_text().strip()=='issue-only'
print('PASS issue only next')
