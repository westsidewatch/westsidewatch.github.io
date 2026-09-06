#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-LAST-SOURCE-WRITE').read_text().strip()=='last'
print('PASS last source write')
