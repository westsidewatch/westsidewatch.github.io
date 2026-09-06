#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-LAST-BEFORE-ISSUE').read_text().strip()=='last'
print('PASS last source before issue')
