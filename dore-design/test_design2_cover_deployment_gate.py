#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-DEPLOYMENT-GATE').read_text().strip()=='deployment'
print('PASS deployment gate')
