#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-FINALIZE').read_text().strip()=='finalized'
print('PASS finalized source slice')
