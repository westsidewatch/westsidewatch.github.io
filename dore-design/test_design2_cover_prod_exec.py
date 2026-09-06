#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-PROD-EXEC').read_text().strip()=='ready'
print('PASS production execution ready')
