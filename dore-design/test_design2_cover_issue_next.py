#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ISSUE-NEXT').read_text().strip()=='issue'
print('PASS rollout issue next')
