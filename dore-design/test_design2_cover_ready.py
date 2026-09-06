#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-READY').read_text().strip()=='source-ready'
print('PASS cover source ready')
