#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-ROLL').read_text().strip()=='go'
print('PASS cover roll go')
