#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-SOURCE-OVER').read_text().strip()=='over'
print('PASS source over')
