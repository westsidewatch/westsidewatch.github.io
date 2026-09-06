#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-FINAL-BUILD').read_text().strip()=='built'
print('PASS final build marker')
