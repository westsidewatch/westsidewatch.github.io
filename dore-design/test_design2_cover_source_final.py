#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-SOURCE-FINAL').read_text().strip()=='final'
print('PASS final source boundary')
