#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-LAST-HEAD').read_text().strip()=='last-head'
print('PASS last head marker')
