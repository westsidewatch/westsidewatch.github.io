#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ISSUE').read_text().strip()=='create-now'
print('PASS rollout issue boundary')
