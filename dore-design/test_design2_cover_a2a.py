#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-A2A').read_text().strip()=='handoff-complete'
print('PASS A2A handoff')
