#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ISSUE-FINAL').read_text().strip()=='create'
print('PASS final rollout issue marker')
