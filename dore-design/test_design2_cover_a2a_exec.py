#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-A2A-EXEC').read_text().strip()=='execute'
print('PASS A2A execution next')
