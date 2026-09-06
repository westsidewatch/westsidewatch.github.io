#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ROLL-EXEC').read_text().strip()=='exec'
print('PASS rollout execution boundary')
