#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-A2A-ROLL').read_text().strip()=='roll'
print('PASS A2A roll final')
