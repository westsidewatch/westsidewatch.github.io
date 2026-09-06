#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-RC-HEAD').read_text().strip()=='closed'
print('PASS rc head closed')
