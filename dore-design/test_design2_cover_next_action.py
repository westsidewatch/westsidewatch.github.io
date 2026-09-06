#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-NEXT-ACTION').read_text().strip()=='create-a2a-issue'
print('PASS final next action')
