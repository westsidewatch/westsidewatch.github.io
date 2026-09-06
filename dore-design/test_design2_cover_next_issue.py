#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-NEXT-IS-ISSUE').read_text().strip()=='issue'
print('PASS A2A issue next')
