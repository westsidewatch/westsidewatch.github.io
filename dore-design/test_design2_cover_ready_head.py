#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-READY-HEAD').read_text().strip()=='ready-head'
print('PASS ready head marker')
