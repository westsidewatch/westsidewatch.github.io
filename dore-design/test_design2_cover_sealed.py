#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-LAST-COMMIT').read_text().strip()=='sealed'
print('PASS rollout source sealed')
