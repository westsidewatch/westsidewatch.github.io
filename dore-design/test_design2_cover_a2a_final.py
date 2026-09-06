#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-A2A-FINAL').read_text().strip()=='handoff'
print('PASS final A2A handoff marker')
