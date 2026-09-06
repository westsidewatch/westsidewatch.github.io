#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-RC-FINAL').read_text().strip()=='rc-final'
print('PASS final rc marker')
