#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-A2A-NEXT').read_text().strip()=='a2a-next'
print('PASS A2A next')
