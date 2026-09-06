#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-A2A-COMMAND').read_text().strip()=='next'
print('PASS A2A command next')
