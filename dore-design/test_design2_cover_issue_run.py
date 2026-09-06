#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ISSUE-RUN').read_text().strip()=='run'
print('PASS issue run final')
